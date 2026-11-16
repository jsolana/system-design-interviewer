---
title: Hotel Reservation System
type: interview
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 7 Hotel Reservation System, pp. 195-223]
concepts: [idempotency, optimistic-concurrency-control, transactions-and-isolation-levels, database-partitioning, caching, change-data-capture, two-phase-commit, saga, unique-id-generation, database-replication]
difficulty: medium
---

# Hotel Reservation System

## Prompt
A reservation system for a hotel chain (Marriott-style): 5,000 hotels and 1 M rooms. Applicable to Airbnb, flight booking or movie ticket booking.

## Functional requirements
- Show the hotel page and the room detail page.
- Reserve a room (full payment at booking; web/app) and cancel.
- Admin panel to add/remove/update hotels and rooms.
- Support **10% overbooking**.
- Dynamic pricing: it can vary each day according to expected occupancy.
- Out of scope: room search.

## Non-functional requirements
- High concurrency (peak season/events: many customers for the same room).
- Moderate latency (acceptable for a reservation to take a few seconds).

## Estimations
- 70% occupancy, average stay 3 days: 1M x 0.7 / 3 = ~233,000 -> ~240,000 reservations/day; average TPS = 240,000/10^5 ~ **3**.
- Funnel (10% proceed to the next step): detail QPS 300 -> booking page QPS 30 -> reservation TPS 3.
- Inventory: 5,000 hotels x 20 types x 2 years x 365 = **73 M rows** (fits in one DB; replicate across regions/AZs for availability).

## API
- Hotel: `GET /v1/hotels/ID`, `POST/PUT/DELETE /v1/hotels` (staff only). Room: `GET/POST/PUT/DELETE /v1/hotels/ID/rooms/ID` (write staff only).
- Reservations: `GET /v1/reservations` (user's history), `GET /v1/reservations/ID`, `POST /v1/reservations`, `DELETE /v1/reservations/ID`.
- `POST /v1/reservations`: startDate, endDate, hotelID, **roomTypeID** (not roomID), reservationID (idempotency key).

## Data model
- Queries: hotel detail; room types available in a date range; record a reservation; query reservation/history.
- Relational (MySQL) chosen: read-heavy load with few writes, ACID essential (avoid double booking/charging) and stable relationships between entities.
- Tables: `hotel`, `room` (room_id, room_type_id, floor, number, hotel_id, is_available), `room_type_rate` (price per type and future date), `guest`, `reservation` (reservation_id PK, hotel_id, room_type_id, start_date, end_date, status, guest_id) and **`room_type_inventory`** (hotel_id, room_type_id, date, total_inventory, total_reserved; composite PK; one row per date; pre-populated for 2 years with a daily job).
- `status`: pending, paid, refunded, canceled, rejected (state machine).
- The first schema with `room_id` in the reservation works for Airbnb, but in a hotel a **room type** is reserved; the number is assigned at check-in.

## Architecture (high-level design)
Microservices: CDN for static assets; **public API gateway** (rate limiting, auth, routing per endpoint); internal API for staff (behind a VPN); **Hotel Service** (static data, cacheable), **Rate Service** (prices per date), **Reservation Service** (reservations and inventory), **Payment Service** (sets the reservation to paid or rejected), **Hotel Management Service** (staff: view/cancel/book for customers). Internal communication with RPC (gRPC). Each service has its own DB (hotel, rate, reservation, payment) and caches.

## Deep dives
**Availability**: two SQL steps: select the rows in the range (`total_inventory`, `total_reserved`) and check `total_reserved + n <= total_inventory` for all dates; with overbooking `<= 110% x total_inventory`.

**Large data**: store only current/future reservations (archive history in cold storage); **sharding by hash(hotel_id) % servers** (almost all queries filter by hotel).

**Concurrency / double booking**
1. *Same user clicks several times*: button disabled on the client (unreliable) or **idempotent API**: the reservation service generates a globally unique `reservation_id` when creating the order (confirmation screen) and it travels with the submit; since it is the PK of `reservation`, the second attempt violates the unique constraint ([[idempotency]]).
2. *Several users, one room*: with non-serializable isolation, two transactions read 99/100 and both write 100 (race). Options:
   - **Pessimistic locking** (`SELECT ... FOR UPDATE`): serializes, simple, useful with high contention; risk of deadlocks and poor scalability (long transactions); not recommended.
   - **[[optimistic-concurrency-control]]** with a version number (better than a timestamp, because of imprecise clocks): no locks, fast with low contention; with high concurrency many retries. Suitable because reservation QPS is low.
   - **Database constraint** `CHECK(total_inventory - total_reserved >= 0)`: easy to implement; under high contention it produces failures ("rooms were left" but it fails); constraints are not easily versioned and not all DBs support them. Also valid here.

**Scalability (e.g. booking.com, QPS x1,000)**: stateless services scale by adding servers; the DB does not. Sharding by hotel_id: 30,000 QPS across 16 shards = 1,875 QPS per shard. **Inventory cache** (Redis with TTL and LRU; only current and future dates matter): key `hotelID_roomTypeID_{date}` -> available rooms; reads go against Redis, the DB is updated first and propagated asynchronously to the cache (from the application or with [[change-data-capture]], e.g. Debezium). The DB remains the source of truth and revalidates availability: a stale cache only produces a friendly error ("someone booked the last one") and is corrected on refresh. Benefits: less load on the DB, in-memory reads; cost: maintaining consistency.

**Consistency across services**: the design uses a hybrid approach (Reservation Service manages reservations and inventory in the same relational DB, to leverage ACID). A microservices purist would demand separate DBs, which breaks the single transaction; solutions: **[[two-phase-commit]]** (atomic but blocking) or **[[saga]]** (local transactions + compensations, eventual consistency). It is decided that their complexity is not worth it.

## Trade-offs and decisions
- Reserve room type and count inventory per date (instead of assigning a specific room).
- Optimistic locking/constraints (low contention) versus pessimistic.
- Hybrid service (inventory + reservations in one DB) versus DB per microservice with 2PC/saga.
- Inventory cache: performance versus tolerated inconsistency (DB validates).

## Related concepts
[[idempotency]], [[optimistic-concurrency-control]], [[transactions-and-isolation-levels]], [[database-partitioning]], [[caching]], [[change-data-capture]], [[two-phase-commit]], [[saga]], [[unique-id-generation]], [[database-replication]]

## Follow-up questions
- If the reservation data does not fit in one DB: archive and shard by hotel_id.
- If it were used at booking.com/Expedia (1,000x QPS).
- Microservices with their own DB per service.

## Variants
Not covered in the source.

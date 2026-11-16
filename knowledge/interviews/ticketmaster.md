---
title: Ticketmaster
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster, Grokking the System Design Interview (PDF), "Design Ticketmaster (*New*)" pp. 154-167]
concepts: [distributed-lock, optimistic-concurrency-control, virtual-waiting-queue, server-sent-events, full-text-search, change-data-capture, idempotency, caching, database-indexing, long-polling]
difficulty: high
---

# Ticketmaster

## Prompt
Ticket-selling platform where users view events, search for them and book tickets. Central challenge: avoid double bookings with enormous traffic on popular events.

## Functional requirements
- View events with a seat map and availability.
- Search events.
- Book tickets.
- Out of scope: viewing past bookings, event creation by admins, dynamic pricing.

## Non-functional requirements
- Availability for search/viewing; strong consistency for booking (no double booking).
- Scale: up to 10M users for a single event.
- Search < 500 ms.
- Read-heavy load (~100:1).
- Out of scope: GDPR, fault tolerance, secure transactions, CI/CD, backups.

## Estimations
No formal section. Figures given: 10M users on one event, tens of millions of concurrent view requests at peak, 100:1 read/write, search < 500 ms, 10-min hold.

## API
- `GET /events/:eventId` -> Event, Venue, Performer, Ticket[] (the tickets draw the map).
- `GET /events/search?keyword&start&end&pageSize&page` -> Event[].
- `POST /bookings/:eventId` {ticketIds, paymentDetails} -> bookingId (later split into reserve and confirm).

## Data model
- Event (date, description, type, performer, venue), User, Performer, Venue (address, capacity, seat map), Ticket (event, seat, price, status; one per seat when the event is created), Booking (user, tickets, total, status in-progress/confirmed).
- Shared PostgreSQL: highly coupled data and need for ACID.

## Architecture (high-level design)
Client -> API Gateway (routing, auth, rate limiting, logging) -> Event Service / Search Service / Booking Service -> PostgreSQL; Stripe for payments; Redis for locks, queues and caches; Elasticsearch synchronized via CDC; SSE for real time.

## Deep dives
**1. Reserving during checkout**
| Option | Approach | Problems |
|---|---|---|
| Bad | `SELECT FOR UPDATE` throughout the checkout | Long locks, deadlocks, blocking after crashes |
| Good | available/reserved/booked states + expiration + cron | Delay in releasing, cron can fail |
| Great | Implicit state: short transaction that reserves if AVAILABLE or expired RESERVED (expires = now + 10 min) | Reads with a double condition (materialized views/composite indexes) |
| Great (chosen) | Distributed lock in Redis, `SET key value NX EX` TTL 10 min (key=ticketId, value=userId) | Requires handling reads and failures |
- Multi-ticket: acquire one by one and release if any fails; Lua script for atomicity if they share a node.
- Reading reserved ones: sorted set by expiration (`ZADD`, count future scores, `ZREMRANGEBYSCORE`).
- Redis outage: errors in payment, but OCC/row locks still prevent double selling.
- TTL expires during payment: one write wins (OCC), the other is refunded; mitigate with a generous TTL or extending it.
- Flow: select seat -> Redis lock -> booking in-progress -> payment with Stripe.js (tokenization, PCI) and PaymentIntent -> Stripe webhook -> transaction: ticket sold, booking confirmed. Idempotent webhook.
See [[distributed-lock]], [[optimistic-concurrency-control]], [[idempotency]].

**2. Scaling the view (tens of millions of requests)**: read-through cache (Redis/Memcached) with long TTL for static data and short TTL for availability, invalidation by triggers; load balancing (round robin/least connections); stateless Event Service with horizontal scaling. See [[caching]].

**3. UX in high-demand sales**
- Good: SSE to update seats in real time (fails in extreme events). See [[server-sent-events]].
- Great: virtual waiting queue (sorted set by timestamp, persistent connection with position, batch admission, `admitted:{eventId}` set with TTL that the Booking Service validates). See [[virtual-waiting-queue]].
- *The source notes that sometimes the best answer is a product one.*

**4. Search < 500 ms**: `LIKE '%term%'` does a full scan. Indexes and optimization (EXPLAIN, LIMIT, UNION instead of OR) -> Postgres full-text (tsvector + GIN) -> Elasticsearch (chosen; inverted index, fuzzy, sync via CDC). See [[database-indexing]], [[full-text-search]], [[change-data-capture]].

**5. Caching repeated searches**: result cache in Redis (key with all parameters, TTL e.g. 24 h; invalidation and fuzzy are hard) or Elasticsearch internal caches (filter/request cache) + CDN for non-personalized responses.

## Trade-offs and decisions
- Distributed lock with TTL: simple and atomic, but depends on Redis; the DB still protects with OCC.
- Shared DB (instead of database-per-service): justified by ACID and coupled data.
- Elasticsearch: better search in exchange for sync (CDC) and operational cost.
- Virtual queue: protects the system at the cost of perceived wait.

## Related concepts
[[distributed-lock]], [[optimistic-concurrency-control]], [[virtual-waiting-queue]], [[server-sent-events]], [[full-text-search]], [[change-data-capture]], [[idempotency]], [[caching]], [[database-indexing]]

## Follow-up questions
- Sharding and replication of the tickets DB.
- What happens if Redis goes down or the TTL expires during payment.
- How to keep the search cache and new events consistent.

## Variants
- **Grokking the System Design Interview (PDF), pp. 154-167** (difficulty Hard): in-memory movie seat booking (BookMyShow) with reservation and waiting services.
  - Requirements: cities, movies, theaters and showtimes; seat map; **5-minute hold** before paying; FIFO waiting list; high concurrency, ACID, no partial orders, max. 10 seats per booking.
  - Estimations: 3 B visits/month, 10 M tickets/month; 500 cities x 10 theaters x 2000 seats x 2 shows x 100 B = 2 GB/day (3.6 TB in 5 years).
  - Search API and `reserveSeats(api_dev_key, session_id, movie_id, show_id, seats_to_reserve)`.
  - **ActiveReservationsService** (in-memory LinkedHashMap + DB: the head is the oldest reservation, for expiring) and **WaitingUsersService** (LinkedHashMap of waiting users; clients with [[long-polling]]); 5 s cushion on the server over the client timer.
  - Concurrency: SQL transactions with isolation level to lock rows before updating.
  - Fault tolerance: master-slave; reservations are rebuilt from the DB but the waiting queue is lost without a replica.
  - Partitioning by ShowID (not by movie, which concentrates release load); consistent hashing to assign servers per show; when a reservation expires/is confirmed, servers with waiting users are notified. See [[virtual-waiting-queue]].

*Note (according to the source)*: mid = API/model and "good" double-booking solution; senior = Elasticsearch, distributed lock, sharding/replication; staff = depth in 2-3 areas.

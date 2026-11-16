---
title: Uber (ride-sharing)
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/uber, Grokking the System Design Interview (PDF), "Designing Uber backend" pp. 148-153]
concepts: [geospatial-indexing, distributed-lock, message-queues, workflow-orchestration, database-partitioning, caching, quadtree, server-sent-events]
difficulty: high
---

# Uber

## Prompt
Platform that connects riders with nearby drivers: fare estimation, ride request, matching and management of acceptance/navigation.

## Functional requirements
- Enter pickup and destination and get an estimated fare.
- Request a ride based on that fare.
- Match with a nearby, available driver.
- The driver accepts/declines and navigates to pickup and destination.
- Out of scope: ratings, scheduled rides, categories (X, XL, Comfort).

## Non-functional requirements
- Low-latency matching (< 1 min to match or fail).
- Strong consistency: a driver is never on two rides at once.
- High throughput at peaks (100k requests from the same place).
- Out of scope: security/GDPR, failover, monitoring, CI/CD.

## Estimations
~10M drivers sending location every ~5 s ≈ **2M writes/s**; on DynamoDB on-demand ($1.25 per million WRUs) with ~100 B/record it would be > $200k/day.

## API
- `POST /fare` {pickup, destination} -> Fare.
- `POST /rides` {fareId} -> Ride (starts matching).
- `POST /drivers/location` {lat, long} (driverId from the session).
- `PATCH /rides/:rideId` {accept/deny}.
- Never trust userIds, timestamps or fares from the client.

## Data model
Entities: Rider, Driver, Fare (separate from Ride, could be merged), Ride (status, route, final fare, timestamps), Location (coordinates + last update). No complete schema in the source.

## Architecture (high-level design)
1. Fare: client -> API Gateway (auth, rate limiting) -> Ride Service -> external maps API -> pricing model -> Fare in DB.
2. Request: Ride with status "requested" linked to the Fare and triggering matching.
3. Matching: Location Service (receives/stores locations) + Ride Matching Service (ranking by proximity, availability, rating).
4. Acceptance: Notification Service (APNs/FCM) notifies the first driver; if they accept, Ride -> accepted and coordinates are returned; if they decline, the next one.

## Deep dives
1. **Location writes and proximity search** ([[geospatial-indexing]]): straight to the DB (bad); batch + geospatial DB (quadtree/PostGIS; stale positions) (good); **geospatial Redis** with GEOADD/GEOSEARCH and a sorted set by timestamp to clean up offline drivers (~30 s) (excellent; durability with RDB/AOF and Sentinel, rebuilt in ~5 s).
2. **Fewer updates without losing accuracy**: adaptive intervals on the client based on speed, direction changes, proximity to requests and state.
3. **Double assignment** ([[distributed-lock]]): application locks (bad); state in the DB with a timeout (good; the in-memory timeout is lost, a cron releases it with a delay); **Redis lock with a 10 s TTL** on driverId (excellent; depends on Redis).
4. **Not losing requests at peaks/outages** ([[message-queues]]): no queue (bad); queue with dynamic scaling (Kafka with offset commit after finding a match; SQS/MSK/Confluent; geographically partitioned; priority queue to avoid FIFO blocking).
5. **Driver does not respond**: delay queue (SQS) with a 10 s timeout (good; message management and cancellation, races) or **durable execution** with Temporal/Step Functions ([[workflow-orchestration]]) iterating over the sorted list (excellent).
6. **Scaling latency/throughput**: vertical (bad); **geo-sharding** with read replicas ([[database-partitioning]]), scatter-gather only at borders; consistent hashing and replication against imbalances.

## Trade-offs and decisions
- Location freshness vs write load (batching, adaptive intervals).
- Redis is fast but has durability risk; the DB remains the source of truth.
- Durable workflow: operational complexity in exchange for robustness.

## Related concepts
[[geospatial-indexing]], [[distributed-lock]], [[message-queues]], [[workflow-orchestration]], [[database-partitioning]], [[server-sent-events]] (real-time push, per the linked pattern)

## Follow-up questions
No list. Expectations: mid = APIs, HLD, spatial index idea and a "good" lock; senior = go deep on 2 of location/locking/queues; staff = 3+ areas with hands-on experience.

## Variants
- **Grokking the System Design Interview (PDF), pp. 148-153** (difficulty Hard; requires Yelp): reuses Yelp's [[quadtree]] adapted to moving objects.
  - Scale: 300 M customers, 1 M drivers, 1 M daily active customers and 500 K daily active drivers; drivers report position every 3 s.
  - Problem: updating the QuadTree for every report is expensive -> hash table `DriverLocationHT` (35 B/driver, 35 MB for 1 M; 19 B x 1 M every 3 s ≈ 19 MB per cycle of bandwidth) and refresh the QuadTree every ~15 s; cushion before re-partitioning grids; replicated Driver Location servers with SSD persistence.
  - Push: pub/sub notification service (subscriptions ≈ 21 MB; 2.5 M subscribers x 19 B ≈ 47.5 MB/s) with long polling or push notifications, but it complicates dynamic driver additions in the area; simpler alternative: the client **pulls every ~5 s**.
  - Ride request: aggregator queries QuadTree servers, sorts by rating and notifies the top 3 at once (the first to accept wins, the others receive a cancellation; if nobody responds, the next 3).
  - Ranking by rating: top-N per partition + aggregator. Advanced topics: slow networks, disconnection during a ride (billing), pull vs push.

---
title: Nearby Friends
type: interview
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 2 Nearby Friends, pp. 35-58]
concepts: [websockets, pub-sub, consistent-hashing, service-discovery, geohash, geospatial-indexing, database-partitioning, stateless-architecture, caching]
difficulty: high
---

# Nearby Friends

## Prompt
Backend for a "Nearby Friends" mobile feature: for users who grant location permission (opt-in), the app shows geographically nearby friends, with distance and timestamp of the last update. Unlike [[proximity-service]], locations change continuously.

## Functional requirements
- See nearby friends (each entry with distance and timestamp).
- The list updates every few seconds.
- "Nearby" = 5 miles (configurable), straight-line distance. Friends inactive > 10 min disappear from the list.
- Location history is stored (useful for ML). GDPR out of scope.

## Non-functional requirements
- Low latency when receiving updates.
- Overall reliability; losing the occasional data point is tolerated.
- Eventual consistency: a few seconds of delay between replicas is acceptable.

## Estimations
- 1,000 M users, 10% use the feature = 100 M DAU; concurrent = 10% of DAU = 10 M.
- Location refresh every 30 s (walking ~3-4 mph) -> **334,000 updates/s** (10M/30).
- 400 friends per user on average; ~10% online and nearby -> 334K x 400 x 10% ~ **14 M forwards/s**; ~40 per update.
- List of 20 friends per page.

## API
WebSocket (not plain HTTP):
1. Periodic location update: client sends lat, long, timestamp; no response.
2. Client receives a friend's location update (location + timestamp).
3. Initialization: client sends lat/long/timestamp, receives friends' locations.
4. Subscribe to a new friend (server sends friend ID; responds with last location).
5. Unsubscribe from a friend.
HTTP (stateless API servers): friend additions/removals, profile, etc.

## Data model
- **Location cache** (Redis): `user_id -> (lat, long, timestamp)`, with a TTL equal to the inactivity timeout (renewed on each update); a single location per user, does not need durability (if it goes down, it is replaced by an empty instance and re-warmed in 1-2 cycles).
- **Location history DB**: (user_id, lat, long, timestamp); massive writes and horizontally scalable -> Cassandra, or relational sharded by user ID.
- **User DB**: profiles and friendships (relational or NoSQL), shard by user ID; at this scale it is usually an internal service owned by another team.

## Architecture (high-level design)
- Peer-to-peer discarded (mobile devices with unstable connections and limited battery). A shared backend is used that receives updates, finds active friends and forwards if they are within the radius.
- Components: load balancer; stateless REST API servers; stateful **WebSocket servers** (one persistent connection per client; client initialization); Redis location cache; user DB; location history DB; **Redis Pub/Sub** as the routing layer.
- Each user has their own Pub/Sub channel; each friend's WebSocket handler subscribes to it.
- Update flow: client -> LB -> WebSocket server -> (in parallel) saves to history DB, updates location cache (renews TTL) and the handler's local variable, publishes to the user's channel -> Pub/Sub broadcasts to subscriber handlers (online friends) -> each handler computes the distance with the stored location and, if within the radius, sends location and timestamp to the client; otherwise discards.
- Client initialization: updates cache and variable, loads friends from the user DB, batch-queries the location cache (inactive ones are absent due to TTL), computes distances and returns the nearby ones, subscribes to the channel of **all** friends (active and inactive) and publishes its current location.

## Deep dives
- **API servers**: stateless, standard autoscaling.
- **WebSocket servers**: stateful; to remove a node it is marked "draining" in the LB and you wait for connections to close; same care in deployments.
- **Location cache**: 10M users x <=100 B fits in one Redis, but 334K writes/s is too much -> shard by user ID; standby replica per shard.
- **Redis Pub/Sub**: creating channels is cheap (a channel with no updates consumes no CPU; messages without subscribers are discarded). Subscribing to all friends simplifies things (no need to manage activations) at the cost of memory.
  - Memory: 100M channels x 20 B per subscriber x ~100 active friends = ~200 GB -> ~2 servers of 100 GB.
  - CPU: 14M pushes/s at ~100,000 pushes/s per server (conservative estimate) -> ~**140 servers**. The bottleneck is CPU, not memory.
  - Distributed cluster: shard by publisher's user ID with a **hash ring** ([[consistent-hashing]]) stored in service discovery (etcd/ZooKeeper, key e.g. `/config/pub_sub_ring`); WebSocket servers cache the ring and subscribe to changes.
  - Scaling: the Pub/Sub cluster is **stateful** (subscriber list per channel). When resizing, many channels change servers and there is a resubscription storm (temporary loss of updates) -> overprovision, resize during off-peak hours, update the ring and watch WebSocket CPU.
  - Replacing a failed node: only its channels move; the operator changes the ring entry (`p_1 -> p_1_new`) and each handler resubscribes to its affected channels.
- **Adding/removing friends**: callback on the client that notifies the WebSocket server to (un)subscribe and receive the last location; same for opt-in/out.
- **Users with many friends**: friend cap (Facebook: 5,000), bidirectional friendship (not the celebrity follower model); subscribers are spread across many WebSocket servers and "whale" users across >100 Pub/Sub servers.
- **Nearby random person (extra)**: pool of Pub/Sub channels by [[geohash]]; each client subscribes to its geohash and the 8 neighbors to cover borders.
- **Alternative to Redis Pub/Sub: Erlang/Elixir** (BEAM/OTP): lightweight processes (~300 B, millions per server), one process per user with native subscription to their friends' processes; lower operational overhead, but little talent is available.

## Trade-offs and decisions
- Pub/Sub per user and subscribing to all friends: more memory for simplicity.
- Location cache without durability with TTL: losing updates during re-warming is accepted.
- Pub/Sub cluster treated as stateful and overprovisioned versus aggressive autoscaling.
- Redis Pub/Sub vs Erlang: simplicity/ecosystem vs efficiency/hiring.

## Related concepts
[[websockets]], [[pub-sub]], [[consistent-hashing]], [[service-discovery]], [[geohash]], [[geospatial-indexing]], [[database-partitioning]], [[stateless-architecture]], [[caching]]

## Follow-up questions
- Show random nearby people who have opted in.
- What happens when scaling or replacing Pub/Sub nodes.
- Users with a huge number of friends.
- Alternatives to routing with Redis Pub/Sub.

## Variants
- Compare with [[yelp]]/[[proximity-service]] (static locations, geohash/quadtree) and with [[uber]] (mobile driver locations with Redis geo).

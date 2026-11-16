---
title: Distributed Rate Limiter
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/distributed-rate-limiter, System Design Interview Vol.1 (Alex Xu) ch. 4, Grokking the System Design Interview (PDF), "Designing an API Rate Limiter" pp. 100-112]
concepts: [rate-limiting, consistent-hashing, hot-keys, database-partitioning, pub-sub, multi-data-center, redis-sorted-sets]
difficulty: medium
---

# Distributed Rate Limiter

## Prompt
A request-level rate limiter for a social network's API: it limits HTTP requests per client and time window and rejects the excess with HTTP 429.

## Functional requirements
- Identify clients by user ID, IP or API key.
- Limit according to configurable rules (e.g. 100 req/min per user).
- On exceeding: 429 with remaining-quota and reset headers.
- Out of scope: analytics on the data, long-term persistence.

## Non-functional requirements
- < 10 ms per check.
- High availability (eventual consistency across nodes).
- 1M req/s with 100M DAU. Out of scope: strong consistency.

## Estimations
- One Redis: ~100-200k ops/s; each check needs several (HMGET + HSET) -> ~50-100k checks/s; plan ≈ 10 shards.
- *Note*: the source mentions "10M users" in the scaling section versus 100M DAU in the requirements.

## API
`isRequestAllowed(clientId, ruleId) -> {passes, remaining, resetTime}`. 429 with X-RateLimit-Limit/Remaining/Reset and optional Retry-After; JSON body. It fails fast (no queueing: it consumes resources, encourages retries, unpredictable latency).

## Data model
- Token bucket state: Redis hash per client (`tokens`, `last_refill`) with a 1 h EXPIRE.
- Fixed window example: keys per window with a counter.
- Rules table (client_type, endpoint, requests_per_minute) queried by the gateways.
- Entities: Rules, Clients, Requests.

## Architecture (high-level design)
- Placement: in-process (bad, sees only its own share); dedicated service (good, network hop and point of failure); **API gateway/LB** (chosen, requires fast shared state: Redis).
- Identifiers: JWT, X-Forwarded-For (beware of NAT), X-API-Key. Layered rules (user, IP, global, endpoint): the most restrictive wins.
- Algorithms ([[rate-limiting]]): fixed window, sliding window log, sliding window counter and **token bucket** (chosen).
- Redis implementation: HMGET -> compute tokens from elapsed time -> MULTI/EXEC + EXPIRE. Race condition when reading outside the transaction -> atomic **Lua script**.

## Deep dives
1. **1M req/s**: shard by client identifier; consistent hashing in the gateways or Redis Cluster (16,384 hash slots, recommended).
2. **HA and fault tolerance**: fail-closed (protects the backend, API partially down) vs fail-open (API up, risk of cascade). Fail-closed chosen. Primary-replica with failover; monitor Redis, rates and alerts when entering fail-open.
3. **Latency**: connection pooling (TCP handshake 20-50 ms), multi-region deployment with eventual consistency; local cache, pipelining and batching only if asked.
4. **Hot keys** ([[hot-keys]]): legitimate clients (client-side rate limiting, batching, premium tiers) and abusive ones (temporary blocklist in Redis, DDoS protection); higher IP limits because of NAT.
5. **Dynamic configuration**: polling (~30 s, simple, delay) vs push (ZooKeeper, [[pub-sub]], persistent connections: fast but complex; for security incidents).

## Trade-offs and decisions
- Token bucket: bursts + simplicity/memory; cold start is delicate.
- Fail-closed for backend protection over availability.
- Gateway: no extra hop but only HTTP context.

## Related concepts
[[rate-limiting]], [[consistent-hashing]], [[hot-keys]], [[database-partitioning]], [[pub-sub]]

## Follow-up questions
No list. Expectations: mid = one algorithm, gateway, Redis; senior = compare algorithms, atomicity, Redis Cluster, fail-open/closed; staff = operations, multi-region, rollouts.

## Variants
- **System Design Interview Vol. 1 (Alex Xu), ch. 4**: algorithm- and middleware-oriented approach. Scope: server-side rate limiter, flexible rules (IP, user ID...), large scale, distributed, inform the user with 429, low latency, low memory and high fault tolerance.
  - Differences from the base design: presents five algorithms (token bucket, leaking bucket, fixed window, sliding window log, sliding window counter; see [[rate-limiting]]) without choosing a single one; counters in Redis with `INCR`/`EXPIRE`; rules on disk that workers load into cache; rate-limited requests can be queued for later processing (as opposed to the base design's "fail fast"); `X-Ratelimit-*` headers.
  - Distributed: race condition (Lua script or sorted sets instead of locks) and synchronization via centralized Redis instead of sticky sessions; multi data center and eventual consistency ([[multi-data-center]]).
  - Wrap-up: hard vs soft limiting, limiting at other OSI layers, avoiding being rate limited (client cache, backoff).
  - Source: System Design Interview Vol. 1 (Alex Xu), ch. 4, pp. 51-69.

- **Grokking the System Design Interview (PDF), pp. 100-112** (difficulty Medium): per-user/IP rate limiter with memory detail per algorithm.
  - Requirements: limit per entity and window (e.g. 15 req/s) enforceable across a cluster; HA and no substantial latency. Hard / soft (e.g. +10%) / elastic throttling.
  - Algorithms: fixed window (allows double the requests at the window boundary and has an atomicity problem) -> **sliding window with a sorted set of timestamps** (~12 KB/user at 500 requests/h, 12 GB for 1 M users) -> **sliding window with counters** per minute in a Redis hash (~1.6 KB/user, 1.6 GB per 1 M). Simple fixed window: 12 B/record + 20 B overhead -> 32 MB per 1 M users.
  - Atomicity with a Redis lock (slow) or a custom implementation; scale: 10 req/s x 1 M users = 10 M QPS -> external Redis/Memcached.
  - Sharding with [[consistent-hashing]] per user (and per API if limits differ); write-back cache of counters; LRU.
  - IP vs user vs hybrid: IP (shared NATs, IPv6 memory) and user (DoS on login) both have weaknesses; the hybrid costs more memory. See [[rate-limiting]] y [[redis-sorted-sets]].

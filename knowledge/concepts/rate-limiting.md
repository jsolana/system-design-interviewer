---
title: Rate limiting
type: concept
aliases: [throttling, token bucket, rate limiter]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/distributed-rate-limiter, System Design Interview Vol.1 (Alex Xu), ch. 4, Grokking the System Design Interview (PDF), "Designing an API Rate Limiter" pp. 100-112]
---

# Rate limiting

## Definition
Limiting how many requests a client can make in a time window; the excess is rejected (HTTP 429).

## Why it matters
Protects backends from abuse, spikes and DDoS.

## How it works
- Identify the client (user ID, IP, API key) and apply rules in layers; the most restrictive wins.
- 429 response with X-RateLimit-Limit/Remaining/Reset and Retry-After; fail fast, do not queue.
- Shared state in Redis, with an atomic read-compute-write operation (Lua script).

## Variants and techniques
| Algorithm | Note |
|---|---|
| Fixed window | simple; bursts at the boundary |
| Sliding window log | exact, lots of memory |
| Sliding window counter | two weighted counters; approximate |
| Token bucket | bursts + constant refill; cheap (chosen) |

Placement: gateway/LB (preferred), dedicated service, in-process. Scaling: shard by client (Redis Cluster, 16,384 slots).

## Trade-offs
Fail-open (availability, risk of cascade) vs fail-closed (protects backend). Multi-region: eventual consistency.

## When to use it / when not to
Public and multi-tenant APIs; always decide the policy for when the store goes down.

## Additional detail (Xu Vol. 1, ch. 4)
Benefits: prevent DoS/starvation, reduce costs (pay-per-call APIs) and avoid server overload.
**Placement**: client-side is unreliable (requests can be forged); server-side or **middleware / API gateway** (also SSL termination, auth, IP whitelisting). Depends on the stack, control over the algorithm and engineering resources; commercial gateway if resources are lacking.

| Algorithm | Parameters | Pros | Cons |
|---|---|---|---|
| Token bucket (Amazon, Stripe) | bucket size, refill rate | simple, low memory, allows bursts | hard to tune parameters |
| Leaking bucket (Shopify) | queue size, outflow rate; FIFO queue at a fixed rate | bounded memory, stable flow | a burst fills the queue with old requests and recent ones are throttled; hard to tune |
| Fixed window counter | threshold per window | simple, low memory | bursts at the boundary let up to 2x the quota through (e.g. 5/min -> 10 in 2:00:30-2:01:30) |
| Sliding window log | timestamps (Redis sorted set) | very accurate | lots of memory (stores even rejected requests) |
| Sliding window counter | counters for current and previous window | smooths spikes, low memory | approximate; Cloudflare: 0.003% misclassified out of 400M |

Sliding window counter formula: `requests_current_window + requests_previous_window x %overlap`. Ex.: 3 + 5 x 0.7 = 6.5 -> 6 with limit 7 (accepted).
Number of buckets: one per endpoint and user (e.g. 1 post/s, 150 friends/day, 5 likes/s = 3 buckets), one per IP, or one global.
**Architecture**: counters in in-memory cache (Redis `INCR` + `EXPIRE`), not on disk. Rules in configuration files on disk (Lyft-style format: domain/descriptors/unit/requests_per_unit), which workers load into cache. Throttled requests: 429 and optionally sent to a queue to process later. Headers: `X-Ratelimit-Remaining`, `X-Ratelimit-Limit`, `X-Ratelimit-Retry-After`.
**Distributed**: race condition in read-check-increment (locks are slow; use a Lua script or Redis sorted sets); synchronization between rate limiters: sticky sessions are discouraged, a centralized store (Redis) is better. Optimization: multi data center/edge ([[multi-data-center]]) and synchronization with eventual consistency. Monitor the effectiveness of the algorithm and the rules (flash sale -> token bucket).
Extras: **hard vs soft** limit; other OSI layers (iptables at layer 3); client best practices (cache, no bursts, catch errors, backoff on retries).

## Additional detail (Grokking, pp. 100-112)
- Types of throttling: hard (never exceeded), soft (up to a % extra), elastic (exceeds if there are free resources).
- Fixed window lets up to 2x through at the boundary and suffers race conditions (read-modify-write); sliding window log with a sorted set ([[redis-sorted-sets]]) ~12 KB/user (500 requests), sliding window with per-minute counters in a Redis hash ~1.6 KB/user; fixed window ~32 MB per 1 M users.
- Limiting by IP (shared NAT, IPv6 memory), by user (DoS on the login endpoint) or hybrid (more memory). Detail in [[distributed-rate-limiter]].

## Appears in
[[camelcamelcamel]], [[distributed-rate-limiter]], [[fb-news-feed]], [[notification-system]], [[stock-exchange]], [[url-shortener]], [[web-crawler]]

## See also
[[hot-keys]], [[consistent-hashing]], [[caching]]

---
title: URL Shortener (Bitly)
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly, System Design Interview Vol.1 (Alex Xu) ch. 8, Grokking the System Design Interview (PDF), "Designing a URL Shortening service like TinyURL" pp. 12-29]
concepts: [unique-id-generation, bloom-filter, rate-limiting, stateless-architecture, base62-encoding, http-redirects, database-indexing, caching, cdn-edge-computing, key-generation-service, consistent-hashing]
difficulty: low
---

# URL Shortener (Bitly)

## Prompt
Design a URL shortener like Bit.ly: it turns long URLs into short links on its own domain and redirects to the original. Analytics out of scope.

## Functional requirements
- Given a long URL, return a short URL (custom alias and expiration date optional).
- Visiting the short URL redirects to the original.
- Out of scope: authentication/accounts, click analytics, spam/malware filtering.

## Non-functional requirements
- Each short code maps to a single long URL.
- Redirect < 100 ms.
- Availability 99.99 % (availability is prioritized over consistency).
- Scale: 1B URLs and 100M DAU.

## Estimations
- Read:write ratio ~1000:1.
- 100M DAU x 5 redirects/day = 500M/day ≈ 5,787 RPS average; assumed 100x peak ≈ 600k reads/s.
- ~100k new URLs/day ≈ 1 write/s.
- Row ~200 B, rounded to 500 B with metadata: 1B rows ≈ 500 GB (fits on an SSD).
- Base62: 62^6 ≈ 56B, 62^7 ≈ 3.5T, 62^8 ≈ 218T; 1B URLs fit in 6 characters.
- References: memory ~100 ns, SSD ~0.1 ms (~100k IOPS), HDD ~10 ms (100-200 IOPS); Redis 100k+ ops/s.

## API
- `POST /urls` {long_url, custom_alias?, expiration_date?} -> {short_url}
- `GET /{short_code}` -> 302 to the long URL; 410 Gone if expired.

## Data model
Table with PK `short_code` -> long URL, creation time, custom alias, expiration date, metadata (creator ID, analytics ID). Entities: Original URL, Short URL, User.

## Architecture (high-level design)
Client -> server (validation, logic, code generation) -> database.
- Create: validate format, (optional dedup; several codes per URL is common), generate a code or check the alias is free, store, return.
- Redirect: look up the code, check expiration, respond 302 (see [[http-redirects]]).
- Cleanup of expired entries with a periodic job, or keep them with their date.
- Final design: separate Read Service and Write Service, Redis counter with batching and failover, cache layer (optional CDN/edge), replicated primary DB with backups.

## Deep dives
**1. Unique codes** (see [[unique-id-generation]], [[base62-encoding]])
- Bad: prefix of the long URL (collisions).
- Good: hash (SHA-256 of the canonicalized URL -> base62 -> first 8 chars). Deterministic, allows dedup; but collisions as the space fills (UNIQUE + bounded retries 3-5 with salt) and guessable without salt/HMAC.
- Great: atomic counter (Redis INCR) + base62. No collisions; but distributed coordination, enumerable sequential codes (mitigation: reversible XOR with a secret key) and growing length.
- Collision with alias: reserved prefix or separate namespace.

**2. Fast redirects**
- Good: B-tree index / PK on short_code (O(log n)); but 600k reads/s exceed one instance.
- Great: in-memory cache (Redis/Memcached), cache-aside, LRU, TTL <= URL expiration. Invalidation is rare (URLs are almost immutable). See [[caching]].
- Great: CDN + edge logic (Cloudflare Workers, Lambda@Edge). Cost/complexity in exchange for latency. See [[cdn-edge-computing]], [[database-indexing]].

**3. Scaling to 1B URLs / 100M DAU**
- 500 GB fit in one Postgres; sharding only as plan B. Any DB works (Postgres/MySQL/DynamoDB) because the cache absorbs reads and there is ~1 write/s.
- High availability: replication + backups.
- Separate Read and Write services; they scale independently.
- Global counter: centralized Redis (atomic, single-threaded); batching (each Write instance reserves blocks, e.g. 1000); Sentinel/Cluster for failover; losing unreplicated values is acceptable (only uniqueness matters; UNIQUE in the DB is the safety net).
- Multi-region: disjoint counter ranges per region (A: 0-1B, B: 1B-2B), writes to local Redis, reads with distributed caches.

## Trade-offs and decisions
| Decision | Option | Cost |
|---|---|---|
| Generation | Hash vs counter | Collisions/guessable vs coordination/enumerable |
| Redirect | 302 vs 301 | 302 always reaches the server (expiration, tracking) but more load |
| Latency | Cache vs CDN/edge | Edge: more expensive and harder to debug |
| Consistency | AP | Losing counter values is accepted |

## Related concepts
[[unique-id-generation]], [[base62-encoding]], [[http-redirects]], [[database-indexing]], [[caching]], [[cdn-edge-computing]]

## Follow-up questions
- How to prevent enumeration of sequential codes.
- How to operate the counter in multi-region.
- How to add click analytics (excluded here).

## Variants
- **System Design Interview Vol. 1 (Alex Xu), ch. 8, pp. 119-131**: same problem with a different scale and approach (classic tinyurl).
  - Requirements: 100M URLs/day, URL as short as possible with [0-9a-zA-Z], no deletion or update.
  - Estimations: 100M/24/3600 ≈ 1,160 writes/s; read:write 10:1 -> ≈ 11,600 reads/s; 10 years = 365,000M records; 100 B/URL -> 365 TB.
  - Length: smallest n with 62^n >= 365,000M -> **n = 7** (62^7 ≈ 3.5 trillion).
  - REST API: `POST api/v1/data/shorten {longUrl}` -> shortURL; `GET api/v1/{shortUrl}` -> redirect.
  - 301 (cached by the browser, less load) vs 302 (click analytics): see [[http-redirects]].
  - Data: relational table (id, shortURL, longURL) instead of an in-memory hash table.
  - Two functions: (a) **hash + collision resolution** (CRC32/MD5/SHA-1 truncated to 7 characters; if it collides a predefined string is appended and it retries; cost: querying the DB on every request, mitigable with a [[bloom-filter]]); (b) **base 62 conversion** of the ID from a distributed generator ([[base62-encoding]], example 11157 = [2,T,X] = "2TX"; ID 2009215674938 -> "zn9edcu"). Comparison: (a) fixed length, no ID generator, collisions resolved, not predictable; (b) no collisions, needs [[unique-id-generation]] (see [[unique-id-generator]]), variable length, predictable (security problem).
  - Shortening flow: if the longURL already exists return its shortURL; otherwise generate an ID, convert to base62 and store the row. Redirect: LB -> <shortURL,longURL> cache -> DB on a miss -> 404/invalid URL.
  - Wrap-up: [[rate-limiting]] against abuse, stateless web tier ([[stateless-architecture]]), DB replication and sharding, analytics, availability/consistency/reliability.

- **Grokking the System Design Interview (PDF), pp. 12-29** (Easy difficulty): same problem with a different scale and approach.
  - Requirements: short, unique alias, redirect, custom alias (max. 16 characters), configurable expiration; HA, low latency, unguessable links. Extended: analytics and REST API.
  - Estimations: 500 M new URLs/month, read:write 100:1 -> 50 B redirects/month; ~200 writes/s and ~20K reads/s; 30 B objects in 5 years x 500 B = 15 TB; ingress 100 KB/s, egress 10 MB/s; cache of 20 % of 1.7 B requests/day = ~170 GB.
  - API: `createURL(api_dev_key, original_url, custom_alias, user_name, expire_date)` and `deleteURL(api_dev_key, url_key)`; the `api_dev_key` allows quota-based throttling against abuse (exhausting keys).
  - Data: two tables (URL, User); billions of objects < 1 KB with no relations -> NoSQL key-value (DynamoDB, Cassandra, Riak).
  - Key generation: hash (MD5/SHA-256) + base64 with problems (same URL -> same key, URL-encoding, collisions) versus [[key-generation-service]] with a key-DB (68.7 B keys of 6 characters = 412 GB), standby and keys cached on app servers.
  - Partitioning by range (unbalanced) or by key hash (+ [[consistent-hashing]]); Memcache cache with LRU and cache replicas; LB at three points (client-app, app-DB, app-cache) Round Robin.
  - Lazy purge of expired links (on access + lightweight job at off-peak hours), reusable keys; telemetry (country, date, referrer, browser) with care on very busy URLs; public/private permissions (HTTP 401).

*Note (expectations per level according to the Hello Interview source)*: mid = basic flow, reasonable uniqueness, 302, index, cache with help; senior = hash vs counter, cache and invalidation, scaling the counter; staff = multi-region, ranges, failover, enumeration security.

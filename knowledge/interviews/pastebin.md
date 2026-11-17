---
title: Pastebin
type: interview
sources: [Cracking the Coding Interview ch. 9.8, Grokking the System Design Interview (PDF), "Designing Pastebin" pp. 30-37]
concepts: [key-generation-service, caching, database-partitioning, consistent-hashing, load-balancer, sql-vs-nosql, base62-encoding]
difficulty: low
---

# Pastebin

## Prompt
Web service where users store plain text and get a randomly generated URL to access it (similar: pastebin.com, pasted.co, chopapp.com). Difficulty in the source: Easy.

## Functional requirements
1. Upload text and receive a unique URL.
2. Text only.
3. Data and links expire after some time (configurable by the user).
4. Optional custom alias.
- Extended: analytics (accesses), REST API for other services.

## Non-functional requirements
- High reliability (do not lose uploaded data) and high availability.
- Real-time access with minimal latency.
- Links must not be guessable.

## Estimations
- Read:write 5:1; 1M new pastes/day -> ~12 pastes/s, 5M reads/day -> ~58 reads/s.
- Average size 10 KB (max 10 MB per paste): 1M x 10 KB = 10 GB/day; 10 years = 36 TB; 3.6 B pastes.
- Keys: 6 base64 characters (64^6 ≈ 68.7 B); 3.6 B x 6 B = 22 GB (negligible). With a maximum occupancy of 70%: ~51.4 TB.
- Bandwidth: ingress 120 KB/s, egress 0.6 MB/s.
- Cache (80-20 rule): 0.2 x 5M x 10 KB ≈ 10 GB.

## API
- `addPaste(api_dev_key, paste_data, custom_url, user_name, paste_name, expire_date)` -> URL or error.
- `getPaste(api_dev_key, api_paste_key)` -> text.
- `deletePaste(api_dev_key, api_paste_key)`.
- `api_dev_key` is used for quota-based throttling.

## Data model
Two stores: metadata (< 100 B per record: URL hash, content key in object storage, expiration, creation, user) and content in object storage (e.g. S3) under a key. No relationships except user-paste.

## Architecture (high-level design)
Application layer (reads/writes) + separate storage layer: metadata DB (MySQL or distributed key-value such as Dynamo/Cassandra) and object storage for the content; so they scale separately. LB and cache in front as in [[url-shortener]].

## Deep dives
- **Write**: the app server generates a random 6-character key; if there is a duplicate, regenerate; if a custom alias already exists, return an error to the user. Alternative: [[key-generation-service]] (key-DB with used/unused keys, standby replica, key cache on app servers).
- **Read**: the app server queries metadata and fetches the content from object storage.
- Purging expired items, partitioning/replication, cache and LB, security/permissions: same as [[url-shortener]].

## Trade-offs and decisions
- Separating metadata and content: allows scaling storage by adding servers without touching the metadata DB.
- Random key + retry (simple) vs KGS (no collisions, extra component).
- Limits on size (10 MB) and custom URL length to avoid abuse.

## Related concepts
[[key-generation-service]], [[caching]], [[database-partitioning]], [[consistent-hashing]], [[load-balancer]], [[sql-vs-nosql]], [[base62-encoding]]

## Follow-up questions
Not covered in the source.

## Variants
- **Cracking the Coding Interview (problem 9.8, pp. 145, 394-395)**: no accounts or editing; per-page analytics behind a "stats" link; documents deleted after long inactivity; URLs must not be guessable.
  - Store documents as files on servers (no search needed) with a DB mapping URL -> server/path; cache hot documents (no invalidation since immutable); shard by hash of URL, or encode the server in the URL and skip the DB (hard to add servers).
  - URL generation: avoid monotonically increasing ints (guessable). Random GUID (128-bit, ugly) or a random 10-char alphanumeric (36^10 combos): per-URL collision chance is tiny but across a billion URLs collisions will happen, so detect (file/DB exists) and retry.
  - Analytics: log raw visits (timestamp, IP, location) to files for flexibility, plus a precomputed per-URL, per-month counter store (sharded by URL); optionally sample visits with a per-URL storage probability that decreases with popularity and scale the count back up; cache the generated stats HTML.
  - Follow-ups: user accounts, new analytics such as referral source, stats shown with each document.

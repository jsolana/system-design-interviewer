---
title: Distributed Unique ID Generator
type: interview
sources: [System Design Interview Vol.1 (Alex Xu), ch. 7, pp. 110-118]
concepts: [unique-id-generation, replication, database-partitioning, multi-data-center]
difficulty: medium
---

# Distributed Unique ID Generator

## Prompt
Design a unique ID generator for distributed systems. A DB's `auto_increment` does not work: a single server is not enough and generating unique IDs across several DBs with low delay is hard.

## Functional requirements
- Unique, numeric-only IDs.
- Fit in 64 bits.
- Ordered by date (grow over time, not necessarily by 1).

## Non-functional requirements
- More than 10,000 IDs per second.
- High availability (critical system).

## Estimations
Only the scale figure: 10,000 IDs/s. One machine can generate up to 4096 IDs per millisecond (12 bits of sequence).

## API
Not covered in the source.

## Data model
64-bit Snowflake ID: 1 sign bit (always 0) + 41 timestamp bits (ms since an epoch, by default Twitter's 1288834974657 = 4 Nov 2010) + 5 bits of datacenter ID (32 DCs) + 5 bits of machine ID (32 machines/DC) + 12 bits of sequence number (reset to 0 every ms).

## Architecture (high-level design)
Options compared ([[unique-id-generation]]):
| Option | Pros | Cons |
|---|---|---|
| Multi-master replication (auto_increment with step k = number of servers) | scales with servers | hard with multiple DCs; IDs do not increase with time across servers; bad when adding/removing servers |
| UUID (128 bits) | no coordination, simple, scales with web servers; collision unlikely (50% after 1,000M/s for ~100 years) | 128 bits (>64), not time-ordered, may not be numeric |
| Ticket server (Flickr; centralized auto_increment) | numeric, easy, valid for small/medium scale | SPOF; several ticket servers require synchronization |
| **Twitter Snowflake** (chosen) | divide and conquer: 64 bits in sections; meets all requirements | assumes synchronized clocks |

## Deep dives
- Datacenter ID and machine ID are fixed at startup; changing them requires review (risk of ID conflicts).
- Timestamp: 2^41-1 ms ≈ **69 years**; a custom epoch close to today delays overflow; afterwards the epoch must be changed or IDs migrated. Because they sit in the high bits, IDs are sortable by time.
- Sequence: 2^12 = 4096 combinations per ms per machine; it is 0 unless several IDs are generated in the same ms.

## Trade-offs and decisions
Snowflake chosen because it meets uniqueness, 64 bits, time ordering and scale without central coordination.

## Related concepts
[[unique-id-generation]], [[replication]], [[database-partitioning]], [[multi-data-center]]

## Follow-up questions
- **Clock synchronization**: the same clock is assumed on all generators; it fails with multiple cores/machines; the usual solution is NTP.
- **Section length tuning**: fewer sequence bits and more timestamp bits for low concurrency and long lifetime.
- **High availability** of the generator.

## Variants
Not covered in the source.

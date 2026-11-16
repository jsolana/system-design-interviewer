---
title: Back-of-the-envelope estimation
type: concept
aliases: [capacity planning, capacity estimation, QPS estimation]
sources: [System Design Interview (Alex Xu), Vol. 1, ch. 2 (pp. 34-40)]
---

# Back-of-the-envelope estimation

## Definition
Estimating capacity or performance with thought experiments and typical figures to know which designs meet the requirements (Jeff Dean).

## Why it matters
Validates that a design fits the scale. The process matters more than the result.

## How it works
Base knowledge: powers of 2 (volume units; one ASCII character = 1 byte), typical latencies (Dean's table, 2010) and availability levels.
Conclusions about latencies: memory is fast and disk is slow; avoid disk seeks; simple compression is fast, so compress before sending over the network; there is notable latency between regions.
**Availability**: measured in "nines" (99%-100%); the SLAs of Amazon, Google and Microsoft are >= 99.9%. More nines = less expected downtime. (The book's numeric tables cannot be extracted from the PDF.)

**Twitter example (exercise figures, not real)**: 300M MAU, 50% daily, 2 tweets/day, 10% with media, 5-year retention.
- DAU = 300M x 50% = 150M
- QPS = 150M x 2 / 24 / 3600 ≈ 3,500; peak = 2 x QPS ≈ 7,000
- Media: 150M x 2 x 10% x 1 MB = 30 TB/day; 5 years: 30 TB x 365 x 5 ≈ 55 PB.

## Variants and techniques
Common estimates: QPS, peak QPS, storage, cache, number of servers.

## Trade-offs
Round and approximate (e.g. 99987/9.1 ≈ 100000/10), write down assumptions and label units (5 KB vs 5 MB).

## When to use it / when not to
In step 2 of the interview ([[system-design-interview-framework]]) after agreeing on the design; warn the interviewer before spending time on it.

## Appears in


## See also
[[system-design-interview-framework]]

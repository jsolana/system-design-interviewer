---
title: Detect Duplicate URLs among 10 Billion
type: interview
sources: [Cracking the Coding Interview, 6th ed. (G. Laakmann McDowell), ch. 9 pp. 137-145 and solutions pp. 372-395 (problem 9.4)]
concepts: [data-deduplication, back-of-the-envelope-estimation, database-partitioning, batch-processing]
difficulty: low
---

# Detect Duplicate URLs among 10 Billion

## Prompt
You have 10 billion URLs. How do you detect duplicates? Duplicate means the URLs are identical.

## Functional requirements
Find all URLs that occur more than once.

## Non-functional requirements
Data does not fit in memory; tolerate failures if distributed.

## Estimations
10 billion URLs x 100 chars x 4 bytes = about 4 TB (4,000 GB).

## API
Not covered in the source.

## Data model
Not covered in the source (a list of URLs split into hash buckets).

## Architecture (high-level design)
- If it fit in memory: hash table URL -> seen (or sort and scan; sorting is slower for little gain).
- **Disk, one machine**: pass 1 writes each URL u into file hash(u) % 4000 (about 1 GB each, so identical URLs share a file). Pass 2 loads each file into a hash table and finds duplicates.
- **Multiple machines**: same, but send each URL to machine hash(u) % 4000.

## Deep dives
- Parallelism is the main pro of the multi-machine option (all 4000 chunks processed at once).
- Con: relies on 4000 machines working; failure handling and complexity grow.

## Trade-offs and decisions
Disk-based (simple, slow, serial) vs multi-machine (fast, fault handling needed). Discuss both with the interviewer.

## Related concepts
[[data-deduplication]], [[database-partitioning]], [[batch-processing]]

## Follow-up questions
Not covered in the source.

## Variants
Not covered in the source.

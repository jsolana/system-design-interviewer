---
title: Materialized views and data cubes
type: concept
aliases: [materialization, precomputed views, OLAP cube, materialized aggregates, view maintenance, hydrating IDs]
sources: [Designing Data-Intensive Applications, 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 2 (pp. 34-36), ch. 3 (pp. 72-75), ch. 4 (pp. 143-145)]
---

# Materialized views and data cubes

## Definition
*2nd edition (framed as a cross-cutting idea).* **Materialization** = precomputing and storing the result of a query. A materialized view is a real copy of query results (a virtual view is only a stored query expanded on read). Reads get faster, writes do more work.

## Why it matters
The book's running example: home timeline. Polling a join over posts/follows at 10M online users = 2M queries/s x 200 followees = 400M lookups/s. Materialized timelines instead: 500M posts/day (~5,800/s avg, peaks 150k/s) x ~200 followers = just over 1M timeline writes/s.

## How it works
- Fan-out on write into per-user timelines (cache); enqueue deliveries on spikes (slightly delayed but reads stay fast). Drop some writes for users following huge numbers of accounts; handle **celebrity** posts separately and merge on read.
- Timeline entries store only IDs; reading **hydrates** IDs (joins to posts/users) because likes, names and photos change fast. Joins at read time are easy to scale (parallel, cost independent of follower counts).
- **Data cube / OLAP cube**: grid of aggregates (e.g. SUM) over dimensions (date x product x ...); fast for precomputed queries, inflexible for other dimensions, so keep raw data too.
- Maintenance by databases automatically, by dedicated systems (Materialize) or by stream processing ([[stream-processing]], [[event-sourcing]] projections/read models, [[cqrs]]).

## Variants and techniques
Denormalization is a form of derived data needing an update process; materialized aggregates in warehouses ([[olap-columnar-stores]]).

## Trade-offs
Read speed vs write cost and consistency of copies after crashes (needs transactions or stream processing).

## When to use it / when not to
Read-heavy, expensive queries; avoid for rarely-read or highly volatile fields.

## Appears in
None yet.

## See also
[[fan-out]], [[derived-data-and-dataflow]], [[data-models]], [[caching]]

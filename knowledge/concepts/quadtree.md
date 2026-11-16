---
title: QuadTree
type: concept
aliases: [dynamic grid]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF) ch. 1 pp. 16-19, 22-23, Grokking the System Design Interview (PDF), "Designing Yelp" pp. 137-147 and "Designing Uber backend" pp. 148-153]
---

# QuadTree

## Definition
Tree in which each node represents a cell (grid) of the map and splits into 4 equally sized children when it exceeds a limit of places (e.g. 500). The leaves hold the list of places.

## Why it matters
It solves the uneven distribution of places: dense areas (downtown San Francisco) have many small cells and empty areas (the ocean) have huge cells. It is an in-memory geospatial index for proximity searches.

## How it works
- Evolution in the source: SQL with indexes on lat/long (huge lists to intersect) -> static grid (cell = search radius, 9 cells are queried; GridID index in a hash table) -> dynamic grid/QuadTree.
- **Construction**: root node = the world; while a node has > limit places, split it into 4 and distribute.
- **Finding a cell**: descend from the root choosing the child that contains the location.
- **Neighbors**: link leaves with a doubly linked list, or go up via parent pointers and down through siblings; expand until covering the radius or gathering N results.
- **Memory** (500M places): store only LocationID (8 B) + lat/long (16 B) = 24 B x 500M = 12 GB; 1M leaves (500M/500) and ~1/3 internal nodes with 4 pointers of 8 B ≈ 10 MB; total ≈ 12 GB, fits on one server.
- **Partitioning**: by region (zip codes; hot/uneven regions) or by LocationID hash (each server builds its QuadTree, all must be queried and results aggregated; the structures may differ but each server has ~ the same number of places). Master-slave replicas; to rebuild, a **QuadTree Index server** stores which places belong to each server.
- **Ranking by popularity**: each partition returns its top-N by rating, an aggregator merges; the rating is updated in the tree 1-2 times a day (during off-peak hours).

## Variants and techniques
**Moving objects (Uber)**: with locations every 3 s, updating the tree on every report is expensive (moving between cells, re-partitioning). Solution: `DriverLocationHT` hash table with the old/new position (35 B per driver ≈ 35 MB for 1M) updated continuously and refresh the QuadTree every ~15 s; leave a margin (cushion) over the limit before splitting/merging cells.

## Trade-offs
Fast for reads and small memory, but frequent updates are costly; uneven distribution complicates sharding by region.

## When to use it / when not to
Mostly static geographic data and radius searches. More modern alternatives: see [[geospatial-indexing]] (geohash, S2, etc.).

## Alternative calculation and operation (Xu & Lam Vol. 2, ch. 1)
- Leaf with <= 100 businesses: 32 B of coordinates + 8 B x 100 IDs = 832 B; internal node 64 B. For 200M businesses: 2M leaves + ~0.67M internal ~ 1.71 GB; construction ~ n log(n/100), minutes.
- It is an in-memory structure on each server (not a DB); during construction the server does not serve traffic: incremental deployments (blue/green overloads the DB).
- Hot updates require locking and rebalancing (O(log n)); alternative: incremental rebuild by subsets of servers with briefly stale data.
- Advantage over geohash: supports k-nearest and adaptive cells. See [[proximity-service]].

## Appears in
[[proximity-service]], [[uber]], [[yelp]]

## See also
[[geospatial-indexing]], [[database-partitioning]], [[consistent-hashing]]

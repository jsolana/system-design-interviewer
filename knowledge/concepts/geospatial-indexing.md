---
title: Geospatial indexing
type: concept
aliases: [geospatial search, nearby search]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF) ch. 1 pp. 1-34, https://www.hellointerview.com/learn/system-design/problem-breakdowns/tinder, https://www.hellointerview.com/learn/system-design/problem-breakdowns/gopuff, Grokking the System Design Interview (PDF), "Designing Yelp" pp. 139-147]
---

# Geospatial indexing

## Definition
Indexing data by location (lat/long) to resolve proximity queries efficiently.

## Why it matters
A SQL bounding-box query over lat/long without a suitable index is inefficient at scale ([[tinder]] feed).

## How it works
- Geospatial indexes in DBs or search engines (Elasticsearch/OpenSearch) combined with attribute filters (age, interests).
- Synchronization with the primary DB via [[change-data-capture]] and batched writes.
- In [[gopuff]]: pruning by fixed radius before using a travel-time service (straight-line distance ignores rivers/traffic).

## Variants and techniques
- [[uber]]: in-memory Redis GEOADD/GEOSEARCH for ~2M location writes/s; cleanup of offline drivers with a sorted set by timestamp (~30 s); batch + quadtree/PostGIS alternative (stale positions); geo-sharding.
Haversine/Euclidean with a threshold (simple, imprecise); radius pruning + driving-time estimation.

## Trade-offs
An additional index to keep in sync; accuracy vs cost of external calls.

## When to use it / when not to
"Near me" queries at scale.

## Additional detail (Grokking: grids and QuadTree)
Progression: SQL (lat/long indexes) -> static grid -> dynamic grid in a [[quadtree]] (max ~500 places per cell, 12 GB for 500M places). For moving objects ([[uber]]) the latest position (hash table) is separated from the periodic refresh of the tree. Detail and partitioning in [[quadtree]] and [[yelp]].

## Taxonomy and comparison (Xu & Lam Vol. 2, ch. 1)
- **Hash**: even grid, [[geohash]], cartesian tiers. **Tree**: [[quadtree]], Google S2, R-tree. Common idea: divide the map into small areas and index them.
- A 2D query with separate lat and long indexes does not scale: each index only helps in one dimension and huge datasets must be intersected.
- **Google S2**: Hilbert curve (points close on the curve = close in 1D), in memory; stands out in geofencing and in Region Cover (min/max level and max cells instead of fixed precision). Used by Google and Tinder.
- Industry use: geohash (Bing, Redis, MongoDB, Lyft), quadtree (Yext), both (Elasticsearch), S2 (Google Maps, Tinder).
- For the geohash index in a DB, one row per (geohash, business_id) is advisable, and scaling with read replicas rather than sharding if the dataset fits on one server. See [[proximity-service]].

## Appears in
[[airbnb-search-ranking]], [[google-maps]], [[nearby-friends]], [[proximity-service]], [[tinder]], [[uber]], [[uber-eta-prediction]]

## See also
[[database-indexing]], [[full-text-search]]

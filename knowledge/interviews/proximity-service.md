---
title: Proximity Service (nearby businesses)
type: interview
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 1 Proximity Service, pp. 1-34]
concepts: [geospatial-indexing, geohash, quadtree, caching, database-replication, database-partitioning, multi-data-center]
difficulty: medium
---

# Proximity Service

## Prompt
Design a service for discovering nearby places (restaurants, hotels, theaters...) such as Yelp's "nearby" search or the k nearest gas stations in Google Maps. It is a Location-Based Service (LBS) with **static** locations (unlike [[nearby-friends]]).

## Functional requirements
- Return businesses given a location (lat/long) and a radius.
- Owners can add, delete or update businesses; it does not need to be reflected in real time (agreed: effective the next day).
- Customers view a business's details.
- Radii allowed in the UI: 0.5, 1, 2, 5 and 20 km (max. 20 km). No constant page refresh (the user moves slowly). If there are not enough results, widen the search (optional, "if there is time").

## Non-functional requirements
- Low latency.
- Privacy of location data (GDPR, CCPA).
- High availability and scalability for spikes in dense areas.

## Estimations
- 100 M DAU, 200 M businesses.
- Seconds/day ~ 10^5 (rounding 86,400). 5 searches/user/day -> Search QPS = 100M x 5 / 10^5 = **5,000**.

## API
- `GET /v1/search/nearby` with `latitude`, `longitude`, `radius` (optional, default 5000 m). Response: `total` + `businesses` list (object with what is needed to render results). Mention pagination.
- Business: `GET /v1/businesses/:id`, `POST /v1/businesses`, `PUT /v1/businesses/:id`, `DELETE /v1/businesses/:id`.

## Data model
- Very read-heavy load (search and view business), few writes -> relational (MySQL) is valid.
- `business` table (PK `business_id`, address, city, state, country, latitude, longitude...).
- `geospatial_index` table (geohash, business_id). Better one row per (geohash, business_id) with a composite key than a JSON array per geohash (the array requires scanning to update/avoid duplicates and locking the row).

## Architecture (high-level design)
- Load balancer with path-based routing to two stateless services:
  - **LBS**: core; read-only, high QPS at peak hours, scales horizontally.
  - **Business service**: owner writes (low QPS) and detail reads (high QPS).
- Primary DB + replicas cluster: writes to the primary, reads to replicas (replication lag is tolerable).
- Search flow: client sends location and radius -> LBS picks geohash length according to radius -> computes the 8 neighbors -> queries the "Geohash" cache (Redis) in parallel -> hydrates with the "Business info" cache -> computes distances, sorts and returns.
- View/edit business: the business service reads from the "Business info" cache or the DB; updates are applied to the cache by a nightly job (consistent with the agreement that changes take effect the next day).

## Deep dives
**Search algorithms** (see [[geospatial-indexing]]):
1. *2D search* with SQL (BETWEEN on lat and long): scans a lot; per-column indexes give two huge datasets whose intersection is expensive (an index only helps in one dimension).
2. *Evenly divided grid*: very uneven distribution (New York vs. desert) and hard neighbors.
3. **[[geohash]]**: reduces 2D to a base32 string; useful lengths 4-6. Radius -> length: 0.5 km->6, 1 km->5, 2 km->5, 5 km->4, 20 km->4.
4. **[[quadtree]]**: in-memory tree on each LBS server, subdivided until <= 100 businesses per leaf (built at startup).
5. **Google S2**: Hilbert curve; flexible (Region Cover with min/max level and max cells), ideal for geofencing; too complex to explain in an interview (used by Google and Tinder).

Quadtree memory calculation: leaf = 32 B of coordinates + 8 B x 100 IDs = 832 B; internal node = 64 B (32 coords + 32 pointers). 200M/100 = 2M leaves; internal nodes ~ 1/3 = 0.67M. Total = 2M x 832 + 0.67M x 64 ~ **1.71 GB**. Build ~ n log(n/100), a few minutes with 200M businesses.

Operational considerations for the quadtree: while building, the server does not serve traffic -> incremental rollout (blue/green saturates the DB when loading 200M rows at once); update by rebuilding incrementally on subsets of servers (briefly stale data, acceptable) or update in place (requires locking with multithreading, complex; rebalancing too).

**Scaling the DB**
- `business` table: shard by `business_id` (uniform distribution).
- Geospatial index: the dataset is small (~1.71 GB equivalent) and fits in a server's working set; the common mistake is to shard immediately. Better **read replicas** (sharding adds application logic).

**Cache**: first ask whether it is needed (read-heavy load, small dataset, replicas as an alternative; requires benchmarking and cost analysis). If used:
- Key is **not** coordinates (imprecise and changing); use the geohash/cell.
- Two caches: `geohash -> list of business_id` (precomputed, TTL 1 day, at the three geohash levels geohash_4/5/6) and `business_id -> business object`.
- Memory: 8 B x 200M x 3 precisions ~ **5 GB** (fits in one Redis; the same content is deployed globally).

**Regions and AZs**: brings the service closer to the user (e.g. 10 ms vs 140 ms), spreads load in dense regions (Japan/Korea) and complies with data residency laws (DNS routing by country).

**Filters (open now, restaurant type)**: after the cell search the result is small; IDs are returned, hydrated and filtered by hours or type.

## Trade-offs and decisions
| Aspect | Geohash | Quadtree |
|---|---|---|
| Implementation | Simple, no tree | More complex |
| Radius | Supports well | Supports k-nearest (adapts until k results) |
| Cell size | Fixed per precision; adapting requires extra logic | Dynamic according to density |
| Updating the index | Easy (delete row) | O(log n), locking and rebalancing |
- Geohash is chosen in the example; S2 is avoided in interviews because of its complexity.
- Replicas instead of sharding for the index; cache only if justified.

## Related concepts
[[geospatial-indexing]], [[geohash]], [[quadtree]], [[caching]], [[database-replication]], [[database-partitioning]], [[multi-data-center]]

## Follow-up questions
- What to do if there are not enough businesses in the cell and its neighbors (see [[geohash]]: widen by removing digits).
- Filter by hours/business type.
- How to update the quadtree without downtime.

## Variants
- Compare with [[yelp]]: the Hello Interview/Grokking approach treats Yelp as a review platform; this chapter isolates the proximity service (Hash vs Tree indexes, 1.71 GB quadtree, geohash cache).

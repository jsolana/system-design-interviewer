---
title: Geohash
type: concept
aliases: [geohashing]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 1 Proximity Service, pp. 10-15, 22-23]
---

# Geohash

## Definition
Encoding that reduces (latitude, longitude) to a string of letters and digits (base32) by recursively dividing the world into grids; it is a hash-based geospatial index.

## Why it matters
It turns a 2D problem into a 1D one (prefix search), usable with a normal DB index or with Redis, with no in-memory tree.

## How it works
- First the planet is divided into 4 quadrants with the prime meridian and the equator: latitude [-90,0]=0, [0,90]=1; longitude [-180,0]=0, [0,180]=1.
- Each subdivision adds a bit, alternating longitude and latitude; this repeats until the desired precision and is encoded in base32 (e.g. Google HQ `9q9hvu`, Facebook HQ `949jhr`, length 6).
- 12 precision levels; only lengths 4-6 are of interest (shorter = huge cell, longer = tiny). Sizes: 4 ~ 39.1 km x 19.5 km; 5 ~ 4.9 x 4.9 km; 6 ~ 1.2 km x 609 m.
- Choose the minimum length whose cell covers the radius circle: 0.5 km->6; 1 km->5; 2 km->5; 5 km->4; 20 km->4.
- Longest common prefix = closest.

## Variants and techniques
- **Boundary problem 1**: two very close points may not share a prefix (on either side of the equator/prime meridian; e.g. La Roche-Chalais `u000` and Pomerol `ezzz`, 30 km). A simple `LIKE 'prefix%'` fails.
- **Boundary problem 2**: long common prefix but different cells. Solution: query the cell and its 8 neighbors (neighbors computable in constant time).
- **Too few results**: (1) return only those within the radius (simple, insufficient); (2) expand by removing the last digit of the geohash until enough are gathered (bigger cell); (3) enlarge the radius and recompute.
- Index table: one row per (geohash, business_id) instead of a JSON array.

## Trade-offs
- (+) Easy to implement and to update (delete a row); good radius support.
- (-) Fixed cell size per precision: doesn't adapt to density (the quadtree does); boundary problems.

## When to use it / when not to
Radius search over relatively static points; used by Bing Maps, Redis, MongoDB, Lyft. For k-nearest or variable density, [[quadtree]]; for geofencing, S2 (see [[geospatial-indexing]]).

## Appears in
[[google-maps]], [[nearby-friends]], [[proximity-service]]

## See also
[[geospatial-indexing]], [[quadtree]], [[proximity-service]]

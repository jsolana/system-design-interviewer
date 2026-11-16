---
title: Google Maps
type: interview
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 3 Google Maps, pp. 59-90]
concepts: [geohash, geospatial-indexing, cdn-edge-computing, message-queues, stream-processing, websockets, server-sent-events, long-polling, cap-theorem, caching]
difficulty: high
---

# Google Maps

## Prompt
Simplified version of Google Maps (1,000 M DAU, 99% coverage): user location updates, navigation with ETA, and map rendering on mobile.

## Functional requirements
- User location updates.
- Navigation service (routes) with ETA, taking traffic into account.
- Map rendering.
- Several travel modes (driving, walking, bus...); multi-stop is desirable but out of focus. Road data: TBs from external sources (assumed available).

## Non-functional requirements
- Accuracy (do not give wrong directions).
- Smooth navigation and rendering on the client.
- Low data and battery consumption.
- Availability and scalability.

## Estimations
- **World map**: zoom level 21 ~ 4.3 trillion tiles; 256x256 PNG tile ~ 100 KB -> ~440 PB; ~90% of the surface is ocean/desert and highly compressible -> reduce 80-90% -> ~50 PB; each lower level takes 4x less (series 50 + 50/4 + ...) -> ~67 PB, **~100 PB** in total.
- Road data: TBs; the derived routing tiles, also TBs.
- **Navigation**: 1,000 M DAU x 35 min/week = 5,000 M min/day. GPS every second = 300,000 M req/day = 3 M QPS; with a batch every 15 s -> **~200,000 QPS**; peak x5 = **1 M QPS**.
- **Map data**: at 30 km/h with 200 m x 200 m tiles: 25 tiles per km^2 = 2.5 MB; 75 MB/h = 1.25 MB/min. CDN: 5,000 M min x 1.25 MB = 62,500 MB/s; with 200 POPs, each POP serves a few hundred MB/s (the source gives it as ~2,500 in the OCR text, illegible; *Note*: 62,500/200 ~ 312 MB/s).

## API
- `POST /v1/locations` with `locs`: JSON array of (lat, long, timestamp), over HTTP keep-alive, sent in batches.
- `GET /v1/nav?origin=...&destination=...` -> distance, duration, polyline, instructions, geocoded waypoints, `travel_mode`.
- Map tile service (alternative): lat/long + zoom -> 9 tile URLs (the central one and the 8 neighbors).

## Data model
- **Routing tiles**: produced offline by the *routing tile processing service* from the road data; graphs (nodes = intersections, edges = roads) serialized as binary adjacency lists in **object storage (S3)**, organized by geohash and aggressively cached in the routing service.
- **User location**: Cassandra, partition key `user_id`, clustering key `timestamp` (fast latest position and efficient time ranges); columns user_mode, navigation_mode, lat/long. Prioritizes availability over consistency (CAP: AP).
- **Geocoding DB**: Redis (key-value, read-heavy, few writes): place/address -> lat/long.
- **Precomputed map images** per zoom level, on a CDN backed by S3.

## Architecture (high-level design)
Three functions behind a load balancer:
1. **Location service**: receives updates (batched every 15 s from the client, which records every second) and writes them to Cassandra and Kafka.
2. **Navigation service**: geocodes origin/destination and calls the route planner.
3. **Map rendering**: the client downloads static tiles from the CDN.

Navigation services: **Route planner** -> **Shortest-path service** (A* over routing tiles; top-k routes without traffic; cacheable because the graph changes little) -> **ETA service** (ML with current and historical traffic, predicts 10-20 min ahead) -> **Ranker** (user filters such as avoiding tolls/highways; sorts by ETA and returns top-k). **Updater services** consume the Kafka stream: traffic update service (feeds the Traffic DB), routing tile processing (new streets/closures), personalization ML, analytics.

## Deep dives
- **"Map 101" fundamentals**: lat/long; 3D->2D projection (Google uses Web Mercator); geocoding/reverse geocoding (interpolation over GIS data); geohash (here base 0-3 per level) for tiling; **map tiling** with tile sets per zoom (level 0 = 1 256x256 tile of the whole world).
- **Hierarchical routing tiles**: the world graph does not fit in memory and is not efficient for Dijkstra/A*; it is divided into tiles loadable on demand and with references between them. Three levels of detail: local streets, arterials, highways/interstates (edges between levels, e.g. a highway on-ramp).
- **Rendering**: (1) generate tiles on the fly (huge load, no cache) vs (2) **pregenerated tiles by geohash served by a CDN** (chosen; ~300 ms without CDN vs ~10 ms with CDN). 21 zoom levels; each level doubles tiles per axis (4x pixels). The client can compute the geohash/URL (fast but the algorithm is hard-wired into the apps and risky to change) or delegate to a **map tile service** that builds URLs (more operational flexibility).
- **Vector tiles (WebGL)**: send paths/polygons instead of images: better compression and smoother zoom (no pixelation when changing level).
- **Use of location data**: Cassandra + Kafka; the stream feeds live traffic, detection of new/closed roads, personalization, analytics.
- **Adaptive ETA and reroute**: we must know which active users are affected by a traffic change. Naive: a `user -> [r_1..r_k]` table and scan everything = O(n x m). Better: store per user the current tile and its "super" tiles at each higher level up to the one containing origin and destination; a user is affected only if the tile with the incident is inside the last tile of their row (filters out many users). To know whether the previous route can be resumed, store alternative routes and recompute ETAs periodically.
- **Server->client delivery protocol**: mobile push (4,096 B payload on iOS, not web), long polling, WebSocket, SSE; WebSocket is chosen (lightweight and bidirectional, e.g. last-mile).

## Trade-offs and decisions
- Client-side location batching: fewer QPS and less battery, at the cost of latency in live traffic.
- Cassandra (AP) for locations: the position becomes stale quickly, availability is prioritized.
- Routing tiles in object storage + cache instead of a DB or full in-memory.
- Static tiles on a CDN vs dynamic generation; client computes the URL vs a URL service; raster vs vector.
- Route accuracy matters more than computation latency (some latency is tolerated).

## Related concepts
[[geohash]], [[geospatial-indexing]], [[cdn-edge-computing]], [[message-queues]], [[stream-processing]], [[websockets]], [[server-sent-events]], [[long-polling]], [[cap-theorem]], [[caching]]

## Follow-up questions
- Multi-stop navigation for business customers (delivery: optimal visit order with live traffic).
- Traffic prediction 10-20 min ahead (algorithmic level, not covered).

## Variants
Not covered in the source (first treatment of Google Maps in the knowledge base).

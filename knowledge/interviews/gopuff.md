---
title: Gopuff (fast local delivery)
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/gopuff]
concepts: [caching, database-partitioning, database-indexing, distributed-lock]
difficulty: low
---

# Gopuff (Local Delivery Service)

## Prompt
Fast delivery service with many micro distribution centers (DCs). The customer sees what is deliverable in ~1 hour and orders without double-booking physical inventory. The source marks it "easy".

## Functional requirements
- Query availability of items deliverable within 1 h by location (union of the inventory of nearby DCs).
- Order several items at once.
- Out of scope: payments, routes/drivers, search/catalog, cancellations/returns.

## Non-functional requirements
- Availability < 100 ms.
- Strong consistency on orders (do not sell the same unit twice).
- 10k DCs, 100k items, ~10M orders/day.
- Out of scope: privacy, security, DR.

## Estimations
10M orders/day / 100k s/day x 10 page views per purchase / 0.05 conversion ≈ **20k QPS** of reads.

## API
- Availability: lat/long + filters (keyword), paginated.
- Place order: location + items (to validate delivery range).

## Data model
- Entities: **Item** (catalog), **Inventory** (physical unit in a DC, with an "ordered" status), **DistributionCenter** (lat/long), **Order**, OrderItems. Postgres, inventory partitioned by region (first 3 digits of the zip).

## Architecture (high-level design)
- Availability Service -> Nearby Service (DCs reachable within 1 h, uses an external Travel Time Service) -> inventory query for those DCs (join with items), sum and respond.
- Orders Service writes to the leader.
- Orders: *good* = two stores (orders and inventory) with [[distributed-lock]]; failures: crash between creating the order and decrementing (overselling, a sweeper is needed) and deadlocks with overlapping sets. *Great* = a single Postgres SERIALIZABLE transaction: check stock, mark "ordered", insert Order/OrderItems; if one is missing, everything fails. Downside: inventory and orders scale together.

## Deep dives
1. **DC by driving time**: bad = Euclidean/Haversine distance; bad = Travel Time Service against all DCs; great = sync DCs every ~5 min, prune with a fixed radius (~60 miles, the most optimistic hour) and call the service only with candidates.
2. **Fast, scalable reads**: great = Redis in front ([[caching]], TTL ~1 min; the Order Service must invalidate when inventory changes); great = [[database-partitioning]] by region + read replicas (tolerable staleness). Challenges: sizing replicas and balancing partitions.

## Trade-offs and decisions
- A transactional DB simplifies consistency but couples inventory and order scaling.
- Cache with short TTL vs active invalidation.

## Related concepts
[[caching]], [[database-partitioning]], [[distributed-lock]], [[database-indexing]]

## Follow-up questions
There is no concrete list in the source. Expectations: mid = APIs, data and both flows; senior = atomic transaction and read scale; staff = 2-3 deep dives with practical choices.

## Variants
Not covered in the source.

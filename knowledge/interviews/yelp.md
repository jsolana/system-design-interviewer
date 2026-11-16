---
title: Yelp (local business reviews)
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/yelp, Grokking the System Design Interview (PDF), "Designing Yelp or Nearby Friends" pp. 137-147]
concepts: [database-indexing, full-text-search, caching, quadtree]
difficulty: medium
---

# Yelp

> Note: the page is partially paywalled; only the prompt, requirements and deep dive questions were readable. Everything else is marked "Not covered in the source".

## Prompt
Design a local business review platform: search businesses, view reviews and leave reviews.

## Functional requirements
- Search businesses by name, location (lat/long) and category.
- View businesses and their reviews.
- Leave reviews: mandatory 1-5 rating and optional text.
- Out of scope: business creation/removal by admins, map view, personalized recommendations.

## Non-functional requirements
- Search latency < 500 ms.
- High availability (eventual consistency acceptable).
- Scale: 100M daily users, 10M businesses.
- Out of scope: GDPR, fault tolerance, spam/abuse.

## Estimations
Not covered in the source (only the scale targets).

## API
Not covered in the source.

## Data model
Not covered in the source.

## Architecture (high-level design)
Three flows: search businesses, view businesses, leave reviews. Detail not visible.

## Deep dives
Only visible questions (answers not covered in the source):
1. Computing and updating the average rating so that it is available in search results.
2. Ensuring a single review per user and business.
3. Handling complex searches more efficiently.
4. Supporting search by predefined places (cities, neighborhoods).

## Trade-offs and decisions
Not covered in the source.

## Related concepts
[[database-indexing]], [[full-text-search]], [[caching]] (*Note*: indicative links based on the type of problem, not confirmed by the source).

## Follow-up questions
The four deep dive questions.

## Variants
- **Grokking the System Design Interview (PDF), pp. 137-147** (difficulty Hard): approach centered on spatial index structures.
  - Scale: 500 M places; place record 793 B (LocationID 8 B, name 256 B, lat/long 8+8 B, description 512 B, category 1 B); reviews separate. Places are almost static (if they move, like taxis, the design is different).
  - Evolution: SQL with indexes on lat/long (huge lists to intersect) -> static grid (cell = radius, 9 cells; in-memory index of ~4 GB = 4 B x 20 M grids + 8 B x 500 M) -> **[[quadtree]]** of dynamic grids (max 500 places per leaf; ~12 GB of leaves + ~10 MB of internal nodes).
  - Neighbors via a doubly linked list of leaves or pointers to the parent.
  - Partitioning by region (zip code; hot and uneven) or by hash of LocationID (query all and aggregate, different trees per server); master-slave replicas and a **QuadTree Index server** for rebuilding; LRU cache of hot places; ranking by popularity with an aggregator and an update 1-2 times a day.

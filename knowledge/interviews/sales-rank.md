---
title: Sales Rank (best sellers overall and per category)
type: interview
sources: [Cracking the Coding Interview, 6th ed. (G. Laakmann McDowell), ch. 9 pp. 137-145 and solutions pp. 372-395 (problem 9.6)]
concepts: [batch-processing, caching, database-indexing, message-queues, back-of-the-envelope-estimation]
difficulty: medium
---

# Sales Rank (best sellers overall and per category)

## Prompt
A large e-commerce company wants to list best-selling products overall and by category (e.g. #1056 overall, #13 in Sports Equipment, #24 in Safety). Design the system.

## Functional requirements
- Rank = total sales over the past week (assumption; to be agreed with the interviewer).
- A product may belong to several categories; no subcategories.
- Categorization is based on the origin of the transaction/product, not price or date.

## Non-functional requirements
- Not 100% fresh: top items (e.g. top 100 per category) up to 1 hour old; less popular up to 1 day old.
- Window need not be exactly 168 hours.
- Precision matters for the most popular items only.

## Estimations
10 million products x (4-byte ID + 4-byte count) is about 40 MB, so in-memory aggregation fits comfortably.

## API
Not covered in the source (frontend reads rank from a rank cache).

## Data model
- Per product: weekly sales as a circular array of 7 day-counters plus a total; each purchase increments today's slot and total; each day the oldest slot is cleared (avoids recomputing a rolling window).
- Separate table product -> categories.

## Architecture (high-level design)
Naive: purchase system writes orders to the DB; hourly job aggregates by category, sorts and stores in an in-memory sales-rank cache; frontend reads that cache.

## Deep dives
- Analytics are expensive: keep only rolling totals instead of scanning all sales.
- Writes too frequent: buffer purchases in memory (plus a log file for durability) and flush periodically. Avoid bias by flushing everything up to a cut-off moment before re-ranking.
- Joins are expensive (tens of thousands of categories): either one join product x category sorted by (category, sales), then walk it once; or store denormalized rows per (product, category).
- Log-file/MapReduce alternative: each category has a directory; purchases are appended as (productID, time range, count); periodic jobs merge files; sorting a directory gives the category rank. Overall rank: write to an "all" directory, or N-way merge of the sorted category lists (cheaper: merge only the top ~100 pairwise; compute the full ranking lazily once a day). Scales by spreading files across servers.

## Trade-offs and decisions
Freshness vs cost (relaxed accuracy for the long tail); DB vs flat files + batch jobs; denormalization vs joins.

## Related concepts
[[batch-processing]], [[caching]], [[database-indexing]], [[database-normalization-and-denormalization]]

## Follow-up questions
Next bottlenecks; subcategories ("Sports" > "Sports Equipment" > "Tennis" > "Rackets"); 30-minute accuracy for all products.

## Variants
Not covered in the source.

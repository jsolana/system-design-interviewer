---
title: Cursor pagination
type: concept
aliases: [keyset pagination, cursor-based pagination]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-live-comments, https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-news-feed, https://github.blog/engineering/architecture-optimization/from-2500-requests-to-24-rebuilding-star-history-without-the-stargazers/]
---

# Cursor pagination

## Definition
Paginate by returning a cursor (id/timestamp of the last item seen) instead of a numeric offset.

## Why it matters
Offset is slow with growing data and unstable if items are inserted/deleted while paging (duplicates or gaps).

## How it works
`GET ...?cursor={last_id}&pageSize=N` -> query `id < cursor` descending with a limit, backed by an index (partition key + sort key in DynamoDB). In the feed, the cursor is the timestamp of the oldest post seen.

## Variants and techniques
`since=` for catch-up of newer items.

## Trade-offs
Does not allow jumping to an arbitrary page.

## When to use it / when not to
Ordered, continuously growing lists (comments, feeds).

## Additional detail (GitHub star history)
A smaller page does not mean a cheaper query: GitHub's stargazers endpoint recounted all stars per page (about 37,000 slow count queries in a week, avg nearly 3 s) and building a star curve needed about 2,511 requests for a 251k-star repo. The replacement endpoint filters by an indexed `created_at` range first, then groups into daily counts (30 weeks per call, about 24 requests, one pass over rows) instead of aggregate-then-LIMIT/OFFSET (about 6M rows examined). Lesson: return only what the use case needs; document remaining trade-offs (dense weeks, removed stars vanish). Source: https://github.blog/engineering/architecture-optimization/from-2500-requests-to-24-rebuilding-star-history-without-the-stargazers/

## Appears in
[[fb-live-comments]], [[google-news]]

## See also
[[database-indexing]]

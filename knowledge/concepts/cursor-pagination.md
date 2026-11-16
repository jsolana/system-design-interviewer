---
title: Cursor pagination
type: concept
aliases: [keyset pagination, cursor-based pagination]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-live-comments, https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-news-feed]
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

## Appears in
[[fb-live-comments]], [[google-news]]

## See also
[[database-indexing]]

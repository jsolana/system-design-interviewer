---
title: Online Auction
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/online-auction]
concepts: [optimistic-concurrency-control, server-sent-events]
difficulty: medium
---

# Online Auction

> Note: mostly paywalled page; only the problem statement, functional requirements and deep dive titles were readable. The source links to Real-time Updates, Dealing with Contention, Redis, Kafka, PostgreSQL, ZooKeeper and Flash Sale.

## Prompt
Online auction service: users list items and bid above the current maximum bid until closing; the highest bid wins.

## Functional requirements
- Post an item with a starting price and an end date.
- Bid: only accepted if it exceeds the current maximum bid.
- View an auction with the current maximum bid.
- Out of scope: search, filter by category, sort by price, history.

## Non-functional requirements
Not covered in the source (hidden).

## Estimations
Not covered in the source.

## API
Not covered in the source.

## Data model
Not covered in the source.

## Architecture (high-level design)
Not covered in the source (three flows: post, bid, view).

## Deep dives
Questions only: strong consistency in bids; fault tolerance and durability; showing the maximum bid in real time; scaling to 10M concurrent auctions.

## Trade-offs and decisions
Not covered in the source.

## Related concepts
[[optimistic-concurrency-control]], [[server-sent-events]] (*Note*: indicative, not confirmed by the source).

## Follow-up questions
The four deep dives.

## Variants
Not covered in the source.

---
title: Google News (news aggregator)
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/google-news]
concepts: [caching, cursor-pagination, cdn-edge-computing]
difficulty: medium
---

# Google News

> Note: paywalled page; only the prompt, requirements and deep dive titles are readable. Tagged pattern: Scaling Reads.

## Prompt
An aggregator that collects articles from thousands of publishers and shows them in a scrollable feed.

## Functional requirements
- View an aggregated feed of articles from thousands of publishers.
- "Infinite" scroll.
- Click an article -> redirect to the publisher's site.
- Out of scope: personalizing by interests, saving, sharing.

## Non-functional requirements
- Availability over consistency (somewhat old content is better than none).
- Feed < 200 ms and articles visible < 30 min after publication (according to the deep dive titles).

## Estimations
Not covered in the source.

## API
Not covered in the source.

## Data model
Not covered in the source.

## Architecture (high-level design)
Not covered in the source.

## Deep dives
Questions only: pagination consistency and efficiency; latency < 200 ms; appearance in < 30 min; efficient media handling; spikes from breaking news; extra: per-category feeds and personalized feeds.

## Trade-offs and decisions
Not covered in the source.

## Related concepts
[[caching]], [[cursor-pagination]], [[cdn-edge-computing]] (*Note*: indicative).

## Follow-up questions
The seven deep dives.

## Variants
Not covered in the source.

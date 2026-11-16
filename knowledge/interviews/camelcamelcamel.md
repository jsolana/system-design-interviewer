---
title: CamelCamelCamel (price tracking)
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/camelcamelcamel]
concepts: [rate-limiting, message-queues]
difficulty: medium
---

# CamelCamelCamel

> Note: page partially paywalled; only the prompt, requirements and deep dive questions are readable.

## Prompt
A service that tracks Amazon product prices and alerts when they drop below a threshold. Its Chrome extension (~1M active users) shows the history on the product page and allows subscribing with one click.

## Functional requirements
- View the price history of products (web or extension).
- Subscribe to price-drop alerts with a threshold.
- Out of scope: search, cross-store comparison, reviews.

## Non-functional requirements
- Availability over consistency (eventual).
- 500M Amazon products.
- History queries < 500 ms.
- Price-drop notification in < 1 h.
- The system must be "polite" to Amazon. Out of scope: strong consistency, real-time updates.

## Estimations
Not covered in the source.

## API
Not covered in the source.

## Data model
Not covered in the source.

## Architecture (high-level design)
Not covered in the source.

## Deep dives
Questions only: discovering and tracking 500M products efficiently; malicious prices sent from the extension; processing changes and notifying subscribers; fast history queries for charts.

## Trade-offs and decisions
Not covered in the source.

## Related concepts
Indicative (the source does not confirm it, inferred from the deep dive titles): [[rate-limiting]] (being "polite" to Amazon), [[message-queues]] (processing price changes and notifying).

## Follow-up questions
The four deep dives.

## Variants
Not covered in the source.

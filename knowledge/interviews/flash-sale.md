---
title: Flash Sale
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/flash-sale]
concepts: [distributed-lock, optimistic-concurrency-control, virtual-waiting-queue, server-sent-events]
difficulty: high
---

# Flash Sale

> Note: paywalled page; the prompt, functional requirements and deep dive questions are readable. Tagged patterns: Real-time Updates, Dealing with Contention, Scaling Writes.

## Prompt
Sell very little inventory under extreme demand (e.g. 10,000 sneakers at noon with tens of millions of users trying to buy within seconds): compete fairly and complete purchases without overselling.

## Functional requirements
- View the flash sale item.
- Reserve an available unit for a limited time while the sale is active.
- Whoever gets a unit completes the payment.
- The source stresses the **reservation** step: payment goes through a third party and takes seconds, and inventory cannot be held in an open transaction; the reservation removes the unit from availability instantly and payment is settled later.
- Out of scope: catalog, shipping/returns/orders, sale administration.

## Non-functional requirements
Not covered in the source.

## Estimations
Not covered in the source (only the example of 10,000 units and tens of millions of users).

## API
Not covered in the source.

## Data model
Not covered in the source.

## Architecture (high-level design)
Only three blocks: view item, reserve unit, complete payment.

## Deep dives
Questions only: consistency under extreme contention; releasing expired reservations efficiently; absorbing millions of users arriving at once; fair access to limited inventory.

## Trade-offs and decisions
Not covered in the source.

## Related concepts
[[distributed-lock]], [[optimistic-concurrency-control]], [[virtual-waiting-queue]], [[server-sent-events]] (*Note*: indicative; similar problem to [[ticketmaster]]).

## Follow-up questions
The four deep dives.

## Variants
Not covered in the source.

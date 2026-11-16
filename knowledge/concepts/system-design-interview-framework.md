---
title: System design interview framework
type: concept
aliases: [4-step process, marco de entrevista]
sources: [System Design Interview (Alex Xu), Vol. 1, ch. 3 (pp. 42-50)]
---

# System design interview framework

## Definition
4-step process for tackling open-ended design questions. The interview simulates collaboration between two colleagues facing an ambiguous problem; the process, communication and handling of ambiguity are evaluated more than the final design.

## Why it matters
The signals sought: collaboration, working under pressure, ability to ask good questions. Red flags: over-engineering, closed-mindedness, stubbornness.

## How it works
| Step | Time (45 min) | Content |
|---|---|---|
| 1. Understand the problem and scope it | 3-10 | Ask (features, users, growth rate, stack, DAU, media); write down assumptions; don't answer like "Jimmy" |
| 2. High-level design and buy-in | 10-15 | Box diagram (clients, APIs, servers, stores, cache, CDN, queue), estimates, concrete use cases, API/schema depending on the problem |
| 3. Deep dive | 10-25 | Prioritize components with the interviewer (e.g. hash function in a URL shortener; latency and presence in chat); avoid irrelevant details (EdgeRank) |
| 4. Wrap up | 3-5 | Bottlenecks, recap, error cases, operations (metrics/logs/rollout), next scale curve |

Example from the book: news feed split into *feed publishing* and *news feed building* ([[fb-news-feed]]).

## Variants and techniques
**Dos**: always ask, propose several options, communicate, treat the interviewer as a teammate, design the critical parts first. **Don'ts**: don't go in unprepared, don't jump to the solution, don't dive into the detail of one component at the start, don't think in silence, don't consider the interview finished.

## Trade-offs
Depth vs. breadth depending on level (senior: bottlenecks and resources).

## When to use it / when not to
Always as a guide; adapt timings to the problem.

## Appears in


## See also
[[back-of-the-envelope-estimation]]

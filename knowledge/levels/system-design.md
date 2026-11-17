---
title: Level expectations - system design interviews
type: level-guide
sources: [Authored guidance synthesized for this knowledge base (not extracted from a single source); calibrate with your target company's leveling guide]
---

# Level expectations: system design interviews

Note: this is general calibration guidance, not an official rubric of any company. Levels are judged on the quality of the whole conversation, not on whether the final diagram matches a reference.

## How the bar moves
| Signal | Junior | Mid | Senior | Staff | Staff+ |
|---|---|---|---|---|---|
| Who drives | Interviewer guides step by step | Follows a known framework, needs nudges on depth | Drives end to end, manages time | Drives and reshapes the problem | Frames the problem space and what not to build |
| Requirements | Takes them as given | Asks basic functional questions | Separates functional/non-functional, quantifies scale, states assumptions | Challenges requirements, identifies the real business constraint | Ties requirements to org/product strategy and cost of being wrong |
| Design breadth | Works for the happy path, one or two components | Complete working design, standard components | Complete design with justified choices and alternatives | Multi-system view: ownership boundaries, platform reuse, evolution | Roadmap across years/teams, build vs buy vs deprecate |
| Depth | Names technologies | Explains how a component works | Goes deep in 1-2 areas (storage, consistency, hot spots) and quantifies | Deep in several areas, anticipates failure and operational reality | Identifies the few decisions that are expensive to reverse |
| Trade-offs | Rarely stated | Mentions pros/cons when asked | Volunteers trade-offs with numbers and a recommendation | Weighs cost, operability, team skills, migration path | Weighs organizational and strategic risk, reversibility |
| Scale and failure | Not considered | Considered when prompted | Proactively handles scale, hot keys, partial failure, retries, idempotency | Capacity, SLOs, multi-region, degradation modes, incident learning | Reliability and cost strategy across a portfolio of systems |
| Operations | None | Basic monitoring mention | Metrics, alerts, rollout, rollback | SLOs/error budgets, safe deploys, on-call burden, migrations | Operating model, platform investments |
| Communication | Hesitant, jargon | Clear but linear | Structured, checks in, uses diagrams well | Teaches, simplifies, handles disagreement | Persuades, builds alignment across audiences |

## What a strong answer shows at each level
- **Junior**: understands the problem, proposes API + data model + a plausible architecture (client, server, database, cache), knows what each component is for. Weak spots expected: estimation, consistency, failure modes.
- **Mid**: complete design with reasonable component choices, basic estimation, can explain indexing, caching, replication and a queue where useful; reacts well to follow-ups.
- **Senior**: asks sharp clarifying questions, sizes the system, identifies the core bottleneck, chooses and defends a data store, reasons about consistency, hot keys, idempotency, backpressure, partial failures, and offers an alternative design with trade-offs.
- **Staff**: reframes ambiguous problems, proposes phases (MVP then scale), handles multi-team boundaries, cost, security, observability, SLOs, migration from the existing system, and knows what not to build.
- **Staff+**: speaks to platform strategy, standardization, org-wide reliability and cost, risk portfolio, long-lived decisions and how to enable other teams; may spend more time on the "why" than the diagram.

## Probing questions by level (use after the candidate's initial design, one at a time)
- **Junior/mid**: What does the schema look like? How do you scale reads? What happens if this server dies? What would you cache and for how long? How would you add pagination?
- **Senior**: How do you size storage and QPS? Where is the hot spot and how do you split it? How do you keep X and Y consistent? What happens on retry and duplicate delivery? Why this database over alternatives? How do you roll this out safely?
- **Staff**: What is the SLO and how do you alert on it? What is the blast radius of a bad deploy or bad config? How do you migrate existing users with no downtime? How does this change at 100x and across regions? What is the cost driver? What would you cut in v1?
- **Staff+**: Should this be a platform for other teams, and what is the contract? What decision here is hardest to reverse? How would you reduce the number of systems doing this across the company? How would you staff and sequence it?

## Frequent reasons candidates are down-leveled
- Jumping to boxes before clarifying requirements or scale.
- Naming technologies without explaining why or what they cost.
- Ignoring failure, retries, idempotency, backpressure or data loss.
- A single solution with no alternatives or trade-offs when the question is open-ended.
- Treating the interviewer's hints as the plan instead of owning the design.
- Not quantifying (no QPS, storage, latency, availability target).

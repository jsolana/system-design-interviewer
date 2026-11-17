---
title: On-call, toil and operational load
type: concept
aliases: [toil, SRE on-call, operational overload, simplicity, 50% rule]
sources: [https://sre.google/sre-book/eliminating-toil/, https://sre.google/sre-book/being-on-call/, https://sre.google/sre-book/simplicity/]
---

# On-call, toil and operational load

## Definition
**Toil** is operational work that is manual, repetitive, automatable, tactical, without enduring value and growing linearly with service size. Overhead like meetings is not toil.

## Why it matters
Toil expands to fill all time, demoralizes engineers and prevents the engineering work that makes systems scale. Design decisions determine whether a system needs a person per N machines or runs itself.

## How it works
- Cap toil below 50% of an SRE's time (surveyed average ~33%, range 0-80%; interrupts are the largest source, then on-call, then releases).
- On-call: at most 25% of time on-call; a 24/7 rotation with primary and secondary needs at least 8 people at one site or 6 per site across two. Max ~2 incidents per 12-hour shift. Response ~5 min (user-facing) to ~30 min.
- Fix overload by: symptom-based alerts ([[alerting-strategy]]), automation, loaning engineers, or returning the pager to the developers.
- Avoid underload too: engineers on-call at least once or twice a quarter, plus drills.
- **Simplicity**: boring, predictable software; resist accidental complexity; delete dead code; small releases; minimal APIs.

## Variants and techniques
Runbook automation, self-healing, service-level tiers, production readiness reviews.

## Trade-offs
Automation takes upfront engineering and can fail at scale (a missing sanity check in automation caused a mass wipe); follow-the-sun rotations add coordination cost but avoid night shifts.

## When to use it / when not to
Relevant when discussing operability and team ownership; keep it brief in interviews.

## Note: what a senior/staff candidate should say
Mention operability as a design goal: idempotent automation with sanity checks, safe defaults, self-healing, and avoiding designs that need manual rebalancing or hand-run migrations.

## Appears in
None yet.

## See also
[[incident-management-and-postmortems]], [[alerting-strategy]], [[scalability-reliability-maintainability]]

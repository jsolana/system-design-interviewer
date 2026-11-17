---
title: Safe deployments and rollback safety
type: concept
aliases: [hands-off deployments, CI/CD pipeline safety, two-phase deployment, one-box, bake time, canary]
sources: [https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/, https://aws.amazon.com/builders-library/ensuring-rollback-safety-during-deployments/]
---

# Safe deployments and rollback safety

## Definition
Deployment practice where changes reach production through automated pipelines with staged blast-radius control, automatic rollback and explicit backward-compatibility discipline, so no human watches a rollout.

## Why it matters
Bad changes (code, config, feature flags) are a leading outage cause; rolling updates mean old and new versions run simultaneously and rollback itself can break things.

## How it works (automated hands-off pipelines)
- Phases: source, build, test, prod. Separate pipelines per concern (app code, infrastructure, OS patching, config/flags, tooling); dependencies auto-upgraded at least weekly. Config and flags get the same rigor as code.
- Last manual step is **code review** (checklist: tests, monitoring, resource neutrality, deployable without alarms, rollback-safe). Builds run without network; unit tests mock dependencies; artifacts signed.
- Pre-prod: alpha/beta (functional, integration), **gamma** production-like in multiple Regions with canaries; one-box test 30-60 min; optional zeta (call prod endpoints).
- **Production waves** (example): wave 1 low-traffic Region, one AZ/cell at a time; wave 2 high-traffic Region; wave 3 three Regions; wave 4 up to 12; wave 5 rest. Avoids simultaneous multi-Region or multi-AZ impact (24 Regions/76 AZs one at a time would take weeks).
- **One-box in prod**: <= ~10% of a Region's/AZ's requests; auto rollback if impact. **Rolling**: <= ~33% of boxes at once (>=66% capacity); some teams 5%.
- **Auto rollback** to previous immutable package (checksum-verified) on alarms (fault rate, P50/P90/P99 latency, CPU, memory, disk, log errors, health checks); aggregate high-severity alarm (incl. canaries) rolls back all in-progress deployments of the team in the Region; one-box-scoped alarms; anomaly detection (traffic to zero).
- **Bake time**: >=1 h after one-box, >=12 h after first regional wave, 2-4 h after later waves, plus minimum data points (e.g. 100 requests). Global rollout ~4-5 business days. Urgent fixes shortened only with Principal Engineer review.
- **Blockers/time windows**: no deploys during alarms; avoid nights, weekends, holidays, often Fridays and late afternoons (too small a window piles up changes, too large prolongs off-hours impact). Pipelines defined as code with inheritance.

## Rollback safety
- Avoid **one-way doors**: assume each version works alone; risk is the transition. Common blocker: protocol/format changes (e.g. enabling compression; heartbeat interval 5 s -> 10 s makes old servers drop connections).
- **Two-phase deployment**: Phase 1 *Prepare*: ship readers that understand the new format while still writing the old. Phase 2 *Activate*: start writing the new. Rollback of one phase is safe, not both after Activate. Example: XML to JSON on persisted data.
- Precautions: all hosts must finish Prepare before Activate (do not accept `minimumHealthyHosts`-style partial success); verify each phase per server; bake days between phases; backfill old data before removing old reader.
- Serialization: use established formats (Protobuf, JSON, etc.), explicit independent serializer versions stored with data, preserve unknown fields on write-back, do not serialize types you do not control, emit metrics of versions read/written.
- **Upgrade-downgrade testing**: production-like multi-AZ environment, same deployment configuration and order (readers before writers on roll-forward; writers before readers on rollback), realistic traffic, sequence: deploy to half, complete, roll back.

## Variants and techniques
Canary/one-box, blue-green, feature flags, cell/AZ/Region waves, two-phase (expand/contract) changes, backfill.

## Trade-offs
Speed vs safety (small waves, long bakes slow delivery); two-phase adds releases, coordination, backfill tooling; production-like test env costs more.

## When to use it / when not to
Always for services with persisted/shared formats; skip two-phase when formats are self-describing and unknown fields are preserved.

## Appears in
None yet.

## See also
[[encoding-and-schema-evolution]], [[shuffle-sharding-and-cell-based-architecture]], [[health-checks]], [[static-stability]], [[distributed-systems-testing]]

## Interview note (senior/staff)
Say: "Deploy in waves by Region/AZ/cell with one-box first, bake time, alarm-driven automatic rollback, and treat schema/protocol changes as two-phase (readers first, then writers) so every step is reversible." Quote concrete numbers (10% one-box, 33% rolling, 1 h/12 h/2-4 h bake) and mention leader-elected or stateful systems make partial deployment harder.

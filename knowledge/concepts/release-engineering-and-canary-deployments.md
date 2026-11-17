---
title: Release engineering and canary deployments
type: concept
aliases: [canary release, progressive rollout, hermetic builds, CI/CD, rollback, config push]
sources: [https://sre.google/workbook/canarying-releases/, https://sre.google/sre-book/release-engineering/, https://sre.google/sre-book/testing-reliability/, https://sre.google/sre-book/emergency-response/, https://sre.google/sre-book/simplicity/]
---

# Release engineering and canary deployments

## Definition
The discipline of building, testing, packaging and deploying software safely and repeatably; a **canary** exposes a new version to a small slice of production traffic before wider rollout.

## Why it matters
Changes (binaries and configuration) are the most common trigger of outages. Frequent, small, well-gated releases make bugs easier to find and shorten recovery.

## How it works
- **Principles**: self-service teams, high velocity (small releases are easier to reason about), **hermetic builds** (repeatable, independent of build-machine libraries), policy enforcement (code review, access control on approvals, cherry-picks, deploys).
- **Pipeline**: build with embedded metadata, branch from mainline (fixes go to mainline first, then cherry-picked), continuous tests, unit tests re-run on the release branch, system tests on packaged artifacts, signed versioned packages labeled dev/canary/production, canary, then staged rollout, with a change report.
- **Canary**: example ramp 0.1% of traffic, 1%, 10%, 100% on successive days; probes and readiness checks can auto-pause or roll back. Most bugs scale linearly with traffic (order 1) and are caught by canaries; higher-order bugs depend on request sequences and must be caught before release.
- **Rollout strategy scales with risk**: hourly auto-deploys in dev; exponential expansion across clusters for big user-facing services; multi-day, region-by-region for sensitive infrastructure.
- **Config management**: mainline config (decoupled, may drift), bundled with binary (coupled), separate versioned config packages, or an external dynamic store (Chubby/Bigtable). All reviewed in the main repo.
- **Testing in production**: configuration tests (running vs version-controlled), stress tests to find limits, probers replaying known-good/bad requests, regression catalog, smoke tests gating deeper tests.
- **Lessons from outages**: a "low-risk" global config push skipped the canary and crash-looped the fleet (rollback ~5 min after push, some services needed up to an hour); canary regardless of perceived risk. Test rollback procedures before large experiments. Break-glass test skips must be noisy.
- **Simplicity**: small releases, no dead code or permanently-off flags (Knight Capital), minimal APIs.

## Additional detail (SRE Workbook, ch. 16 Canarying Releases)
Source: https://sre.google/workbook/canarying-releases/
- **Definition:** a partial, time-limited deployment plus an evaluation; canary = subset with the change, control = the rest; effectively an A/B test. Feature flags decouple launch from binary release.
- **Population and duration:** representative yet small; do not run overlapping canaries; duration must fit release cadence (daily releases cannot afford week-long canaries) yet include peak load, since perf bugs may appear only under heavy traffic. Pipelines: at least one full work unit, keep a unit's workers in one pool. Workbook ramp example: 1%, 10%, 50%, 100%.
- **Metrics:** a small set (about a dozen max) of user-visible signals, ideally SLIs; CPU is noisy; treat 4xx separately; use per-process not per-machine measures; metric window no longer than the canary (an hourly metric muddies a 30-min canary).
- **Evaluation:** compare canary vs control, not the aggregate: a 5% canary failing 20% of requests looks like ~1% service-wide. Also check absolute SLOs, since shared backends/caches/clients blur isolation. Before/after comparison is weak (weekday/weekend noise).
- **Cost model:** error-budget impact is proportional to exposed traffic; detection and rollback time are similar to a full rollout but harm is 5% instead of 100%. Gradual canaries: crash/failure signals first, subtler metrics later.
- **Blue/green** can serve as an A/B canary with gradual traffic shift but needs ~2x resources. Synthetic load misses state coverage and is unsafe for billing; traffic teeing is realistic but complex and can distort shared caches.
- Over-modeling leads to endless tuning; too many metrics erode operator trust. For very high targets (99.999%) canarying is the main defense since alerts are too slow ([[slo-burn-rate-alerting]]). Config pushes need the same treatment: [[configuration-management-and-safe-config-changes]].
- *Note (interview):* say "1% -> 10% -> 50% -> 100%, canary vs control on SLIs, auto-halt and rollback; blast radius = canary share".

## Variants and techniques
Canary vs blue-green vs rolling; feature flags and dark launches; push-on-green continuous delivery; automated canary analysis against SLIs.

## Trade-offs
Slower rollout lowers blast radius but lengthens time to fix; canary traffic that is too small misses rare bugs; rollbacks are not free with schema or data changes (see [[encoding-and-schema-evolution]]).

## When to use it / when not to
All services; make rollout cautiousness proportional to blast radius and error budget ([[slos-slis-and-error-budgets]]).

## Note: what a senior/staff candidate should say
Describe staged rollout by region/cell with automated health gates and one-click rollback, versioned backward-compatible schemas, config changes treated like code, and rollout halted when the error budget is burned.

## Appears in
None yet.

## See also
[[incident-management-and-postmortems]], [[distributed-systems-testing]], [[ab-testing]], [[multitenancy-and-cell-based-architecture]]

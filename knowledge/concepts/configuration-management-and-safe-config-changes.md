---
title: Configuration management and safe config changes
type: concept
aliases: [config as code, hermetic configuration, configuration design, dynamic config, feature flags config]
sources: [https://sre.google/workbook/configuration-design/, https://sre.google/workbook/configuration-specifics/]
---

# Configuration management and safe config changes

## Definition
Designing how a system is configured (what knobs exist, in what language, how validated, versioned and rolled out) so configuration stops being the main source of outages.

## Why it matters
The workbook states config changes tend to dominate outage root causes over time. Config is also toil: error-prone for those unfamiliar with the system, especially during incidents.

## How it works
**Design philosophy**
- Ideal is no config: infer from environment (thread count from cores, heap from container memory), allow override.
- Fewer knobs; ask about intent (goals), not implementation. Minimize mandatory questions, give safe defaults (e.g. dry-run by default); defaults matter because most users keep them. Offer escape hatches for experts.
- Example: a canary analysis service took about one month to cut mandatory questions and choose defaults, and was adopted with little support.

**Representation**
- Infrastructure consumes plain static data (protobuf, JSON, YAML); users write higher-level layer (DSL such as Jsonnet, Python DSL, UI) compiled to it. Do not couple user format to internal structures; keep source metadata for authorship.
- Prefer an existing DSL over home-grown or general-purpose code. Separate config from data: evaluate first, expose data for analysis, then apply side effects.
- Templates with per-instance overrides, hidden fields, required fields that error until set.

**Hermetic evaluation:** same output regardless of where/when run (no DNS, build versions, network FS dependencies). Required for reliable rollback and replay.

**When to evaluate:** check in generated output (reviewable, but large/secret/merge conflicts); at build time (Google's common choice, simple runtime, harder review); at runtime (most dynamic, bugs surface late, needs sandbox for untrusted config with resource limits).

**Validation:** schema validation (JSON Schema, protobuf), domain checks (ranges, referenced files), reject unknown fields (typos), precommit hooks, unit-tested template libraries, semantic checks (units, paths).

**Safe rollout:** version everything in VCS, single owner per snippet, log changes and resulting state, deploy gradually ([[release-engineering-and-canary-deployments]]), fast rollback, auto-halt if operator access is lost (firewall lockout; like the screen-resolution confirm prompt).

## Variants and techniques
Static vs dynamic config; build-time vs runtime evaluation; feature flags to decouple launch from deploy.

## Trade-offs
Flexibility (many knobs) vs usability and error rate; runtime evaluation vs reviewability; DSL power vs unbounded resource use (even non-Turing-complete languages can exhaust memory).

## When to use it / when not to
Always treat config as code. Avoid adding knobs without a concrete use case or pushing global changes in one step.

## Note: what a senior/staff candidate should say
"Config changes are code changes: reviewed, validated against a schema, versioned, hermetic, rolled out progressively with automatic rollback." When designing a service, say which settings are dynamic (flags, limits) and that a kill switch exists.

## Appears in
None yet.

## See also
[[release-engineering-and-canary-deployments]], [[incident-management-and-postmortems]], [[slos-slis-and-error-budgets]]

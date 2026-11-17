---
title: Health checks (liveness, local, dependency, anomaly detection)
type: concept
aliases: [health check, liveness probe, fail open, zombie servers, black hole]
sources: [https://aws.amazon.com/builders-library/implementing-health-checks/]
---

# Health checks

## Definition
Mechanisms that detect unhealthy servers so traffic stops flowing to them, designed so a false positive does not take down the whole fleet.

## Why it matters
Failing servers rarely fail cleanly. Under least-requests balancing a broken server that errors fast becomes a **black hole** attracting more traffic (a catalog server with a full disk returning empty answers quickly caused a site-wide outage). One bad server in 10 means <=90% availability. Tension: thorough checks catch single-server faults, but correlated false positives cause full outages.

## How it works
Four layers:
1. **Liveness** (TCP accepts, HTTP 200): platform-provided.
2. **Local** health (disk writable, critical/support processes alive, proxy-to-app path): not shared with peers, so safe to act on fast.
3. **Dependency** checks (credentials, config, peer reachability, deadlocks/leaks): can catch local issues but turn soft dependencies into hard ones and give correlated false positives.
4. **Anomaly detection**: compare peers' error rate/latency; catches clock skew, stale code, wrong status codes, suspiciously fast errors. Needs homogeneous fleet doing similar work; external instrumentation.

Reacting safely:
- **Fail open**: if all servers look unhealthy, route to all (NLB, ALB, Route 53); beware partial dependency failures causing flapping below the threshold.
- **No circuit breaker on self**: LBs and queue pollers use liveness and local checks only; dependency checks and anomaly detection run in external monitoring with thresholds, rate limits and human escalation (stateful stores follow this).
- **Prioritize health checks under load**: more worker threads than proxy max connections; connection limits; always admit health checks; background thread updating an `isHealthy` flag (monitor that thread).
- **Limit scope of impact**: per-API isolation (data plane keeps running if control plane dependency fails); cache fallback for reads.
- Real patterns: deployments that report success without testing health (alarms + AZ-phased rollout); queue workers with full disks keep pulling messages (visibility timeout redelivery, error alarms); full disks blinding monitoring (external pings, Lambda every minute with DynamoDB state to cap marked-unhealthy); **zombie servers** returning with old software (health response carries version; central agent blocks outdated).

## Variants and techniques
Shallow vs deep checks, external observers, version reporting, fail-open LBs.

## Trade-offs
Depth vs correlated failure risk; fast local removal vs centralized slow decisions.

## When to use it / when not to
Always; keep fast automated removal to definitively local faults and gate dependency-driven actions.

## Appears in
None yet.

## See also
[[load-balancer]], [[service-discovery]], [[static-stability]], [[safe-deployments-and-rollbacks]], [[cascading-failures]]

## Interview note (senior/staff)
Say: "LB checks are shallow/local; deep dependency checks would make a dependency outage fleet-wide, so I use fail-open and centralized, rate-limited remediation, plus anomaly detection to catch fast-failing black holes." Mention reserving capacity so health checks answer under overload.

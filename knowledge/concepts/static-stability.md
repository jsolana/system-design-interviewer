---
title: Static stability (control plane vs data plane, AZ overprovisioning)
type: concept
aliases: [statically stable, control plane vs data plane, AZ failure tolerance]
sources: [https://aws.amazon.com/builders-library/static-stability-using-availability-zones/]
---

# Static stability

## Definition
A system is statically stable if it keeps operating when a dependency is impaired, without needing to take any new action or receive new changes. Capacity and state needed for failover are **provisioned in advance**, not created reactively during the failure.

## Why it matters
Reactive recovery (launch instances in healthy AZs after one fails) depends on control planes and APIs that are the most likely to be degraded during an event.

## How it works
- **Control plane vs data plane**: control plane = create/modify/propagate resources (many moving parts, more likely to fail); data plane = day-to-day work (packet routing, volume I/O; higher volume, often matters more). Scale and secure them separately; keep recovery paths off the control plane. Running EC2 instances keep routes and security rules when the control plane is impaired.
- **Active-active (stateless)**: Auto Scaling group across 3+ AZs, overprovisioned. With 3 AZs add 50% capacity so each AZ runs at ~66% of its load-tested level; a lost AZ is absorbed by health checks plus load balancer shifting, no action needed. Same for queue consumers.
- **Active-standby (stateful)**: primary plus warm standby in another AZ (RDS); failover repoints DNS; clusters elect a leader from existing standbys rather than launch new nodes.
- **Zonal design**: deploy AZ by AZ (a zonal calendar), keep traffic within its AZ (zonal NAT gateway per AZ), replicate hard state across AZs only for DR (backups to S3, cross-AZ replicas).
- **Dependency arithmetic**: with 3 AZs and one impaired, N regional hops each have 2/3 chance of avoiding it -> (2/3)^N; N zonal-to-zonal hops stay at 2/3. Gray failures pass health checks, so this matters.

## Variants and techniques
Regional-calls-regional (simple, default for most services) vs zonal-to-zonal (for foundational data-plane components; also cuts cross-AZ cost).

## Trade-offs
Overprovisioning cost (50% extra with 3 AZs); more operational complexity for zonal stacks (per-AZ gateways, route tables).

## When to use it / when not to
Use for foundational and critical data-plane components. For ordinary services regional-calls-regional with overprovisioning is enough.

## Appears in
None yet.

## See also
[[multi-data-center]], [[shuffle-sharding-and-cell-based-architecture]], [[constant-work-pattern]], [[health-checks]], [[safe-deployments-and-rollbacks]]

## Interview note (senior/staff)
Say "the recovery path must not depend on the control plane: pre-provision N+1 AZ capacity (e.g. 50% headroom for 3 AZs), fail over via health checks and DNS/LB, not autoscaling." Quote the (2/3)^N argument when discussing cross-AZ call chains and mention keeping traffic zone-local. Note that AZ-level capacity planning interacts with load shedding (it can mask real headroom).

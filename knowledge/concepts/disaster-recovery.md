---
title: Disaster recovery
type: concept
aliases: [DR, DiRT, failover drills, recovery testing, RTO RPO]
sources: [https://sre.google/sre-book/data-integrity/, https://sre.google/sre-book/being-on-call/, https://sre.google/sre-book/emergency-response/, https://sre.google/sre-book/managing-critical-state/, https://sre.google/sre-book/addressing-cascading-failures/]
---

# Disaster recovery

Note: the SRE book has no dedicated DR chapter; this file collects its recovery-related guidance. Terms RPO/RTO are standard practice, not used verbatim in the source.

## Definition
Preparing for, and rehearsing recovery from, loss of a component, datacenter, dataset or the tools used to respond.

## Why it matters
Recovery paths that are never exercised fail when needed ("hope is not a strategy"). In the emergency-response cases, an untested rollback prevented undoing a test within minutes, and slow recovery after a mass wipe lasted days to months.

## How it works
- **Data**: tiered backups and restore tests ([[data-integrity-and-backups]]); the 2011 Gmail restore worked because it was rehearsed with a central plan.
- **Capacity**: N+2 across failure domains so a datacenter loss plus maintenance is survivable ([[capacity-planning]]); failover must not overload survivors ([[cascading-failures]]).
- **Consensus groups**: 5 replicas tolerate 2 failures (3 tolerate 1); place replicas across failure domains balancing latency; a 6th replica does not improve fault tolerance over 5.
- **Drills**: Wheel of Misfortune (simulated incidents), annual DiRT-style disaster recovery testing, rollback testing before large experiments, regular on-call exposure.
- **Tooling for degraded situations**: out-of-band communication and CLI tools that work when the primary stack is down; slow-start and gradual ramp-up when bringing traffic back so caches warm.
- **Failover speed budgets**: distributed cron needed failover under one minute for 5-minute jobs ([[distributed-periodic-scheduling]]).

## Variants and techniques
Active-passive vs active-active ([[multi-data-center]]), pilot light and cold standby (Note: standard industry terms, not in source), regional evacuation by traffic drain.

## Trade-offs
Faster recovery costs standby capacity and drill effort; active-active improves RTO but complicates consistency ([[conflict-resolution]]).

## When to use it / when not to
Match the investment to the SLO; mission-critical data and control planes always need tested restores.

## Note: what a senior/staff candidate should say
Give recovery time and data-loss targets per tier, the failure domain you survive (host, AZ, region), how often you actually test failover and restore, and what the plan is when the control plane itself is down.

## Appears in
[[distributed-message-queue]]

## See also
[[data-integrity-and-backups]], [[multi-data-center]], [[incident-management-and-postmortems]], [[consensus]]

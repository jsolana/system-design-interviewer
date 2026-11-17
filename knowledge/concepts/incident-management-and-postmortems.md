---
title: Incident management and postmortems
type: concept
aliases: [incident command, blameless postmortem, emergency response, troubleshooting, on-call response]
sources: [https://danluu.com/postmortem-lessons/, https://danluu.com/cache-incidents/, https://sre.google/workbook/incident-response/, https://sre.google/workbook/postmortem-culture/, https://sre.google/sre-book/managing-incidents/, https://sre.google/sre-book/postmortem-culture/, https://sre.google/sre-book/effective-troubleshooting/, https://sre.google/sre-book/emergency-response/, https://sre.google/sre-book/tracking-outages/]
---

# Incident management and postmortems

## Definition
A structured process to detect, mitigate and learn from production incidents: defined roles during the incident, systematic troubleshooting, and a blameless written postmortem afterward.

## Why it matters
Mean time to recovery is driven as much by coordination and mitigation discipline as by engineering skill; learning from failures prevents recurrence.

## How it works
- **Roles** (can be delegated recursively): Incident Commander (holds the big picture, delegates), Ops lead (only group that changes the system), Communications (updates stakeholders), Planning (bugs, handoffs, tracking divergence from normal).
- **Declare early** if a second team is needed, customers see the outage, or it is unsolved after ~1 hour of focused work. Keep a live shared incident document; explicit handoff at shift change.
- **Priorities**: stop the bleeding, restore service, preserve evidence. Mitigate first (drain traffic, roll back, shed load, disable a subsystem); root-causing comes later.
- **Troubleshooting** (hypothetico-deductive): triage, examine (metrics, logs, traces), diagnose (check recent changes first; bisect the system), test and treat with reversible, documented changes. Pitfalls: irrelevant symptoms, improbable causes ("horses not zebras"), spurious correlations (common causes such as a power outage).
- **Postmortem triggers**: user-visible impact above a threshold, any data loss, on-call intervention (rollback, rerouting), long resolution time, monitoring failure (found manually).
- **Blameless**: focus on contributing causes and fixing systems, not people. Contents: impact, timeline, root causes, prioritized action items with owners. Review by senior engineers, publish widely, track follow-ups; an unreviewed postmortem might as well not exist.
- **Outage tracking**: aggregate incidents and annotate them to find recurring causes.
- **Emergency case lessons**: automation without sanity checks (empty response treated as "all machines") wiped machines worldwide; recovery took ~3 h for first reinstall, days for most capacity, 1-2 months for stragglers. Out-of-band communication and tested CLI tools matter when the usual tools are down. Practice via Wheel of Misfortune and DiRT-style drills.

## Additional detail (SRE Workbook, ch. 9-10)
Sources: https://sre.google/workbook/incident-response/, https://sre.google/workbook/postmortem-culture/
- **Roles:** IC (holds any undelegated role), Ops lead, Comms lead (may fold into IC for small incidents). Long incidents rotate IC and on-call (PagerDuty: every 4 h). Keep decisions on the call, details in chat; shared doc of theories and eliminated causes with 3+ responders.
- **Declare early and often** with written criteria. Case lessons: an undeclared Google Home issue recurred three times because mitigations hid the unknown root cause and the rollout continued; a GKE incident ran ~2 h without structure and lacked a generic rollback; well-run cases (Belgium power outage, PagerDuty NTP) escalated methodically, validated recovery, and assigned the postmortem before closing.
- **Order:** assess impact, mitigate (rollback, drain, reroute; build these tools beforehand), root-cause, fix, postmortem.
- **Drills:** Wheel of Misfortune, DiRT, weekly failure-injection days, treating minor problems as major for practice.
- **Postmortem content:** metadata, executive summary, quantified impact, root causes and trigger, timeline, lessons (went well/poorly/luck), action items typed as prevent, mitigate, detect, repair, investigate with owner, priority and tracking bug. Rule: a user-affecting outage should produce at least one P0/P1 item; avoid vague verbs; prefer changing automation over changing people. Publish fast (good example ~4 days vs 4 months).
- **Culture levers:** reward closing action items, share widely, monthly process review, FixIt weeks twice a year; warning signs: avoidance, no time to write, repeat incidents.

## Additional detail (Dan Luu, reading postmortems)
Source: https://danluu.com/postmortem-lessons/ and https://danluu.com/cache-incidents/.
- Yuan et al. (48 critical failures in 5 distributed systems): ~92% from incorrectly handled errors (25% ignored, 8% wrong exception caught, 2% TODOs; 23% detectable by statement coverage/review); 98% reproduced on 3 nodes, 26% non-deterministic.
- Configuration: ~50% of the global-outage postmortems found by search were config changes (unrepresentative sample); Gray 1985: 42% of failures from operators/config/maintenance; config often pushed to all machines at once while code is staged.
- Hardware: DRAM error rates >10x advertised; Ethernet checksums can pass malformed packets; backup generators failing under load despite failover tests. Automation usually beats extra manual checks. Missing monitoring/escalation is a frequent contributing factor.
- Twitter cache incidents 2011-2022 (6 SEV-0, 6 SEV-1): mostly runaway feedback loops (latency, retries, GC, connection growth), aggressive client retries without backpressure, host/kernel settings (IRQ affinity), config errors (2016: adding 115 nodes at once dropped hit rate 99.8% to 84% and overloaded the DB; connection failures ~160k connections per host), hot keys missed, unrealistic load tests. Lessons: test failure modes, clients compute retry policies, apply backpressure early, spread hosts across rack failure domains, alert on success not process start.

## Variants and techniques
Severity levels, runbooks/playbooks, game days and chaos testing, five-whys.

## Trade-offs
Early declaration costs some process overhead but prevents chaos; blameless culture needs leadership buy-in; too many postmortems become toil.

## When to use it / when not to
Any production service with an SLO; scale the ceremony to the severity.

## Note: what a senior/staff candidate should say
Cover detection (alerts), mitigation levers designed in (kill switches, traffic drains, rollbacks), roles, and how postmortem actions feed back into the design and error budget.

## Appears in
None yet.

## See also
[[alerting-strategy]], [[observability-and-monitoring]], [[release-engineering-and-canary-deployments]], [[on-call-and-toil]], [[disaster-recovery]]

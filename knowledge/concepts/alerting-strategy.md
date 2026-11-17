---
title: Alerting strategy
type: concept
aliases: [paging, alert fatigue, ratio alerts, on-call alerting]
sources: [https://sre.google/workbook/alerting-on-slos/, https://sre.google/sre-book/monitoring-distributed-systems/, https://sre.google/sre-book/practical-alerting/, https://sre.google/sre-book/being-on-call/]
---

# Alerting strategy

## Definition
Deciding what conditions notify a human, how urgently, and how alerts are routed, grouped and suppressed.

## Why it matters
Too many pages cause alert fatigue, hide real incidents and burn out on-call engineers; too few miss user-visible outages.

## How it works
- A page must be **urgent, actionable, novel and need human judgment**. A robotic response means automate it or delete the alert.
- Page on **symptoms** that threaten the SLO; send causes to dashboards. Alert on a cause only when it is definite and imminent (disk about to fill).
- Prefer **ratio alerts**: errors / total requests over a window (example: non-200 ratio above 1% and more than 1 error/s). Use a window long enough to tolerate a failed collection (10 min) and a pending period (at least two evaluation cycles, e.g. 2 min) to prevent flapping.
- An alerting manager does routing, **deduplication, grouping and inhibition** (suppress downstream alerts when an upstream one fires). Aim for about one alert per incident.
- Email alerts are low value; use dashboards for sub-critical issues.
- Response targets: ~5 minutes for user-facing time-critical services, ~30 minutes for less sensitive ones.
- **Load targets**: fewer than 2 pages per 12-hour shift (an incident costs ~6 hours of work including follow-up) and fewer than 5 tickets per day; median pages per day should be zero.
- Case studies: Bigtable temporarily relaxed its SLO target and silenced email alerts to escape over-alerting and fix root causes; Gmail's frequent rote-response pages signaled automation debt.

## Variants and techniques
Threshold alerts, ratio alerts, multi-window SLO burn-rate alerts (details, formulas and recommended windows in [[slo-burn-rate-alerting]], from the SRE Workbook https://sre.google/workbook/alerting-on-slos/; judge alerts by precision, recall, detection time and reset time), blackbox probe alerts, tiered paging vs ticketing.

## Trade-offs
Sensitivity vs precision; fast detection vs flapping; paging on symptoms gives less diagnostic context.

## When to use it / when not to
Page only when waiting would hurt users or the error budget. Everything else is a ticket or dashboard.

## Note: what a senior/staff candidate should say
"I would page on SLO-impacting symptoms such as error ratio and latency percentiles, group alerts per incident, and keep cause metrics on dashboards." Mention on-call sustainability as a design input.

## Appears in
[[metrics-monitoring]]

## See also
[[observability-and-monitoring]], [[slos-slis-and-error-budgets]], [[incident-management-and-postmortems]], [[on-call-and-toil]]

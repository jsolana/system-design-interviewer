---
title: SLO burn-rate alerting (multiwindow, multi-burn-rate)
type: concept
aliases: [burn rate alerts, multiwindow alerts, multi-burn-rate alerting, error budget alerting]
sources: [https://sre.google/workbook/alerting-on-slos/, https://sre.google/workbook/implementing-slos/]
---

# SLO burn-rate alerting (multiwindow, multi-burn-rate)

## Definition
Alert on how fast the service is consuming its error budget ([[slos-slis-and-error-budgets]]) rather than on raw error thresholds. **Burn rate** = observed error ratio / allowed error ratio (1 - SLO). Burn rate 1 means the budget lasts exactly the whole SLO window; burn rate N exhausts it in window/N.

## Why it matters
A fixed threshold either pages for trivial blips (low precision) or misses slow leaks (low recall). Burn rate ties every page to "how much budget is at stake", so urgency scales with severity and alerts match the SLO.

## How it works
Four properties to judge an alert: **precision** (alerts that matter), **recall** (significant events caught), **detection time**, **reset time** (how long it keeps firing after recovery).

Key formulas (period P, e.g. 30 d = 720 h):
- Budget consumed when alert fires = burn_rate x alert_window / P.
- Burn rate for "X% of budget in window W" = X x P / W (5% in 1 h of 720 h = 36).
- Time to exhaustion = P / burn_rate.

For a 99.9% SLO: burn 1 = 0.1% errors = 30 days; burn 2 = 15 days; burn 10 = 1% errors = 3 days; burn 1000 = 100% errors = 43 min.

**Recommended config (99.9% SLO, 30 d):**

| Severity | Long window | Short window | Burn rate | Budget consumed |
|---|---|---|---|---|
| Page | 1 h | 5 min | 14.4 | 2% |
| Page | 6 h | 30 min | 6 | 5% |
| Ticket | 3 d | 6 h | 1 | 10% |

Fire when BOTH windows of a row exceed the burn-rate threshold (the workbook also shows a 24 h/2 h pair at burn 3 for tickets). Short window is about 1/12 of the long one, so the alert resets about 5 min after errors stop and avoids firing on already-resolved incidents.

## Variants and techniques (the six approaches, progression)
1. Error rate >= SLO threshold over a short window: fast detection, terrible precision (up to ~144 alerts/day could still meet the SLO).
2. Longer window: better precision, but ~36 h reset time and costly queries.
3. `for:` duration clause: poor recall, a 100% outage waits as long as a 0.2% one, and spiky failures reset the timer. Not recommended.
4. Single burn rate (1 h window, threshold 36): good precision and cheap, but low recall: a 35x burn never fires yet empties the 30-day budget in about 20.5 h; reset time still ~58 min.
5. Multiple burn rates: page vs ticket by urgency; needs suppression to avoid several notifications per incident.
6. Multiwindow multi-burn-rate: best precision, recall and reset time; most parameters to maintain. Recommended.

**Low-traffic services:** with ~10 req/h one failure is a 10% hourly error rate. Options: synthetic traffic (limited coverage, can mask real errors), group services sharing a failure domain into one SLO, client retries with backoff and jitter or fallbacks, a looser SLO (99.9 -> 99%) as a product decision, longer alert windows.

**Extreme targets:** at 99.999% a full outage burns the monthly budget in ~26 s, faster than detection, so prevention (canarying, see [[release-engineering-and-canary-deployments]]) matters more than alerts. At 90%, a 1 h total outage uses only ~1.4% so a 2%-page rule can never fire; tune windows.

**At scale:** use one parameter set for all services; bucket request classes (e.g. CRITICAL 99.99%, HIGH_FAST 99.9% with 100 ms/200 ms, HIGH_SLOW 99.9% with 1 s/5 s, LOW 99%, NO_SLO) instead of per-service tuning.

## Trade-offs
- More windows = better coverage but more parameters and alert-suppression logic.
- Long windows cost more to query (needs months of retention, see [[observability-and-monitoring]]).
- Alerts on SLO symptoms say "users hurt" but not why; keep cause dashboards.

## When to use it / when not to
Use for any service with a request-based SLO and meaningful traffic. For tiny traffic or ultra-high nines, rely on synthetic probes and prevention.

## Note: what a senior/staff candidate should say
"I page on budget burn: 14.4x over 1 h confirmed by 5 min (2% of a 30-day budget), 6x over 6 h (5%), and ticket at 1x over 3 days. Two windows give fast detection and quick reset." Mention precision/recall/detection/reset trade-offs and that single-threshold alerts are noisy.

## Appears in
[[metrics-monitoring]]

## See also
[[alerting-strategy]], [[slos-slis-and-error-budgets]], [[observability-and-monitoring]], [[incident-management-and-postmortems]]

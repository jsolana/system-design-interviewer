---
title: Load shedding and overload handling
type: concept
aliases: [load shedding, admission control, goodput, brownout, overload protection]
sources: [https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/, https://sre.google/sre-book/handling-overload/, https://sre.google/sre-book/addressing-cascading-failures/]
---

# Load shedding and overload handling

## Definition
When nearing overload, reject excess requests early and cheaply so the requests that are accepted finish within the client timeout (keeping **goodput** high), instead of making every request slow.

## Why it matters
Latency rises with load (contention, context switching, GC; Universal Scalability Law). Timeouts convert latency into availability loss (if median latency equals the client timeout ~50% fail). Timed-out work is wasted, retries multiply offered load, deep call graphs amplify it exponentially, and overload becomes a stable state (see [[overload-and-metastable-failures]]). Throughput = all requests sent; goodput = requests handled successfully within useful latency.

## How it works
- **Test past the breaking point**; ideal goodput plateaus near full utilization as throughput keeps rising; availability falling to zero signals insufficient shedding. Test with autoscaling and fixed fleets, chaos tools, removed servers; measure client-perceived availability. Test overload before adding mechanisms.
- **Cheap rejection**: make drops cheaper than processing (watch accidental log statements). If fast fail attracts traffic under least-outstanding-requests balancing, slow errors to match success latency.
- **Visibility**: false-positive rejection target is zero; log client/operation of rejections, alarm on volume; keep fast-failed requests out of latency metrics.
- **Prioritization**: load balancer pings first (else fleet shrinks), humans over crawlers, in-quota over burst. Shape traffic at the entry service.
- **Watch the clock**: skip work for timed-out requests; clients send deadline hints; propagate remaining time (durations avoid clock sync but need monotonic timers); enforce deadline after dequeue; prefer server-side per-request TTL over fancy latency estimators.
- **Finish what you started**: bounded work per request (pagination); prioritize `end()` over `start()`, later pages over first pages.
- **Hidden queues** (executors, socket buffers): measure wait time, bound size and age, LIFO where possible; prefer spillover/fast-fail to load balancer surge queues (Classic LB surge queue vs ALB rejection).
- **Layers**: server-local logic; max connections set high on LB/proxy (below server threads/file descriptors so health checks pass); iptables connection caps as emergency (keep runbook); API Gateway rate limits; WAF. Trade-off: earliest rejection is cheapest but least observable.
- **Interactions**: shedding can mask real capacity (headroom for AZ loss) and block CPU-based autoscaling if thresholds overlap; may shed off-peak non-critical traffic to avoid full AZ redundancy cost, with business buy-in.
- Serverless/isolated units (Lambda one request per environment, DynamoDB adaptive capacity) give predictable goodput by design.

## Variants and techniques
Per-tenant quotas and 429 ([[multi-tenancy-and-fairness]]), backpressure to producers ([[queue-backlog-management]]), deadline propagation ([[retries-timeouts-and-backoff]]).

## Trade-offs
Shedding costs something; beyond a point Amdahl's law wins. Rejections lower availability if false positives. Reduces tuning of magic numbers (thread pool, max connections) when platform isolation is used.

## When to use it / when not to
Any service with bursty or retry-amplified load. Not a substitute for capacity planning or per-tenant limits when one tenant causes the spike.

## Additional detail (Google SRE Book, ch. 21-22)
- **Per-customer quotas** negotiated per client and deliberately oversubscribed (10,000 CPUs: Gmail 4,000, Calendar 4,000, Android 3,000, others 500 CPU-s/s = 13,500 total); aggregated in real time and pushed to tasks.
- **Signals**: CPU used / CPU reserved (memory folded in) and smoothed executor load average (active threads); QPS is a poor capacity metric as per-query cost drifts.
- **Criticality**: CRITICAL_PLUS, CRITICAL (default prod), SHEDDABLE_PLUS (default batch), SHEDDABLE; propagated downstream, lower classes shed first at lower utilization thresholds. Four levels judged enough; more is costlier to operate.
- **Client-side adaptive throttling**: each client tracks requests and accepts over the last 2 minutes and rejects locally with rising probability once requests >= K x accepts (K = 2 default; K = 1.1 means ~1 rejection per 10 accepted). Lower K = more aggressive; poor for sporadic clients with stale views.
- **Targets**: a task should stay healthy at roughly 2x-10x provisioned capacity; keep queues at ~50% of thread pool or less; use LIFO/CoDel; return HTTP 503 above an in-flight limit.
- **Connection load**: connection upkeep and health checks can cost more than serving; use subsetting (20-100 backends), cheaper health checks, batch proxies as a fuse; backends in lame-duck state drain in 10-150 s ([[load-balancer]]).
- Related: [[cascading-failures]], [[graceful-degradation]].

## Appears in
[[distributed-rate-limiter]]

## See also
[[rate-limiting]], [[health-checks]], [[constant-work-pattern]], [[static-stability]], [[message-queues]]

## Interview note (senior/staff)
Say: "Under overload I protect goodput: reject early and cheaply (503/429), drop requests whose deadline has passed, prioritize health checks and in-flight work, bound every queue, and load test beyond the break point measuring client-side availability." Mention that shedding can hide capacity problems and interferes with autoscaling.

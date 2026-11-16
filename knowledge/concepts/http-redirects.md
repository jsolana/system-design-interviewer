---
title: HTTP redirects (301 vs 302)
type: concept
aliases: [301 vs 302, redirects]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly, https://www.hellointerview.com/learn/system-design/problem-breakdowns/ad-click-aggregator, System Design Interview Vol.1 (Alex Xu), ch. 8]
---

# HTTP redirects (301 vs 302)

## Definition
Status codes that tell the browser to go to another URL.

## Why it matters
Determines whether requests keep reaching your server.

## How it works
- **301** (permanent): cacheable by the browser; subsequent visits skip the server.
- **302** (temporary): not cached; every visit reaches the server.
- **410 Gone** for expired links.

## Variants and techniques
A URL shortener uses 302 so it can apply expiration, change destinations and record clicks.

## Trade-offs
302: control and tracking, more load. 301: less load, loss of control.

## When to use it / when not to
301 only if the mapping is immutable and no tracking is needed.

## Additional detail
- [[ad-click-aggregator]]: client-side redirect (can be skipped) vs server-side 302 that records the click and guarantees tracking, at the cost of latency.

## Additional detail (Xu Vol. 1, ch. 8)
301: the browser caches and subsequent requests do not reach the shortener (reduces load); 302: every request goes through the service (better for click and referrer analytics).

## Appears in
[[ad-click-aggregator]], [[url-shortener]]

## See also
[[caching]], [[cdn-edge-computing]]

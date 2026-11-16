---
title: CDN and edge computing
type: concept
aliases: [CDN, edge functions]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly, https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster, https://www.hellointerview.com/learn/system-design/problem-breakdowns/dropbox, https://www.hellointerview.com/learn/system-design/problem-breakdowns/youtube, https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-live-comments, https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-post-search, System Design Interview Vol.1 (Alex Xu), ch. 1, System Design Interview Vol.1 (Alex Xu), ch. 14]
---

# CDN and edge computing

## Definition
A network of global Points of Presence (PoPs) that serve content and, with edge functions, run logic close to the user.

## Why it matters
Reduces latency and offloads the origin.

## How it works
- Serve the short domain via the CDN and run the redirect at the edge (Cloudflare Workers, Lambda@Edge): popular codes never reach the origin.
- Cache non-personalized search responses that are identical per query in the CDN.

## Variants and techniques
Edge caching vs edge compute.

## Trade-offs
Invalidation across nodes, cost at high traffic, execution limits, harder debugging and monitoring.

## When to use it / when not to
When global latency matters and the cost is acceptable; not for personalized content.

## Additional detail
- [[dropbox]]: downloads with short-lived CDN signed URLs (CloudFront).
- [[youtube]]: segments and manifests cached at the edge.
- [[fb-live-comments]]: mega-streams served by the CDN with per-second snapshots.
- [[fb-post-search]]: search results with Cache-Control at the CDN.

## Additional detail (Xu Vol. 1, ch. 1)
CDN flow: the user requests a URL on the CDN domain; if it is not cached, the CDN requests it from the origin (web server or S3), which responds with a TTL; the CDN caches it until it expires and serves subsequent users.
- Considerations: **cost** (charged per transfer; remove rarely used content from the CDN); appropriate **expiration**; **fallback** to the origin if the CDN fails; **invalidation** via the provider's API or **object versioning** (`image.png?v=2`).
- Only static content is covered (JS, CSS, images, video); caching of dynamic content is outside the book's scope.

## Additional detail (Xu Vol. 1, ch. 14)
Cost: 5M DAU x 5 videos x 0.3 GB x $0.02/GB = $150,000/day. Reduction: serve only popular videos from the CDN (long-tail distribution), encode rarely watched content on demand, do not replicate per region what is only popular in one, and use a custom CDN with ISPs (Netflix). Upload centers via a CDN close to the user. See [[youtube]].

## Appears in
[[dropbox]], [[fb-live-comments]], [[fb-news-feed]], [[fb-post-search]], [[google-maps]], [[google-news]], [[instagram]], [[stock-exchange]], [[typeahead]], [[url-shortener]], [[youtube]]

## See also
[[caching]], [[http-redirects]]

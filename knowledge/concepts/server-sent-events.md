---
title: Server-Sent Events (SSE)
type: concept
aliases: [SSE]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster]
---

# Server-Sent Events (SSE)

## Definition
Unidirectional HTTP channel server -> client for pushing updates.

## Why it matters
Simpler than WebSockets when only the server sends (seat changes, queue position).

## How it works
Persistent connection; the server emits events (seat map, position and wait time).

## Variants and techniques
WebSocket as a bidirectional alternative.

## Trade-offs
Insufficient on its own in extreme events where seats disappear instantly: there [[virtual-waiting-queue]] is added.

## When to use it / when not to
Unidirectional push updates; not if the client needs to send a lot to the server.

## Additional detail (FB Live Comments)
- Chosen over [[websockets]] when the ratio is almost read-only; writes go through normal POSTs.
- Automatic reconnection with the `Last-Event-ID` header (ID = comment id) to replay what was missed; complementary catch-up via HTTP `since`.
- Challenges: proxies/LBs that buffer, browser limit on SSE connections per domain, monitoring of long-lived connections. ~100k connections per server as a usual capacity.

## Appears in
[[chatgpt]], [[dropbox]], [[fb-live-comments]], [[flash-sale]], [[google-maps]], [[online-auction]], [[robinhood]], [[ticketmaster]], [[uber]]

## See also
[[virtual-waiting-queue]]

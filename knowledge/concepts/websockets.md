---
title: WebSockets
type: concept
aliases: [conexiones bidireccionales, heartbeat]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/whatsapp, System Design Interview Vol.1 (Alex Xu), ch. 12]
---

# WebSockets

## Definition
A persistent bidirectional client-server connection (over TLS) for real-time push.

## Why it matters
Enables low-latency message delivery without polling. Unidirectional alternative: [[server-sent-events]].

## How it works
- The server keeps a userId -> socket map; with many servers, "host confusion" must be resolved ([[consistent-hashing]] or [[pub-sub]]).
- Failure detection: do not rely on TCP keepalive (minutes); ACK timeouts with retry (500-2000 ms) or application **heartbeats** (ping 10-30 s, pong < 5 s -> detection ≈ 15 s).
- The client ACK confirms receipt; reconnection -> sync from Inbox.
- One server can hold 1-2M connections (WhatsApp reference).

## Variants and techniques
Periodic polling and sequence numbers as a backstop; WebSockets versus 5 s polling (ruled out in the leaderboard as overkill).

## Trade-offs
Server-side state, heartbeat cost (20M pings/s at 200M users), mass reconnections.

## When to use it / when not to
Chat, collaboration, games; not if polling or unidirectional push is enough.

## Additional detail (Xu Vol. 1, ch. 12)
Connection initiated by the client, bidirectional and persistent; it starts as HTTP and is "upgraded" with a handshake. It usually passes through firewalls because it uses ports 80/443. Used for both sender and receiver (simplifies the design); the remaining features (login, profile) can stay on HTTP. Efficient connection management on the server is critical; the client assigned by [[service-discovery]] stays on its chat server for as long as it lives. Estimate: 1M connections x ~10 KB ≈ 10 GB. See [[whatsapp]].

## Appears in
[[distributed-email-service]], [[dropbox]], [[fb-live-comments]], [[google-docs]], [[google-maps]], [[nearby-friends]], [[online-chess]], [[whatsapp]]

## See also
[[long-polling]] (comparison of polling vs long-polling vs WebSockets vs SSE), [[server-sent-events]], [[pub-sub]]

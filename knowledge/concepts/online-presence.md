---
title: Online presence
type: concept
aliases: [presence indicator, online status, heartbeat, last seen]
sources: [System Design Interview (Alex Xu), Vol. 1, ch. 12 (pp. 194-197)]
---

# Online presence

## Definition
A mechanism that determines and communicates whether a user is online (green dot) using presence servers connected via WebSocket.

## Why it matters
An essential feature in chat apps; a naive design causes indicator flickering and a high fanout cost.

## How it works
- **Login**: after the WebSocket is established, online status and `last_active_at` are stored in the key-value store.
- **Logout**: the status changes to offline in the KV store.
- **Disconnection**: marking offline on every drop would be wrong (tunnels, unstable networks); a **heartbeat** is used: the client sends an event every 5 s to the presence server; if none arrives within x seconds (e.g. 30 s) the user goes offline.
- **Status fanout**: [[pub-sub]] model with one channel per pair of friends (A-B, A-C, A-D); when A's status changes it is published to their channels and subscribed friends receive the event over WebSocket.

## Variants and techniques
For large groups (e.g. 100,000 members = 100,000 events per change) the status is queried only when entering the group or when manually refreshing the list.

## Trade-offs
Heartbeat: tolerance of brief disconnections at the cost of a small delay in reflecting the drop. The per-pair channel only scales for small groups (WeChat limits to 500).

## When to use it / when not to
Small groups/contacts: push per channel. Large groups: on-demand pull.

## Appears in
[[whatsapp]]

## See also
[[websockets]], [[pub-sub]], [[gossip-protocol]]

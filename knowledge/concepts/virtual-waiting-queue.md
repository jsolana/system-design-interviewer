---
title: Virtual waiting queue
type: concept
aliases: [virtual waiting room, admission control]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster]
---

# Virtual waiting queue

## Definition
A front queue that limits how many users reach the critical part (seat map/booking) during spikes.

## Why it matters
Protects the system and improves UX in massive sales (10M users, one event).

## How it works
- Queue in a Redis sorted set ordered by timestamp.
- Persistent connection ([[server-sent-events]] or WebSocket) with position and estimated time.
- Batched admission (by time or tickets sold); set `admitted:{eventId}` with TTL; the Booking Service rejects non-admitted users.

## Variants and techniques
Batches by time vs by sales.

## Trade-offs
Long or imprecise waits frustrate users; real-time feedback mitigates this. Sometimes it is a product decision.

## When to use it / when not to
Extreme spikes over scarce resources; unnecessary with moderate load.

## Appears in
[[flash-sale]], [[ticketmaster]]

## See also
[[server-sent-events]], [[distributed-lock]]

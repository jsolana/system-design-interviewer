---
title: Pub/Sub
type: concept
aliases: [publish-subscribe, redis pub/sub]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF) ch. 2 pp. 35-58, https://www.hellointerview.com/learn/system-design/problem-breakdowns/whatsapp, System Design Interview Vol.1 (Alex Xu), ch. 12]
---

# Pub/Sub

## Definition
Messaging where publishers send to channels/topics and subscribers receive in real time.

## Why it matters
Solves routing between servers with persistent connections without each one needing to know the others.

## How it works
- Each Chat Server subscribes to a channel per connected user and publishes to the recipient's channel.
- Redis Pub/Sub: at-most-once delivery; durability comes from writing to Inbox/Message first.
- Redis shard by userId.

## Variants and techniques
Channel per user (optimal for 1:1) vs per chat (large groups); adaptive with a threshold (~25 users) and double publishing during the transition. Kafka with a topic per user does not scale (~50 KB/topic).

## Trade-offs
+ a few ms of latency, connections from each server to each shard; lost messages -> polling/sequence numbers/heartbeats.

## When to use it / when not to
Real-time fan-out with durability solved separately.

## Additional detail (Xu Vol. 1, ch. 12)
Presence: one channel per pair of friends; the presence server publishes A's status changes to channels A-B, A-C, A-D, to which B, C and D are subscribed via WebSocket. Only viable with small groups ([[online-presence]]).

## Additional detail (Xu & Lam Vol. 2, ch. 2 Nearby Friends)
- Redis Pub/Sub as a location routing layer: one channel per user, each friend subscribed; channels are cheap (without messages they consume no CPU; without subscribers the message is dropped; there is no persistence).
- Sizing: ~200 GB of memory for 100M channels x 100 subscribers x 20 B; CPU is the bottleneck (14M pushes/s at ~100K/s per server = ~140 servers).
- Distribution via a hash ring in service discovery; the cluster is stateful because of the subscriber lists: resizing causes mass resubscriptions and brief loss of updates, hence it is overprovisioned. Alternative: Erlang/OTP with one process per user. See [[nearby-friends]].

## Appears in
[[distributed-message-queue]], [[distributed-rate-limiter]], [[fb-live-comments]], [[nearby-friends]], [[robinhood]], [[whatsapp]]

## See also
[[websockets]], [[consistent-hashing]], [[message-queues]]

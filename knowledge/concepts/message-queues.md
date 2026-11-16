---
title: Message queues
type: concept
aliases: [colas, SQS, async workers, kafka]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF) ch. 4 pp. 91-130, https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-news-feed, System Design Interview Vol.1 (Alex Xu), ch. 1, System Design Interview Vol.1 (Alex Xu), ch. 10, Designing Data-Intensive Applications (Kleppmann), ch. 11]
---

# Message queues

## Definition
Durable buffer between producers and workers that decouples and makes work asynchronous.

## Why it matters
It absorbs spikes, avoids blocking the request, and lets workers scale independently.

## How it works
- The service enqueues a message (e.g. postId + creatorId); workers consume it and do the work (update followers' feeds).
- Requires at-least-once delivery (-> idempotent consumers, see [[idempotency]]) and scalability (SQS).

## Variants and techniques
Split very uneven tasks (1M vs 1K followers).

## Trade-offs
Added latency, ordering and duplicates, tasks of uneven size.

## When to use it / when not to
Deferrable work with large fan-out; not for synchronous responses.

## Additional detail (Xu Vol. 1, ch. 1)
Durable in-memory queue that decouples producers (publishers) and consumers (subscribers): the producer publishes even if the consumer is unavailable and vice versa. Example: photo processing (crop, sharpen, blur) by workers; if the queue grows, workers are added; if it is empty, they are reduced. Producer and consumer scale independently.

## Additional detail (Xu Vol. 1, ch. 10)
One queue per notification type (iOS, Android, SMS, email) isolates the outage of an external provider; the key metric is the number of queued messages (if it grows, add workers); send failures are re-enqueued for retry with an alert if they persist ([[notification-system]]).

## Additional detail (DDIA, ch. 11)
- **Two families**: traditional brokers (AMQP/JMS, RabbitMQ; the broker delivers and deletes after *ack*, redelivers if there is no ack, **no ordering guarantee** with parallel consumers; shared load or fan-out) vs **partitioned logs** (Kafka, Kinesis: append-only, each partition with total order, consumers keep an *offset*; the message is retained and can be re-read/replayed; a slow consumer doesn't affect the others; parallelism limited to the number of partitions, and a slow message delays the following ones in its partition — head-of-line blocking).
- Logs allow reprocessing, adding new consumers, using offsets as recovery points, and *log compaction*; see [[change-data-capture]], [[event-sourcing]], [[stream-processing]].
- Choice: broker with ack for expensive individual tasks where order is irrelevant; log for high throughput, per-key ordering and replay. Backpressure (finite disk -> retention).
- At-least-once delivery -> idempotent consumers, see [[exactly-once-processing]].

## Additional detail (Xu & Lam Vol. 2, ch. 4)
- Traditional queue (point-to-point, deletes after ack, no ordering) vs event streaming platform (Kafka/Pulsar: long retention, re-consumption, per-partition ordering). Topic -> partitions (FIFO, offset) -> brokers; consumer groups with one partition per consumer in the group; point-to-point is simulated with a single group.
- Storage: WAL in segments (sequential access); batching in producer/broker/consumer; pull preferable to push (with long polling).
- Leader-follower replication with ISR and ACK=0/1/all; at-most/at-least/exactly-once semantics depending on when the offset is committed and on producer retries.
- Extras: tag filtering, delayed/scheduled messages (delay levels, hierarchical time wheel), retry topic, historical archive. See [[distributed-message-queue]].

## Appears in
[[ad-click-aggregator]], [[camelcamelcamel]], [[chatgpt]], [[distributed-email-service]], [[distributed-message-queue]], [[dropbox]], [[fb-news-feed]], [[fb-post-search]], [[gaming-leaderboard]], [[google-maps]], [[job-scheduler]], [[leetcode]], [[metrics-monitoring]], [[notification-system]], [[payment-system]], [[stock-exchange]], [[uber]], [[web-crawler]], [[whatsapp]], [[youtube]]

## See also
[[fan-out]], [[idempotency]]

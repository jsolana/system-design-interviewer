---
title: Distributed Message Queue
type: interview
sources: [https://www.confluent.io/blog/10x-apache-kafka-elasticity/, System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 4 Distributed Message Queue, pp. 91-130, https://www.linkedin.com/blog/engineering/infrastructure/introducing-northguard-and-xinfra]
concepts: [queue-backlog-management, message-queues, pub-sub, write-ahead-log, replication, consensus, service-discovery, exactly-once-processing, idempotency, long-polling, database-partitioning, retries-timeouts-and-backoff, disaster-recovery, tiered-storage, shard-rebalancing, online-data-migration]
difficulty: high
---

# Distributed Message Queue

## Prompt
Design a distributed message queue (Kafka/Pulsar/RocketMQ/RabbitMQ style). It is designed with features typical of event streaming platforms (long retention, re-consumption, ordering); the chapter points out where the design is simplified if a traditional queue is requested.

## Functional requirements
- Producers send messages to a queue; consumers consume them.
- Messages consumable repeatedly (by different consumers) or only once.
- Historical data can be truncated (2-week retention).
- Text messages, KB range.
- Delivery in production order.
- Configurable delivery semantics: at-most-once, at-least-once, exactly-once.

## Non-functional requirements
- High throughput (log aggregation) or low latency (traditional queue), configurable.
- Scalable (volume spikes).
- Persistent and durable: to disk and replicated across several nodes.
- *Traditional queue*: retention only in memory until consumed, small disk overflow, no ordering guarantee (simplifies a lot).

## Estimations
Not covered in the source (no capacity figures; hundreds of MB/s of sequential disk on RAID are cited).

## API
Not treated as a REST API. Client contract: producer sends to a topic (with optional key), consumer subscribes and pulls from an offset; see "Message data structure" below.

## Data model
Message structure (single contract producer -> queue -> consumer to avoid copies/mutations):
- `key` (byte[], optional; decides the partition with `hash(key) % numPartitions`; not unique and not equivalent to a KV key), `value` (payload, text or compressed binary), `topic`, `partition`, `offset`, `timestamp`, `size`, `CRC` (integrity); optional fields such as tags for filtering.
- A message is located by (topic, partition, offset).
- Data on disk: each partition = folder with **segments** of an append-only WAL; only the active segment receives writes, inactive ones are read-only and are truncated by retention/capacity.
- Consumer state: partition-consumer mapping and last consumed offset per group and partition. Metadata: topics, number of partitions, retention, replica distribution.

## Architecture (high-level design)
- **Models**: point-to-point (a message to a single consumer, deleted after ack) and publish-subscribe (topics). The design is naturally pub-sub; point-to-point is simulated with a single **consumer group**.
- **Topic -> partitions -> brokers**: a topic is divided into partitions (FIFO queue; ordering only within a partition) spread across brokers; capacity scales by adding partitions. Producer: key -> same partition; no key -> random.
- **Consumer groups**: each group maintains its offsets; a partition is consumed by only **one** consumer in the group (preserves ordering); if there are more consumers than partitions, the extras sit idle. It is advisable to preallocate enough partitions.
- Components: clients (producer, consumer group); brokers with **data storage**; **state storage**; **metadata storage**; **coordination service** (service discovery of live brokers and leader election of the active controller broker that assigns partitions; ZooKeeper or etcd). In the ZooKeeper version, metadata and state storage move to ZooKeeper and the broker only keeps the data.

## Deep dives
**Three decisions for throughput**: (1) on-disk structure with sequential access (rotating disks in RAID give hundreds of MB/s sequentially and the OS page cache is aggressive); (2) message immutable end to end to avoid copies; (3) batching everywhere (producer, broker, consumer).

**Storage**: write-heavy and read-heavy load, no updates/deletes, sequential access. A DB (relational or NoSQL) is a poor fit -> **[[write-ahead-log]]** in segments (offset ~ position in the log).

**Batching**: amortizes network round-trips and allows large sequential writes and contiguous disk cache. Throughput vs latency trade-off: small batch for a traditional queue (somewhat less disk); if tuned for throughput, more partitions per topic.

**Producer flow**: option 1, a routing layer that queries the *replica distribution plan* in metadata (cached) and sends to the leader replica; followers pull and the leader acknowledges when "enough" replicas have synced. Drawbacks: extra network hop and no batching. Option 2 (chosen): routing + **buffer** inside the producer library (fewer hops, own partitioning logic, batching).

**Consumer flow**: the consumer indicates an offset and receives a block of messages. **Push vs pull**: push gives low latency but can overwhelm slow consumers and the broker doesn't know their capacity; pull lets the consumer control the pace, favors batching and catch-up, at the cost of empty polling, mitigable with **[[long-polling]]**. **Pull** is chosen.

**Consumer rebalancing** (coordinator): consumers send heartbeats. Join: the new consumer does JoinGroup; the coordinator notifies the others via their next heartbeat so they rejoin, picks a leader among them, the leader generates the assignment plan and the others get it via SyncGroup. Leave: LeaveGroup and rebalance. Crash: no heartbeat for some time -> marked dead and rebalance.

**State and metadata storage**: consumer state: frequent reads/writes but low volume, random access, **consistency important** -> ZooKeeper-style KV (Kafka moved offsets to the brokers themselves). Metadata: little change, low volume, high consistency -> ZooKeeper.

**Replication**: each partition has several replicas on different brokers (leader receives, followers pull); a broker chosen with the coordination service generates and persists the replica distribution plan.

**In-sync replicas (ISR)**: replicas that are caught up with the leader within the configured threshold (e.g. `replica.lag.max.messages`); the leader maintains the list by computing the lag. *Committed offset* = everything before it is synced in the ISR. ISR reflects the performance/durability trade-off: waiting for all replicas would let one slow replica block the partition. ACK settings:
- **ACK=all**: waits for the whole ISR; maximum durability, higher latency.
- **ACK=1**: acknowledges once the leader persists; if it fails before replicating the message is lost; low latency.
- **ACK=0**: no waiting or retrying; minimum latency, possible loss (metrics, logs).
Consumers read from the leader for simplicity (few connections: one partition per consumer in the group; if a topic is hot, more partitions); if the consumer is in another data center, it can read from the closest ISR.

**Scalability**:
- Producers: add/remove instances. Consumers: isolated groups; rebalance on joins/leaves/crashes.
- Brokers, failure: the controller detects the failure, recomputes the plan and creates new replicas that catch up with the leader. Considerations: ISR minimum (safety vs latency), don't place replicas of a partition on the same node, replicating across data centers costs latency (alternative: mirroring).
- Brokers, addition: temporarily allow more replicas than configured; when the new one catches up, the redundant one is removed (avoids data loss); same when removing brokers.
- Partitions: increasing -> no migration (old data stays; new data is distributed; producers and consumers adapt). Decreasing: the removed partition stops receiving but is kept until retention passes; afterwards, group rebalance; doesn't free space immediately.

**Delivery semantics**:
- *At-most-once*: ACK=0 without retries; the consumer commits the offset **before** processing. Metrics.
- *At-least-once*: ACK=1/all with retries; commit **after** processing; possible duplicates (dedup in the consumer with a unique key). General use.
- *Exactly-once*: the most costly and complex; for payments, trading, accounting, when the destination is not idempotent.

**Advanced features**: *message filtering* (better in the broker by **tags** in metadata, without reading/decrypting the payload; complex filters would require a parser/scripting, too heavy; the alternative of a dedicated topic per consumer couples and duplicates data); *delayed messages* (temporary storage in special topics + timing function: predefined delay levels like RocketMQ (1s...2h) or **hierarchical time wheel**); *scheduled messages* similar.

## Trade-offs and decisions
- Event streaming (retention, ordering, replay) vs traditional queue (in memory, no ordering, simpler).
- Sequential WAL vs database.
- Pull vs push; large batch (throughput) vs small (latency).
- ACK=0/1/all: latency vs durability; ISR versus "all replicas".
- Read from the leader (simple) vs a nearby replica.
- Number of replicas and their location: safety vs cost/latency.

## Related concepts
[[message-queues]], [[pub-sub]], [[write-ahead-log]], [[replication]], [[consensus]], [[service-discovery]], [[exactly-once-processing]], [[idempotency]], [[long-polling]], [[database-partitioning]]

## Follow-up questions
- Protocol (AMQP, Kafka protocol): cover production, consumption, heartbeat, efficient transport and integrity.
- Consumption retry without blocking: dedicated retry topic.
- Historical archive: replay already truncated messages -> HDFS or object storage.

## Variants
- **LinkedIn Northguard / Xinfra (Kafka successor)**, source: https://www.linkedin.com/blog/engineering/infrastructure/introducing-northguard-and-xinfra. Differs: motivated by Kafka limits at ~32T records/day, 17 PB/day, 400K topics, 10K+ machines, 100-150 clusters. Data model records -> segments (replication unit, sealed at 1 GB / 1 h / replica failure) -> ranges -> topics, so load balances by striping with no partition rebalancing; sharded metadata in Raft-backed vnodes on a consistent-hash ring; SWIM membership; WAL + file per segment, Direct I/O, sparse RocksDB index; fsync on all replicas before ack (batched about 10 ms) vs Kafka lazy sync; deterministic simulation testing. Xinfra virtualizes Pub/Sub over Northguard and Kafka for live topic migration (dual writes, producers then consumers); 80%+ fewer clusters, 90%+ apps on Xinfra clients. See [[shard-rebalancing]], [[online-data-migration]].

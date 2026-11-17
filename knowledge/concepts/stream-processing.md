---
title: Stream processing
type: concept
aliases: [Flink, Kafka, windowing, watermarks, tumbling windows]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 6 Ad Click Event Aggregation, pp. 159-193, https://www.hellointerview.com/learn/system-design/problem-breakdowns/top-k, Designing Data-Intensive Applications (Kleppmann), chs. 11-12, DDIA 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 12 (pp. 487-529)]
---

# Stream processing

## Definition
Processing continuous streams of events (Kafka + Flink) with aggregations over time windows.

## Why it matters
Drastically reduces the volume of DB writes by aggregating beforehand (2-100x) and enables near-real-time results.

## How it works
- Kafka partitioned by key (videoId); consumers scale per partition.
- Flink: tumbling windows (e.g. 1 h), BoundedOutOfOrderness watermarks (~30 s) for late events, checkpoints and rewinding Kafka offsets for recovery; large state in RocksDB.
- Batched output to a DB or Redis sorted sets.

## Variants and techniques
- Tumbling (fixed, simple) vs sliding (increment the last minute and decrement the one from N ago; high memory cost if the slide is short).
- Sliding only where the product requires it (last hour).

## Additional detail (Ad Click Aggregator)
- Batch (Spark/MapReduce via cron) -> data minutes behind; streaming with Flink (event time, watermarks, exactly-once) -> near real time; flush to OLAP every few seconds with minute windows.
- Stream sharded by key; hot keys with a random suffix and upsert with SUM.
- Retention (~7 days) for replay; **Lambda reconciliation**: archive in a data lake (S3) + periodic batch that corrects the store ([[ad-click-aggregator]]).

## Trade-offs
Requires deep knowledge of Flink; risk of turning the interview into a low-level debate.

## When to use it / when not to
Massive aggregable writes (counters, metrics); not for low volumes.

## Additional detail (DDIA, chs. 11-12)
- **Streams vs batch**: unbounded input; a broker log ([[message-queues]]) as the source; same operators as batch plus time and state management ([[batch-processing]]).
- **Uses**: complex event processing (patterns over events), analytics with aggregations over windows (with approximate algorithms such as Bloom filter/HyperLogLog/percentiles), maintaining materialized views ([[derived-data-and-dataflow]]), search over streams, RPC with actors (not stream processing).
- **Event time vs processing time**: using processing time distorts results with delays or reprocessing; with event time you must decide when a window is "complete": ignore *stragglers* or publish a correction. There are three possible timestamps on mobile devices (event on the device, send, receipt at the server) and the device clock offset is corrected.
- **Window types**: tumbling (fixed, no overlap), hopping (with overlap), sliding (events within an interval), session (groups a user's activity, no fixed duration).
- **Stream joins**: stream-stream (window, per-key state; e.g. impressions with clicks), stream-table (enrich events with a local copy of the table updated via CDC; see [[change-data-capture]]) and table-table (maintain a materialized view). Ordering across streams is non-deterministic -> *slowly changing dimensions* with version IDs.
- **Fault tolerance and exactly-once**: microbatching, checkpoints, idempotence ([[exactly-once-processing]]).

## Additional detail (Xu & Lam Vol. 2, ch. 6)
- **Event time vs processing time**: event time is more accurate but forces you to handle late events; a **watermark** (extended aggregation window, e.g. 15 s) is used, which improves accuracy at the cost of latency; anything very late is corrected via batch reconciliation.
- **Windows**: tumbling (fixed, no overlap; per-minute counts) and sliding (overlapping; top N of the last M minutes); also hopping and session.
- **Map -> Aggregate -> Reduce DAG**: nodes with a single task, intermediate data in memory (TCP or shared memory); state recoverable with periodic snapshots (offset + state) and replay from Kafka.
- **End-to-end exactly-once**: sending downstream, saving the offset and the ack must be in a distributed transaction (second Kafka queue for atomic commit). See [[ad-click-aggregator]] and [[derived-data-and-dataflow]] (Lambda vs Kappa).

## Additional detail (DDIA 2nd edition, ch. 12)
- *2nd edition (verification)*: chapter now "Stream Processing" (ch. 12) merges messaging, CDC and processing; the 1st-edition concepts hold. Additions:
- **Fault tolerance**: *microbatching* (Spark Streaming, ~1 s batches; implicit tumbling window by processing time) vs *rolling checkpoints* via barriers (Flink). Both give exactly-once only inside the framework; external side effects (DB writes, emails) need atomic commit of outputs + state + offsets, or **idempotent** writes (see [[exactly-once-processing]]). Actor frameworks usually do not guarantee delivery after crashes.
- **Materialized view maintenance** by stream processors (Kafka Streams, ksqlDB); event-sourced views need all events back to the start (no window). Databases often refresh views by batch (`REFRESH MATERIALIZED VIEW`); triggers work only for easily incremental cases; **incremental view maintenance (IVM)** compiles queries into incremental operators (e.g. Materialize). See [[materialized-views]].
- Stream joins (stream-stream, stream-table enrichment, table-table) and "search on streams" appear as uses; batch jobs use event timestamps, not the machine clock.

## Appears in
[[ad-click-aggregator]], [[ad-click-prediction]], [[fb-live-comments]], [[food-delivery-time-estimation]], [[google-maps]], [[metrics-monitoring]], [[top-k]], [[typeahead]]

## See also
[[message-queues]], [[count-min-sketch]], [[redis-sorted-sets]]

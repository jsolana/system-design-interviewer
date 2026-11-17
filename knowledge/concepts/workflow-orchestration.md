---
title: Workflow orchestration
type: concept
aliases: [Temporal, DAG, durable execution]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/youtube, System Design Interview Vol.1 (Alex Xu), ch. 14, DDIA 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 5 (pp. 187-189), https://discord.com/blog/how-discord-automates-scylladb-clusters-at-scale]
---

# Workflow orchestration

## Definition
Engine that reliably coordinates tasks with dependencies (DAG), with retries and state.

## Why it matters
Multi-step pipelines (e.g. transcoding) have parallel, independent tasks and a final step that depends on all of them.

## How it works
An engine like Temporal manages the DAG; intermediate data lives in storage (S3) and only URLs are passed between workers.

## Variants and techniques
Internal queue to absorb bursts; queue depth triggers worker autoscaling.

## Trade-offs
Additional dependency in exchange for reliability and visibility of progress.

## When to use it / when not to
Long, multi-stage processes; not for simple single-step tasks.

## Additional detail (Xu Vol. 1, ch. 14)
DAG model for the video transcoding pipeline: the preprocessor generates the DAG from configuration files, the DAG scheduler splits it into stages and enqueues them, the resource manager assigns tasks to workers ([[video-transcoding]]).

## Additional detail (DDIA 2nd edition, ch. 5)
- *2nd edition (new)*: workflow = graph of tasks run by an engine split into **orchestrator** (schedules) and **executor** (runs tasks). Families: data/ETL (Airflow, Dagster, Prefect), graphical BPMN (Camunda, Orkes), **durable execution** (Temporal, Restate).
- Durable execution logs every RPC and state change to durable storage (like a write-ahead log); on retry it replays the code, skipping calls already done and returning their recorded results. Gives exactly-once semantics for multi-service workflows (e.g. charge card + deposit funds) where a DB transaction is impossible.
- Caveats: external APIs must still be idempotent (unique IDs); replay requires deterministic code (no raw random/clock; use framework versions) and same call order, so deploy changed workflows as a new version.

## Additional detail (Discord Scylla Control Plane)
Discord replaced fragile scripts for ScyllaDB ops (rolling restarts, expansion, OS upgrades, shadow clusters; dozens of clusters, hundreds of nodes, 7-person team) with a Rust framework: tasks (node/cluster) with preconditions and idempotent execute, blocking conditions polling Scylla/Prometheus with stabilization windows, YAML workflows (retries, abort, parallelism by `concurrency_unit`/`concurrency_limit`), jobs persisted in local SQLite for resume, recoverable vs unrecoverable error classes, webhook alerts. Serial node joins per AZ protect quorum at the cost of speed. A 36 h manual operation became under 2 h of active attention. Source: https://discord.com/blog/how-discord-automates-scylladb-clusters-at-scale

## Appears in
[[job-scheduler]], [[uber]], [[youtube]]

## See also
[[message-queues]], [[adaptive-bitrate-streaming]]

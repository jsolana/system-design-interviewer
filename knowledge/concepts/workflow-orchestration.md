---
title: Workflow orchestration
type: concept
aliases: [Temporal, DAG, durable execution]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/youtube, System Design Interview Vol.1 (Alex Xu), ch. 14]
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

## Appears in
[[job-scheduler]], [[uber]], [[youtube]]

## See also
[[message-queues]], [[adaptive-bitrate-streaming]]

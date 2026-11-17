---
title: Job Scheduler
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/job-scheduler]
concepts: [message-queues, workflow-orchestration, distributed-periodic-scheduling, retries-timeouts-and-backoff, leader-election, queue-backlog-management]
difficulty: medium
---

# Job Scheduler

> Note: partially paywalled page; only the statement, requirements and deep dive questions were readable. Tagged patterns: Managing Long Running Tasks and Scaling Writes.

## Prompt
A system that automatically runs jobs at the specified time or interval (repetitive tasks, maintenance, batch). **Task** = reusable unit of work (e.g. sending an email); **Job** = an instance of a task with a schedule and parameters.

## Functional requirements
- Schedule immediate, future or recurring jobs (e.g. daily at 10:00).
- Monitor job status.
- Out of scope: cancelling or rescheduling.

## Non-functional requirements
- Scale: 10k jobs/s. The deep dives involve executing within < 2 s of the scheduled time. Full list not visible.

## Estimations
Only 10k jobs/s.

## API
Not covered in the source.

## Data model
Not covered in the source.

## Architecture (high-level design)
Not covered in the source.

## Deep dives
Questions only: execute jobs within 2 s of their time; scale to 10k jobs/s; guarantee at-least-once execution.

## Trade-offs and decisions
Not covered in the source.

## Related concepts
[[message-queues]], [[workflow-orchestration]] (*Note*: indicative).

## Follow-up questions
The three deep dives.

## Variants
Not covered in the source.

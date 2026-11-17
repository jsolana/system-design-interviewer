---
title: A/B testing for ML models
type: concept
aliases: [budget-splitting, online experiments, traffic allocation]
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 1 pp. 58-59, 81-82]
---

# A/B testing for ML models

## Definition
Online controlled experiments that send a share of traffic to a new model and compare business metrics against the production model.

## Why it matters
Final arbiter of model value; offline metrics may not move online metrics. In production dozens of models can each receive a traffic share (SageMaker, LinkedIn).

## How it works
Users split into control (current model) and treatment (new model); compare CTR, watch time, revenue lift, conversion; ramp traffic gradually, then replace the production model.
**Budget-splitting** (LinkedIn; ads marketplace): normal A/B tests let control and treatment compete for the same campaign budget, so a revenue lift may just be budget shifting. Fix: split members into equal groups, split each campaign budget 50/50 into two sub-campaigns, assign one to each group. Sub-campaigns are independent and the test runs on a large population (more statistical power).

## Variants and techniques
Cohort analysis for time-spent metrics; reference: "Trustworthy Online Controlled Experiments".

## Trade-offs
Duration vs percentage of traffic; interference between groups in marketplaces.

## When to use it / when not to
Always before full rollout; use budget-splitting for shared-budget ad systems.

## Appears in
[[gmail-smart-compose]]

## See also
[[ml-evaluation-metrics]], [[exploration-exploitation]]

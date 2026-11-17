---
title: GenAI system design interview framework
type: concept
aliases: [ML system design framework, GenAI interview steps]
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 1]
---

# GenAI system design interview framework

## Definition
Seven-step structure for open-ended GenAI design questions: clarify requirements, frame as an ML task, prepare data, develop the model, evaluate, design the overall system, deploy and monitor.

## Why it matters
Interviews are open-ended; a structure keeps answers organized and shows reasoning rather than a single "correct" answer.

## How it works
1. **Clarify requirements**: business objective, features, data (sources, size, labels), constraints (compute), scale (users, growth), performance (latency, quality vs speed); also privacy, ethics, security.
2. **Frame as ML task**: define input/output modalities; pick discriminative vs generative, task type (classification/regression vs text/image/video generation), then algorithm (VAE, GAN, diffusion, autoregressive), discussing trade-offs and unified vs per-modality models.
3. **Data preparation**: structured data (ETL, feature engineering/feature stores) vs unstructured GenAI data (large-scale collection, cleaning, dedup, safety/NSFW filtering, bias, sensitive data, synthetic data with caveats, storage on HDFS/S3 and Parquet/ORC, retrieval via sharding, indexing, caching).
4. **Model development**: architecture (e.g. U-Net vs DiT), training methodology (multi-stage), data per stage, ML objective, loss, task-specific challenges, efficiency ([[distributed-training-parallelism]]), sampling.
5. **Evaluation**: offline (generative metrics need subjective/human methods) and online (CTR, conversion, engagement, churn, feedback, retention, task completion); bias, robustness, human evaluation.
6. **Overall system design**: components, safety and moderation, feedback loops and retraining, scalability (load balancing, distributed inference), security, bias, robustness.
7. **Deployment and monitoring**.

## Variants and techniques
Context: GenAI quality drivers are data (self-supervised on unlabeled data; Llama 3 used 15T tokens, about 50 TB), model capacity (parameters, FLOPs) and compute; risks: ethics/IP, environmental cost, hallucination, deepfakes and adversarial misuse.

## Trade-offs
Depth in one area vs breadth; tailor emphasis to the role (infra, LLM, monitoring).

## When to use it / when not to
Use for any GenAI design prompt.

## Appears in
None yet.

## See also
[[system-design-interview-framework]], [[llm-training-stages]], [[transformer-architecture]]

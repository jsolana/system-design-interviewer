---
title: Ad Click Prediction (ML)
type: interview
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 6 pp. 185-194, https://engineering.fb.com/2026/10/28/ml-applications/meta-andromeda-next-gen-ads-retrieval-gpu-co-design/]
concepts: [ml-evaluation-metrics, ml-loss-functions, model-calibration, imbalanced-data-and-sampling, feature-engineering-for-ml, deep-learning-recsys-architectures, model-retraining, ml-model-serving, training-serving-skew-and-feature-store, stream-processing]
difficulty: high
---

# Ad Click Prediction (ML)

## Prompt
Build a model that predicts whether an ad will be clicked. The cascade of classifiers common in ad tech is ignored. Ad requests flow through a waterfall: publishers first try direct sales at high CPM and pass the impression to other networks until sold.

## Functional requirements
- Return click probability for each candidate ad (candidates come from upstream services).
- Challenges named: latency (waterfall) and overspend (repeatedly serving the same ad can overspend the campaign budget).

## Non-functional requirements
- Serving latency 50-100 ms.
- Training: very imbalanced data (CTR 1-2%); retrain many times per day; split train/validation by time.

## Estimations
- 40k ad requests/s or 100 billion/month; ~1% CTR -> 1 billion clicked ads/month.
- Book computes 100 x 10^9 x 500 B = 5 x 10^13 B = 50 TB per month (also states 50 bytes per record in the assumptions: source inconsistency). Reduce by downsampling to 1-10% or training on one week and validating on the next day.
- Scale: 100 million users.

## API
Not covered in the source.

## Data model
Historical records (user, ad, click_or_not) with hundreds of features; logs and Kafka events land in a data lake.

## Architecture (high-level design)
- **Training**: logs + event data (Kafka) -> data lake -> batch data prep (ETL) -> training data store -> batch/scheduled/on-demand training jobs -> model store (S3-like).
- **Serving**: ad candidates from upstream; stream data prep pipeline computes online features into key-value storage; standalone model serving service returns click probability.
- Model: sparse logistic regression (efficient, copes with sparse features); alternative DCNv2 ([[deep-learning-recsys-architectures]]). Subsample negatives at various ratios while keeping validation distribution like test; post-process with calibration.
- Features: advertiser ID (embedding or hashing, thousands of advertisers), temporal (one hot), user click history (scaled), user similarity embeddings, cross features ([[feature-engineering-for-ml]]).

## Deep dives
- **Metrics**: NCE (insensitive to background CTR) and calibration (expected vs observed clicks) offline; revenue lift online via A/B test, trading traffic share vs duration ([[ml-evaluation-metrics]], [[model-calibration]]).
- **Scaling**: 50k-100k candidates in 50-100 ms is not feasible with one instance per request; an **aggregator service** splits candidates across serving instances and merges results ([[ml-model-serving]]).

## Trade-offs and decisions
Logistic regression (fast, sparse-friendly) vs DCNv2 (auto crosses); downsampling (cheap training) vs probability bias that calibration must fix; time-based split to mimic production.

## Related concepts
[[imbalanced-data-and-sampling]], [[ml-loss-functions]], [[model-retraining]], [[training-serving-skew-and-feature-store]], [[stream-processing]].

## Follow-up questions
Not covered in the source beyond the pointers above (see [[ad-click-aggregator]] for the non-ML event aggregation problem).

## Variants
<!-- One entry per variant: source + how it differs from the base design -->
- **Meta Andromeda (first-stage ads retrieval)**, source: https://engineering.fb.com/2026/10/28/ml-applications/meta-andromeda-next-gen-ads-retrieval-gpu-co-design/. Differs: retrieval-stage systems co-design. Mixture-of-experts retrieval (user-tower experts, ad tower, attention gating top-K) in one fused GPU pipeline (index matching, scoring, top-K) so only compact payloads travel; fused kernels keep intermediates on-chip because memory traffic, not FLOPs, is the bottleneck. Claims >1B ads/s in production (about 100x 2024), ~300x fewer inference FLOPs, ~100x less network traffic, INT8 gating up to 2x over FP16, +2.4% conversions on Facebook. See [[ml-model-serving]].

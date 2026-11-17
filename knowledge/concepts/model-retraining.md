---
title: Model retraining and data splits
type: concept
aliases: [warm start, nonstationarity, data drift, retraining levels, training pipeline]
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 1 pp. 33-42, 126]
---

# Model retraining and data splits

## Definition
Keeping models fresh as the data distribution shifts, and building a training pipeline that is fast and correctly split in time.

## Why it matters
Data is nonstationary (viral videos, trends, game-day traffic); stale models under-estimate delivery time or mis-rank ads. A scheduler typically retrains many times per day.

## How it works
- **Four levels** (LinkedIn): L0 train and forget (stationary); L1 cold-start periodic full retrain on batch; L2 near-line per-key component retraining on streams; L3 warm-start retraining of personalized per-key components in bulk once enough data accumulates.
- **Storage**: column formats (Parquet, Avro, ORC; tfrecord for TensorFlow), partitioned by year/month to avoid scanning everything and to parallelize. Parquet can be ~30x faster / 99% cheaper in scanned data vs CSV (book's AWS Athena figure). See [[olap-columnar-stores]].
- **Splits**: respect chronology for forecasting/ads (train on past, test on future); ensure entities (store IDs) appear in both; **sliding window** (day 0-60 train, 61-90 test; then 10-70 / 71-100) or **expanding window** (0-60/61-90, then 0-70/71-100). Replay evaluation for feeds.
- Practical: keep last 6-12 months in the data lake, archive older in cold storage; fine-tune existing DL model on recent data; balance model complexity and training time; decide frequency by cost vs online gain ("it depends").
- **Drift handling**: Bayesian logistic regression (LinkedIn Lambda Learner combines historical and near-time data), though cumbersome; feature drift alerts ([[training-serving-skew-and-feature-store]]).

## Variants and techniques
Spark / EMR / Dataproc feature pipelines; model repo in S3 pulled by serving by timestamp; schedulers ([[workflow-orchestration]]).

## Trade-offs
Fresher models cost compute and operational complexity; incremental retraining risks drift in calibration.

## When to use it / when not to
Ads, feeds, delivery/ETA: retrain hours-level. Stationary problems: level 0.

## Appears in
[[ad-click-prediction]], [[fb-news-feed]], [[food-delivery-time-estimation]], [[linkedin-course-recommendation]], [[realistic-face-generation]], [[uber-eta-prediction]], [[youtube]]

## See also
[[exploration-exploitation]], [[imbalanced-data-and-sampling]], [[ml-model-serving]]

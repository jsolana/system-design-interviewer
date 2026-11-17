---
title: Training-serving skew and feature store
type: concept
aliases: [feature logging, feature store, feature drift, TFDV]
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 1 pp. 90-96, ch. 5-8 feature store sections]
---

# Training-serving skew and feature store

## Definition
Training-serving skew: features are computed differently when training and when serving, silently degrading predictions. A feature store is the key-value layer serving low-latency features (and versioned training features).

## Why it matters
Spotify's podcast model ("Shows you might like") ran four months with a few lines of differing feature-transform code in the online path before it was noticed.

## How it works
- **Solutions**: (1) a single transformation shared by training and serving (e.g., TensorFlow Transform embeds preprocessing in the graph); (2) **feature logging**: log the already-transformed features at serving time (owned by the ML team rather than upstream services) and train on those logs. Spotify chose logging, implemented the transform in Java, used TensorFlow Data Validation to compare schemas/distributions regularly, and alerts on drift (Chebyshev distance).
- **Log volume**: log rotation; in Kubernetes, node-level logging agent, sidecar container, or push to a backend directly.
- **Feature store**: key-value (e.g., DynamoDB) for near-real-time features (clicks in last 3h/24h) plus rarely changing ones (home country); stream pipeline (Kafka) aggregates; training reads versioned data from S3/Parquet; feature version chosen by event date.
- **Retrieval vs ranking service split**: pros: versioned models, swap backend DB without touching models, better throughput/latency; con: more prone to skew.

## Variants and techniques
Offline + nearline embedding serving (LinkedIn feature marketplace).

## Trade-offs
Logging fixes skew but costs storage; shared transforms constrain languages/teams.

## When to use it / when not to
Any online ML where serving is built by a different team than training.

## Appears in
[[ad-click-prediction]], [[airbnb-search-ranking]], [[food-delivery-time-estimation]]

## See also
[[feature-engineering-for-ml]], [[ml-model-serving]], [[model-retraining]], [[stream-processing]]

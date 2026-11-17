---
title: Uber ETA Prediction (DeepETA)
type: interview
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 3 pp. 151-153]
concepts: [ml-loss-functions, feature-engineering-for-ml, embeddings, geospatial-indexing, model-retraining, ml-model-serving]
difficulty: medium
---

# Uber ETA Prediction (DeepETA)

## Prompt
Predict arrival time, using an ML model as a post-processing step on top of the routing engine's ETA.

## Functional requirements
Global ETA predictions across all lines of business (mobility, delivery).

## Non-functional requirements
- Latency: milliseconds.
- Accuracy: MAE significantly better than the incumbent XGBoost model.
- Generality across business lines.

## Estimations
Not covered in the source.

## API
Not covered in the source.

## Data model
Continuous features: quantile buckets then embedding; categorical: embedding; location: geospatial embeddings via exact indexing, feature hashing or multiple feature hashing.

## Architecture (high-level design)
Encoder-decoder model. Serving: requests -> uRoute (front end for routing lookups) -> routing engine produces route lines and ETA -> uRoute calls the Michelangelo online prediction service with ETA + features -> DeepETA returns the refined ETA. Training pipeline periodically retrains and validates.

## Deep dives
Loss: asymmetric Huber (tunable outlier robustness and under/over-prediction trade-off), see [[ml-loss-functions]].

## Trade-offs and decisions
Post-process the routing ETA (simple, flexible) instead of replacing the router.

## Related concepts
[[geospatial-indexing]], [[embeddings]], [[ml-model-serving]]. See [[uber]] for the ride-matching system.

## Follow-up questions
Not covered in the source.

## Variants
<!-- One entry per variant: source + how it differs from the base design -->

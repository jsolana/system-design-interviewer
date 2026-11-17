---
title: Model calibration
type: concept
aliases: [calibration plot, Platt scaling, isotonic regression, calibration ratio]
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 2 pp. 121-125, ch. 6 p. 187, 189]
---

# Model calibration

## Definition
Predicted probabilities should match observed frequencies: if the model says 0.2, 20% of those cases are positive. **Calibration = sum(predictions) / sum(labels)** (expected vs observed clicks).

## Why it matters
Ads bid on the actual click probability, and probability-critical domains (patient is sick) need it. AUC alone can mislead: an SVM had AUC 0.97 vs logistic regression 0.858 but was badly under-confident at low scores and over-confident at high ones.

## How it works
- Diagnose with a **calibration plot**: x = mean prediction per bin, y = fraction of positives; plus a histogram of predictions (10 bins).
- Causes: poor generalization, nonstationarity, selection bias from resampling, training/serving label misalignment.
- Fixes: **isotonic regression** (non-parametric, minimizes squared error), **Platt scaling** (`p = 1/(1+exp(A*pred+B))`, fit by max likelihood), temperature scaling.
- **After negative downsampling** (Facebook): `q = p / (p + (1-p)/w)` where p is the prediction and w the negative downsampling rate.

## Variants and techniques
Post-processing step in ad click pipelines.

## Trade-offs
Extra fitting stage and data needed; ranking-only use cases may not need it.

## When to use it / when not to
Needed when the absolute probability is used (ads, risk); skip when only order matters.

## Appears in
[[ad-click-prediction]]

## See also
[[imbalanced-data-and-sampling]], [[ml-loss-functions]], [[ml-evaluation-metrics]]

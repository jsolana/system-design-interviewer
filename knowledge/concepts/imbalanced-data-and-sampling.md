---
title: Imbalanced data and sampling techniques
type: concept
aliases: [class imbalance, negative downsampling, SMOTE, importance sampling, reservoir sampling, stratified sampling, negative sampling]
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 1 pp. 34-36, 60-67]
---

# Imbalanced data and sampling techniques

## Definition
Methods to train on skewed labels (ad click ~0.2-2% positive, fraud, spam) and to draw representative or negative samples.

## Why it matters
With few positives the model spends its capacity on negatives. Many "novel" architectures are really clever sampling (noise-contrastive negative sampling, Twitter importance sampling for delayed feedback).

## How it works
- **Class weights** in the loss (`-w0*y*log p - w1*(1-y)*log(1-p)`; quiz: 100 positive vs 300 negative -> depends, 3 is the usual choice).
- **Naive resampling**: downsample the majority (most common at Facebook/Google scale; via SQL `WHERE RAND() < 0.1`); keep validation and test intact. For deep models, downsample then **upweight**: `example_weight = original_weight * downsampling_factor` to keep calibration. Predictions must be corrected afterwards ([[model-calibration]]); otherwise online precision is lower than offline.
- **Synthetic resampling (SMOTE)**: interpolate between a minority point and its k nearest neighbors; rarely used at scale.
- **Sampling techniques**: random (e.g., unseen videos as negatives to start), rejection (proposal q with k*q >= p; rand7 -> rand10), weighted, **importance** (estimate E_p[h] by sampling q and weighting p/q), stratified (preserve group ratios), reservoir (k of n unknown, O(n)).
- **Label generation**: LinkedIn feed -> chronological ordering collects data but has serving bias, random serving hurts UX, so rank with a model and randomly permute within the top (some exploration); Facebook places -> liked places as positives, seen-but-not-liked or all others as negatives.

## Variants and techniques
Cold-start labels (LinkedIn Learning): skill taxonomy, taggers, supervised (course, skill) classifier, semi-supervised per-skill models.

## Trade-offs
Downsampling speeds training but biases probabilities; SMOTE is costly and rarely beneficial at scale.

## When to use it / when not to
Downsampling + upweight/calibration for click/booking prediction at scale; weights for modest imbalance.

## Appears in
[[ad-click-prediction]], [[airbnb-search-ranking]], [[fb-news-feed]], [[linkedin-course-recommendation]], [[youtube]]

## See also
[[model-calibration]], [[ml-loss-functions]], [[model-retraining]]

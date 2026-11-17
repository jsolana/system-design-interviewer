---
title: Learning to rank
type: concept
aliases: [RankNet, pairwise ranking, pointwise ranking, position bias, inverse propensity score]
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 2 pp. 110-118]
---

# Learning to rank

## Definition
Training models whose purpose is ordering results (search, feed, ads), formulated point-wise, pairwise or list-wise.

## Why it matters
Ordering quality (nDCG, MAP) and click-probability estimation pull in different directions; position bias contaminates click labels.

## How it works
- **Point-wise**: predict a score per item, sort. Needs absolute labels (ordinal regression is hard).
- **Pairwise**: only learn which of two items ranks higher; naive cost n(n-1)/2 comparisons (100 results -> 4,950). **RankNet**: model f(x); `P_ij = e^{o_ij}/(1+e^{o_ij})` with `o_ij = f(x_i)-f(x_j)`; cross-entropy cost against target probability; pairs need not be complete or consistent; any DL architecture (e.g., 2 fully connected layers). Observation: pairwise gets high AUC but poor nDCG/click-probability calibration (good order, bad probability estimates).
- **Position bias**: users click top results regardless of quality, so labels are biased. Fixes: feed position as a training feature and set it to a constant/missing at serving; in wide and deep put it in the shallow tower; Instagram feeds sparse position into the last fully connected layer; probabilistic click models `P(relevance|pos)`; **inverse propensity score** (propensity estimated by randomization; unstable when behavior changes daily); position weights such as `w=1+p`, `log(beta+p)`, `1-1/(alpha+p)`.

## Variants and techniques
LinkedIn talent search found pairwise better than point-wise in practice; Airbnb optimizes booking likelihood with nDCG.

## Trade-offs
Pairwise: fewer label requirements, higher compute, poor calibration. Point-wise: simple, calibrated, needs labels.

## When to use it / when not to
Pairwise when only relative preference is observable; point-wise (logistic regression) when calibrated probabilities matter (ads, see [[model-calibration]]).

## Appears in
[[linkedin-talent-search]]

## See also
[[recommendation-system-pipeline]], [[ml-evaluation-metrics]]

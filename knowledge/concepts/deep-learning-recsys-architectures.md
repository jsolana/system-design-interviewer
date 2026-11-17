---
title: Deep learning architectures for recommendation
type: concept
aliases: [wide and deep, deep cross network, DCN v2, multitask learning, DLRM]
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 1 pp. 68-80]
---

# Deep learning architectures for recommendation

## Definition
Common neural architectures for ranking/retrieval with sparse and dense features.

## Why it matters
Choosing among them is a frequent interview step after features and metrics.

## How it works
- **Wide and Deep** (Google Play): wide part (cross/co-occurrence features such as installed x impression apps) gives memorization; deep part (embeddings of categoricals) gives generalization.
- **Two-tower**: retrieval, see [[embeddings]].
- **Deep Cross Network v2**: cross layers learn explicit feature crosses (degree grows with depth) alongside an MLP; stacked (cross layers between input and hidden layers, usually better) or parallel. Google reports 0.6% AUC-loss improvement over a production model (0.1% is significant); 2 cross layers best; low-rank with rank = input/4 keeps accuracy.
- **Multitask learning** (YouTube Watch Next ranking): shared bottom layers, heads for p(like), p(comment)...; combine as a weighted score. Blending video vs photo: map probabilities to a well-behaved distribution (Gaussian) first (Instagram).
- **DLRM** (Facebook): categorical -> embeddings; continuous -> MLP to same-size vector; interaction op (concat/dot/sum); top MLP; sigmoid. Metric: accuracy/AUC for clicks.
- Airbnb lessons: DL is not a drop-in replacement for GBDT (no initial gain); dropout did not help online; do not init weights/embeddings to zero (Xavier, uniform [-1,1] for embeddings); LazyAdam helps with large embeddings.

## Variants and techniques
GBDT (XGBoost) remains a strong alternative for tabular features (LinkedIn talent search, DoorDash).

## Trade-offs
Capacity and automatic crosses vs training/serving cost.

## When to use it / when not to
Many sparse features and enough data: DCN/DLRM; small tabular data: GBDT.

## Appears in
[[ad-click-prediction]], [[youtube]]

## See also
[[feature-engineering-for-ml]], [[embeddings]], [[recommendation-system-pipeline]]

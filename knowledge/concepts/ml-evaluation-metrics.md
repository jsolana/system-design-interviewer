---
title: ML evaluation metrics (offline and online)
type: concept
aliases: [nDCG, MAP, MRR, AUC, precision at k, CTR, offline metrics, online metrics]
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 1 pp. 53-59, ch. 3-8 metrics sections]
---

# ML evaluation metrics (offline and online)

## Definition
Metrics used before deployment (offline, on held-out data) and after (online, on live traffic) to decide whether a model improves the product.

## Why it matters
Offline gains do not always translate online (Airbnb: +1% offline nDCG from dropout, no online gain); nonstationary data makes offline metrics weak predictors.

## How it works
**Offline**: log loss, MAE, R2, RMSE; **AUC** (ROC: TPR vs FPR; random = 0.5); precision/recall/F1/accuracy; **P@K**; **MAP** (`AP@n = 1/GTP * sum P@k*rel@k`); **MRR** (`1/n * sum 1/rank_i` of the first relevant result, e.g., ranks 3,2,1 -> 11/18); **DCG** `sum rel_i / log2(i+1)`, **nDCG = DCG/IDCG** (graded relevance, position discounted; example listed=0, clicked=1, ordered=2 -> nDCG@5 = 0.587); NCE and calibration for ads ([[ml-loss-functions]], [[model-calibration]]). Plain cumulative gain ignores order; do not use MRR if several correct results matter.
**Online**: A/B test ([[ab-testing]]) on CTR (clicks/visitors), watch time, time spent per active user (total time / active users), conversion rate, revenue lift, bookings per search, InMail acceptance rate, satisfaction (dismissals, surveys). Rollout: staging with a small traffic share -> gradually larger -> replace production model.

## Variants and techniques
Replay evaluation (LinkedIn feed): train up to T, take T+1 impressions, re-rank by the model and count matches where a predicted click lands at the right position, to avoid biased offline evaluation.

## Trade-offs
Accuracy-type metrics vs ranking metrics vs calibration: pairwise models can have high AUC and poor nDCG/calibration ([[learning-to-rank]]).

## When to use it / when not to
Pick metrics matching the formulation: ranking -> nDCG/MAP/MRR; classification with imbalance -> precision/recall/NCE; forecasting -> MAE/MAPE.

## Appears in
[[ad-click-prediction]], [[airbnb-room-classification]], [[airbnb-search-ranking]], [[fb-news-feed]], [[food-delivery-time-estimation]], [[linkedin-course-recommendation]], [[linkedin-people-you-may-know]], [[linkedin-talent-search]]

## See also
[[ml-loss-functions]], [[ab-testing]]

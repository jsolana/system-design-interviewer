---
title: ML loss functions
type: concept
aliases: [MSE, MAE, Huber loss, quantile loss, cross entropy, normalized cross entropy, focal loss, hinge loss]
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 1 pp. 43-52]
---

# ML loss functions

## Definition
The objective minimized when training a model; choosing it (and the tracked metric) is one of the key decisions in an ML design.

## Why it matters
The loss encodes the business asymmetry (over vs under-estimation), robustness to outliers and sensitivity to class imbalance or background rate.

## How it works
**Regression**
- **MSE** = mean (target-pred)^2; sensitive to outliers (example: one outlier 50 vs 35 moves MSE from ~4 to 56.5 while MAE goes 1.7 -> 4).
- **MAE** = mean |target-pred|; robust, gradient not continuous at 0.
- **Huber**: quadratic when |error| <= delta, linear beyond (`delta|e| - delta^2/2`); needs tuning delta. Uber uses pseudo-Huber/log-cosh in distributed XGBoost; asymmetric Huber in DeepETA.
- **Quantile loss**: `lambda|y-p|` for under- and `(lambda-1)|y-p|` for over-prediction; lambda=0.5 equals MAE. Use for ETA/delivery time where over-estimating hurts conversion (DoorDash moved from MSE to quantile/asymmetric MSE). Two quantiles (0.05, 0.95) give a prediction interval.

**Classification**
- **Cross entropy / log loss** (binary: `-y log p - (1-y) log(1-p)`). Accuracy is not differentiable, so it cannot be a loss.
- **Normalized cross entropy (NCE)** (Facebook ad click): `logloss(model) / logloss(background CTR)`; NCE<1 means better than always predicting the average, insensitive to the background CTR. Example: fixed 0.2 predictor with CTR 0.1 has log loss 0.362 (NCE 1.11) while the "fancy" model on CTR 0.5 has 0.655 (NCE 0.945): raw log loss alone misleads.
- **Focal loss** `-(1-p_t)^gamma log(p_t)`: down-weights easy examples, focuses on hard ones under imbalance (gamma=0 -> cross entropy); object detection; Amazon package-size experiments.
- **Hinge loss**: `max(0, 1 - y*f(x))`, also penalizes correct predictions inside the margin; used by Airbnb Aerosolve and Uber Eats (GraphSAGE).

**Forecast metrics**: MAPE (scale-free, undefined at 0 actuals, penalizes over-forecast more so favors under-forecast), SMAPE (bounded 0-200% but unstable near 0).

## Variants and techniques
Weighted loss for imbalance ([[imbalanced-data-and-sampling]]); RMSE for delivery-time (treats under/over equally -> use quantile).

## Trade-offs
Outlier robustness vs smooth gradients (MSE vs MAE vs Huber); symmetric vs asymmetric cost.

## When to use it / when not to
See per-loss notes; do not choose by popularity: tie to the business cost of each error type.

## Appears in
[[ad-click-prediction]], [[fb-news-feed]], [[food-delivery-time-estimation]], [[uber-eta-prediction]]

## See also
[[ml-evaluation-metrics]], [[model-calibration]]

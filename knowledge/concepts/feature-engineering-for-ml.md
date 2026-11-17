---
title: Feature engineering for ML
type: concept
aliases: [feature hashing, one hot encoding, mean encoding, cross features, feature scaling]
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 1 pp. 12-32]
---

# Feature engineering for ML

## Definition
Turning raw data (categorical, numeric, text, location, time) into numeric inputs a model can consume, in a way that is identical in training and serving.

## Why it matters
Sparse, high-cardinality features (user IDs, advertisers, listings, locations) dominate production recommenders and ad models; the encoding choice drives memory, latency and accuracy.

## How it works
- **Numeric features**: min-max normalization to [0,1] or [-1,1]; standardization (mean 0, std 1) for roughly normal data; for power-law data use `log((1+v)/(1+median))`; clip min/max because they are usually outliers. Netflix example: raw timestamps gave +30% offline but the production model always sees a "current" timestamp never seen in training, so it needs frequent retraining.
- **One hot encoding**: for medium cardinality. Problems: tree models ignore very sparse columns; huge dimensionality for thousands/millions of values; must handle unseen values (`pandas.get_dummies` does not remember the mapping, sklearn `OneHotEncoder` does and fits in a Pipeline). Group rare levels into "Other".
- **Mean (target) encoding**: replace a category with the mean of the target (e.g., average income per age). Must be computed on separate data (else label leakage); use additive smoothing or cross-validation. Used at Instacart.
- **Feature hashing (hashing trick)**: `index = hash(value) mod d` (MurmurHash3, CityHash...), fixed dimension, handles unseen values. Trade-off: collisions (small d) vs memory (large d); Booking.com plots hash size vs logloss. Used by Booking, Yahoo, Criteo, ad-tech.
- **Cross features**: conjunction of two categoricals (cardinality c1 x c2), usually hashed; e.g., lat x long = city block, lets a linear model learn non-linear interactions (`x3 = x1*x2`). Deep Cross Network learns them automatically ([[deep-learning-recsys-architectures]]).
- **Embeddings** for high-cardinality entities: see [[embeddings]].

## Variants and techniques
Quick choice (book quiz): low cardinality -> one hot; high cardinality -> embedding or hashing; numeric -> normalization/standardization (+log).

## Trade-offs
| Technique | Pros | Cons |
|---|---|---|
| One hot | simple, interpretable | dimension explosion, bad for trees |
| Mean encoding | one dense column | leakage risk |
| Hashing | fixed size, unseen-safe | collisions |
| Embedding | semantic similarity | needs training data, extra storage |

## When to use it / when not to
Hashing/embeddings when cardinality is thousands or more; one hot for small vocabularies and linear/DL models.

## Appears in
[[ad-click-prediction]], [[airbnb-room-classification]], [[airbnb-search-ranking]], [[food-delivery-time-estimation]], [[linkedin-people-you-may-know]], [[uber-eta-prediction]]

## See also
[[embeddings]], [[training-serving-skew-and-feature-store]], [[imbalanced-data-and-sampling]]

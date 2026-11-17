---
title: Collaborative filtering
type: concept
aliases: [matrix factorization, content-based filtering, WALS]
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 2 pp. 103-108]
---

# Collaborative filtering

## Definition
Recommend items to a user based on the tastes of similar users, using the user-item feedback matrix A (m users x n items).

## Why it matters
Captures taste similarity without hand-crafted item features and widens a user's interests (content-based filtering cannot); inference is fast.

## How it works
**Matrix factorization**: find U (m x d) and V (n x d) with `U V^T ~ A`; row i of U is user i's embedding, row j of V is item j's. Score = dot product. Toy example: two latent categories (children/action) per movie and user.

## Variants and techniques
| Algorithm | Pros | Cons |
|---|---|---|
| SGD | flexible loss, parallelizable | harder with unobserved entries |
| WALS (weighted alternating least squares) | faster convergence, handles unobserved entries, parallelizable | specific loss |
Softmax / two-tower models generalize it and handle unseen features ([[embeddings]]).

## Trade-offs
Cold start for new users/items (use an average user, features, or content-based fallback); does not use side features.

## When to use it / when not to
Candidate generation with enough interaction data; otherwise content-based or two-tower with features.

## Appears in
[[youtube]]

## See also
[[recommendation-system-pipeline]], [[embeddings]]

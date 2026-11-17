---
title: Recommendation system pipeline
type: concept
aliases: [candidate generation, retrieval and ranking, multistage recommender, re-ranking]
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 2 pp. 102-120, ch. 5 pp. 156-168]
---

# Recommendation system pipeline

## Definition
Multistage architecture: **candidate generation** (billions -> hundreds/thousands), **ranking/scoring** (precise model, ~10 items shown), **re-ranking** (filters and business rules).

## Why it matters
Scores for the whole corpus are too expensive; splitting stages lets each scale and be deployed independently (different teams, stacks and scaling needs).

## How it works
- **Candidate generation**: content-based filtering (recommend items similar to those the user liked; scalable, niche-friendly, but does not widen interests), [[collaborative-filtering]], two-tower retrieval ([[embeddings]]). YouTube merges several generators (topic match, co-watch, CF, two-tower). Pinterest: co-occurrence counting with MapReduce on boards, **online random walk** on the pin-board bipartite graph (like PageRank; helps rare pins), session co-occurrence (Pins2Vec). Aim for high recall.
- **Ranking**: point-wise (predict a score/probability per item; most popular), pairwise, list-wise ([[learning-to-rank]]). Usually a binary classifier of click/watch/book likelihood.
- **Re-ranking**: remove disliked/click-bait/political items, boost freshness, enforce diversity and fairness.
  - Freshness: frequent retraining/warm start ([[model-retraining]]), "average" user for new users, models that take features (two-tower), item age as a feature.
  - Diversity: several candidate generators and rankers with different objectives; re-rank by genre/metadata.
  - Fairness: models for under-served groups, more data, track metrics per demographic.
  - Impression discount (LinkedIn PYMK): a plug-in discount factor learned from past impressions so the same unconverted suggestion is not shown forever.

## Variants and techniques
Layered ranking (LinkedIn talent search L1 distributed retrieval+score, L2 refinement with dynamic features from caches); seeds + kNN expansion (Instagram).

## Trade-offs
Two stages add complexity and a recall ceiling set by retrieval; benefits: independent build/deploy/scale, lower memory per service.

## When to use it / when not to
Any large-corpus personalization (video, feed, ads, jobs). Not needed for small catalogs.

## Appears in
[[fb-news-feed]], [[instagram]], [[linkedin-course-recommendation]], [[linkedin-people-you-may-know]], [[linkedin-talent-search]], [[youtube]]

## See also
[[embeddings]], [[approximate-nearest-neighbor-search]], [[ml-model-serving]], [[exploration-exploitation]]

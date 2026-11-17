---
title: Embeddings
type: concept
aliases: [entity embedding, word2vec, item2vec, two-tower model, two tower architecture, store2vec]
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 1 pp. 18-30, 70-71, 84-90]
---

# Embeddings

## Definition
Dense, low-dimensional vectors representing entities (words, users, videos, pins, stores, listings) such that proximity reflects semantic or engagement similarity. One hot/hashing do not preserve such proximity.

## Why it matters
Core building block of retrieval, ranking and similarity search in recommenders and search ([[approximate-nearest-neighbor-search]]).

## How it works
Two ways to train:
1. **Pre-trained, word2vec style** (CBOW: predict the middle item from its neighbors; skip-gram: predict neighbors from one item). Sessions are treated as sentences: Instagram (account sequences in a session), Pinterest Ads/Pins2Vec, DoorDash Store2Vec (stores viewed in the same session; classify whether a pair co-occurs). Best when user intent is strong.
2. **Co-trained**, e.g., **two-tower model**: left tower encodes (user, context), right tower encodes the item; the final layers are the embeddings; score = dot product (or cosine). Framed as multi-class classification with softmax `P(y|x)=e^{s(x,y)}/sum_i e^{s(x,y_i)}` and log-likelihood loss.
   - Huge corpus: sample negatives within each mini-batch (power-law sampling); correct popularity bias with `s_c(x,y)=s(x,y)-log(p_j)`.
   - Use a continuous reward (e.g., watch time) instead of treating all engaged items equally.
   - Both towers must output the same dimension (quiz: 32 vs 64 fails the dot product).
   - LinkedIn: "pyramid" two-tower (layers growing wider), Hadamard product instead of cosine so the model learns its own distance without a fully connected layer (low scoring latency).
   - Visual embeddings: last layer of a CNN (ResNet50, VGG16) fine-tuned on own data (Pinterest).

## Variants and techniques
- **Similarity**: cosine, dot product (favors large norms: popular items dominate; bad init can promote rare items), Euclidean distance (smaller is more similar), Hadamard product.
- **Dimension**: rule of thumb d = D^(1/4) (D = number of categories) or tune as a hyperparameter on a downstream task.
- **Evaluation**: downstream task metrics; t-SNE/UMAP visualization; clustering (k-means, kNN). Engagement-optimized embeddings often show no clear structure.
- **Serving**: precompute and store in key-value storage; LinkedIn does offline serving (versioned user/job subgraphs, embeddings in a feature marketplace) plus nearline (on a new job post, standardize features, run models in parallel, publish to KV + Kafka).
- **New entities**: use low-level features (demographics, history) or hash the ID into buckets; "average" user for matrix factorization.

## Trade-offs
Embeddings add semantic quality but need training data per entity (listing IDs: only millions with few bookings each -> weak embeddings, cold start).

## When to use it / when not to
Use for high-cardinality entities and retrieval; avoid ID embeddings when there is little data per ID.

## Appears in
[[airbnb-search-ranking]], [[chatpdf-rag]], [[instagram]], [[linkedin-course-recommendation]], [[linkedin-talent-search]], [[uber-eta-prediction]], [[youtube]]

## See also
[[feature-engineering-for-ml]], [[recommendation-system-pipeline]], [[collaborative-filtering]], [[approximate-nearest-neighbor-search]]

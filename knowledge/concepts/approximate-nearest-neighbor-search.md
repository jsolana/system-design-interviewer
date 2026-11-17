---
title: Approximate nearest neighbor search
type: concept
aliases: [ANN, FAISS, ScaNN, semantic search, vector search]
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 6, Machine Learning Design Interview (Khang Pham, 2022), ch. 1 pp. 88-89, DDIA 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 4 (pp. 147-150)]
---

# Approximate nearest neighbor search

## Definition
Finding the items whose embeddings are closest to a query embedding among hundreds of millions or billions, trading exactness for speed.

## Why it matters
Backbone of embedding-based retrieval (similar pins, jobs, videos, semantic search).

## How it works
Libraries: Facebook **FAISS** and Google **ScaNN**. Example (Onebar): keyword search via Elasticsearch; semantic search by encoding text with the Universal Sentence Encoder (REST service), building a FAISS index of embeddings, running FAISS as a standalone gRPC service (dockerized). Open questions the book raises: scaling user embeddings in near real time; embeddings for new users.

## Variants and techniques
Seeds + kNN pipelines (Instagram candidate retrieval).

## Trade-offs
Recall vs latency/memory; index must be rebuilt/updated as embeddings change.

## When to use it / when not to
Large corpora with similarity retrieval; small corpora can brute-force.

## Additional detail (DDIA 2nd edition, ch. 4)
- *2nd edition (new section "Vector Embeddings")*: an embedding model (often an LLM, multimodal now) turns text/images into a float vector (often >1,000 dims); similar meaning -> nearby points, measured by **cosine similarity** or **Euclidean distance**. Used for semantic search and RAG. R-trees do not work for high dimensions, so specialized vector indexes are used:
  - **Flat**: stores vectors as is, scans all; exact but slow.
  - **IVF** (inverted file): clusters the space into partitions (centroids); a query checks a number of *probes* (partitions); more probes = more accurate, slower; approximate (neighbors may sit in another partition).
  - **HNSW** (Hierarchical Navigable Small World): multi-layer graph; search starts in the sparse top layer at the nearest node and descends to denser layers following proximity edges; approximate.
- Implemented in Faiss (several IVF/HNSW variants) and PostgreSQL pgvector (both).

## ANN categories (Generative AI System Design Interview, ch. 6)
- Exact (linear) search: O(N x D), too slow for tens of millions of vectors (40M comparisons per query in the RAG example).
- ANN gives sublinear time, e.g. O(log N x D): tree-based (k-d tree, R-trees, Annoy), LSH (hash close points to the same bucket), clustering-based (inter-cluster search against centroids, then intra-cluster search), graph-based (HNSW, hierarchical navigation of a proximity graph).
- Frameworks: Elasticsearch, FAISS (Meta), ScaNN (Google). The RAG chapter picks clustering-based ANN for simplicity.

## Appears in
[[chatpdf-rag]], [[instagram]]

## See also
[[embeddings]], [[recommendation-system-pipeline]], [[full-text-search]]

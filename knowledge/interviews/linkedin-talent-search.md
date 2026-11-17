---
title: LinkedIn Talent Search and Recommendation
type: interview
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 3 pp. 140-143, https://www.linkedin.com/blog/engineering/search/reimagining-linkedins-search-stack]
concepts: [recommendation-system-pipeline, learning-to-rank, embeddings, inverted-index, full-text-search, ml-evaluation-metrics]
difficulty: medium
---

# LinkedIn Talent Search and Recommendation

## Prompt
Help recruiters fill roles: show candidates matching criteria; recruiters send InMail and candidates hopefully accept. Optimize accepted InMail requests.

## Functional requirements
Retrieve and rank candidates for a recruiter query, including fuzzy matches (query "Machine Learning Engineer" should include "Data Scientist").

## Non-functional requirements
Fresh index data (important for ML features); context-aware ranking.

## Estimations
Not covered in the source.

## API
Not covered in the source.

## Data model
Features in three sets: recruiter context, query context, candidate profile. Text embeddings with tri-grams ("machine learning engineer"). Search index: **inverted field** (term -> members) and **forward field** (member -> metadata).

## Architecture (high-level design)
Retrieval stack on Lucene: searchers with the index, broker that fans out queries (aggregator), live-updater that keeps the index near real time. Layered ranking: **L1** retrieval + scoring in a distributed fashion; **L2** refines the shortlist with dynamic features from external caches.

## Deep dives
- Context-aware ranking (searching dentists must not yield software engineers): context as features; pairwise ranking worked better than point-wise.
- Fuzzy matching: fuzzy semantic title-ID match vs co-occurrence graph embedding of profile data (scales better, less maintenance); optionally pairwise two-tower (candidate tower vs recruiter query tower).
- Model: XGBoost (feature interactions, rich complexity) or two-tower with pairwise ranking.
- Metrics: offline P@5, P@25, nDCG; online InMail acceptance rate.

## Trade-offs and decisions
Pairwise vs pointwise; embedding fuzzy match vs maintained taxonomy.

## Related concepts
[[inverted-index]], [[learning-to-rank]], [[recommendation-system-pipeline]], [[embeddings]].

## Follow-up questions
Not covered in the source.

## Variants
<!-- One entry per variant: source + how it differs from the base design -->
- **LinkedIn LLM-based job/people search stack**, source: https://www.linkedin.com/blog/engineering/search/reimagining-linkedins-search-stack. Differs: LLM era design. Query understanding (fine-tuned 1.5-4B model + router to keyword retrieval), dual-tower embedding retrieval with exhaustive GPU vector search over precomputed embeddings, decoder-only SLM cross-encoder ranker (yes/no logits, score caching), auction layer; LLM policy judge (7B teacher distilled to 8B) grading tens of millions of pairs daily. Distillation 7B -> 1.7B -> 0.6B; pruning plus summarization raised throughput from 290 to 2,200 items/s/GPU (NDCG@10 0.9432 -> 0.9218), embedding compression reached 22,000 items/s/GPU at NDCG@10 0.9239.

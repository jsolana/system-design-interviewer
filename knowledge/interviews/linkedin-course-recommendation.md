---
title: LinkedIn Learning Course Recommendation
type: interview
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 1 pp. 36-39, ch. 3 pp. 146-150]
concepts: [recommendation-system-pipeline, imbalanced-data-and-sampling, embeddings, model-retraining, batch-processing, ml-evaluation-metrics, ml-model-serving]
difficulty: medium
---

# LinkedIn Learning Course Recommendation

## Prompt
Recommend courses to learners, initially to acquire new learners with highly relevant courses; later with engagement data (clicks, saves).

## Functional requirements
Per-member ranked course list; cold-start solution before engagement data exists.

## Non-functional requirements
Offline scoring acceptable because course preference changes slowly (reliability, low latency).

## Estimations
Candidate generation selects 500-1,000 courses per member. A single course-data shard sufficed.

## API
Not covered in the source.

## Data model
User skills (profile, self-tagged), course description/tagged skills/transcripts, engagement logs. Features versioned and selected by event date.

## Architecture (high-level design)
- **Cold start via skills**: map learners to skills and courses to skills; rank by relevance.
  - Course -> skill: taxonomist-mapped categories (high precision, low coverage); skill taggers; supervised (course, skill) classifier trained on both (negatives sampled, balanced) with a per-skill semi-supervised variant and skill-correlation graph augmentation. Evaluate with skill coverage and precision/recall vs human labels.
  - Member -> skill: profile free text standardized by a model, plus cohort mapping by title and industry; combined as weighted sum (`profile*w1 + cohort*w2`).
- **Supervised stage**: labels from clicks/impressions/watches across channels; downsample negatives, inject random negatives; distributed training (Spark); daily feature pipeline from logs and DB snapshots; transcript skills embedded.
- **Scoring**: offline; candidates merged from a high-precision taxonomy skill model, a downsampled high-recall learned-skill model and courses similar to previously engaged; MapReduce flow merges candidates, member and course data; course shard replicated across reducers, member data keyed to a random reducer holding the shard; can move to in-memory stream scoring.
- Metrics: AUC, CTR.

## Deep dives
Cold start; label generation ([[imbalanced-data-and-sampling]]); offline scoring pipeline ([[batch-processing]]).

## Trade-offs and decisions
Manual taxonomy (precision) vs learned mapping (coverage); offline scoring (cheap) vs fresh online scoring.

## Related concepts
[[recommendation-system-pipeline]], [[embeddings]], [[model-retraining]].

## Follow-up questions
Not covered in the source.

## Variants
<!-- One entry per variant: source + how it differs from the base design -->

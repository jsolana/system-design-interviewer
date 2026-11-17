---
title: Text generation evaluation metrics
type: concept
aliases: [perplexity, BLEU, ROUGE, METEOR, ExactMatch, CIDEr]
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 2, 3]
---

# Text generation evaluation metrics

## Definition
Offline metrics that score generated text against reference text.

## Why it matters
Generative output has no single ground truth, so metrics compare to references or measure likelihood.

## How it works
- **Perplexity**: exp of the average negative log-likelihood of the correct tokens; lower is better. Measures how well the model predicts the exact token sequence of held-out text.
- **ExactMatch@N**: share of generated N-word suggestions exactly equal to the first N words of the ground truth; compute for several N and average (autocomplete).
- **BLEU**: precision of n-gram overlap with reference(s), geometric mean with weights per n, times a brevity penalty (1 if candidate longer than reference, exponential decay otherwise). Simple, but penalizes correct paraphrases.
- **ROUGE-N**: recall-oriented n-gram overlap; no contextual understanding.
- **METEOR**: combines precision and recall and credits synonyms (WordNet) and stems; better correlation with human judgement, but heavier and depends on linguistic resources per language.

## Variants and techniques
Online counterparts: acceptance rate, usage rate, average completion time, system response time, feedback rate, user ratings, engagement, human evaluation.

## Trade-offs
N-gram metrics are cheap but surface-level; semantic metrics and human review are costlier.

## When to use it / when not to
Use perplexity for language-model quality; BLEU/ROUGE/METEOR for translation and summarization.

## Appears in
[[gmail-smart-compose]], [[google-translate]], [[image-captioning]]

## See also
[[llm-evaluation]], [[ml-evaluation-metrics]]

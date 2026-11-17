---
title: RAG evaluation (context relevance, faithfulness, answer relevance)
type: concept
aliases: [RAG triad, faithfulness, hallucination detection]
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 6]
---

# RAG evaluation

## Definition
Evaluating each part of a RAG pipeline using a triad of query, retrieved context and response.

## Why it matters
Final text quality depends on retrieval and generation together; a single metric hides which part fails.

## How it works
- **Context relevance**: do relevant chunks appear at the top of retrieval results (ranking/retrieval metrics).
- **Faithfulness**: is the response grounded in the retrieved context (no hallucination); checked by human review, automated fact-checking tools, consistency checks across queries.
- **Answer relevance**: completeness and absence of redundancy relative to the query, judged e.g. by another language model.
- **Answer correctness**: similarity to a reference answer using text metrics ([[text-generation-metrics]]).

## Variants and techniques
Online: user feedback, engagement.

## Trade-offs
Automated judges scale but may be wrong; human review is accurate but slow.

## When to use it / when not to
Any RAG or grounded-generation system.

## Appears in
[[chatpdf-rag]]

## See also
[[retrieval-augmented-generation]], [[llm-evaluation]]

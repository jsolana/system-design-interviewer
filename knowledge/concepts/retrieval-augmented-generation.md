---
title: Retrieval-augmented generation (RAG)
type: concept
aliases: [RAG, RAFT, document chunking, vector retrieval, knowledge base chatbot]
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 6]
---

# Retrieval-augmented generation (RAG)

## Definition
Combining a general-purpose LLM with a retrieval system: relevant chunks are fetched from an external knowledge base at inference time and added to the prompt so the answer is grounded in current, private data.

## Why it matters
Lets an LLM answer from company documents, real-time data or user files without retraining, with references to sources.

## How it works
1. **Parse** documents (PDF): rule-based (cheap, brittle across layouts) or AI-based (layout detection with object detection, OCR, structured output of text blocks/tables/images; tools Dedoc, Layout-Parser, Google Document AI).
2. **Chunk**: length-based (with overlap, e.g. 500 chars/200 overlap), regex/sentence-based, or structure-aware (HTML, Markdown, code splitters). Whole documents embed poorly and exceed token limits.
3. **Index**: encode each chunk to an embedding (text encoder: encoder-only Transformer; image encoder aligned to text via a shared space such as CLIP, or via image captioning) and store in a vector index.
4. **Retrieve**: encode query with the same encoder, run [[approximate-nearest-neighbor-search]], return top chunks.
5. **Generate**: LLM with a prompt containing the query and retrieved context ([[prompt-engineering]]), top-p sampling.

Sizing example: 5M pages x (1500 chars / (500-200) per text chunk + 3 images) = about 40M chunks, growing about 20 percent a year; exact search would need 40M comparisons per query.

## Variants and techniques
Compared options for adding knowledge:
| Approach | Pros | Cons |
|---|---|---|
| Finetuning | Customized, accurate | Costly, needs frequent retraining, expertise, lots of data, no references |
| Prompt engineering only | Easy, cheap, flexible | Inconsistent, limited to the LLM's knowledge, context window overflow |
| RAG | Fresh data, contextual, scalable, citations | Two components to build, quality bounded by retrieval |

Retrieval techniques: keyword, full-text search (Elasticsearch), knowledge graph (costly to maintain), vector-based (chosen). **RAFT**: finetune the LLM with labeled relevant (golden) and irrelevant (distractor) documents so it ignores noisy retrieval. Finetune only after tuning retrieval and prompts. Optional query expansion, safety filtering of queries.

## Trade-offs
Retrieval quality caps answer quality; more chunks add latency and cost; ANN trades recall for speed.

## When to use it / when not to
Use for large, evolving private corpora; use plain prompting for small static context; finetune when the model fails despite good retrieval.

## Appears in
[[chatpdf-rag]]

## See also
[[embeddings]], [[approximate-nearest-neighbor-search]], [[prompt-engineering]], [[rag-evaluation]], [[full-text-search]]

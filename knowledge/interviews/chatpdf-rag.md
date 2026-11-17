---
title: ChatPDF / enterprise RAG chatbot
type: interview
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 6]
concepts: [retrieval-augmented-generation, prompt-engineering, rag-evaluation, approximate-nearest-neighbor-search, embeddings, transformer-architecture]
difficulty: medium
---

# ChatPDF / enterprise RAG chatbot

## Prompt
Design a ChatGPT-like system that answers questions over a company's continuously updated document collection (PDFs with text and images).

## Functional requirements
- Answer user prompts using the company knowledge base (text and images).
- Handle a continuously updated document database.
- Provide references to sources.

## Non-functional requirements
- Priority: data handling, architecture and performance; safety discussed but secondary.

## Estimations
About 5M pages, 1,500 characters and 3 images per page; chunk size 500 with 200 overlap gives about 5 text chunks plus 3 image chunks per page: 5M x (1500/(500-200) + 3) = 40M chunks, growing about 20 percent per year.

## API
Not covered in the source.

## Data model
Index table of chunk embeddings (text and images in a shared embedding space) with pointers to source chunks; built after PDF parsing and chunking.

## Architecture (high-level design)
Indexing pipeline: document parsing -> chunking -> text/image encoders (CLIP) -> vector index.
Inference: safety filtering of the query -> query expansion (flow, typos) -> retrieval (CLIP text encoder + ANN search) -> generation (LLM with prompt engineering, CoT, citations, top-p) .

## Deep dives
- Finetuning vs prompt engineering vs RAG: RAG chosen.
- Rule-based vs AI-based PDF parsing (layout detection, OCR).
- Chunking strategies; retrieval technique choice (vector-based).
- Text/image alignment: CLIP shared embedding space or image captioning.
- Exact vs ANN search categories; clustering-based ANN.
- RAFT finetuning only if retrieval and prompting are insufficient.
- Prompt design principles and techniques; RAG evaluation triad.

## Trade-offs and decisions
RAG over finetuning (no references, retraining cost) and over pure prompting (context window); vector retrieval over keyword/KG; ANN over exact search.

## Related concepts
[[retrieval-augmented-generation]], [[prompt-engineering]], [[rag-evaluation]], [[approximate-nearest-neighbor-search]], [[embeddings]], [[transformer-architecture]]

## Follow-up questions
The source lists extra topics (end of chapter) such as query expansion details, multimodal retrieval and safety filtering.

## Variants
Not covered in the source.

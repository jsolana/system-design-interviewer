---
title: Prompt engineering
type: concept
aliases: [chain-of-thought, few-shot prompting, role prompting, prompt template, test-time compute]
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 2, 4, 6]
---

# Prompt engineering

## Definition
Designing the input to a general-purpose LLM to steer its output without changing weights.

## Why it matters
Decouples model architecture from input structure: many inputs (subject, recipient, retrieved context, user profile) become one tagged text sequence.

## How it works
Principles: start simple and iterate; break complex tasks into steps; clear action instructions placed first with delimiters; be specific about format/style; tune prompt length.

## Variants and techniques
- Chain-of-thought: intermediate reasoning steps; good for multi-hop questions; extended by exploring multiple reasoning paths; more inference-time compute improves hard tasks (as in OpenAI o1).
- Few-shot: include input/output examples to show format and tone.
- Role prompting: tell the model to act as an expert (lawyer, doctor).
- User-context prompting: include profile/location for personalization.
- RAG prompt: instructions to answer concisely and directly, cite retrieved results by index, admit when unknown, answer in the query's language.

## Trade-offs
Cheap and flexible, but inconsistent and limited by context window and the model's knowledge.

## When to use it / when not to
First lever before finetuning.

## Appears in
[[chatpdf-rag]]

## See also
[[retrieval-augmented-generation]], [[llm-training-stages]]

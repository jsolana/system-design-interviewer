---
title: Transformer architecture for generative models
type: concept
aliases: [attention, self-attention, multi-head attention, decoder-only transformer, encoder-decoder transformer, positional encoding, RoPE, LLM architecture]
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 1, 2, 3, 4]
---

# Transformer architecture for generative models

## Definition
Neural architecture built on the attention mechanism that processes token sequences in parallel; the backbone of LLMs and most GenAI systems.

## Why it matters
Parallelizable (unlike RNN/LSTM) and captures long-range dependencies. Interview answers must justify which variant fits the task.

## How it works
- **Self-attention (scaled dot-product)**: each token embedding is projected into query Q, key K, value V; scores = softmax(QK^T / sqrt(d_k)) applied to V. Multi-head attention runs several heads in parallel and concatenates them. Cost is O(n^2) in sequence length n.
- **Block**: multi-head attention + feed-forward (+ residual, layer norm, dropout); blocks are stacked.
- **Pipeline**: text embedding -> positional encoding -> Transformer blocks -> prediction head (linear + softmax over the vocabulary).
- **Positional encoding** is needed because attention is permutation-invariant.

## Variants and techniques
| Variant | Use | Examples |
|---|---|---|
| Encoder-only | Understanding/classification (sentiment, NER, language detection with average pooling or last-token head) | BERT |
| Decoder-only | Text generation, causal (masked) self-attention | GPT-4, LLaMA, Gemini |
| Encoder-decoder | Input-to-output transformation (translation); decoder has cross-attention over encoder output | T5, BART |

Positional encoding options:
- Fixed (sine-cosine): no extra parameters, handles any length, but may be suboptimal.
- Learned: matrix N x d trained with the model; can be optimal but overfits to seen lengths.
- Relative (T5, DeBERTa): encode distance between tokens; loses simple dot-product form so blocks efficient linear attention.
- **RoPE** (rotary): rotates embeddings by position-dependent angle; encodes absolute and relative position, translation-invariant, generalizes to longer sequences; used by popular LLMs; slightly more math.
- Masking: the encoder attends to all tokens; the decoder only to earlier ones.

## Trade-offs
Quadratic attention cost limits context length (efficient attention variants exist); absolute encodings generalize poorly past trained lengths (a model trained to 512 tokens struggles at 4096).

## When to use it / when not to
Decoder-only for open-ended generation, encoder-decoder for sequence transformation, encoder-only for classification.

## Appears in
[[chatgpt]], [[chatpdf-rag]], [[gmail-smart-compose]], [[google-translate]], [[high-resolution-image-synthesis]], [[image-captioning]], [[text-to-image-generation]], [[text-to-video-generation]]

## See also
[[tokenization]], [[llm-training-stages]], [[text-generation-sampling]], [[embeddings]]

---
title: Tokenization and token indexing
type: concept
aliases: [BPE, byte-pair encoding, subword tokenization, SentencePiece, tokenizer]
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 2 and 3]
---

# Tokenization and token indexing

## Definition
Converting raw text into a sequence of integers a model can consume: first split text into tokens (tokenization), then map each token to an integer ID using a vocabulary built from the training text (token indexing).

## Why it matters
Choice of tokenizer sets vocabulary size, training cost, and ability to handle rare or unseen words and multiple languages.

## How it works
- Clean and normalize text first (remove duplicates, PII such as phone numbers/URLs replaced by placeholders, irrelevant symbols, language filtering).
- Build a vocabulary of unique tokens; token <-> ID lookup table.
- Special tokens: end of sequence, begin of sequence, mask, word-end marker.

## Variants and techniques
| Level | Pros | Cons |
|---|---|---|
| Character | Tiny vocabulary, simple | Tokens carry little meaning; long sequences; lower quality |
| Word | Meaningful tokens | Huge vocabulary (Transformer-XL: 267,735 tokens), out-of-vocabulary words |
| Subword (BPE, SentencePiece) | Manageable vocabulary, rare words decomposed into known pieces, works across languages | More complex to implement |

- **BPE**: start with characters (plus a word-end marker), repeatedly merge the most frequent adjacent pair into a new token until the target vocabulary size is reached. Example corpus cat/cats/dog/dogs merges: do, dog, ca, cat, s</w>. The end marker distinguishes "cat" as a word from "cat" as a prefix.
- GPT-4 uses a BPE variant (Tiktoken library); Gemini uses SentencePiece.
- Modern Transformers skip classical steps (lowercasing, stop-word removal, stemming, punctuation removal) because they hurt meaning; named entities may be replaced by placeholders in translation.

## Trade-offs
Larger vocabulary = shorter sequences but more embedding parameters; smaller = longer sequences.

## When to use it / when not to
Subword tokenization is the default for LLMs and multilingual systems.

## Appears in
[[chatgpt]], [[gmail-smart-compose]], [[google-translate]], [[image-captioning]]

## See also
[[transformer-architecture]], [[embeddings]]

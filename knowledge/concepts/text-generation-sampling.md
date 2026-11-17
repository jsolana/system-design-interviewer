---
title: Text generation sampling methods
type: concept
aliases: [beam search, greedy search, top-k sampling, top-p sampling, nucleus sampling, temperature, decoding strategies]
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 1, 2, 4]
---

# Text generation sampling methods

## Definition
Strategies for selecting the next token from the model's predicted probability distribution when generating output.

## Why it matters
Controls consistency vs diversity, repetition, coherence and latency of generated text.

## How it works
**Deterministic**
- Greedy: always pick the highest-probability token; repetitive and can miss better sequences.
- Beam search: keep the top-k partial sequences by cumulative probability (expand, prune until EOS or max length). Good for short, predictable outputs (autocomplete, translation); limited diversity, costly for long outputs, repeats on open-ended text.

**Stochastic**
- Multinomial: sample from the full distribution; too incoherent.
- Top-k: sample among the k most probable tokens (renormalized); fixed k is bad for sharp or flat distributions.
- Top-p (nucleus): smallest set of tokens whose cumulative probability exceeds p; adapts to the distribution; standard in modern LLMs.

**Modifiers**
- Temperature T scales logits before softmax: T<1 sharper/more deterministic (summarization, translation), T>1 flatter/more creative; T=0 deterministic; practical range about 0.1-1.5 (providers allow 0-2).
- Repetition penalty: stop on repeated n-grams (no_repeat_ngram_size) or frequency penalty on tokens already generated.

## Trade-offs
Deterministic: consistency, predictability, safer suggestions, but low diversity. Stochastic: creativity, but inconsistency and risk of odd output.

## When to use it / when not to
Smart Compose and translation: beam search. Chatbots/creative writing: top-p with temperature.

## Appears in
[[chatgpt]], [[gmail-smart-compose]], [[google-translate]], [[high-resolution-image-synthesis]], [[image-captioning]]

## See also
[[transformer-architecture]], [[llm-training-stages]]

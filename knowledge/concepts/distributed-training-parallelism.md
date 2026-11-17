---
title: Distributed training and efficiency techniques for large models
type: concept
aliases: [data parallelism, tensor parallelism, pipeline parallelism, FSDP, ZeRO, mixed precision, gradient checkpointing, scaling laws]
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 1]
---

# Distributed training and efficiency techniques

## Definition
Techniques to train models too large or slow for one device: parallelism across devices plus memory/compute savings.

## Why it matters
Training large models costs tens of millions of dollars. Rule of thumb from the book: PaLM-2 needed about 10^22 FLOPs; an H100 at about 60 TFLOP/s does about 5.18x10^18 FLOPs/day, so about 5.5 years on one GPU, hence thousands of GPUs. GPT-4 training reportedly exceeded 100 million dollars.

## How it works
- **Data parallelism**: full model copy per device, data split; parameter server aggregates gradients. Synchronous (consistent, waits for stragglers) vs asynchronous (faster, stale parameters).
- **Model parallelism**: *pipeline parallelism* splits layers across devices (activations forward, gradients back); *tensor parallelism* splits operations inside a layer (matrix multiplication column/row-wise).
- **Hybrid** parallelism combines both; ZeRO (Microsoft) and FSDP (Meta) remove redundant memory across devices.
- **Gradient checkpointing**: store only some activations, recompute others in backward pass.
- **Mixed precision / AMP**: 16-bit with 32-bit for critical operations.
- Scaling laws: OpenAI 2020 found performance improves as a power law with model size, data and compute, more than from architecture tweaks; DeepMind 2022 found many LLMs undertrained, data should scale with model size. FLOPs for a fully connected layer: outputs x (inputs mults + inputs-1.. adds), book example 3 x (4+3) = 21.

## Variants and techniques
Capacity measured by parameters (e.g. GPT-3 175B, Llama 3 405B, PaLM 540B) and FLOP count.

## Trade-offs
Sync vs async consistency/speed; memory vs recompute; communication overhead across devices.

## When to use it / when not to
Needed for LLM and video/image diffusion training; discuss briefly in interviews.

## Appears in
[[text-to-image-generation]], [[text-to-video-generation]]

## See also
[[llm-training-stages]], [[horizontal-vs-vertical-scaling]]

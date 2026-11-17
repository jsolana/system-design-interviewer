---
title: High-resolution image synthesis
type: interview
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 8]
concepts: [image-generation-approaches, image-tokenization-vq-vae, transformer-architecture, text-generation-sampling, image-generation-evaluation]
difficulty: high
---

# High-resolution image synthesis

## Prompt
Design a system that generates high-resolution images (unconditional/from tokens) using an autoregressive Transformer.

## Functional requirements
Generate high-resolution, realistic and diverse images. (Detailed requirements dialogue not captured; training set of about 5 million images.)

## Non-functional requirements
Speed in seconds per image; quality and diversity; cost per generation monitored.

## Estimations
- 1024x1024 image, 64x64 pixel chunks = 256 tokens.
- Autoregressive pixel-level is O(N^2) for N x N; diffusion O(T x N) with T denoising steps (high-res diffusion slower, seconds vs longer).

## API
Not covered in the source.

## Data model
Images normalized, resized, then converted by the trained tokenizer into cached discrete token sequences.

## Architecture (high-level design)
- Generation service: runs the image generator (decoder-only Transformer) to produce a token sequence.
- Decoding service: image tokenizer decoder converts tokens to an image; separate from generation so each scales independently (different compute and latency).
- Super-resolution service: pretrained model upscales (e.g. generated 1024 to 2048).

## Deep dives
- Why autoregressive over diffusion for this chapter (chunk-based speed).
- VQ-VAE/VQGAN tokenizer, codebook, losses (reconstruction, quantization, perceptual, adversarial), see [[image-tokenization-vq-vae]].
- Image generator training with next-token prediction; step-by-step autoregressive sampling.
- Evaluation: Inception score, FID, human evaluation; time per image, cost per generation; online user feedback, periodic surveys, subscription rate.

## Trade-offs and decisions
Tokenizer as an independent model; separate decoding/generation services; chunk tokens vs pixels.

## Related concepts
[[image-generation-approaches]], [[image-tokenization-vq-vae]], [[transformer-architecture]], [[text-generation-sampling]], [[image-generation-evaluation]]

## Follow-up questions
Image completion and super-resolution, diversity vs fidelity via temperature, adversarial training stability, progressive growing and multi-scale architectures, interactive refinement.

## Variants
Not covered in the source.

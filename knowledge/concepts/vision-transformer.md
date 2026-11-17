---
title: Vision Transformer and image encoders
type: concept
aliases: [ViT, CNN image encoder, patch embedding, image patches]
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 5, 7, 8]
---

# Vision Transformer and image encoders

## Definition
Encoders that turn an image into embeddings: CNNs (convolution filters producing a feature grid) or Vision Transformers (image split into patches, each flattened and linearly projected to an embedding, plus positional encoding).

## Why it matters
Multimodal GenAI systems need an image encoder to feed a text decoder or diffusion model.

## How it works
- CNN: filters detect edges, textures, objects at multiple scales; output grid (e.g. 3x3xc) is flattened into a sequence of 9 vectors.
- ViT: example 256x256 image cut into patches, flattened, projected to size c, positional encoding added (1D over flattened order or 2D row/column; learnable or fixed; ViT uses learnable 1D), then Transformer blocks.

## Variants and techniques
Encoder output as one token (global, simple, generic) vs a sequence of tokens (local + global, works with attention).

## Trade-offs
CNNs capture local patterns efficiently but struggle with long-range dependencies; Transformers model local and global relations via self-attention at higher cost.

## When to use it / when not to
Prefer ViT when long-range context matters (captioning, generation); reuse pretrained encoders.

## Appears in
[[image-captioning]]

## See also
[[transformer-architecture]], [[embeddings]]

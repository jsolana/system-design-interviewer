---
title: Image tokenization (VQ-VAE / VQGAN)
type: concept
aliases: [VQ-VAE, VQGAN, vector quantization, codebook, image tokenizer, perceptual loss]
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 8, 9]
---

# Image tokenization (VQ-VAE / VQGAN)

## Definition
A separately trained model that converts an image to a short sequence of discrete tokens (and back) so a Transformer can generate images token by token.

## Why it matters
Pixel-by-pixel autoregression is O(N^2) for an N x N image and unparallelizable; chunk tokens cut it drastically (a 1024x1024 image with 64x64 chunks = 256 tokens).

## How it works
- **Encoder**: CNN with ReLU maps the image to a lower-dimensional continuous latent grid.
- **Quantizer**: replaces each continuous vector with the nearest entry of a learnable **codebook** (embedding table of k tokens); discretization avoids posterior collapse and makes sequential prediction tractable.
- **Decoder**: CNN with transposed convolutions reconstructs the image from tokens.
- Gradient through the lookup is approximated by copying decoder-input gradients to the encoder output (straight-through).
- **Losses**: reconstruction (pixel difference), quantization (encoder output vs nearest codebook entry, with stop-gradient), plus for high resolution perceptual loss (features of a pretrained model such as VGG) and adversarial loss (patch-based discriminator, VQGAN); overall = weighted sum of the terms.
- Tokenizer is trained self-supervised (5M images plus public sets such as LAION-400M for a richer codebook); then all training images are tokenized once and cached for the image generator.

## Variants and techniques
Image generator: decoder-only Transformer over token embeddings + positional encoding, next-token prediction + cross-entropy; sampling starts from a random codebook token and iterates (typically top-p / temperature).

## Trade-offs
Bigger codebook = richer detail but harder prediction; tokenizer quality caps final image quality (artifacts at high resolution).

## When to use it / when not to
Autoregressive image or video generation; not needed for pixel-space diffusion.

## Appears in
[[high-resolution-image-synthesis]]

## See also
[[image-generation-approaches]], [[transformer-architecture]], [[latent-diffusion-text-to-image]]

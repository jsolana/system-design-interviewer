---
title: GAN architecture and training
type: concept
aliases: [adversarial training, mode collapse, Wasserstein loss, minimax loss, transposed convolution, StyleGAN]
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 7]
---

# GAN architecture and training

## Definition
A generator and a discriminator trained against each other until the discriminator cannot tell generated from real images.

## Why it matters
GANs give fast, high-quality generation, but training is delicate; interviewers probe the failure modes.

## How it works
- **Generator**: random noise (e.g. 1x1x100) through upsampling blocks of transposed convolution + batch norm + ReLU, last block Tanh (outputs in -1..1 matching normalized pixels). Example: 1x1x100 -> 4x4x1024 -> 8x8x512 ...
- **Discriminator**: strided Conv2D downsampling blocks (BatchNorm, ReLU) + one or two FC layers with sigmoid; binary classifier.
- **Training**: alternate: train discriminator for some steps with the generator frozen, then the generator with the discriminator frozen, to keep them balanced.
- **Losses**: discriminator minimizes binary cross-entropy; generator minimizes log(1 - D(G(z))) in the minimax formulation, which is modified to maximize log D(G(z)) to avoid stalled gradients.
- Normalization layers: batch, layer, instance, group norm (group norm for tiny batches).
- Sampling: random sampling from a Gaussian latent distribution (diversity) vs truncated sampling (high-probability region, more realism, fewer outliers).
- Data prep: remove low-res/low-quality images, augment (flip, rotate, color), resize (e.g. 1024x1024) and normalize to -1..1, balance demographic attributes using classifiers.

## Variants and techniques
Failure modes and fixes:
- Vanishing gradients (discriminator too strong): modified minimax loss, Wasserstein loss (critic outputs a realness score; WGAN), gradient penalty.
- Mode collapse (generator repeats one plausible output): Wasserstein loss, unrolled GAN.
- Non-convergence (discriminator accuracy approaches 50 percent so feedback becomes useless): normalization, different learning rates for G and D, regularization (weight decay), noise on discriminator inputs.

## Trade-offs
Fast single-pass generation vs unstable training and limited novelty.

## When to use it / when not to
Domain-specific generation with attribute control (faces); not for open-ended text-to-image.

## Appears in
[[realistic-face-generation]]

## See also
[[image-generation-approaches]], [[image-generation-evaluation]]

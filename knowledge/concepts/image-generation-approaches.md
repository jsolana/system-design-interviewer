---
title: Image generation approaches (VAE, GAN, autoregressive, diffusion)
type: concept
aliases: [VAE, GAN, generative adversarial network, autoregressive image generation, diffusion models]
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 7, 9]
---

# Image generation approaches

## Definition
The four main model families for generating images, each with distinct quality, speed, control and training trade-offs.

## Why it matters
Choosing the family is the first modeling decision in any image/video GenAI interview.

## How it works
| Approach | Idea | Pros | Cons |
|---|---|---|---|
| VAE | Encode image to a latent space, decode to reconstruct | Fast, efficient compact representation | Blurry, limited novelty and control |
| GAN | Generator (noise to image) vs discriminator (real or fake), adversarial | High quality, fast sampling, attribute control through latent space | Unstable training (mode collapse, non-convergence), limited control and novelty |
| Autoregressive | Image as a token sequence generated one by one with a Transformer | Detail, stable training, text/multimodal conditioning, novelty (DALL-E, Muse) | Slow sequential generation, huge models, no structured latent space |
| Diffusion | Train a network to predict noise added to images; generate by iterative denoising from noise | Detail, stable training, control, novelty, robust to noise (DALL-E 3) | Slow multi-step generation, huge models, no structured latent space |

## Variants and techniques
- VAE compression is reused in latent diffusion (see [[latent-diffusion-text-to-image]]).
- StyleGAN modifies the generator to control attributes (age, hair, expression).
- Face generation choice: GAN, because the structured latent space allows attribute control and sampling is fast (under a second).

## Trade-offs
Quality and novelty (autoregressive/diffusion) vs speed and attribute control (GAN/VAE).

## When to use it / when not to
GAN for fast, domain-specific generation with attribute editing; diffusion/autoregressive for text-conditioned open-domain images.

## Appears in
[[high-resolution-image-synthesis]], [[realistic-face-generation]], [[text-to-image-generation]]

## See also
[[gan-training]], [[image-generation-evaluation]], [[latent-diffusion-text-to-image]], [[vision-transformer]]

---
title: Image generation evaluation metrics
type: concept
aliases: [Inception score, FID, Frechet Inception distance, KID, CLIPScore, human evaluation images]
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 7, 9, 10, 11]
---

# Image generation evaluation metrics

## Definition
Metrics for the quality and diversity of generated images (and, for conditioned generation, alignment to the prompt).

## Why it matters
No ground-truth image exists for a generation, so distribution-level and learned-model metrics are used.

## How it works
- **Inception score (IS)**: classify generated images with Inception v3; per-image class distribution should be peaked (quality) while the average (marginal) distribution should be near uniform (diversity); IS = exp of the mean KL divergence between them. Higher is better.
- **FID**: extract deep-layer Inception features for real and generated images, compare mean and covariance via the Frechet distance. Lower is better; captures quality and diversity relative to real data.
- **KID**: kernel variant.
- Weakness: ImageNet-based features can disagree with human judgment; CLIP-based features align better but do not replace humans.
- **Human evaluation**: e.g. pairwise comparison of images from two models ("which looks more photorealistic").
- Online: user feedback (surveys, ratings), latency (request to delivered image), engagement.

## Variants and techniques
Text-conditioned generation adds prompt-image alignment metrics (see [[latent-diffusion-text-to-image]]).

## Trade-offs
Automated metrics are cheap but biased; humans are reliable but slow.

## When to use it / when not to
Use FID/IS during development, human and online metrics before launch.

## Appears in
[[high-resolution-image-synthesis]], [[personalized-headshot-generation]], [[realistic-face-generation]], [[text-to-image-generation]], [[text-to-video-generation]]

## See also
[[image-generation-approaches]], [[llm-evaluation]]

---
title: Realistic face generation
type: interview
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 7]
concepts: [image-generation-approaches, gan-training, image-generation-evaluation, model-retraining]
difficulty: medium
---

# Realistic face generation

## Prompt
Design a system that generates realistic images of human faces, for entertainment and content creation (and possibly marketing/VR).

## Functional requirements
- Generate a new realistic face on request (input is random noise).
- Faces only, diverse in ethnicity, age and gender.
- No attribute control initially; optional extension (age, expression, hairstyle).

## Non-functional requirements
- Near real-time, under one second per face.
- Licensed, privacy-compliant training data.

## Estimations
70,000 diverse face images in the training set.

## API
Not covered in the source.

## Data model
Preprocessed image set: low-quality/low-res removed, augmented, resized to 1024x1024, normalized to -1..1, attribute-tagged to balance diversity.

## Architecture (high-level design)
- Face generator service: samples a latent vector and runs the trained GAN; attribute control by adjusting the noise vector using StyleGAN properties.
- Training service: periodic retraining.
- Evaluation service: automatically scores new models on predefined metrics to decide promotion.
- Deployment service: low-downtime rollout and monitoring.

## Deep dives
- Approaches compared (VAE, GAN, autoregressive, diffusion): GAN chosen for fast generation and attribute control.
- GAN architecture (transposed convolutions, normalization, Tanh, discriminator), adversarial alternating training, minimax/modified/Wasserstein losses.
- Challenges: vanishing gradients, mode collapse, non-convergence, with mitigations.
- Sampling: random vs truncated (random chosen for diversity).
- Evaluation: Inception score, FID, human evaluation; online user feedback and latency.

## Trade-offs and decisions
GAN over diffusion (speed, controllability); random over truncated sampling; accept unstable training with mitigations.

## Related concepts
[[image-generation-approaches]], [[gan-training]], [[image-generation-evaluation]], [[model-retraining]]

## Follow-up questions
Stabilizing GAN training (Wasserstein, gradient penalty), conditional GANs for attribute control.

## Variants
Not covered in the source.

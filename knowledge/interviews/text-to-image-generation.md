---
title: Text-to-image generation
type: interview
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 9]
concepts: [latent-diffusion-text-to-image, image-generation-approaches, image-generation-evaluation, generative-ai-system-pipelines, distributed-training-parallelism, transformer-architecture]
difficulty: high
---

# Text-to-image generation

## Prompt
Design a system that generates images from detailed text prompts (like DALL-E 3 or Imagen).

## Functional requirements
- English prompts (architecture extensible to other languages); detailed prompts up to a maximum length.
- Wide range of images: landscapes, portraits, abstract art.
- Fairness (no bias by age, race, gender) and content safety filters.

## Non-functional requirements
- Near real-time: about 10 seconds per image.

## Estimations
About 500 million image-caption pairs from user assets. DALL-E 2 has about 3.5B parameters.

## API
Not covered in the source.

## Data model
Cleaned image-caption pairs: drop small images (under 64x64), dedupe, NSFW filter, drop low-aesthetic images, resize + center crop, normalize; missing/non-English captions regenerated (BLIP-3), poor pairs re-captioned or removed by CLIP score; T5 caption embeddings precomputed and cached.

## Architecture (high-level design)
Pipelines: data, training, evaluation, model optimization, inference. Inference: prompt auto-complete -> prompt safety -> prompt enhancement -> T5 encoder + diffusion model -> harm detection -> super-resolution (e.g. 64 -> 256 -> 1024) -> user.

## Deep dives
- Autoregressive vs diffusion: diffusion chosen for quality and speed/quality flexibility.
- U-Net (cross-attention to text) vs DiT; forward/backward diffusion, noise schedule, MSE loss on noise.
- Sampling: classifier-free guidance, DDIM (1000 to about 20 steps).
- Training challenges: mixed precision, FSDP/DeepSpeed, latent diffusion. Slow inference: parallel sampling, distillation, quantization.
- Evaluation: DrawBench prompts; IS, FID, CLIPScore (CLIP cosine similarity of image and text embeddings); human evaluation of quality (photorealism comparison) and alignment (yes/somewhat/no = 100/50/0). Online: CTR, time on page, conversion, latency, resource use, average cost per user per month.

## Trade-offs and decisions
Diffusion over autoregressive; U-Net chosen for teaching though DiT is promising; super-resolution cascade since diffusion cannot directly generate high resolution cheaply.

## Related concepts
[[latent-diffusion-text-to-image]], [[image-generation-approaches]], [[image-generation-evaluation]], [[generative-ai-system-pipelines]], [[distributed-training-parallelism]], [[transformer-architecture]]

## Follow-up questions
Inpainting/outpainting, multiple aspect ratios (Patch n' Pack), ControlNet and finer control.

## Variants
Not covered in the source.

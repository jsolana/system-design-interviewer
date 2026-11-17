---
title: Text-to-video generation
type: interview
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 11]
concepts: [latent-diffusion-text-to-image, generative-ai-system-pipelines, distributed-training-parallelism, image-generation-evaluation, transformer-architecture]
difficulty: high
---

# Text-to-video generation

## Prompt
Design a system that turns a text description into a five-second 720p (1280x720) video (like Sora or Movie Gen).

## Functional requirements
- Input: descriptive text; output: 5 s, 720p video aligned with text visually and temporally.

## Non-functional requirements
- Efficient training and inference (video is far more costly than images); detailed latency target not captured.

## Estimations
- 100 million (text, video) pairs.
- 5 s at 24 FPS = 120 frames; 720p has about 3.6x the pixels of 512x512.
- Compression of 512x in latent space; cached latents for 100M videos about 200 TB.

## API
Not covered in the source.

## Data model
Clips split to 5 s, resized/cropped to standard size, deduplicated, NSFW-filtered, re-captioned with video captioning models; latents and text embeddings precomputed and cached.

## Architecture (high-level design)
Latent diffusion: video VAE compression network (separate) + DiT (or temporal U-Net) diffusion model + text encoder; data and training pipelines like text-to-image; inference adds spatial super-resolution.

## Deep dives
- Latent diffusion model and 512x compression.
- U-Net with temporal attention/convolutions vs DiT with spatio-temporal patchify/unpatchify; DiT chosen (scales better).
- Training: noise prediction with MSE; scarce video data handled by joint image+video training or image pretraining; efficiency: LDM, precomputed latents, spatial super-resolution, distributed (tensor) parallelism.
- Evaluation: FID/IS on frames, Frechet Video Distance (temporal consistency), CLIP video-text similarity averaged over frames, human pairwise comparison; online like text-to-image.

## Trade-offs and decisions
Latent vs pixel diffusion; DiT vs U-Net; image+video joint training in one stage.

## Related concepts
[[latent-diffusion-text-to-image]], [[generative-ai-system-pipelines]], [[distributed-training-parallelism]], [[image-generation-evaluation]], [[transformer-architecture]]

## Follow-up questions
Variable durations/resolutions/aspect ratios, video editing tasks (inpainting, interpolation, stylization), controlling motion level.

## Variants
Not covered in the source.

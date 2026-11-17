---
title: Diffusion models for text-to-image and video (latent diffusion)
type: concept
aliases: [diffusion model, U-Net, DiT, latent diffusion model, LDM, classifier-free guidance, CLIPScore, DDIM, cross-attention conditioning, text-to-video]
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 9, 11]
---

# Diffusion models for text-to-image and video

## Definition
Generative models that learn to reverse a gradual noising process, conditioned on a text prompt and timestep; latent diffusion runs the process in a compressed latent space.

## Why it matters
State of the art for detailed, novel, controllable images and video (Imagen, DALL-E 2/3, Stable Diffusion, Sora, Movie Gen).

## How it works
- **Forward process** (no ML): add Gaussian noise over T steps (about 1000) following a noise schedule beta_t; x_t can be computed directly from x_0 for a random t.
- **Training**: sample t, noise the image, the network predicts the added noise given x_t, the caption embedding (text encoder: CLIP or T5, usually precomputed/cached) and timestep encoding; loss = MSE between true and predicted noise (predicting noise works better than predicting x_0).
- **Backbones**: U-Net (downsampling blocks with Conv2D + BatchNorm + cross-attention to text tokens, symmetric upsampling; queries from image features, keys/values from text embeddings) or DiT (patchify, positional encoding, Transformer, unpatchify; scales better with data/compute).
- **Sampling**: start from Gaussian noise and iteratively denoise. **Classifier-free guidance** (train with and without prompt, amplify the conditioned direction) improves prompt alignment; **DDIM** cuts steps from 1000 to about 20.
- **Latent diffusion (LDM)**: a VAE compression network (trained separately) maps pixels to latents; diffusion runs there; the decoder reconstructs the output. For video, compressing time and space can give about 512x smaller representations (training about 512x cheaper); precompute and cache latents (about 200 TB for 100M videos in the example).
- **Video extensions**: U-Net gains temporal attention and temporal (3D) convolution layers interleaved with spatial ones; DiT patchify works on spatio-temporal patches. Little video data, so train on images and videos together (image = 1-frame video) or pretrain on images.
- **Super-resolution cascade**: base model at low resolution (e.g. 64x64), then SR models to 256 and 1024.

## Variants and techniques
Autoregressive (token-by-token) vs diffusion: autoregressive is simpler/more statistically efficient and fixed cost per sample; diffusion gives better detail and a speed/quality knob (steps).
Training scale (DALL-E 2 about 3.5B parameters): mixed precision, FSDP/DeepSpeed, latent diffusion ([[distributed-training-parallelism]]). Inference speed: parallel sampling, distillation, quantization, fewer steps.

## Trade-offs
Quality and flexibility vs slow multi-step sampling and heavy compute; video adds frames (5 s at 24 FPS = 120 frames; 720p about 3.6x pixels of 512x512).

## When to use it / when not to
Text-conditioned image/video generation; GANs for fast narrow domains.

## Appears in
[[personalized-headshot-generation]], [[text-to-image-generation]], [[text-to-video-generation]]

## See also
[[image-generation-approaches]], [[image-generation-evaluation]], [[image-tokenization-vq-vae]], [[parameter-efficient-finetuning]]

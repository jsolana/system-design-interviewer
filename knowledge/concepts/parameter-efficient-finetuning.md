---
title: Personalization of diffusion models (textual inversion, DreamBooth, LoRA)
type: concept
aliases: [LoRA, DreamBooth, textual inversion, tuning-free personalization, low-rank adaptation, prior preservation loss]
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 10, 6]
---

# Personalization of diffusion models and parameter-efficient finetuning

## Definition
Adapting a pretrained text-to-image model to a specific subject (identity) using a few reference images.

## Why it matters
Enables personalized outputs (e.g. headshots) without training from scratch.

## How it works
Tuning-free (e.g. Meta Imagine Yourself): train once with a visual encoder; one reference image at inference; no per-user training, but weaker detail and special adjustments. Tuning-based: finetune per subject, better detail, handles non-face subjects.

| Method | What is trained | Pros | Cons |
|---|---|---|---|
| Textual inversion | New special token embedding only | Efficient, tiny storage, preserves model | Hard to learn details |
| DreamBooth | All diffusion parameters, subject tagged by a rare-token identifier ([V]) | Best identity detail, few images, about 15 min | GBs per subject, heavy GPU, overfitting |
| LoRA | Low-rank matrices: delta W = B x A with rank r, r x (d_in + d_out) parameters instead of d_in x d_out | Fast, low memory, MBs per subject, original weights frozen | Less effective than DreamBooth, slight inference overhead |

- Identifier choice: common words ("special") carry prior meaning; random characters get tokenized into character priors; rare tokens avoid both.
- DreamBooth overfitting is mitigated by a **class-specific prior preservation loss** using generic images of the class (e.g. generated faces); overall loss = alpha x reconstruction (subject) + beta x prior preservation.
- LoRA also used to finetune LLMs.

## Variants and techniques
Personalization evaluation: text alignment (CLIPScore), quality (FID), image alignment with the subject (CLIP image embeddings, DINO/DINOv2 score preferred for fine visual detail, plus facial similarity score for identity).

## Trade-offs
Capacity and fidelity vs storage and compute per user.

## When to use it / when not to
DreamBooth when users pay and a short training wait and no model storage are acceptable; LoRA/textual inversion when storage or cost dominate.

## Appears in
[[personalized-headshot-generation]]

## See also
[[latent-diffusion-text-to-image]], [[llm-training-stages]], [[tokenization]]

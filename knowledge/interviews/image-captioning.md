---
title: Image captioning
type: interview
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 5]
concepts: [transformer-architecture, tokenization, llm-training-stages, text-generation-sampling, text-generation-metrics, vision-transformer]
difficulty: medium
---

# Image captioning

## Prompt
Design a system that generates a short caption describing an image, used to suggest asset names to designers when they upload images.

## Functional requirements
- General everyday images, English captions.
- Captions short but descriptive and clear.
- Skip the suggestion when the image is ambiguous or confidence is low.
- Avoid biased or unsafe captions.

## Non-functional requirements
- Fast but not strictly real-time.
- Images at least a minimum resolution (256x256 used for filtering).
- Fairness and safety.

## Estimations
400 million image-caption pairs, unprocessed (mixed languages, noisy, some with several captions).

## API
Not covered in the source.

## Data model
Training pairs (image, caption). Caption prep: drop non-English, drop duplicates, drop pairs with low CLIP image-text relevance (threshold about 0.25), summarize long captions with an LLM (e.g. Llama), BPE tokenization. Image prep: drop images under 256x256, normalize pixels to 0-1, drop blurry/over/underexposed images (e.g. LAION Aesthetics Predictor), resize preserving aspect ratio (resize shorter side, then center-crop).

## Architecture (high-level design)
Multimodal encoder-decoder: the image is a new "language". Image encoder produces embeddings; text decoder (decoder-only Transformer) generates the caption.
Inference components: image preprocessing -> caption generator (beam search; if cumulative probability below threshold, disable suggestion) -> post-processing (replace biased terms; disable suggestion on offensive words).

## Deep dives
- Encoder output as a single token (simple, generic captions, loses local detail) vs a sequence of tokens (richer, suits attention).
- CNN encoder (grid of features flattened to a sequence; local patterns, weak long-range dependencies) vs [[vision-transformer]] (patches, positional encoding 1D vs 2D, learnable vs fixed; ViT uses learnable 1D). Chose ViT.
- Training: pretrained text decoder (GPT-2/Llama) and pretrained image encoder, then joint training on 400M pairs with next-token prediction and cross-entropy.
- Sampling: beam search for quality, consistency, coherence.
- Offline: CIDEr (TF-IDF vectors, cosine similarity averaged over multiple reference captions; consensus-based, weak semantics e.g. "coffee on the table" vs "table on the coffee"); multiple references per image help training and evaluation.
- Online metrics are secondary: captioning is usually part of a larger system and quality feedback is subjective.

## Trade-offs and decisions
Single vs sequence tokens; CNN vs ViT; reuse pretrained components to avoid pretraining cost; beam search over stochastic sampling.

## Related concepts
[[transformer-architecture]], [[vision-transformer]], [[tokenization]], [[llm-training-stages]], [[text-generation-sampling]], [[text-generation-metrics]]

## Follow-up questions
Visual question answering, multilingual captions, generating and ranking several captions, BLIP-2/BLIP-3 and extra losses.

## Variants
Not covered in the source.

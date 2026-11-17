---
title: Google Translate (language translation)
type: interview
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 3]
concepts: [transformer-architecture, tokenization, llm-training-stages, text-generation-sampling, text-generation-metrics]
difficulty: medium
---

# Google Translate (language translation)

## Prompt
Design a machine translation system for multiple languages.

## Functional requirements
- Four languages: English, Spanish, Korean, French (pairs among them).
- Language auto-detection of the input.
- Inputs up to 1,000 tokens/words.

## Non-functional requirements
- Internet connection assumed; on-device deployment out of scope.
- Real-time translation raised as a question; accuracy prioritized over simplicity in the model choice.

## Estimations
- 300 million translation examples (sentence pairs) across the languages; terabytes of general text per language. Google Translate: 130+ languages, 1B+ users (context).

## API
Not covered in the source.

## Data model
Translation tables per language pair (source token IDs, target token IDs). Preprocessing: drop missing pairs, noisy data (HTML, wrong language), duplicates; replace named entities with placeholders (ENTITY_1...) and restore afterwards. Do not lowercase, remove stop words/punctuation, or stem.

## Architecture (high-level design)
- Language detector: encoder-only Transformer for sequence classification (average pooling or last-token representation into a classification head).
- Translation service: picks the model for the detected source and requested target language, runs beam search, detokenizes.
- Model: encoder-decoder Transformer; encoder (embedding, positional encoding, MHA stack) and decoder with masked self-attention plus cross-attention to encoder output, then prediction head.

## Deep dives
- BPE tokenization worked example (cat/cats/dog/dogs).
- Pretraining with masked language modeling (not next-token, which would let the decoder cheat); data C4, Wikipedia, StackExchange keeping all four languages; or reuse T5/BART.
- Supervised finetuning with next-token + cross-entropy.
- Bilingual per-pair models (accuracy, isolation of issues, costly) vs one multilingual model (simpler; mT5/mBART); chose language-pair models.
- Beam search for accuracy and consistency.
- Offline: BLEU, ROUGE, METEOR; online: user feedback and engagement.

## Trade-offs and decisions
Bilingual vs multilingual; standard attention suffices for 1,000 tokens; MLM for pretraining; beam search over stochastic sampling.

## Related concepts
[[transformer-architecture]], [[tokenization]], [[llm-training-stages]], [[text-generation-sampling]], [[text-generation-metrics]]

## Follow-up questions
Low-resource languages with transfer learning, decoder-only translation, continuous improvement from feedback, on-device efficient inference, WER and other metrics.

## Variants
Not covered in the source.

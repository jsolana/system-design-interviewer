---
title: Gmail Smart Compose
type: interview
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 2]
concepts: [transformer-architecture, tokenization, llm-training-stages, text-generation-sampling, text-generation-metrics, ab-testing]
difficulty: medium
---

# Gmail Smart Compose

## Prompt
Design the Gmail feature that suggests the next few words while a user writes an email.

## Functional requirements
- Suggest a short completion of the text typed so far, only when confident.
- Input limited to the email body (subject/recipient/previous emails as an extension).
- English; no personalization (for simplicity).
- Must not make biased suggestions.

## Non-functional requirements
- Real-time, imperceptible latency (about 100 ms stated).
- Computing cost matters but is optimized later.

## Estimations
- Dataset: about 1 billion email messages.
- Gmail about 1.8 billion users; up to 500 emails sent per user per day.

## API
Not covered in the source.

## Data model
Training data: general text (books, web, social media) for pretraining plus 1B emails for finetuning. Cleaning: language ID, remove confidential data (names, URLs, phone, card numbers replaced by placeholders), remove irrelevant symbols and duplicates, normalize formats. Then subword tokenization (BPE/SentencePiece) and token indexing.

## Architecture (high-level design)
Framing: text generation (input = typed words, output = continuation); decoder-only Transformer.
Components:
1. **Triggering service**: watches keystrokes, activates only when enough context (e.g. "I hope" but not "I") and avoids too-frequent suggestions.
2. **Phrase generator**: beam search yields top-k completions with confidence; filter out too-long suggestions and low-confidence ones; pass the best one on.
3. **Post-processing service**: rule-based bias handling (pronoun replacement, gender-neutral words, flagged sensitive terms, NSFW filter).
Flow: monitor -> trigger -> beam search -> filter -> post-process -> display.

## Deep dives
- Two-stage training: pretrain with next-token prediction + cross-entropy on general data, finetune on emails with the same objective and loss.
- Extra context (subject, recipient, previous emails) merged into one sequence by a prompt template with tags; training with missing fields makes the model robust.
- Positional encoding: fixed sine-cosine chosen for efficiency and generalization.
- Sampling: deterministic beam search preferred (consistency, common phrases, fewer inappropriate outputs, short suggestions).
- Evaluation: offline perplexity and ExactMatch@N; online acceptance rate, usage rate, average completion time, system response time, feedback rate, human evaluation.

## Trade-offs and decisions
- Decoder-only over encoder-only/encoder-decoder (generation task).
- Fixed vs learned positional encoding: fixed.
- Deterministic vs stochastic sampling: deterministic.
- Rule-based post-processing for bias as a cheap safeguard.

## Related concepts
[[transformer-architecture]], [[tokenization]], [[llm-training-stages]], [[text-generation-sampling]], [[text-generation-metrics]], [[ab-testing]]

## Follow-up questions
Multilingual support, additional context, BPE vs SentencePiece details, masked language modeling vs next-token objectives, multi-token prediction.

## Variants
Not covered in the source.

---
title: LLM training stages (pretraining, finetuning, SFT, RLHF)
type: concept
aliases: [pretraining, supervised finetuning, SFT, RLHF, instruction tuning, reward model, transfer learning, alignment]
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 1, 2, 3, 4]
---

# LLM training stages

## Definition
Staged training of a language model: pretraining on huge general data, finetuning on task data, and (for chatbots) alignment with human preferences.

## Why it matters
Training from scratch on task data alone risks overfitting, lacks data and is expensive. Staging reuses the costly general pretraining across tasks.

## How it works
**Two-stage (Smart Compose, translation)**: pretrain on general text (Common Crawl, C4, Wikipedia), then finetune on task data (e.g. 1B emails, 300M sentence pairs). Benefits: adaptability, generalization, fast finetuning, handles data scarcity, regularization, reuse of pretraining cost.

**Three-stage (chatbot)**:
1. *Pretraining*: next-token prediction + cross-entropy on trillions of tokens (Common Crawl, C4, GitHub, Wikipedia, Books, ArXiv, StackExchange; Llama 1 used about 1.4T tokens). Output: base model that only continues text.
2. *SFT / instruction finetuning*: 10k-100k high-quality (prompt, response) demonstrations written by educated labelers; same objective and loss. Output: SFT model.
3. *RLHF*: (a) train a reward model (copy of the SFT model with a scoring head) on (prompt, winning, losing) preference pairs, from human rankings of several sampled responses (ranking is more consistent than scoring), using margin ranking loss; (b) optimize the SFT model with RL (PPO, or DPO) to maximize reward-model score.

**Objectives**: next-token prediction for decoder-only; masked language modeling (MLM) for encoder-decoder pretraining (next-token would let the decoder "cheat" through the encoder); encoder-decoder finetuning is supervised with next-token objective.

Public pretrained models (T5, BART) are often reused to avoid pretraining cost.

## Variants and techniques
Bilingual (one model per language pair: more accurate, easier to debug, costly to maintain) vs multilingual (single model, simpler; mT5, mBART often match bilingual). Multiple inputs (subject, recipient, body) are combined into one sequence with a prompt template.

## Trade-offs
Demonstration data is small but costly (domain experts); RLHF needs human ranking effort.

## When to use it / when not to
Chatbots need all three stages; narrow generation tasks usually only pretrain + finetune.

## Appears in
[[chatgpt]], [[gmail-smart-compose]], [[google-translate]], [[image-captioning]]

## See also
[[transformer-architecture]], [[text-generation-sampling]], [[distributed-training-parallelism]], [[model-retraining]]

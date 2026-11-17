---
title: ChatGPT
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/chatgpt, Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 4]
concepts: [server-sent-events, message-queues, transformer-architecture, tokenization, llm-training-stages, text-generation-sampling, llm-evaluation]
difficulty: high
---

# ChatGPT

> Note: the page is mostly paywalled; the prompt, requirements, scale and deep dive questions are readable.

## Prompt
A conversational product: the user sends natural-language prompts and receives streamed LLM responses; conversations are saved so they can be resumed. The LLM is a black box; the serving system is what gets designed: fast token streaming, scheduling of limited GPUs and cost control as conversations grow. Text only.

## Functional requirements
- Send a prompt in a chat and receive the generated response.
- View past chats and resume them with the prior context in the prompt.
- Out of scope: editing/branching messages, image/audio/video, sharing, custom GPTs/tools/browsing, full-text search over history.

## Non-functional requirements
- Time to first token matters more than total time (several seconds of blank screen looks like a failure).
- GPUs are limited and expensive: allocate compute deliberately.
- Scale: 200M+ DAU, few prompts/user/day.

## Estimations
~20k prompts/s at peak; multi-second responses -> ~120k concurrent streams.

## API
Not covered in the source.

## Data model
Not covered in the source.

## Architecture (high-level design)
Titles only: send a prompt and receive a response; view and resume chats with context across turns.

## Deep dives
Questions only: streaming tokens to the client; keeping the stream alive across reconnections and deploys; routing and scheduling generation across GPU workers; preventing heavy users from monopolizing the fleet and giving paid tiers a better experience; controlling inference cost as conversations grow without the assistant seeming forgetful. Hidden section: canceling a run and reclaiming the GPU.

## Trade-offs and decisions
Not covered in the source.

## Related concepts
[[server-sent-events]], [[message-queues]] (*Note*: indicative).

## Follow-up questions
The five deep dives.

## Variants
- **Model-centric ML design (Aminian & Sheng, ch. 4)**: personal-assistant chatbot (text in/out, context window of at least 4096 tokens, follow-ups within a session, 80,000 instruction/answer examples for personalization) designed as an ML system rather than serving infrastructure.
  - Architecture: decoder-only Transformer with RoPE positional encoding; three-stage training (pretraining, SFT, RLHF with reward model and PPO/DPO), see [[llm-training-stages]].
  - Sampling: top-p with temperature and repetition penalties (beam/greedy repeat on open-ended text), see [[text-generation-sampling]].
  - Evaluation: perplexity plus task and safety benchmarks, human evaluation, online ratings/engagement/conversion/leaderboards, see [[llm-evaluation]].
  - Inference pipeline: input safety filter (harmful prompts) -> prompt enhancer (expand acronyms, fix typos, add context) -> response generator (optionally several candidates ranked) -> output safety filter -> refusal/fallback response generator; a session/chat-history manager feeds prior turns plus the enhanced prompt to the generator.
  - Follow-ups: dialogue state tracking, multi-token prediction, RAG, distillation, domain adaptation, PPO vs DPO vs rejection sampling, chain-of-thought, verifiable justifications.

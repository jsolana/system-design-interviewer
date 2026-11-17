---
title: LLM and GenAI evaluation (benchmarks, safety, human, online)
type: concept
aliases: [LLM benchmarks, MMLU, safety evaluation, human evaluation, chatbot arena]
sources: [Generative AI System Design Interview (Aminian & Sheng, 2024), ch. 1, 4]
---

# LLM and GenAI evaluation

## Definition
Assessing generative models across capabilities, safety and production impact, since a single metric like perplexity does not show skills.

## Why it matters
Generative output is subjective and multi-faceted; interviewers expect offline, online, bias, robustness and human evaluation to be covered.

## How it works
**Task benchmarks**: common-sense (PIQA, SIQA, HellaSwag, WinoGrande, OpenBookQA, CommonsenseQA); world knowledge (TriviaQA, Natural Questions, SQuAD); reading comprehension (SQuAD, QuAC, BoolQ); math (MATH, GSM8K); code (HumanEval, MBPP); composite (MMLU, MMMU, AGIEval, instruction benchmarks).
**Safety**: toxicity (RealToxicityPrompts, ToxiGen, HateCheck), bias (CrowS-Pairs, BOLD), truthfulness (TruthfulQA), privacy/leakage, adversarial robustness (AdvGLUE).
**Human evaluation**: raters score helpfulness and safety; most reliable for nuance.
**Online**: user ratings, engagement (queries, session duration), conversion rate, task completion, retention/churn, leaderboards such as LMSYS Chatbot Arena (crowdsourced pairwise votes).

## Variants and techniques
For image generation see [[image-generation-evaluation]].

## Trade-offs
Benchmarks are automatic but narrow and can leak into training data; human evaluation is accurate but slow and subjective.

## When to use it / when not to
Combine benchmarks pre-launch with online metrics tied to business goals.

## Appears in
[[chatgpt]]

## See also
[[text-generation-metrics]], [[ab-testing]], [[ml-evaluation-metrics]]

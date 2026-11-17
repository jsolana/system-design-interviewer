---
title: Level expectations - ML and GenAI system design interviews
type: level-guide
sources: [Authored guidance synthesized for this knowledge base (not extracted from a single source); calibrate with your target company's leveling guide]
---

# Level expectations: ML and GenAI system design interviews

Note: general calibration guidance, not an official rubric.

| Dimension | Junior/mid | Senior | Staff+ |
|---|---|---|---|
| Problem framing | Turns the product goal into an ML task (classification, ranking...) | Defines business metric, offline metric and online metric and how they relate | Questions whether ML is needed, defines success across product and risk (fairness, safety, cost) |
| Data | Identifies data sources and labels | Handles label quality, imbalance, bias, leakage, feedback loops | Data strategy: collection, governance, privacy, labeling cost |
| Features and model | Reasonable features and a baseline model | Compares models (simple baseline vs deep), embeddings, multi-stage retrieval + ranking | Platform view: shared features/embeddings, reuse across teams |
| Evaluation | Offline metrics (AUC, precision/recall) | Calibration, A/B tests, guardrail metrics, offline-online gap | Experimentation platform, long-term effects, interference |
| Serving and operations | Mentions batch vs real-time | Latency budget, caching, ANN search, retraining cadence, drift monitoring, training-serving skew | Cost per prediction, rollout/rollback of models, on-call and incident process for models |
| GenAI specifics | Prompting, basic RAG | Retrieval quality, chunking, evaluation of LLM outputs, safety filters, latency/cost of tokens | Model strategy: build vs buy vs fine-tune, eval harness, governance |

Probes: What is your baseline and how will you know the model beat it? What happens when data drifts? How do you detect a silent failure? What is the cost per request at 10x traffic? How do you evaluate quality without labels?

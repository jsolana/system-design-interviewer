---
title: LinkedIn People You May Know
type: interview
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 2 pp. 119-120, ch. 3 pp. 144-145]
concepts: [recommendation-system-pipeline, feature-engineering-for-ml, ml-evaluation-metrics]
difficulty: medium
---

# LinkedIn People You May Know

## Prompt
Recommend new connections a member may know, to grow their professional network and engagement.

## Functional requirements
Show top 3-5 suggestions per member; avoid repeatedly showing ignored suggestions.

## Non-functional requirements
Not covered in the source.

## Estimations
Not covered in the source.

## API
Not covered in the source.

## Data model
Member features f_u, f_v and edge features f_uv: number of common friends, common close friends, same school and major, similar skills.

## Architecture (high-level design)
Score a pair: `score(u,v) = P(u,v) * sum_o w(u,o) * V(u,v,o)`, where P = probability u invites v and v accepts; V = value to u on objective o of the connection; w = member's objective weight.
- **Link prediction**: regression `P = lambda(alpha^T f_u + beta^T f_v + f_u^T A f_v + gamma^T f_uv)` (interaction term between member features).
- **Value**: expected marginal weekly interactions if the connection is formed, via GLMs on member, edge and network/activity features.

## Deep dives
**Impression discount** (plug-in, keeps the existing model): from historical impressions learn a discount factor d that maximizes conversion-rate improvement `(new - old)/old`, so unconverted suggestions fade instead of staying at the top.

## Trade-offs and decisions
Plug-in discount vs retraining the model; multi-objective weighting per member.

## Related concepts
[[recommendation-system-pipeline]] (re-ranking), [[feature-engineering-for-ml]].

## Follow-up questions
Not covered in the source.

## Variants
<!-- One entry per variant: source + how it differs from the base design -->

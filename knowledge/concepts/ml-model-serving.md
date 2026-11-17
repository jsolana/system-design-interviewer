---
title: ML model serving and deployment patterns
type: concept
aliases: [aggregator service, model as a service, inference service, autoscaling inference]
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 1 pp. 83-94, ch. 5-8]
---

# ML model serving and deployment patterns

## Definition
How trained models are packaged, routed and scaled to answer online requests within a tight latency budget.

## Why it matters
Typical budgets: feed ranking 50 ms of a 200 ms page, ads 50-100 ms, search ranking 50-100 ms, video recommendations 100-200 ms.

## How it works
- **Aggregator (broker) service**: receives the request, splits a large candidate list (e.g., 50k-100k ads) across a pool of inference workers (by load, round-robin or request parameter), waits and merges; also the LinkedIn search broker pattern.
- **Serving logic / multiple models**: route by candidate type or user cohort; adds complexity and data dilution.
- **Model as a service**: containers (Docker) on Kubernetes; model repo in S3 with timestamps, services pull the latest model periodically; same model per user for consistent experience (item store).
- **Retrieval service separate from ranking service**: different scaling needs and teams.
- **Autoscaling** on demand (requests above threshold, scale down with cool-down; CPU/memory metrics less effective). Needs stateless services, graceful shutdown, similar instance performance; the load balancer is rarely the bottleneck, downstream services are. Kube-proxy can let candidate generation call ranking directly to cut latency.
- **Delivery mode**: offline batch inference when preferences change slowly (Airbnb room classification, LinkedIn course scoring), online for real-time, event-driven with Kafka push for delivery-time updates.

## Variants and techniques
Michelangelo (Uber online prediction); feature store lookups ([[training-serving-skew-and-feature-store]]).

## Trade-offs
Splitting services = independent scaling/release but more hops; batch scoring = cheap and reliable but stale.

## When to use it / when not to
Split stages when scale/latency differ; precompute when inputs change slowly.

## Appears in
[[ad-click-prediction]], [[airbnb-room-classification]], [[airbnb-search-ranking]], [[fb-news-feed]], [[food-delivery-time-estimation]], [[linkedin-course-recommendation]], [[uber-eta-prediction]], [[youtube]]

## See also
[[load-balancer]], [[stateless-architecture]], [[recommendation-system-pipeline]], [[model-retraining]]

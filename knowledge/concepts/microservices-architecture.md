---
title: Microservices architecture
type: concept
aliases: [microservices, service-oriented decomposition, database per service]
sources: [https://martinfowler.com/articles/microservices.html, https://martinfowler.com/articles/microservice-trade-offs.html, https://microservices.io/patterns/microservices.html]
---

# Microservices architecture

## Definition
Structuring one application as a suite of small, independently deployable, loosely coupled services, each running in its own process, organized around business capabilities and owning its data (Fowler/Lewis; microservices.io).

## Why it matters
It trades in-process simplicity for team autonomy and independent deployment; most interview designs implicitly choose a side, so you must justify it.

## How it works
Fowler's nine characteristics: componentization via services; organization around business capabilities (cross-functional teams, "you build it, you run it"); products not projects; smart endpoints and dumb pipes (HTTP/lightweight messaging, not an ESB); decentralized governance; decentralized data management (polyglot persistence, eventual consistency, compensation instead of distributed transactions); infrastructure automation; design for failure; evolutionary design. Microservices.io frames the decision as forces: splitting ("dark energy": simple components, autonomy, fast pipelines, polyglot, segregation by scalability/availability/security) vs grouping ("dark matter": simple and efficient interactions, ACID over eventual consistency, low runtime/design-time coupling).

## Variants and techniques
Distributed operations use collaboration patterns: [[saga]] (commands), API composition / command-side replica / [[cqrs]] (queries), reliable messaging via [[transactional-outbox]], edge via [[api-gateway]], resilience via [[circuit-breaker]]. Migration via [[strangler-fig-migration]].

## Trade-offs
- Benefits (Fowler "trade-offs"): strong module boundaries, independent deployment, technology diversity.
- Costs, the "microservice premium": distribution (slow, failing remote calls), eventual consistency, operational complexity, harder refactoring across boundaries, complexity moves into the connections. Chained synchronous calls compound downtime (the Guardian aims for at most one synchronous call per user request).
- Use when the system is complex enough, domain well understood (wrong boundaries are costly; monolith-first is a common advice), the team is large, and CD/ops maturity exists. If releases must be coordinated it is not really microservices.

## When to use it / when not to
Use for large teams and independently evolving capabilities. A well-modularized monolith is usually better for small teams or unclear domains.

## Appears in
None yet.

## See also
[[saga]], [[cqrs]], [[event-sourcing]], [[service-discovery]], [[api-gateway]], [[strangler-fig-migration]], [[cloud-native-architecture]], [[stateless-architecture]]

## Note: what a senior/staff candidate should say
Do not recommend microservices by default for a first version; say where the service boundaries follow data ownership and team ownership, which operations become distributed (hence sagas/outbox) and what you give up (ACID across services).

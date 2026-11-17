---
title: API gateway
type: concept
aliases: [backend for frontend, BFF, API composition at the edge]
sources: [https://microservices.io/patterns/apigateway.html]
---

# API gateway

## Definition
A single entry point for all clients of a microservices application. It either proxies a request to one service or fans out to several and aggregates the result; the Backends-for-Frontends (BFF) variant gives each client type (web, mobile, third party) its own gateway.

## Why it matters
Fine-grained service APIs would force clients to make many calls per screen (e.g. a product page), over varying network conditions, and to know where instances live and how the app is partitioned.

## How it works
- Routes and aggregates (API composition), translating public web protocols into internal ones.
- Can expose a different API per client, and handle cross-cutting concerns such as authorization/authentication checks.
- Uses service discovery to find instances and [[circuit-breaker]] when calling services.

## Variants and techniques
BFF per client type; single shared gateway; reactive/event-driven implementation (Netty, Reactor, Node.js) for high load.

## Trade-offs
- Benefits: clients shielded from partitioning, fewer round trips (mobile), simpler clients, tailored APIs.
- Drawbacks: one more component to build/deploy/manage; an extra hop (usually insignificant latency); more gateways to maintain with BFF; it is a potential availability bottleneck (the source does not discuss it, points to circuit breaker).

## When to use it / when not to
When many services are behind multiple client types. For a monolith or one client type it is unnecessary.

## Appears in
None yet.

## See also
[[microservices-architecture]], [[proxies]], [[load-balancer]], [[service-discovery]], [[rate-limiting]], [[circuit-breaker]]

## Note: what a senior/staff candidate should say
Draw the gateway first in almost any microservices design, say what lives there (auth, rate limiting, routing, aggregation) and what must not (business logic), and that it must be stateless and horizontally scaled behind a load balancer.

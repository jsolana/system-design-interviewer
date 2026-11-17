---
title: Strangler fig migration
type: concept
aliases: [strangler application, incremental rewrite, gradual replacement]
sources: [https://martinfowler.com/bliki/StranglerFigApplication.html, https://microservices.io/patterns/refactoring/strangler-application.html]
---

# Strangler fig migration

## Definition
Replace a legacy system incrementally by building a new system around it and moving behavior over piece by piece, instead of a big-bang rewrite. Named after the vine that grows around a host tree.

## Why it matters
Big-bang rewrites tend to take long, deliver no value meanwhile, and the scope is hard to pin down (existing behavior is hard to specify and much of it is unwanted).

## How it works
- Fowler (after Cartwright, Horn, Lewis) four activities: understand desired outcomes; break the problem into parts; deliver parts successfully; change the organization so this continues.
- Find **seams**; replace small components first (low risk, early value, learning); build **transitional architecture** so old and new coexist (to be removed later).
- Microservices.io: the strangler app has services reimplementing monolith functionality and services implementing new features; new-feature services show the business the value early.

## Variants and techniques
Typically a routing facade/proxy in front sends each request to old or new implementation, shifting traffic gradually (the routing detail is the usual implementation, not elaborated in the sources).

## Trade-offs
Transitional code is overhead; culture/organization must change or the new system re-creates the old problems (Conway's law); tightly embedded systems remain hard. Benefit: investment and returns become gradual and visible.

## When to use it / when not to
Migrating monolith to services, or moving a datastore/API with live traffic. Not for small systems cheap to rewrite.

## Appears in
None yet.

## See also
[[microservices-architecture]], [[api-gateway]], [[change-data-capture]]

## Note: what a senior/staff candidate should say
Propose a facade for incremental traffic shift, dual-run/shadow comparison, and an explicit end state with rollback at each step; call out data migration as the hard part.

---
title: Multitenancy, tenant sharding and cell-based architecture
type: concept
aliases: [multitenant, cell-based architecture, tenant isolation, per-tenant shard]
sources: [Designing Data-Intensive Applications, 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 7 (pp. 254-255) and ch. 1 (p. 17)]
---

# Multitenancy, tenant sharding and cell-based architecture

## Definition
*2nd edition (new).* In SaaS/cloud services each customer is a tenant with a self-contained dataset. Sharding can assign one shard per tenant (or group small tenants). In a **cell-based architecture** services and storage for a set of tenants are grouped into an independent cell.

## Why it matters
Benefits: resource isolation (a heavy tenant hurts others less), permission isolation (bugs less likely to leak data across tenants), **fault isolation** per cell, per-tenant backup/restore, simple GDPR/CCPA deletion and export, data residency placement, gradual per-tenant schema migrations.

## How it works
Shard by tenant ID (or hash of it); route requests by tenant; optionally replicate the whole stack per cell.

## Variants and techniques
Group small tenants in a shared shard; sub-shard giant tenants.

## Trade-offs
- A tenant must fit on a node, else shard within the tenant.
- Many tiny tenants -> overhead; grouping makes moving tenants between shards a problem.
- Cross-tenant joins and features get harder.

## When to use it / when not to
SaaS with clear tenant boundaries and compliance needs; not when most queries span tenants.

## Appears in
None yet.

## See also
[[database-partitioning]], [[cloud-native-architecture]], [[multi-data-center]], [[shuffle-sharding-and-cell-based-architecture]], [[multi-tenancy-and-fairness]]

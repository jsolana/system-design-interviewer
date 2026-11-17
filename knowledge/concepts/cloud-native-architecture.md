---
title: Cloud-native architecture (separation of storage and compute)
type: concept
aliases: [cloud native, disaggregated storage, separation of storage and compute, multitenant cloud services, cloud vs self-hosting]
sources: [Designing Data-Intensive Applications, 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 1 (pp. 12-19) and ch. 4 (pp. 135-136)]
---

# Cloud-native architecture (separation of storage and compute)

## Definition
*2nd edition (new).* Systems designed from the ground up to build on lower-level cloud services (object storage, etc.) instead of just running self-hosted software on VMs. Key traits: storage and compute are disaggregated, local disks are treated as ephemeral cache, and services are multitenant.

## Why it matters
The book claims cloud-native systems show better performance on the same hardware, faster failure recovery, quick scaling of compute to match load and support for larger datasets.

## How it works
- **Layering**: object stores (S3, Azure Blob, R2) hide the physical machines and replicate data; higher services (Snowflake builds on S3, other services build on Snowflake).
- **Virtual disks** (EBS, persistent disks) emulate a 4 KiB block device over the network: they let classic disk software run in the cloud, but add overhead and make every I/O sensitive to network glitches. Cloud-native services avoid them.
- **Separation of storage and compute**: compute nodes (VMs) hold no durable state; data lives in a storage service with a database-specific API. Similar to shared-disk, but without the NAS/SAN locking and contention problems.
- Object stores suit large files (hundreds of KB to several GB); small values go to a separate service and large blocks with many values go to the object store.
- **Multitenancy**: customers share hardware; better utilization and easier scaling, but needs care for performance and security isolation (see [[multitenancy-and-cell-based-architecture]]).
- Examples (book table): OLTP self-hosted MySQL/PostgreSQL/MongoDB vs cloud-native Aurora, Azure SQL Hyperscale, Spanner; OLAP self-hosted Teradata/ClickHouse/Spark vs Snowflake, BigQuery, Synapse.

## Variants and techniques
- Cloud vs self-hosting trade-offs, operations in the cloud era (capacity planning becomes financial planning; performance optimization becomes cost optimization; quotas matter), microservices and serverless, data residency/sustainability as reasons to distribute.

## Trade-offs
| Pro | Con |
|---|---|
| Less ops work, elasticity for spiky loads (e.g. analytics) | No control: cannot add features, debug internals or wait less during outages |
| Provider expertise | Vendor lock-in (no standard APIs), sanctions/trust/compliance risk |
| Pay only for what is used | Compute-storage data transfer over the network |

## When to use it / when not to
Variable load, no in-house expertise to run the system. Not for very latency-sensitive cases needing hardware control (high-frequency trading) or specialist needs.

## Appears in
None yet.

## See also
[[object-storage]], [[olap-columnar-stores]], [[horizontal-vs-vertical-scaling]], [[scalability-reliability-maintainability]], [[stateless-architecture]]

---
title: Online (zero-downtime) data migration
type: concept
aliases: [live migration, zero-downtime migration, dual writes migration, online resharding]
sources: [https://stripe.dev/blog/how-stripes-document-databases-supported-99.999-uptime-with-zero-downtime-data-migrations, https://shopify.engineering/horizontally-scaling-the-rails-backend-of-shop-app-with-vitess, https://slack.engineering/how-slack-rebuilt-notifications/, https://www.linkedin.com/blog/engineering/infrastructure/introducing-northguard-and-xinfra, https://www.uber.com/es/en/blog/high-performance-search-platform/]
---

# Online (zero-downtime) data migration

## Definition
Moving data (between shards, databases, engines or schemas) while the system keeps serving reads and writes, with a cutover short enough to hide behind normal retries or failovers.

## Why it matters
Resharding, bin-packing, version upgrades and engine swaps are unavoidable at scale; a maintenance window is not an option for payments or messaging.

## How it works
Stripe DocDB's data movement platform (5M+ queries/s, 2,000+ shards, PB of data) uses one primitive in six steps:
1. **Register** the migration in chunk metadata and build target indexes.
2. **Bulk import** a snapshot taken at time T (inserting in index-sorted order gave about 10x write throughput by keeping B-tree writes local).
3. **Async replication** of changes since T via CDC (oplog -> Kafka -> S3), tagged to avoid replication loops; bidirectional so traffic can roll back.
4. **Correctness check** on point-in-time snapshots (no load on live shards).
5. **Traffic switch**: bump a version token on the source so stale requests are rejected, drain replication, update routes; under 2 s, failed requests succeed on retry.
6. **Deregister** and drop source data.

## Variants and techniques
- **Version fencing**: stale routes/tokens fail safely and are retried.
- **Cutover shorter than failover + retry budget** (Stripe).
- **Vitess phases (Shopify Shop app)**: put a VTTablet next to each MySQL as a single-shard keyspace -> split tables into keyspaces with MoveTables -> reshard (about a week) with VDiff verification -> switch replica reads, then primary. Keep old tables renamed rather than dropping (dropping huge tables can stall MySQL 5.7). Replace auto-increment with sequences; enforce "query verifiers" (missing sharding key, cross-shard transaction) in log-only mode first.
- **Read-time migration (Slack notifications)**: interpret legacy values at read time (legacy "Off" = mentions + push disabled) plus backfill a new field, instead of rewriting rows; keeps rollback safe. A disabled-push value must never send push, even on rollback.
- **Dual writes + virtualization (LinkedIn Xinfra, Uber search)**: clients talk to a virtual API; topics migrate across clusters via epochs and dual writes, producers then consumers; Uber dual-writes to the legacy and new search engines at platform level for every entity.

## Trade-offs
- Bidirectional sync and fencing add complexity; custom engine patches (Stripe's MongoDB version gating) raise upgrade cost.
- Eliminating cross-shard transactions before sharding is mandatory because they can partially commit.
- Dual writes add temporary load.

## When to use it / when not to
Use for any stateful system with availability SLOs. For small data and tolerant SLAs a maintenance window is simpler.

## Appears in
[[distributed-message-queue]], [[notification-system]], [[payment-system]], [[twitter-search]]

## See also
[[change-data-capture]], [[database-partitioning]], [[shard-rebalancing]], [[replication]], [[reconciliation]]

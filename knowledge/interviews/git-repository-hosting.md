---
title: Git repository hosting at agent scale (GitHub)
type: interview
sources: [https://github.blog/engineering/architecture-optimization/inside-githubs-new-git-storage-architecture/]
concepts: [consensus, object-storage, storage-compaction, caching, replication, write-ahead-log, database-partitioning]
difficulty: high
---

# Git repository hosting at agent scale (GitHub)

## Prompt
Design the storage layer for a Git host where a single repository may receive thousands of writes per second from parallel automated agents, with CI, deploys and agents multiplying reads. Source: GitHub engineering post "Project Rubicon" (a real-system case study, not an interview prompt).

## Functional requirements
- Push (write packs, update references), fetch/clone (read), maintenance (pack merging, garbage collection).

## Non-functional requirements
- Thousands of writes/s on one repo; multiple writer nodes (pack indexing and connectivity checks are CPU heavy; also fault tolerance).
- Low commit latency (agents block on push); per-reference ordering, linearizable across references when needed.
- Cheap reads when nothing changed; each component scales independently.
- Target: at least two orders of magnitude beyond the next planned increment.

## Estimations
- One repo's daily requests went about 44M -> 181M (March -> May 2026).
- Internal tests: 5,000 concurrent agents, 7,200 pushes/s on one repo, low read latency; Ref-CAS tens of thousands of transactions/s.

## API
Not covered in the source (Git protocol; future: atomic multi-file commit API, event streams).

## Data model
- Immutable, content-addressed Git objects in packs + indexes (Azure Blob Storage); a pack manifest and references in Ref-CAS (pointers only); log sequence number (LSN) per commit = repo version.

## Architecture (high-level design)
- **Spokes**: routing, load balancing, placement, tenant isolation, fairness.
- **Virtual replicas**: disposable compute for reads/writes; local disk is only a cache; correctness never depends on which replica serves.
- **Blob Storage**: durable packs, accelerators, leases, cached fetch responses, ref checkpoints.
- **Ref-CAS**: replicated log of references and manifest; per-reference locking, expected-value check, commit on majority.
- **Compaction nodes**: merge packs and GC offline.
- Write: index pack -> upload to Blob Storage -> one Ref-CAS transaction (manifest + refs). Read: send known version; if current, one comparison; else get refs/pack pointers and pull packs.

## Deep dives
- **Minimize coordination**: objects are immutable so no agreement needed; only small ref updates are ordered.
- **Pre-commit durability** so refs only point to durable objects.
- **Ref log alternatives**: single WAL blob with conditional writes (simple, mid-hundreds writes/s); refs split across segment blobs (higher ceiling, reads check every segment); dedicated replicated log (tens of thousands ops/s, cheap version checks, needs a consensus service) -> chosen.
- **Sharded lease-based compaction** in tiers with verification before publish.

## Trade-offs and decisions
- Only ordered state behind consensus; bulk data in object storage.
- Disposable replicas: easy scaling/failure, cold cache cost (mitigate with sticky routing).
- Reads cheap, writes pay one consensus round trip.
- Extra systems to run (Ref-CAS, compaction fleet). One architecture for all repos, no special-casing hot repos.

## Related concepts
[[consensus]], [[object-storage]], [[storage-compaction]], [[caching]], [[replication]], [[write-ahead-log]], [[database-partitioning]]

## Follow-up questions
Planned: single-object reads, partial replicas, materialized views, global replicas with bounded staleness, scale-to-zero, clone-free agent work.

## Variants
Not covered in the source.

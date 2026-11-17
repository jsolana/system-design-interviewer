---
title: Storage compaction and garbage collection (immutable stores)
type: concept
aliases: [volume compaction, space reclamation]
sources: [https://dropbox.tech/infrastructure/improving-storage-efficiency-in-magic-pocket-our-immutable-blob-store, https://github.blog/engineering/architecture-optimization/inside-githubs-new-git-storage-architecture/]
---

# Storage compaction and garbage collection (immutable stores)

## Definition
In stores where written data is never modified in place, deletes only mark data dead (garbage collection); compaction physically reclaims space by copying live data into new containers and retiring old ones.

## Why it matters
Fragmentation silently raises storage overhead. Dropbox's Magic Pocket (exabyte-scale immutable blob store, trillions of blobs, millions of deletes/day, erasure coded) saw volumes with under 5% live data after a change that lowered write amplification, each still consuming a full fixed-size volume.

## How it works: layered strategies by fill level (Magic Pocket)
- **L1**: pick a highly filled host volume and pack live data from donor volumes into it (reclaims under one volume per run).
- **L2**: group under-filled volumes and use bounded dynamic programming (bytes scaled by a granularity factor, capped source volumes) to nearly fill a new volume; overhead recovered 2-3x faster than L1, 30-50% lower overhead over a week.
- **L3**: stream live blobs from the sparsest volumes into the on-the-fly erasure coder (Live Coder) to form new volumes; every blob gets a new ID and location entry, so it adds metadata load.
- **Dynamic threshold controller** adjusts host eligibility from fleet signals; rate limiting and per-cell locality protect user traffic and cross-DC bandwidth.

## Variants and techniques
- GitHub's new Git storage: sharded, lease-based compaction nodes merge packs in tiers directly against Blob Storage and Ref-CAS (verify outputs hold exactly the input objects, add to manifest, remove inputs in a separate step), keeping load off serving replicas.
- LSM-tree compaction is the same idea at the file level ([[lsm-trees]]).

## Trade-offs
- Denser packing costs compute/memory; aggressive rates risk overloading storage, metadata, network.
- Metadata capacity can be the real constraint; strategies preserving blob IDs within a volume rewrite fewer location entries.
- Threshold too high -> few eligible volumes; too low -> I/O for little space.

## When to use it / when not to
Any append-only/immutable store with deletes. Monitor fill distribution and overhead trends for early warning.

## Appears in
[[git-repository-hosting]], [[s3-object-storage]]

## See also
[[object-storage]], [[erasure-coding]], [[lsm-trees]], [[write-ahead-log]]

---
title: Erasure coding
type: concept
aliases: [erasure code, Reed-Solomon, parity coding]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 9 S3-like Object Storage, pp. 270-276]
---

# Erasure coding

## Definition
Durability technique that splits data into *k* equal-sized fragments, computes *m* parity fragments with a mathematical formula (e.g. Reed-Solomon) and spreads them across different servers/failure domains; the data can be reconstructed from any *k* fragments out of the *k+m*.

## Why it matters
Increases durability with less storage overhead than full replication. In object storage, where disk is the dominant cost, it is worth the complexity.

## How it works
- **(4+2)**: 4 data chunks d1..d4 + 2 parities p1, p2 (e.g. simplified p1 = d1 + 2·d2 - d3 + 4·d4); if d3 and d4 are lost they are solved from d1, d2, p1, p2. Overhead 50% (1 parity for every 2 data).
- **(8+4)**: 12 fragments of the same size in 12 failure domains; tolerates the loss of up to 4 nodes.
- Normal read: you must read from at least *k* nodes (8 in 8+4); a write requires computing the parities before persisting.
- With per-object checksums: if the checksum does not match, read from other failure domains.

## Variants and techniques
**Replication vs erasure coding**
| | Replication (3 copies) | Erasure coding (8+4) |
|---|---|---|
| Durability | ~6 nines (3 copies with annual disk failure rate of 0.81%) | ~11 nines (Backblaze calculation) |
| Storage overhead | 200% | 50% |
| Compute | None | Parity computation |
| Write latency | Lower | Higher (parity before writing) |
| Read | From one replica; no change on failure | From several nodes; on failure it must reconstruct (slower) |

## Trade-offs
Lower cost and higher durability versus more complexity, more CPU and slower reads. Replication is preferred in latency-sensitive applications; erasure coding to minimize storage cost.

## When to use it / when not to
Cold/massive object storage (S3-like). Not when read/write latency is critical or when data node simplicity is the priority.

## Appears in
[[s3-object-storage]]

## See also
[[replication]], [[object-storage]], [[s3-object-storage]], [[multi-data-center]]

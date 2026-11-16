---
title: Vector clocks
type: concept
aliases: [vector clock, versioning, conflict detection]
sources: [System Design Interview (Alex Xu), Vol. 1, ch. 6 (pp. 97-99)]
---

# Vector clocks

## Definition
A `[server, version]` pair associated with a piece of data, `D([S1,v1],[S2,v2],...)`, that makes it possible to tell whether one version precedes, succeeds or conflicts with another.

## Why it matters
With replication and eventual consistency ([[key-value-store]]), concurrent writes on different nodes create divergent versions (v1, v2) with no clear resolution criterion. Each modification is treated as a new immutable version and the vector clock detects the conflict.

## How it works
- When writing D on server Si: increment vi if `[Si, vi]` exists; otherwise, create `[Si, 1]`.
- Example: D1[(Sx,1)] -> D2[(Sx,2)] (descendant of D1, overwrites it) -> D3[(Sx,2),(Sy,1)] and D4[(Sx,2),(Sz,1)] (conflict) -> the client reconciles and D5[(Sx,3),(Sy,1),(Sz,1)] is written.
- **Ancestor (no conflict)**: X is an ancestor of Y if all of Y's counters are >= those of X. **Conflict (siblings)**: if any counter of Y is less than that of X (e.g. [s0,1],[s1,2] vs [s0,2],[s1,1]).

## Variants and techniques
To bound growth, a length threshold is set and the oldest pairs are removed (this may make it harder to determine the descendant relationship; Dynamo says it has not suffered from this in production).

## Trade-offs
Adds complexity to the client (conflict resolution logic) and the pairs can grow quickly.

## When to use it / when not to
AP stores with concurrent writes (Dynamo-style). Unnecessary with single leader or consensus.

## Appears in
[[key-value-store]]

## See also
[[quorum]], [[cap-theorem]], [[replication]]

---
title: Merkle tree
type: concept
aliases: [hash tree, anti-entropy]
sources: [System Design Interview (Alex Xu), Vol. 1, ch. 6 (pp. 102-103)]
---

# Merkle tree

## Definition
Hash tree: each non-leaf node holds the hash of its children; the leaves hold the hash of the values.

## Why it matters
It lets you detect and synchronize inconsistencies between replicas (**anti-entropy** protocol) by transferring only what differs, useful after permanent replica failures.

## How it works
1. Divide the key space into buckets (e.g. 4 for keys 1-12) that act as the leaf level to limit depth.
2. Hash each key in the bucket with uniform hashing.
3. One hash per bucket.
4. Build upward to the root.
To compare two trees: if the roots match, the data is the same; if not, descend through the left/right children until locating the out-of-sync buckets, and synchronize only those.

## Variants and techniques
Realistic example: 1 million buckets for 1,000 million keys (1,000 keys/bucket).

## Trade-offs
The data to synchronize is proportional to the differences, not to the total volume; cost of maintaining the hashes on writes.

## When to use it / when not to
Replica repair in leaderless stores ([[key-value-store]]); complements hinted handoff (temporary failures, see [[quorum]]).

## Appears in
[[key-value-store]]

## See also
[[replication]], [[gossip-protocol]]

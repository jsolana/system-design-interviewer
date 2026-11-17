---
title: Inverted index for pair counting
type: algorithm
aliases: [posting lists, sparse similarity]
sources: [Cracking the Coding Interview, 6th ed., ch. 17 pp. 186-191 / solutions pp. 530-627]
---

# Inverted index for pair counting

## Definition
Map each item to the list of containers (documents) that contain it, then derive pair statistics only from items that actually overlap.

## When to use it
- Sparse overlap: most pairs share nothing and should never be touched.

## How it works
Intersection size of two documents = number of shared words. Build word -> documents; for each word, increment a counter for every pair in its list; similarity = intersection / (|A| + |B| - intersection). Alternative: tag every word with its doc ID and sort by word, then pair up equal runs (slower, sorting). Comparing all pairs by sorted merge costs O(A + B) per pair, which is wasteful when similarity is mostly zero.

## Complexity
Work proportional to the actual overlaps rather than all pairs; worst case same as brute force.

## Common pitfalls
- Empty documents must not be printed.
- Union = |A| + |B| - intersection (do not double count).

## Appears in
[[sparse-similarity]]

## See also
[[hash-table]], [[recursion]]

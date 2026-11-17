---
title: Bidirectional search
type: algorithm
aliases: [two-ended BFS]
sources: [Cracking the Coding Interview 6th ed., ch. 17 Hard (pp. 186-191, solutions pp. 530-627); Cracking the Coding Interview 6th ed., ch. 4 (book pp. 108-109)]
---

# Bidirectional search

## Definition
Run two simultaneous BFS, one from source and one from target, until they collide.

## When to use it
Shortest path between a known source and destination in a graph with high branching factor.

## How it works
With branching factor k and shortest path length d: plain BFS visits O(k^d) nodes; bidirectional visits about 2*k^(d/2), faster by a factor of k^(d/2) (supports paths twice as long).

## Additional detail (CtCI 9.2 and 17.22)
- Alternate one level at a time from each side, keeping a visited map that stores the previous node; when one side reaches a node visited by the other, merge the two half paths. 100 friends per person and path length 4: 100^4 = 100M nodes vs 2 x 100^2 = 20,000.
- Works for word transformation graphs (words one edit apart; grouping words by wildcard patterns like b_ll gives neighbors without trying all 26 letters per position) with cost about O(E^(D/2)) for E neighbors per word and distance D.
- In distributed graphs mark visited with a per-search hash table, not a flag on the node.

## Complexity
O(k^(d/2)) time and space.

## Common pitfalls
Needs a known target and the ability to traverse edges backward from it.

## Appears in
[[word-transformer]]

## See also
[[breadth-first-search]]

---
title: Topological sort
type: algorithm
aliases: [build order, dependency ordering, Kahn's algorithm]
sources: [Cracking the Coding Interview 6th ed., ch. 4 solution 4.7 (book p. 110)]
---

# Topological sort

## Definition
Linear ordering of vertices of a directed acyclic graph so that for every edge (a, b), a comes before b. Impossible if there is a cycle.

## When to use it
Build orders, task scheduling, course prerequisites.

## How it works
- **Kahn (in-degree)**: track incoming-edge count per node; add all zero-in-degree nodes to the order; for each processed node decrement children's counts and add those reaching zero; repeat. If the order has fewer nodes than the graph, there is a cycle.
- **DFS**: DFS each unvisited node with states BLANK/PARTIAL/COMPLETE; after finishing a node's children, push it on the front of the order. Meeting a PARTIAL node means a cycle.
- Isolated nodes (no edges) must still be included.

## Complexity
O(P + D): P projects (nodes), D dependency pairs (edges).

## Common pitfalls
Reversed edge direction; missing nodes that appear in no dependency; no cycle detection.

## Appears in
[[build-order]]

## See also
[[depth-first-search]], [[graph-representations]]

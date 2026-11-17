---
title: Depth-First Search and Flood Fill
type: algorithm
aliases: [DFS, BFS, paint fill, flood fill, connected components]
sources: [Cracking the Coding Interview 6th ed., ch. 17 Hard (pp. 186-191, solutions pp. 530-627); Cracking the Coding Interview 6th ed., ch. 8 Recursion and Dynamic Programming (pp. 130-136, solutions pp. 342-380); Cracking the Coding Interview 6th ed., ch. 4 Trees and Graphs (pp. 107-108, solutions 4.1, 4.7); Cracking the Coding Interview 6th ed., ch. 16 Moderate (pp. 181-185, solutions)]
---

# Depth-First Search and Flood Fill

## Definition
Explore all cells/nodes reachable from a start by recursively visiting neighbors and marking visited ones. Breadth-first search works equally.

## When to use it
Grids with regions: paint fill, pond sizes, islands; reachability.

## How it works
Paint fill: if cell has the original color, set new color and recurse to the 4 neighbors (stop at bounds or different color; return early if new color equals old to avoid infinite loop). Pond sizes: for each unvisited water cell run DFS over 8 neighbors (loop dr,dc in -1..1), marking visited by setting -1 or using a separate visited matrix, collecting each region's size.

## General graph/tree DFS (CtCI ch. 4)
- Visit a node, mark it visited, recurse into each unvisited neighbor; exhaust one branch before the next. Pre-order and other tree traversals are DFS; graphs need the visited check to avoid infinite loops.
- Preferred when visiting every node; simpler than BFS (plain recursion). BFS is better for shortest paths ([[breadth-first-search]]).
- Cycle detection / topological order: three states BLANK, PARTIAL (in progress), COMPLETE; reaching a PARTIAL node means a cycle ([[topological-sort]]).
- Route-between-nodes: DFS or BFS from one node, checking for the other.
- Time O(V+E), recursion depth up to O(V).

## Connected components / equivalence classes (CtCI 17.7)
To group names declared synonymous: build a graph with an edge per synonym pair, then for each unvisited node run a DFS/BFS that sums the counts of its component; each node and edge is touched once, so O(B + P). Alternative: keep each name's set and merge by copying into the larger set (O(N log N) worst case, like merge sort), or union-find.

## Complexity
O(W*H); each cell touched a constant number of times. Do not multiply per-call cost by number of calls (calls get cheaper as regions grow).

## Common pitfalls
Using x/y instead of row/col (matrix[y][x]); infinite recursion without visited marks; deep recursion stack on big grids.

## Appears in
[[baby-names]], [[build-order]], [[paint-fill]], [[paths-with-sum]], [[pond-sizes]], [[route-between-nodes]]

## See also
- [[recursion]]
- [[matrix-traversal]]

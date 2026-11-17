---
title: Pond Sizes
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.19 (p. 184)]
algorithms: [depth-first-search,matrix-traversal]
difficulty: medium
---

# Pond Sizes

## Prompt
A matrix holds heights; 0 is water; ponds are 8-connected water regions. Return all pond sizes.

## Examples
Input rows 0 2 1 0 / 0 1 0 1 / 1 1 0 1 / 0 1 0 1 gives 2, 4, 1.

## Constraints and clarifying questions
Diagonal connectivity.

## Approaches
- Scan; at each unvisited zero run DFS/BFS over 8 neighbors, marking visited (set to -1 or use a visited matrix) and counting size.

## Complexity
O(W*H).

## Edge cases
Out of bounds; do not multiply per-call and call-count bounds.

## Hints
Mark cells visited as you count.

## Related algorithms
- [[depth-first-search]]
- [[matrix-traversal]]

## Variants
Not covered in the source.

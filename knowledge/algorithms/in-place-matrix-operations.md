---
title: In-place matrix operations
type: algorithm
aliases: [matrix rotation, layer-by-layer, reuse first row as markers]
sources: [Cracking the Coding Interview 6th ed., ch. 1 solutions 1.7, 1.8]
---

# In-place matrix operations

## Definition
Techniques for transforming a matrix in O(1) extra space.

## When to use it
Rotate an NxN image, zero rows/columns, spiral/transposition problems.

## How it works
- Rotate 90 degrees by layers: for each layer and offset, do a 4-way swap (top->right->bottom->left->top) saving one element in a temp, so O(1) space.
- Reduce state: only row/column flags are needed, not exact cells. Store flags in the first row/column (remember separately whether they themselves contained zeros), then nullify.

## Complexity
O(N^2) / O(MN) time (optimal: must touch all cells).

## Common pitfalls
Setting zeros while scanning (cascades to the whole matrix); off-by-one in layer indices.

## Appears in
[[rotate-matrix]], [[zero-matrix]]

## See also
[[character-counting]]

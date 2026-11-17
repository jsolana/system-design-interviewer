---
title: Precomputation tables and sweeps
type: algorithm
aliases: [prefix sums, 2D prefix sum, left/right max arrays, lookup tables]
sources: [Cracking the Coding Interview, 6th ed., ch. 17 pp. 186-191 / solutions pp. 530-627]
---

# Precomputation tables and sweeps

## Definition
Spend one or two linear passes to precompute per-index information so each later query is O(1).

## When to use it
- Repeated scans for "max to the left/right", "next occurrence", "sum of rectangle".

## How it works
- Water in a histogram: sweep left-to-right storing left max, right-to-left tracking right max; water above bar i = min(leftMax, rightMax) - height[i] if positive; O(N).
- Max black-bordered square: for each cell precompute the number of consecutive black cells to the right and below (sweep from bottom-right), so validating the four edges of a candidate square is O(1) and the overall search is O(N^3).
- Shortest supersequence: backward sweep per needed value storing the next occurrence; the closure of an index is the max of those; keep only a running min row for O(B) space.
- Submatrix sums: Val(x,y) = Val(x-1,y) + Val(x,y-1) - Val(x-1,y-1) + M[x][y]; area(D) = Val(D) - Val(A u C) - Val(A u B) + Val(A).

## Complexity
Typically O(N) to O(N^2) preprocessing, O(1) per query.

## Common pitfalls
- Merging the sweeps into one may not be faster, only less clear.
- Index off-by-one in 2D prefix sums.

## Appears in
[[max-black-square]], [[max-submatrix]], [[shortest-supersequence]], [[volume-of-histogram]]

## See also
[[dynamic-programming]], [[recursion]]

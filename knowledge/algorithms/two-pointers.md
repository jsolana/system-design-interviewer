---
title: Two Pointers
type: algorithm
aliases: [two-pointer technique, merge from the back]
sources: [Cracking the Coding Interview 6th ed., ch. 17 Hard (pp. 186-191, solutions pp. 530-627); Cracking the Coding Interview 6th ed., ch. 10 Sorting and Searching (pp. 146-151, solutions pp. 396-416); Cracking the Coding Interview 6th ed., ch. 16 Moderate (pp. 181-185, solutions)]
---

# Two Pointers

## Definition
Walk two indices through one or two arrays (often sorted) so each step discards candidates.

## When to use it
Sorted arrays, pair with target sum or difference, merging, smallest difference, staircase search in a sorted matrix.

## How it works
- Sorted merge in place: A has a buffer at the end; fill from the back with the larger of the tails of A and B so nothing is shifted; remaining A elements are already in place.
- Smallest difference between two arrays: sort both; advance the pointer at the smaller value.
- Sum swap: need a-b = (sumA-sumB)/2; with sorted arrays move a if difference too small, else b.
- Pairs with sum: sort, first/last pointers; sum too small -> first++, too big -> last--.
- Sorted matrix (rows and columns ascending): start top-right; if value > x go left, else go down; O(M+N) (versus binary search per row O(M log N)).
- Sub sort: find end of sorted prefix and start of sorted suffix, then shrink them against min and max of the middle.

## Closest positions (CtCI 17.11)
For repeated word-distance queries store word -> sorted positions; walk pointers pA, pB through two position lists, record the gap, then advance the pointer at the smaller value (moving the other can only widen the gap): O(A + B) per query.

## Complexity
Usually O(n) after an O(n log n) sort.

## Common pitfalls
Forgetting duplicates, moving the wrong pointer, not sorting first.

## Appears in
[[common-elements-of-sorted-arrays]], [[one-away]], [[pairs-with-sum]], [[peaks-and-valleys]], [[permutations-of-string-in-longer-string]], [[smallest-difference]], [[sorted-matrix-search]], [[sorted-merge]], [[sub-sort]], [[sum-swap]], [[urlify]], [[word-distance]]

## See also
- [[sorting-algorithms]]
- [[binary-search]]
- [[hash-table]]

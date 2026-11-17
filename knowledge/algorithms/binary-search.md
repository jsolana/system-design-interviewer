---
title: Binary Search
type: algorithm
aliases: [bisection]
sources: [Cracking the Coding Interview 6th ed., ch. 10 Sorting and Searching (pp. 146-151, solutions pp. 396-416)]
---

# Binary Search

## Definition
Search a sorted sequence by comparing the target with the midpoint and discarding half of the range each step.

## When to use it
Sorted (or partially ordered) data; a predicate that is monotonic; a condition that tells which side to keep. Also 'search with unknown size' (exponential back-off) and 'sorted matrix'.

## How it works
Compare x to the middle: smaller -> left half, larger -> right half, repeat until found or subarray empty. Variants from the book:
- Magic index (A[i]==i) in a sorted distinct array: if A[mid] > mid go left, else right, since values must drop at least 1 per index. With duplicates, cannot pick a side: search left range start..min(mid-1, A[mid]) and right range max(mid+1, A[mid])..end.
- Rotated sorted array: one half is always in order; use it to decide where x can be. If left==mid (e.g. 2,2,2,3,4,2), check whether right differs; otherwise search both halves (O(n) with many duplicates).
- Unknown size (Listy returning -1 past the end): double the index 1,2,4,8... until past the end or beyond x, then binary search treating -1 as 'too big'. O(log n).
- Sparse array with empty strings: when mid is empty move to the nearest non-empty neighbor. Worst case O(n), unavoidable.
- Sorted matrix: see [[two-pointers]] staircase search vs divide into quadrants using the sorted diagonal.

## Complexity
O(log n) time, O(1) iterative.

## Common pitfalls
Off-by-one errors (plus/minus ones), mid overflow, ordering assumptions broken by duplicates. Book: easy to understand, hard to implement flawlessly; test thoroughly.

## Appears in
[[common-elements-of-sorted-arrays]], [[count-pairs-with-difference-k]], [[magic-index]], [[search-rotated-array]], [[sorted-matrix-search]], [[sorted-search-no-size]], [[sparse-search]]

## See also
- [[sorting-algorithms]]
- [[binary-search-tree]]

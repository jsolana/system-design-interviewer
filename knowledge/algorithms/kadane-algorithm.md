---
title: Kadane's Algorithm (Maximum Subarray)
type: algorithm
aliases: [max contiguous sum]
sources: [Cracking the Coding Interview 6th ed., ch. 17 Hard (pp. 186-191, solutions pp. 530-627); Cracking the Coding Interview 6th ed., ch. 16 Moderate (pp. 181-185, solutions)]
---

# Kadane's Algorithm (Maximum Subarray)

## Definition
Single pass computing the maximum sum of a contiguous subarray by keeping a running sum and resetting it when it turns negative.

## When to use it
Largest sum contiguous sequence in an array of positive and negative numbers.

## How it works
Insight: never include part of a positive or negative run; a negative running prefix only hurts. Keep sum += a[i]; update maxSum if sum is larger; if sum < 0 reset to 0.

## 2D extension (CtCI 17.24)
Largest-sum submatrix: for each pair of rows (rowStart, rowEnd) sum every column across those rows (incrementally as rowEnd grows) and run the 1-D algorithm over the column sums: O(R^2 C). Brute force is O(N^6); with 2D prefix sums (Val(x,y) = Val(x-1,y) + Val(x,y-1) - Val(x-1,y-1) + M[x][y]) it is O(N^4).

## Complexity
O(n) time, O(1) space.

## Common pitfalls
All-negative array: decide with the interviewer whether the empty sequence (0), the largest element, or an error is returned.

## Appears in
[[contiguous-sequence]], [[max-submatrix]]

## See also
- [[two-pointers]]

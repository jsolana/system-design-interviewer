---
title: Max Submatrix
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.24, solution p. 605]
algorithms: [kadane-algorithm, precomputation-tables]
difficulty: high
---

# Max Submatrix

## Prompt
Given an NxN matrix of positive and negative integers find the submatrix with the largest sum.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Not covered in the source.

## Approaches
1. Brute force over all submatrices with a sum each: O(N^6).
2. Precompute 2D prefix sums so any rectangle sum is O(1): O(N^4).
3. For each pair of rows add the columns between them and run the maximum-subarray algorithm over the column sums: O(R^2 C).

## Complexity
O(R^2 C).

## Edge cases
All negative values.

## Hints
Reduce 2D to 1D by fixing row pairs.

## Related algorithms
[[kadane-algorithm]] [[precomputation-tables]]

## Variants
Not covered in the source.

---
title: Common Elements of Two Sorted Arrays
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. VII Technical Questions / VI Big O (introductory examples), Best Conceivable Runtime (book pp. 73-75)]
algorithms: [two-pointers, hash-table, binary-search, problem-solving-techniques]
difficulty: low
---

# Common Elements of Two Sorted Arrays

## Prompt
Given two sorted, equal-length arrays of distinct elements, count elements in common.

## Examples
- A: 13 27 35 40 49 55 59; B: 17 35 39 40 55 58 60 -> 3

## Constraints and clarifying questions
- Sorted, distinct.

## Approaches
- Brute force: search each A element in B: O(N^2). BCR is O(N) (must touch every element).
- Binary search per element: O(N log N).
- Hash set of B: O(N) time but O(N) space.
- Since sorted, resume each search where the previous left off, i.e. a linear merge-like scan with two pointers: O(N) time, O(1) space.

## Complexity
- O(N) time, O(1) space (meets BCR).

## Edge cases
- Empty arrays, no overlap.

## Hints
Not covered in the source.

## Related algorithms
[[two-pointers]], [[hash-table]], [[binary-search]], [[problem-solving-techniques]]

## Variants
- Shows how BCR guides optimization: once at BCR, optimize space.

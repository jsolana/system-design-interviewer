---
title: Magic Index
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 8 Recursion and Dynamic Programming, problem 8.3 (p. 135, solution pp. 345-347)]
algorithms: [binary-search,recursion]
difficulty: medium
---

# Magic Index

## Prompt
In a sorted array A, a magic index satisfies A[i] = i. Find one. Follow-up: values not distinct.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Distinct sorted integers in the base problem.

## Approaches
- Brute force linear scan O(n).
- Distinct values: binary search. If A[mid] > mid the answer is left (values drop at least 1 per index step left, so they cannot catch up); if A[mid] < mid go right.
- With duplicates you cannot choose a side. Search the left range start..min(mid-1, A[mid]) and the right range max(mid+1, A[mid])..end.

## Complexity
O(log n) distinct; worst case O(n) with duplicates.

## Edge cases
No magic index.

## Hints
Which side can a magic index not be on?

## Related algorithms
- [[binary-search]]
- [[recursion]]

## Variants
Duplicates follow-up described above.

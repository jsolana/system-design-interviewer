---
title: Count Pairs with Difference K
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. VII Technical Questions / VI Big O (introductory examples), BUD example (book p. 67)]
algorithms: [hash-table, problem-solving-techniques, binary-search]
difficulty: low
---

# Count Pairs with Difference K

## Prompt
Given an array of distinct integers, count pairs with difference k.

## Examples
- {1,7,5,9,2,12,3}, k=2 -> 4 pairs: (1,3),(3,5),(5,7),(7,9)

## Constraints and clarifying questions
- Distinct values.

## Approaches
- Brute force: for each element search the rest, O(N^2). Bottleneck: searching for the other side (x+k or x-k).
- Sort + binary search per element: O(N log N), but sorting is now the bottleneck.
- Put all values in a hash set; for each x look up x+k (count each pair once): O(N).

## Complexity
- Hash set O(N) time, O(N) space.

## Edge cases
- k = 0 (no pairs with distinct values), empty array.

## Hints
Not covered in the source.

## Related algorithms
[[hash-table]], [[problem-solving-techniques]], [[binary-search]]

## Variants
- Demonstrates BUD: bottleneck removal.

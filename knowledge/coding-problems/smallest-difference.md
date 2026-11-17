---
title: Smallest Difference
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.6 (p. 181)]
algorithms: [two-pointers,sorting-algorithms]
difficulty: medium
---

# Smallest Difference

## Prompt
Given two integer arrays, find the pair (one from each) with the smallest non-negative difference; return the difference.

## Examples
{1,3,15,11,2} and {23,127,235,19,8} returns 3 (11 and 8).

## Constraints and clarifying questions
Empty arrays return -1.

## Approaches
- Brute force all pairs O(AB).
- Sort both; pointers a and b; update the minimum; advance the pointer at the smaller value.

## Complexity
O(A log A + B log B).

## Edge cases
Empty arrays; zero difference can stop early.

## Hints
Moving the larger only grows the gap.

## Related algorithms
- [[two-pointers]]
- [[sorting-algorithms]]

## Variants
Not covered in the source.

---
title: Sum Swap
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.21 (p. 184)]
algorithms: [hash-table,two-pointers]
difficulty: medium
---

# Sum Swap

## Prompt
Find one value from each of two arrays to swap so the arrays have equal sums.

## Examples
{4,1,2,1,1,2} and {3,6,3,3} gives {1,3}.

## Constraints and clarifying questions
Sum difference must be even.

## Approaches
- Need a - b = (sumA - sumB)/2 (target). If the difference is odd, no answer.
- Brute force O(AB).
- Put B in a hash set; for each a check a - target is in B: O(A+B).
- If sorted, two pointers on the difference.

## Complexity
O(A+B).

## Edge cases
Odd sum difference.

## Hints
Not covered in the source.

## Related algorithms
- [[hash-table]]
- [[two-pointers]]

## Variants
Not covered in the source.

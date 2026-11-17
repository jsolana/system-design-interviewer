---
title: Contiguous Sequence (Maximum Subarray)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.17 (p. 183)]
algorithms: [kadane-algorithm]
difficulty: medium
---

# Contiguous Sequence (Maximum Subarray)

## Prompt
Given integers (positive and negative) find the contiguous sequence with the largest sum; return the sum.

## Examples
{2,-8,3,-2,4,-10} returns 5 ({3,-2,4}).

## Constraints and clarifying questions
Whether empty sequence allowed.

## Approaches
- Reduce to alternating runs; extend only if it increases the total. Keep sum and maxSum; add each element, update max, reset sum to 0 when it goes negative.

## Complexity
O(n) time, O(1) space.

## Edge cases
All negatives: return 0, the largest element, or error (agree with interviewer).

## Hints
Not covered in the source.

## Related algorithms
- [[kadane-algorithm]]

## Variants
Not covered in the source.

---
title: Stack of Boxes
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 8 Recursion and Dynamic Programming, problem 8.13 (p. 136, solution pp. 365-369)]
algorithms: [dynamic-programming,recursion]
difficulty: high
---

# Stack of Boxes

## Prompt
n boxes with width, height, depth, no rotation. A box can sit on another only if strictly smaller in all three dimensions. Return the height of the tallest stack.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Stack height is the sum of the box heights.

## Approaches
- Try each box as the bottom, then recursively the best stack on top of it among smaller boxes. Sort boxes by height descending so you only look forward.
- Memoize the tallest stack with box i at the bottom (stackMap[i]); make cache read and write symmetric.
- Alternative: at each box decide include or skip, returning the better of the two, with the same cache.

## Complexity
O(n^2) with memo; O(2^n)-like without.

## Edge cases
Strictly larger in every dimension; the cached value is valid only if the box can actually go on the current bottom.

## Hints
Sort first.

## Related algorithms
- [[dynamic-programming]]
- [[recursion]]

## Variants
Not covered in the source.

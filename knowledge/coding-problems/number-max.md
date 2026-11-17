---
title: Number Max Without Comparison
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.7 (p. 181)]
algorithms: [bit-manipulation]
difficulty: medium
---

# Number Max Without Comparison

## Prompt
Return the max of two numbers without if-else or comparison operators.

## Examples
Not covered in the source.

## Constraints and clarifying questions
No comparison operators.

## Approaches
- k = 1 if a-b is non-negative (sign bit), result = a*k + b*(1-k).
- a-b can overflow when signs differ; then use the sign of a for k, otherwise the sign of a-b.

## Complexity
O(1).

## Edge cases
Overflow.

## Hints
Not covered in the source.

## Related algorithms
- [[bit-manipulation]]

## Variants
Not covered in the source.

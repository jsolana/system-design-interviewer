---
title: Operations with Only Addition
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.9 (p. 182)]
algorithms: [bit-manipulation]
difficulty: medium
---

# Operations with Only Addition

## Prompt
Implement multiply, subtract and divide for integers using only the add operator.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Do not assume positive operands.

## Approaches
- Subtract a-b = a + negate(b); negate by repeatedly adding the sign until zero (O(k)), or with growing deltas that reset (O((log a)^2)).
- Multiply: add a to itself |b| times, negate if b negative; swap so the smaller count loops.
- Divide: count how many times |b| can be added without exceeding |a|; fix the sign; reject division by zero.

## Complexity
Multiply O(b); divide O(a/b).

## Edge cases
Division by zero; negative numbers.

## Hints
Reuse negate and abs.

## Related algorithms
- [[bit-manipulation]]

## Variants
Not covered in the source.

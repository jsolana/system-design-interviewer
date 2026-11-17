---
title: Calculator
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.26 (p. 185)]
algorithms: [expression-evaluation,stack-and-queue]
difficulty: high
---

# Calculator

## Prompt
Compute the result of an arithmetic expression of positive integers with + - * / and no parentheses.

## Examples
2*3+5/6*3+15 gives 23.5.

## Constraints and clarifying questions
Operator precedence.

## Approaches
- Left-to-right with a 'processing' cluster: apply * and / immediately, fold into the result at + or -.
- Two stacks (numbers, operators): collapse top while the new operator's priority <= top priority; final collapse.

## Complexity
O(N).

## Edge cases
Malformed input.

## Hints
Not covered in the source.

## Related algorithms
- [[expression-evaluation]]
- [[stack-and-queue]]

## Variants
Not covered in the source.

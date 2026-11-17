---
title: Boolean Evaluation (Count Parenthesizations)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 8 Recursion and Dynamic Programming, problem 8.14 (p. 136, solution pp. 369-374)]
algorithms: [dynamic-programming,recursion]
difficulty: high
---

# Boolean Evaluation (Count Parenthesizations)

## Prompt
Given an expression of 0, 1, & | ^ and a desired result, count the ways to fully parenthesize it so it evaluates to the result.

## Examples
countEval('1^0|0|1', false) = 2; countEval('0&0&0&1^1|0', true) = 10.

## Constraints and clarifying questions
Fully parenthesized but not redundantly.

## Approaches
- For each operator position split into left and right; combine counts: AND true = LT*RT; OR true = LT*RT + LF*RT + LT*RF; XOR true = LT*RF + LF*RT. Count of false = total - true where total = (LT+LF)*(RT+RF).
- Same sub-expressions recur, so memoize on (expression, result) in a hash map.

## Complexity
Polynomial with memo; exponential without.

## Edge cases
Single-character base case; empty string returns 0.

## Hints
Compute false by subtraction to shorten code.

## Related algorithms
- [[dynamic-programming]]
- [[recursion]]

## Variants
Not covered in the source.

---
title: Add Without Plus
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.1, solution p. 530]
algorithms: [bit-manipulation]
difficulty: medium
---

# Add Without Plus

## Prompt
Write a function that adds two numbers without using + or any arithmetic operators.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Bits are the only tool left; clarify whether negatives are in scope.

## Approaches
1. Mimic schoolbook addition in binary: compute the sum without carries (a XOR b) and the carries ((a AND b) shifted left by 1).
2. Add those two results the same way (recursion or loop) until the carry is zero.

## Complexity
O(number of bits) iterations.

## Edge cases
Zero operands; negative numbers (two's complement).

## Hints
Think about how addition really works in binary; split "add" from "carry".

## Related algorithms
[[bit-manipulation]]

## Variants
Not covered in the source.

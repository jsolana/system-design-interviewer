---
title: Next Number (same number of 1 bits)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 5 Bit Manipulation, problem 5.4]
algorithms: [bit-manipulation]
difficulty: high
---

# Next Number (same number of 1 bits)

## Prompt
Given a positive integer, find the next smallest and next largest numbers with the same count of 1 bits.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Not covered in the source.

## Approaches
- Brute force: increment/decrement and count ones.
- getNext (bit manipulation): let c0 = trailing zeros, c1 = block of ones right after them, p = c0 + c1. Set bit p to 1, clear all bits below p, then set c1 - 1 ones at the bottom. Arithmetic form: n + (1<<c0) + (1<<(c1-1)) - 1.
- getPrev: c1 = trailing ones, c0 = zero block after them, p = c0 + c1. Clear bits 0..p, then set c1 + 1 ones immediately below position p. Arithmetic form: n - (1<<c1) - (1<<(c0-1)) + 1.

## Complexity
- O(b).

## Edge cases
- No next exists (e.g. 11..100 patterns, all ones, 0).

## Hints
- Flipping a 0 to 1 left of a 1 to 0 increases the number; flip the rightmost non-trailing zero.

## Related algorithms
[[bit-manipulation]]

## Variants


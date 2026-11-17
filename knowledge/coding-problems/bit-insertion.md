---
title: Insertion (insert M into N at bits i..j)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 5 Bit Manipulation, problem 5.1]
algorithms: [bit-manipulation]
difficulty: medium
---

# Insertion (insert M into N at bits i..j)

## Prompt
Given 32-bit N and M and bit positions i and j, insert M into N so M occupies bits j through i. Assume M fits.

## Examples
- N=10000000000, M=10011, i=2, j=6 -> 10001001100

## Constraints and clarifying questions
- Bits j..i have enough room for M.

## Approaches
- 1) Clear bits j..i in N with a mask: left part of ones above j, right part of ones below i, AND them. 2) Shift M left by i. 3) OR them.

## Complexity
- O(1).

## Edge cases
- i=0, j=31 (shift overflow), M longer than the window (invalid).

## Hints
Not covered in the source.

## Related algorithms
[[bit-manipulation]]

## Variants


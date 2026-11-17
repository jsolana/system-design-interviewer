---
title: Debugger: what does ((n & (n-1)) == 0) do?
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 5 Bit Manipulation, problem 5.5]
algorithms: [bit-manipulation]
difficulty: low
---

# Debugger: what does ((n & (n-1)) == 0) do?

## Prompt
Explain what ((n & (n-1)) == 0) does.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Not covered in the source.

## Approaches
- n-1 flips the lowest 1 to 0 and the trailing zeros to 1s; n & (n-1) == 0 means n and n-1 share no 1 bits, so n has a single 1 bit: n is a power of two (or 0).

## Complexity
- O(1).

## Edge cases
- n = 0 returns true.

## Hints
Not covered in the source.

## Related algorithms
[[bit-manipulation]]

## Variants


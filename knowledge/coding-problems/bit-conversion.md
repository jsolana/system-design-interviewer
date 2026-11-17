---
title: Conversion (bits to flip)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 5 Bit Manipulation, problem 5.6]
algorithms: [bit-manipulation]
difficulty: low
---

# Conversion (bits to flip)

## Prompt
Count the bits to flip to convert integer A to integer B.

## Examples
- 29 (11101), 15 (01111) -> 2

## Constraints and clarifying questions
- Not covered in the source.

## Approaches
- XOR A and B; count ones in the result.
- Count ones faster by looping c = c & (c-1) (clears lowest set bit) until 0.

## Complexity
- O(number of set bits).

## Edge cases
- A == B.

## Hints
Not covered in the source.

## Related algorithms
[[bit-manipulation]]

## Variants


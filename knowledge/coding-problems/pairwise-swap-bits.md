---
title: Pairwise Swap (swap odd and even bits)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 5 Bit Manipulation, problem 5.7]
algorithms: [bit-manipulation]
difficulty: low
---

# Pairwise Swap (swap odd and even bits)

## Prompt
Swap odd and even bits of an integer with as few instructions as possible (bit 0 with 1, 2 with 3...).

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- 32-bit assumed; mask changes for 64-bit.

## Approaches
- Mask even bits (0x55555555) and shift left by 1; mask odd bits (0xAAAAAAAA) and logical shift right by 1; OR the two. Five instructions. Use the logical shift so the sign bit gets 0.

## Complexity
- O(1).

## Edge cases
- Negative numbers (use logical shift).

## Hints
Not covered in the source.

## Related algorithms
[[bit-manipulation]]

## Variants


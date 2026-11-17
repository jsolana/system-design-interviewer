---
title: Flip Bit to Win
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 5 Bit Manipulation, problem 5.3]
algorithms: [bit-manipulation]
difficulty: medium
---

# Flip Bit to Win

## Prompt
Flip exactly one bit from 0 to 1 to get the longest possible sequence of 1s; return its length.

## Examples
- 1775 (11011101111) -> 8

## Constraints and clarifying questions
- Not covered in the source.

## Approaches
- Convert to alternating run lengths of 0s and 1s; where a 0-run has length 1 merge adjacent 1-runs: O(b) time/space.
- Optimal: single scan tracking current and previous 1-run length; on a 0, previous = (next bit is 1) ? current : 0; current = 0; track max of previous+current+1. O(b) time, O(1) space (BCR reached).

## Complexity
- O(b) with b bits.

## Edge cases
- All ones, all zeros (answer 1).

## Hints
Not covered in the source.

## Related algorithms
[[bit-manipulation]]

## Variants
- Use b for bit count; avoid ambiguous n.

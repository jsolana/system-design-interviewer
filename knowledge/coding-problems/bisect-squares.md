---
title: Bisect Squares
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.13 (p. 182)]
algorithms: [computational-geometry]
difficulty: medium
---

# Bisect Squares

## Prompt
Given two axis-aligned squares, find a line that cuts both in half.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Line as segment ending on the squares' edges.

## Approaches
- Any line through a square's center bisects it, so use the line through both centers. Extend it to each square's edge (steep slope hits top/bottom at half size in y, shallow slope hits left/right); pick the farthest points as segment ends.

## Complexity
O(1).

## Edge cases
Same center, vertical slope, slope exactly 1.

## Hints
Not covered in the source.

## Related algorithms
- [[computational-geometry]]

## Variants
Not covered in the source.

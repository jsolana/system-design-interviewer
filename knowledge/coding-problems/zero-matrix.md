---
title: Zero Matrix
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 1 Arrays and Strings, problem 1.8]
algorithms: [in-place-matrix-operations]
difficulty: medium
---

# Zero Matrix

## Prompt
In an MxN matrix, if an element is 0 set its entire row and column to 0.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Zeroing while scanning cascades; flag first, nullify later.

## Approaches
- Two boolean arrays (rows with a zero, columns with a zero), then nullify: O(M+N) space.
- O(1) space: use first row and first column as the flag arrays; first record whether the first row/column themselves contain zeros, process the rest, then nullify the first row/column last.

## Complexity
- O(MN) time; O(M+N) or O(1) space.

## Edge cases
- Zero in first row or first column.

## Hints
Not covered in the source.

## Related algorithms
[[in-place-matrix-operations]]

## Variants


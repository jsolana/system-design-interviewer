---
title: Sorted Matrix Search
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 10 Sorting and Searching, problem 10.9 (p. 151, solution pp. 408-410)]
algorithms: [two-pointers,binary-search]
difficulty: medium
---

# Sorted Matrix Search

## Prompt
An MxN matrix has rows and columns sorted ascending; find an element.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Both row and column sortedness.

## Approaches
- Binary search each row: O(M log N).
- Elimination: start at top-right. If value > x move left (column too big); if value < x move down. O(M+N).
- Divide and conquer: binary search the diagonal for the first value > x, then recurse into the lower-left and upper-right quadrants (top-left cannot have it, bottom-right is too big). More code, same idea.

## Complexity
O(M+N) staircase; O(M log N) row search.

## Edge cases
Non-square matrices.

## Hints
Look at the corners of rows and columns.

## Related algorithms
- [[two-pointers]]
- [[binary-search]]

## Variants
Not covered in the source.

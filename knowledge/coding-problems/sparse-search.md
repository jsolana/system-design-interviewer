---
title: Sparse Search
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 10 Sorting and Searching, problem 10.5 (p. 150, solution pp. 401-403)]
algorithms: [binary-search]
difficulty: medium
---

# Sparse Search

## Prompt
A sorted array of strings contains empty strings interspersed. Find a given string.

## Examples
Search 'ball' in {'at','','','','ball','','','car','','','dad','',''} returns 4.

## Constraints and clarifying questions
What to do when asked to find the empty string (error or search).

## Approaches
- Binary search; if mid is empty scan outward to the nearest non-empty string and use it for the comparison, then continue left or right accordingly.

## Complexity
Worst case O(n); cannot be better because all but one element may be empty.

## Edge cases
Searching for ''.

## Hints
Move mid to the closest non-empty element.

## Related algorithms
- [[binary-search]]

## Variants
Not covered in the source.

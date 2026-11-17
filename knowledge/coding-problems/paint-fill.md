---
title: Paint Fill
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 8 Recursion and Dynamic Programming, problem 8.10 (p. 136, solution pp. 360-361)]
algorithms: [depth-first-search,recursion,matrix-traversal]
difficulty: low
---

# Paint Fill

## Prompt
Given a 2D array of colors, a point and a new color, fill the connected region of the original color.

## Examples
Click on a green pixel and fill adjacent green pixels.

## Constraints and clarifying questions
4-neighbor connectivity.

## Approaches
- Recurse to up, down, left and right neighbors that have the old color after recoloring the current pixel. This is DFS on a grid; BFS also works.
- Return immediately if old color == new color, otherwise infinite recursion.

## Complexity
O(pixels).

## Edge cases
Out-of-bounds; same old and new color.

## Hints
Use row/column rather than x/y.

## Related algorithms
- [[depth-first-search]]
- [[recursion]]
- [[matrix-traversal]]

## Variants
Not covered in the source.

---
title: Robot in a Grid
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 8 Recursion and Dynamic Programming, problem 8.2 (p. 134, solution pp. 344-345)]
algorithms: [recursion,dynamic-programming,matrix-traversal]
difficulty: medium
---

# Robot in a Grid

## Prompt
A robot at the top-left of an r x c grid moves only right or down; some cells are off limits. Find a path to the bottom-right.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Return the path or none.

## Approaches
- Work backward from (r,c): a path exists if there is one to (r-1,c) or (r,c-1). Plain recursion is O(2^(r+c)).
- The same cell is reached repeatedly; remember cells (or points) that failed in a set so each is explored once: O(r*c).

## Complexity
O(r*c) time and space with memoization.

## Edge cases
Origin blocked; no path.

## Hints
Look for duplicate work: (r-1,c-1) is reached via two routes.

## Related algorithms
- [[recursion]]
- [[dynamic-programming]]
- [[matrix-traversal]]

## Variants
Not covered in the source.

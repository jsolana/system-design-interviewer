---
title: Langton's Ant
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.22 (p. 185)]
algorithms: [hash-table,matrix-traversal]
difficulty: medium
---

# Langton's Ant

## Prompt
Simulate K moves of Langton's ant on an infinite grid (white: flip, turn right, move; black: flip, turn left, move) and print the board.

## Examples
Not covered in the source.

## Constraints and clarifying questions
You design the grid structure.

## Approaches
- Fixed 2K x 2K array: wasteful and not extensible.
- Resizable array doubling when the ant leaves the edge (shift coordinates for negative growth).
- Set of white cells plus ant position and orientation; track top-left and bottom-right bounds to print.

## Complexity
O(K).

## Edge cases
Printing bounds.

## Hints
Not covered in the source.

## Related algorithms
- [[hash-table]]
- [[matrix-traversal]]

## Variants
Not covered in the source.

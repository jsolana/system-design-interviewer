---
title: Tic Tac Win
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.4 (p. 181)]
algorithms: [matrix-traversal,hash-table]
difficulty: medium
---

# Tic Tac Win

## Prompt
Design an algorithm to check whether someone has won tic-tac-toe.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Called once or many times? Is the last move known? 3x3 or NxN? Prioritize compactness, speed or clarity.

## Approaches
- Many calls: precompute 3^9 (about 20,000) boards keyed by a base-3 integer.
- Last move known: check only its row, column and diagonals.
- 3x3 hard-coded: simple but error-prone indices.
- NxN: nested loops (ugly), or a helper that walks from a start with row/column increments, or an iterator over positions for each of N rows, N columns and 2 diagonals.

## Complexity
O(N) per call with last move; O(N^2) full scan.

## Edge cases
Non-square boards, empty first cell.

## Hints
Discuss design decisions first.

## Related algorithms
- [[matrix-traversal]]
- [[hash-table]]

## Variants
Not covered in the source.

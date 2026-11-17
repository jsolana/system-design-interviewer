---
title: Eight Queens
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 8 Recursion and Dynamic Programming, problem 8.12 (p. 136, solution pp. 363-365)]
algorithms: [backtracking,recursion]
difficulty: medium
---

# Eight Queens

## Prompt
Print all ways of placing 8 queens on an 8x8 board so no two share a row, column or diagonal.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Fixed 8x8.

## Approaches
- One queen per row; try each column in the current row, check validity against placed queens, recurse to the next row; on reaching row 8 record a solution.
- Store only a column-per-row array. Two queens share a diagonal if the column distance equals the row distance.

## Complexity
Pruned search; 92 solutions in total (Note: not stated in the source).

## Edge cases
Check only earlier rows.

## Hints
Place the last queen and enumerate its column.

## Related algorithms
- [[backtracking]]
- [[recursion]]

## Variants
Not covered in the source.

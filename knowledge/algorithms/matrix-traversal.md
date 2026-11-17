---
title: Matrix and Grid Traversal Patterns
type: algorithm
aliases: [grid problems]
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate (pp. 181-185, solutions); Cracking the Coding Interview 6th ed., ch. 8 Recursion and Dynamic Programming (pp. 130-136, solutions pp. 342-380)]
---

# Matrix and Grid Traversal Patterns

## Definition
Systematic ways to walk and check 2D arrays.

## When to use it
Board games, grids, simulations.

## How it works
Use row/column names instead of x/y. Generalize row/column/diagonal checks with a start and (rowDelta,colDelta) iterator. Tic-tac-toe: for repeated queries pre-store all 3^9 boards (base-3 encoding) in a table; if the last move is known check only its row, column and diagonals; for NxN use increment-based checks. Robot in grid: recurse backward from the target and remember failed cells. Infinite grid (Langton's ant): keep a hash set of white cells plus ant position and track min/max bounds for printing, or a doubling resizable array.

## Complexity
Per problem.

## Common pitfalls
Mixing row/column order; not discussing tradeoffs of compact vs clear code.

## Appears in
[[langtons-ant]], [[paint-fill]], [[pond-sizes]], [[robot-in-grid]], [[tic-tac-toe-winner]]

## See also
- [[depth-first-search]]
- [[hash-table]]

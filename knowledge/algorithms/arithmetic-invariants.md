---
title: Arithmetic invariants (sum, sum of squares, product)
type: algorithm
aliases: [missing number math, sum formula]
sources: [Cracking the Coding Interview, 6th ed., ch. 17 pp. 186-191 / solutions pp. 530-627]
---

# Arithmetic invariants (sum, sum of squares, product)

## Definition
Detect missing/changed elements by comparing a cheap aggregate of the actual data with the aggregate of the expected data.

## When to use it
- One or two missing numbers from 1..N in O(N) time and O(1) space.

## How it works
Requirements for the computation: unique per input, reversible, constant time and space per element. One missing: n(n+1)/2 minus the actual sum. Two missing (x, y): the sum difference s = x + y and the sum-of-squares (or product) difference t give a quadratic 2x^2 - 2sx + (s^2 - t) = 0 whose two roots are x and y. Product of 1..n overflows quickly (needs big integers); sums delay overflow; squares are a good second equation.

## Complexity
O(N) time, O(1) space.

## Common pitfalls
- Overflow; discuss with the interviewer.
- Linear second equations do not separate x and y.

## Appears in
[[missing-two]]

## See also
[[recursion]]

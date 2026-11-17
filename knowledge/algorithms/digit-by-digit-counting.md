---
title: Digit-by-digit counting
type: algorithm
aliases: [count digit occurrences in a range]
sources: [Cracking the Coding Interview, 6th ed., ch. 17 pp. 186-191 / solutions pp. 530-627]
---

# Digit-by-digit counting

## Definition
Count how many times a digit appears in 0..n by analyzing each decimal position separately instead of enumerating numbers.

## When to use it
- "Count the 2s between 0 and n" and similar digit-occurrence counts.

## How it works
For digit position d of n: let y be n rounded down to a multiple of 10^(d+1). If the digit at d is less than 2, the count at that position is y/10; if greater than 2, round up instead (round up(n) to 10^(d+1), divided by 10); if equal to 2, the count is round-down/10 plus the remainder to the right (n mod 10^d) plus 1. Sum over all positions.

## Complexity
O(number of digits of n) = O(log n).

## Common pitfalls
- The boundary case digit = 2 (partial range).
- Zero and single-digit inputs; test heavily.

## Appears in
[[count-of-twos]]

## See also
[[recursion]]

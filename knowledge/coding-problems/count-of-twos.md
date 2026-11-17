---
title: Count of 2s
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.6, solution p. 538]
algorithms: [digit-by-digit-counting]
difficulty: high
---

# Count of 2s

## Prompt
Count the number of 2s that appear in all numbers from 0 to n inclusive.

## Examples
n = 25 -> 9 (2, 12, 20, 21, 22 (counts twice), 23, 24, 25).

## Constraints and clarifying questions
n >= 0.

## Approaches
1. Brute force: count 2s in each number, O(n log n); put per-number counting in its own helper.
2. Digit by digit: for each position d, compare the digit with 2 (less, equal, greater) to count 2s at that position using round-down/round-up to a multiple of 10^(d+1) and, for equal, the remainder on the right plus 1.

## Complexity
O(log n) for the digit approach.

## Edge cases
Single digits, numbers with 0 digits, n = 2.

## Hints
Roughly 1/10 of numbers have a 2 in any given position; handle the boundary cases separately.

## Related algorithms
[[digit-by-digit-counting]]

## Variants
Not covered in the source.

---
title: Coins (Number of Ways to Make Change)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 8 Recursion and Dynamic Programming, problem 8.11 (p. 136, solution pp. 361-363)]
algorithms: [dynamic-programming,recursion]
difficulty: medium
---

# Coins (Number of Ways to Make Change)

## Prompt
Given unlimited quarters, dimes, nickels and pennies, count the ways to represent n cents.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Order of coins does not matter (combinations).

## Approaches
- Fix a denomination order. ways(amount, denomIndex) = sum over k coins of the current denomination of ways(amount - k*denom, next index). Last denomination (pennies) contributes 1.
- Repeats the same (amount, index) states; cache in a 2D array [amount][index].

## Complexity
O(n * denominations * n/denom) with memo.

## Edge cases
Counting permutations instead of combinations if the order of coins is not fixed.

## Hints
Use denominations from largest to smallest.

## Related algorithms
- [[dynamic-programming]]
- [[recursion]]

## Variants
Not covered in the source.

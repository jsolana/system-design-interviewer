---
title: Recursive Multiply
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 8 Recursion and Dynamic Programming, problem 8.5 (p. 135, solution pp. 349-351)]
algorithms: [recursion,bit-manipulation,dynamic-programming]
difficulty: medium
---

# Recursive Multiply

## Prompt
Multiply two positive integers without * or /, using add, subtract and shift, minimizing operations.

## Examples
17 x 23.

## Constraints and clarifying questions
Positive ints.

## Approaches
- Think of a x b as counting cells in a grid: count half and double it; when odd, add the other half.
- Naive halving recomputes (minProduct(4,23) appears twice), so memoize on the smaller number.
- Better: for even smaller number, result = 2 * product(smaller/2, bigger); for odd add bigger once. Recursion goes straight down, so no cache needed.

## Complexity
O(log(smaller)).

## Edge cases
Zero and one as base cases; pick the smaller number to recurse on.

## Hints
What does multiplication really mean?

## Related algorithms
- [[recursion]]
- [[bit-manipulation]]
- [[dynamic-programming]]

## Variants
Not covered in the source.

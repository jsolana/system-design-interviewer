---
title: Triple Step (Staircase Ways)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 8 Recursion and Dynamic Programming, problem 8.1 (p. 134, solution pp. 342-343)]
algorithms: [recursion,dynamic-programming]
difficulty: low
---

# Triple Step (Staircase Ways)

## Prompt
A child climbs n stairs hopping 1, 2 or 3 steps. Count the ways.

## Examples
countWays(0)=1 by convention.

## Constraints and clarifying questions
Define base case: 0 steps remaining counts as 1 way (negative = 0).

## Approaches
- Last hop was 1, 2 or 3 steps, so ways(n) = ways(n-1)+ways(n-2)+ways(n-3). Add, do not multiply.
- Brute force recursion: about O(3^n).
- Memoize in an array indexed 0..n: O(n) time and space. A bottom-up version needs only three variables.

## Complexity
O(n) time with memo; O(3^n) brute force.

## Edge cases
Overflow: an int overflows at n=37; a long delays it; BigInteger fixes it.

## Hints
What is the very last step?

## Related algorithms
- [[recursion]]
- [[dynamic-programming]]

## Variants
Generalizes to k hop sizes.

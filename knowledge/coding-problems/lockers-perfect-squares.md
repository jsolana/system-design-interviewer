---
title: 100 Lockers
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 6 Math and Logic Puzzles, problem 6.9 (p. 124, solution p. 296)]
algorithms: [number-theory]
difficulty: low
---

# 100 Lockers

## Prompt
100 closed lockers. Pass i toggles every ith locker for i = 1..100. How many are open at the end?

## Examples
Locker 15 is toggled on passes 1, 3, 5, 15.

## Constraints and clarifying questions
Pass 1 opens all lockers.

## Approaches
- Locker n is toggled once per divisor of n. It is open iff the divisor count is odd.
- Divisors pair as (d, n/d); an odd count happens only when n is a perfect square (the root pairs with itself).
- Perfect squares up to 100: 1, 4, ..., 100 = 10, so 10 lockers are open.

## Complexity
O(1) after the insight; simulation is O(n log n).

## Edge cases
Counting the sqrt pair twice.

## Hints
Count factors.

## Related algorithms
- [[number-theory]]

## Variants
Not covered in the source.

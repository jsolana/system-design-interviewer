---
title: Poisoned Bottle with Test Strips
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 6 Math and Logic Puzzles, problem 6.10 (p. 124, solution pp. 297-300)]
algorithms: [bit-manipulation]
difficulty: high
---

# Poisoned Bottle with Test Strips

## Prompt
1000 bottles, exactly one poisoned. 10 test strips turn permanently positive from a drop; strips can be reused while negative; tests run once a day and results take 7 days. Find the poisoned bottle in as few days as possible. Follow-up: write a simulation.

## Examples
Bottle 438: day 7 positive strip 4, day 8 strip 3, day 9 strip 8 in the digit approach.

## Constraints and clarifying questions
Strips are reusable; many drops per strip allowed.

## Approaches
- Naive (28 days): split bottles over 10 strips, wait 7 days, keep the bottles of the positive strip (100, 10, 1), repeat.
- Digit approach (10 days): on day 0 strip i gets bottles whose hundreds digit is i, on day 1 tens digit, day 2 units digit (results arrive days 7, 8, 9). Ambiguity when digits repeat (e.g. 383 vs 388): add a 4th test on day 3 with the units digit shifted by one, and unshift to disambiguate.
- Optimal (7 days): run all tests on day 0 using binary encoding: strip i gets a drop of every bottle whose bit i is 1 (2^10 = 1024 >= 1000). After 7 days the pattern of positive strips is the binary number of the poisoned bottle.

## Complexity
Naive 28 days, digits 10 days, binary 7 days (minimum possible since results take 7).

## Edge cases
Duplicate digits in the digit approach; bottle numbering from 0.

## Hints
Why would the problem say results take seven days? Because you should run tests in parallel.

## Related algorithms
- [[bit-manipulation]]

## Variants
Not covered in the source.

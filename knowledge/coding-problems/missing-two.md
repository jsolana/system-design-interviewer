---
title: Missing Two
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.19, solution p. 591]
algorithms: [arithmetic-invariants]
difficulty: high
---

# Missing Two

## Prompt
One number from 1..N is missing: find it in O(N) time and O(1) space. Then do it when two numbers are missing.

## Examples
Not covered in the source.

## Constraints and clarifying questions
No extra storage proportional to N.

## Approaches
1. One missing: expected sum n(n+1)/2 minus actual sum (product also works but overflows).
2. Two missing x, y: the sum difference gives x + y; the sum of squares (or product) difference gives a second equation; solve the quadratic 2x^2 - 2sx + (s^2 - t) = 0; its two roots are x and y.

## Complexity
O(N) time, O(1) space.

## Edge cases
Overflow for large N (discuss).

## Hints
You need a calculation that is unique, reversible and O(1).

## Related algorithms
[[arithmetic-invariants]]

## Variants
Not covered in the source.

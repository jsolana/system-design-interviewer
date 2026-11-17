---
title: Binary to String (fraction)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 5 Bit Manipulation, problem 5.2]
algorithms: [bit-manipulation]
difficulty: medium
---

# Binary to String (fraction)

## Prompt
Given a real number between 0 and 1 (e.g. 0.72) as a double, print its binary representation; print "ERROR" if it needs more than 32 characters.

## Examples
- 0.72 -> ERROR (not representable in 32 chars)

## Constraints and clarifying questions
- Not covered in the source.

## Approaches
- Mirror decimal places: multiply by 2; if >= 1 emit 1 and subtract 1, else emit 0. Stop when the fraction is 0; error if length >= 32.
- Equivalent: compare with 0.5, 0.25, ... subtracting.

## Complexity
- O(1) (at most 32 steps).

## Edge cases
- 0, 1, numbers like 0.72 that never terminate.

## Hints
Not covered in the source.

## Related algorithms
[[bit-manipulation]]

## Variants


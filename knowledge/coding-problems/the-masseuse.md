---
title: The Masseuse (Max Non-Adjacent Sum)
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.16, solution p. 576]
algorithms: [dynamic-programming, recursion]
difficulty: medium
---

# The Masseuse (Max Non-Adjacent Sum)

## Prompt
Given back-to-back appointment lengths and a need for a break (no adjacent appointments) pick the set with the largest total minutes.

## Examples
{30, 15, 60, 75, 45, 15, 15, 45} -> 180 ({30, 60, 45, 45}).

## Constraints and clarifying questions
No two adjacent requests.

## Approaches
1. Greedy by longest fails ({45, 60, 45, 15}).
2. Recursion: take i (then i+2) or skip it (i+1): O(2^n).
3. Memoize by index: O(n) time and space.
4. Iterate backwards; only the best at i+1 and i+2 are needed: O(n) time, O(1) space. (Never skip three consecutive items.)

## Complexity
O(n) time, O(1) space.

## Edge cases
Empty list; one or two requests.

## Hints
Look at best(i) as a function of best(i+1) and best(i+2).

## Related algorithms
[[dynamic-programming]] [[recursion]]

## Variants
Not covered in the source.

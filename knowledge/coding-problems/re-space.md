---
title: Re-Space (Unconcatenate a Document)
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.13, solution p. 563]
algorithms: [dynamic-programming, recursion]
difficulty: high
---

# Re-Space (Unconcatenate a Document)

## Prompt
A document lost its spaces and punctuation. Given a dictionary, split it so as to minimize the number of unrecognized characters.

## Examples
jesslookedjustliketimherbrother -> jess looked just like tim her brother (7 unrecognized).

## Constraints and clarifying questions
Do not try to understand the meaning; only count unrecognized characters.

## Approaches
1. Recursion: choose where the first word ends; each prefix not in the dictionary counts its length as invalid; return count and parse; short-circuit when invalid exceeds best or reaches 0. O(2^n).
2. Memoize by start index (array of results): each split(i) is computed once, O(n^2) total.

## Complexity
O(n^2) with memoization.

## Edge cases
Empty string; no dictionary words at all.

## Hints
The start index identifies a subproblem.

## Related algorithms
[[dynamic-programming]] [[recursion]]

## Variants
Not covered in the source.

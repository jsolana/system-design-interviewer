---
title: Print All Permutations of a String
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. VII Technical Questions / VI Big O (introductory examples), Base Case and Build (book p. 71)]
algorithms: [recursion, backtracking]
difficulty: medium
---

# Print All Permutations of a String

## Prompt
Print all permutations of a string of unique characters.

## Examples
- abc -> abc, acb, bac, bca, cab, cba

## Constraints and clarifying questions
- Unique characters.

## Approaches
- Base case and build: P("a")={a}; P("ab")={ab,ba}; to build P(s1..sn) take each string of P(s1..sn-1) and insert sn at every position.

## Complexity
- n! results; O(n^2 * n!) for the straightforward recursive generator (Big O chapter example).

## Edge cases
- Empty string, single char.

## Hints
Not covered in the source.

## Related algorithms
[[recursion]], [[backtracking]]

## Variants
- Lists of unique chars only; duplicates require handling elsewhere in the book.

See also: [[permutations]] (different source and chapter; overlapping technique).

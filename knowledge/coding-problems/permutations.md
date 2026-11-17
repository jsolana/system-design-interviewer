---
title: Permutations (with and without Duplicates)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 8 Recursion and Dynamic Programming, problem 8.7 and 8.8 (p. 135, solution pp. 353-358)]
algorithms: [recursion,backtracking,hash-table]
difficulty: medium
---

# Permutations (with and without Duplicates)

## Prompt
Compute all permutations of a string of unique characters. Variant: characters may repeat and the output must not contain duplicates.

## Examples
'abc' gives abc, acb, bac, bca, cab, cba.

## Constraints and clarifying questions
Number of results n!.

## Approaches
- Approach 1: permutations of the first n-1 chars, insert the nth char in every position.
- Approach 2: choose each char as the first char and permute the remainder; or push a prefix down the recursion and emit it when the remainder is empty.
- With duplicates: build a frequency map of the letters; at each level try each letter with count > 0 (decrement, recurse, restore). Avoids generating duplicates; a set-based dedupe is O(n!) always, even for 'aaaa...'.

## Complexity
O(n!) time; the frequency-map version is much faster for many duplicates.

## Edge cases
Empty string returns one empty permutation.

## Hints
Base case and build.

## Related algorithms
- [[recursion]]
- [[backtracking]]
- [[hash-table]]

## Variants
8.8 permutations with duplicates is the frequency-map version.

See also: [[print-all-permutations]] (different source and chapter; overlapping technique).

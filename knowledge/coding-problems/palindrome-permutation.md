---
title: Palindrome Permutation
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 1 Arrays and Strings, problem 1.4]
algorithms: [hash-table, bit-vector, character-counting]
difficulty: medium
---

# Palindrome Permutation

## Prompt
Check whether a string is a permutation of a palindrome (palindrome need not be a dictionary word).

## Examples
- "Tact Coa" -> true ("taco cat", "atco cta")

## Constraints and clarifying questions
- Ignore case and non-letters (book maps letters to 0..25, others -1).

## Approaches
- Insight: at most one character may have an odd count (even-length strings need all even; odd-length exactly one odd).
- Hash/count table, then verify at most one odd count.
- Track the odd count while scanning (same big-O).
- Bit vector: toggle bit per letter; at the end `v == 0 || (v & (v-1)) == 0`.
- Do not generate all permutations (factorial).

## Complexity
- O(n) time; bit vector uses O(1) space.

## Edge cases
- Empty string, single character, punctuation/spaces.

## Hints
Not covered in the source.

## Related algorithms
[[hash-table]], [[bit-vector]], [[character-counting]]

## Variants


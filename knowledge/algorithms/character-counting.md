---
title: Character counting and bit vectors
type: algorithm
aliases: [frequency array, character count array, bit vector, counting array]
sources: [Cracking the Coding Interview 6th ed., ch. 1 (book pp. 90-97, solutions)]
---

# Character counting and bit vectors

## Definition
Represent per-character information in a fixed-size array indexed by character code (128/256 for ASCII), or compress boolean/parity information into the bits of an integer (bit vector).

## When to use it
Uniqueness, permutation/anagram checks, palindrome-permutation, ransom-note, one-pass frequency questions over a bounded alphabet. Ask the interviewer whether the charset is ASCII or Unicode.

## How it works
- Boolean array: flag seen characters; length greater than alphabet size means a duplicate exists (pigeonhole).
- Count array: increment for string 1, decrement for string 2; negative count means mismatch.
- Bit vector: one bit per letter (a-z fits in one int). Toggle a bit per occurrence to track parity; "at most one odd" is `v == 0 || (v & (v-1)) == 0`.
- Generalize to a [[hash-table]] of counts for words/Unicode.

## Complexity
O(n) time, O(1) space (O(c) for charset size c). Bit vector reduces space 8x versus boolean array.

## Common pitfalls
Assuming charset without asking; case sensitivity and whitespace significance; non-letter characters.

## Appears in
[[check-permutation]], [[is-unique]], [[palindrome-permutation]], [[ransom-note]], [[urlify]]

## See also
[[bit-manipulation]], [[hash-table]]

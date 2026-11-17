---
title: Find Duplicates with 4 KB
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 10 Sorting and Searching, problem 10.8 (p. 151, solution pp. 407-408)]
algorithms: [bit-vector]
difficulty: medium
---

# Find Duplicates with 4 KB

## Prompt
An array holds numbers 1..N (N <= 32,000) with possible duplicates; N unknown. With 4 KB of memory print all duplicates.

## Examples
Not covered in the source.

## Constraints and clarifying questions
4 KB = 32,768 bits.

## Approaches
- Bit vector of 32,000 bits; for each value check its bit; if set, print duplicate; else set it.

## Complexity
O(n) time, 4 KB.

## Edge cases
Value 1-based vs bit index 0-based.

## Hints
32,000 bits fits in 4 KB.

## Related algorithms
- [[bit-vector]]

## Variants
Not covered in the source.

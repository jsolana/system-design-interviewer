---
title: Missing Int (Four Billion Integers)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 10 Sorting and Searching, problem 10.7 (p. 150, solution pp. 403-407)]
algorithms: [bit-vector,bit-manipulation]
difficulty: high
---

# Missing Int (Four Billion Integers)

## Prompt
A file has four billion non-negative integers; generate one not in it with 1 GB of memory. Follow-up: only 10 MB, values distinct and at most one billion numbers.

## Examples
Not covered in the source.

## Constraints and clarifying questions
There are 2^31 non-negative ints, so the file must miss some.

## Approaches
- Bit vector with 2^31 (or 2^32) bits (<= 1 GB); set bit per value; scan for the first 0 bit.
- 10 MB: pass 1 counts values per range (block). Block size must satisfy arraySize <= about 2^21 counters and rangeSize <= 2^26 bits; e.g. range 2^20. Find a block with fewer values than its size, pass 2 builds a bit vector for just that block and finds a zero.
- Even less memory: more passes (per million, then per thousand, then bit vector).

## Complexity
Two passes, O(n) each.

## Edge cases
Counts rely on distinct values.

## Hints
Use bits, then use ranges.

## Related algorithms
- [[bit-vector]]
- [[bit-manipulation]]

## Variants
Not covered in the source.

---
title: Bit Vector (Bitmap / BitSet)
type: algorithm
aliases: [bitset, bitmap]
sources: [Cracking the Coding Interview 6th ed., ch. 10 Sorting and Searching (pp. 146-151, solutions pp. 396-416)]
---

# Bit Vector (Bitmap / BitSet)

## Definition
An array of ints where each bit stores one boolean, giving one bit of memory per possible value.

## When to use it
Memory-limited problems about presence of integers in a bounded range: missing number, duplicates.

## How it works
bit for value v is bit (v mod 32) of word (v / 32) (v>>5 and v&31). Missing int among 4 billion with 1 GB: 2^32 bits = 512 MB fits; set bits, scan for first 0. With 10 MB: two passes, first count values per block (range size between 2^11 and 2^20 works, e.g. 2^20), find a block with fewer than range-size values, then bit-vector only that block. With even less memory, use more passes (counts per million, then per thousand, then bit vector). Duplicates in 1..32000 with 4 KB: 32000 bits < 32768 bits, so one bit per number; print when bit already set.

## Complexity
O(n) time, O(range/8) bytes.

## Common pitfalls
Off-by-one for 1-based values; number of non-negative ints is 2^31 not 2^32; dedupe assumptions.

## Appears in
[[find-duplicates]], [[is-unique]], [[missing-int]], [[palindrome-permutation]]

## See also
- [[bit-manipulation]]
- [[hash-table]]

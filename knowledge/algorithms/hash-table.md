---
title: Hash table
type: algorithm
aliases: [hash map, dictionary, hash set]
sources: [Cracking the Coding Interview 6th ed., ch. 17 Hard (pp. 186-191, solutions pp. 530-627); Cracking the Coding Interview 6th ed., ch. 1 Arrays and Strings (book p. 88); ch. 10 and 16 solutions (pp. 396-416, ch. 16)]
---

# Hash table

## Definition
Maps keys to values for fast lookup. Typical implementation: array of linked lists (buckets) plus a hash function.

## When to use it
Need O(1) membership/lookup/counting; "seen before", duplicates, frequency counts, complement lookup (x+k), grouping by key, prefix-sum counts. First thing to consider when a brute force repeatedly searches.

## How it works
1. Compute key's hash code. 2. Index = hash % array_length. 3. Store (key, value) in the linked list at that index (collisions: different keys with the same hash or index). Lookup repeats the process and scans the bucket.
Alternative: balanced BST keyed by key: O(log N) lookup, less space, ordered iteration.

Patterns from the Sorting/Searching and Moderate chapters:
- Word frequency: single query is a linear scan; for repeated queries preprocess into a word-to-count table.
- Group anagrams: key = sorted characters, value = list of words (bucket-sort style, avoids a full sort).
- Pair/complement search: store seen elements (or counts of unpaired ones); look up target - x. Sum swap: put one array in a set and look up one - target, O(A+B).
- T9 precomputation: map digit string to words by converting every dictionary word to digits.
- Best line: key lines by slope floored to an epsilon and also probe neighboring buckets.
- Mastermind: frequency array of unmatched solution colors. Sparse grids: set of marked cells.
- LRU cache: hash map from key to a node of a [[doubly-linked-list]].
- Memoization keys must capture the entire state.

## Chaining implementation and extra patterns (CtCI 7.12, 17.x)
- Store both key and value in each chain cell: after a collision (e.g. "jim" and "bob" with a length-based hash) the key is needed to find the right entry.
- Memoization tables for DP, per-search visited maps, word -> list of positions (repeated word-distance queries), name equivalence classes, word -> documents (inverted index), wildcard word -> words one edit apart.

## Complexity
Average O(1) insert/lookup/delete; worst case O(N) with many collisions. Technically O(K) in key length.

## Common pitfalls
Floating-point keys need epsilon handling; custom keys need consistent equals and hashCode. Keying by value when reference identity is required (e.g. list intersection); forgetting to undo changes when backtracking (see [[prefix-sum]] on trees); assuming ordering.

## Appears in
[[baby-names]], [[best-line]], [[common-elements-of-sorted-arrays]], [[count-pairs-with-difference-k]], [[equal-sums-of-cubes]], [[group-anagrams]], [[hash-table-with-chaining]], [[langtons-ant]], [[letters-and-numbers]], [[longest-word]], [[lru-cache]], [[master-mind]], [[pairs-with-sum]], [[palindrome-permutation]], [[paths-with-sum]], [[pattern-matching]], [[permutations]], [[permutations-of-string-in-longer-string]], [[ransom-note]], [[remove-duplicates-linked-list]], [[sparse-similarity]], [[sum-swap]], [[t9-words]], [[tic-tac-toe-winner]], [[word-distance]], [[word-frequencies]]

## See also
[[trie]], [[dynamic-array]], [[problem-solving-techniques]]

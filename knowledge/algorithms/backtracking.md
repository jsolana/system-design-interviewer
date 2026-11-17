---
title: Backtracking and Combinatorial Generation
type: algorithm
aliases: [subsets, permutations, enumeration]
sources: [Cracking the Coding Interview 6th ed., ch. 17 Hard (pp. 186-191, solutions pp. 530-627); Cracking the Coding Interview 6th ed., ch. 8 Recursion and Dynamic Programming (pp. 130-136, solutions pp. 342-380)]
---

# Backtracking and Combinatorial Generation

## Definition
Build candidates incrementally, recursing on each valid choice and abandoning (undoing) a partial candidate as soon as it cannot lead to a valid solution.

## When to use it
'Print all valid...', all subsets, permutations, combinations of parentheses, board placements, word completions with a dictionary.

## How it works
- Subsets (power set): for each element choose in/out: 2^n subsets, total output n*2^(n-1) elements, so O(n*2^n) is optimal. Two ways: recursively clone P(n-1) and add element n, or enumerate integers 0..2^n-1 as bitmasks.
- Permutations of distinct chars: insert the first char in every position of the permutations of the rest, or pick each char as prefix and recurse on the remainder (pass the prefix down). n! results.
- Permutations with duplicates: recurse over a frequency map of remaining letters so no duplicate is ever generated (faster than generating all then deduplicating with a set).
- Valid parentheses: build char by char; may add '(' while some remain; may add ')' only if more '(' than ')' used so far. Every string is unique, no dedup needed (versus inserting '()' into previous results, which creates duplicates).
- N-queens: place one queen per row, keeping a column array, and check column and diagonal conflicts (same diagonal when column distance equals row distance).
- Prune with a trie when searching dictionary words (T9).

## Pruned constructive search (CtCI 17.25)
Try the largest target size first so the first success is optimal; extend a partial rectangle row by row and check that every column is a valid prefix (via a [[trie]]) before recursing, then full-word validity at the end.

## Complexity
Output-bound: subsets O(n*2^n), permutations O(n!), parentheses Catalan-number many.

## Common pitfalls
Generating duplicates then filtering wastes work; pruning conditions must be checked before recursing; clone mutable state when saving a result.

## Appears in
[[bst-sequences]], [[eight-queens]], [[generate-parentheses]], [[permutations]], [[power-set]], [[print-all-permutations]], [[t9-words]], [[word-rectangle]]

## See also
- [[recursion]]
- [[trie]]
- [[bit-manipulation]]

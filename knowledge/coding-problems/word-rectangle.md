---
title: Word Rectangle
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.25, solution p. 606]
algorithms: [trie, backtracking]
difficulty: high
---

# Word Rectangle

## Prompt
From a list of millions of words build the largest rectangle (rows and columns are all words; equal row length, equal column height).

## Examples
Not covered in the source.

## Constraints and clarifying questions
Words need not be consecutive in the list.

## Approaches
1. Group words by length; try rectangle areas from the largest down so the first success is the best.
2. For a fixed size build row by row, checking after each row that every column is a valid prefix (via a trie per length); prune immediately on failure; at full height verify each column is a complete word.

## Complexity
Exponential worst case; heavy pruning in practice.

## Edge cases
No rectangle exists; 1xN rectangles.

## Hints
Preprocess the dictionary; prune on prefixes.

## Related algorithms
[[trie]] [[backtracking]]

## Variants
Not covered in the source.

---
title: Word Frequencies
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.2 (p. 181)]
algorithms: [hash-table]
difficulty: low
---

# Word Frequencies

## Prompt
Find the frequency of a word in a book; what changes if queried many times?

## Examples
Not covered in the source.

## Constraints and clarifying questions
Case and whitespace handling.

## Approaches
- Single query: linear scan, O(n).
- Many queries: preprocess into a hash map word -> count, then O(1) lookups.

## Complexity
O(n) preprocess, O(1) query.

## Edge cases
Null table or word; unseen word.

## Hints
Preprocess for repeated queries.

## Related algorithms
- [[hash-table]]

## Variants
Not covered in the source.

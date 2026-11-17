---
title: Word Distance
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.11, solution p. 557]
algorithms: [two-pointers, hash-table]
difficulty: medium
---

# Word Distance

## Prompt
In a large text file find the shortest distance in words between two given words; optimize for repeated queries on the same file.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Ask whether order of the two words matters (assumed not).

## Approaches
1. Single pass remembering the last position of each word; update the best distance at each occurrence.
2. Repeated queries: preprocess word -> sorted list of positions in one pass; for each query walk two pointers over the two lists, advancing the one at the smaller value.

## Complexity
Single pass O(N); repeated: O(N) preprocessing, O(A + B) per query.

## Edge cases
Words that do not appear; same word twice.

## Hints
Compare closest elements of two sorted lists.

## Related algorithms
[[two-pointers]] [[hash-table]]

## Variants
Not covered in the source.

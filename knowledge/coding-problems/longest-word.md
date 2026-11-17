---
title: Longest Word Made of Other Words
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.15, solution p. 573]
algorithms: [dynamic-programming, hash-table]
difficulty: high
---

# Longest Word Made of Other Words

## Prompt
Given a list of words find the longest word that can be built from other words in the list.

## Examples
cat, banana, dog, nana, walk, walker, dogwalker -> dogwalker

## Constraints and clarifying questions
Not covered in the source.

## Approaches
1. Sort by length descending; for each word split into prefix/suffix.
2. For two-word composites just look up both halves in a hash set.
3. For any number of words recurse: prefix in the set and the remainder buildable; memoize results per string; a word must not count as built from itself (skip the cache for the original word).

## Complexity
Memoized: polynomial in word length per word.

## Edge cases
Word consisting of itself only; duplicates.

## Hints
Solve the two-word case first.

## Related algorithms
[[dynamic-programming]] [[hash-table]]

## Variants
Not covered in the source.

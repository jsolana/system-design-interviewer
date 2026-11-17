---
title: Minimal Tree
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 4 Trees and Graphs, problem 4.2]
algorithms: [binary-search-tree, recursion]
difficulty: low
---

# Minimal Tree

## Prompt
Given a sorted array of unique integers, build a binary search tree of minimal height.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Not covered in the source.

## Approaches
- Make the middle element the root; recursively build the left subtree from the left half and the right subtree from the right half. (Inserting one by one would cost O(N log N).)

## Complexity
- O(N) time; O(log N) recursion.

## Edge cases
- Empty array, off-by-one in mid +/- 1.

## Hints
Not covered in the source.

## Related algorithms
[[binary-search-tree]], [[recursion]]

## Variants


---
title: Validate BST
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 4 Trees and Graphs, problem 4.5]
algorithms: [binary-search-tree, tree-traversal, recursion]
difficulty: medium
---

# Validate BST

## Prompt
Check whether a binary tree is a binary search tree.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Duplicate policy (left <= node < right).

## Approaches
- In-order traversal and check sorted by tracking only the last value seen; fails to distinguish trees with duplicates.
- Min/max ranges: pass (min, max) down; going left sets max, going right sets min; every node must be in range. Checking only parent-child is insufficient (a 25 deep in the left subtree of 20).

## Complexity
- O(N) time, O(log N) space on balanced tree.

## Edge cases
- Duplicates, null min/max, Integer extremes.

## Hints
Not covered in the source.

## Related algorithms
[[binary-search-tree]], [[tree-traversal]], [[recursion]]

## Variants


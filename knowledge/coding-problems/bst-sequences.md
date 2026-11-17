---
title: BST Sequences
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 4 Trees and Graphs, problem 4.9]
algorithms: [recursion, backtracking, binary-search-tree]
difficulty: high
---

# BST Sequences

## Prompt
Given a BST with distinct elements, print all arrays that could have produced it by successive insertion.

## Examples
- Tree 2 with children 1 and 3 -> {2,1,3}, {2,3,1}

## Constraints and clarifying questions
- Distinct values.

## Approaches
- The root must come first. Relative order inside the left and right subtrees matters only within each subtree, but any interleaving of the two is valid.
- Recursively compute all sequences of left and right subtrees, "weave" every pair (all interleavings preserving each list order), and prepend the root. Weave recursively: take head of first or head of second, recurse, restore (backtrack).

## Complexity
- Output size can be exponential.

## Edge cases
- Single node, missing child.

## Hints
Trust each recursive function does its job while writing the other.

## Related algorithms
[[recursion]], [[backtracking]], [[binary-search-tree]]

## Variants


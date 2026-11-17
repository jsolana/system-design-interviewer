---
title: List of Depths
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 4 Trees and Graphs, problem 4.3]
algorithms: [breadth-first-search, tree-traversal, linked-list]
difficulty: low
---

# List of Depths

## Prompt
Given a binary tree, create a linked list of all nodes at each depth (D lists for depth D).

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Not covered in the source.

## Approaches
- Pre-order traversal passing the level; add the node to lists[level] (create if missing).
- BFS level by level: the next level is built from the children of the previous level.

## Complexity
- O(N) time; space O(N) for output (recursion adds O(log N)).

## Edge cases
- Empty tree.

## Hints
Not covered in the source.

## Related algorithms
[[breadth-first-search]], [[tree-traversal]], [[linked-list]]

## Variants


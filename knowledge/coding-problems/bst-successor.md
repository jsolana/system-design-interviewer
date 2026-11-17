---
title: In-order Successor in BST
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 4 Trees and Graphs, problem 4.6]
algorithms: [binary-search-tree, tree-traversal]
difficulty: medium
---

# In-order Successor in BST

## Prompt
Find the in-order successor of a given node in a BST; nodes have parent links.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- No successor for the last node (return null).

## Approaches
- If the node has a right subtree, the successor is the leftmost node of that subtree.
- Otherwise go up until you move from a left child to its parent; that parent is the successor. If you reach the root from the right, there is none.

## Complexity
- O(H).

## Edge cases
- Rightmost node, root with no right subtree.

## Hints
Not covered in the source.

## Related algorithms
[[binary-search-tree]], [[tree-traversal]]

## Variants


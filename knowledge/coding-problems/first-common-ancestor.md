---
title: First Common Ancestor
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 4 Trees and Graphs, problem 4.8]
algorithms: [lowest-common-ancestor, tree-traversal, recursion]
difficulty: high
---

# First Common Ancestor

## Prompt
Find the first common ancestor of two nodes in a binary tree (not necessarily a BST), avoiding extra storage of nodes.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Parent links available? Are both nodes guaranteed to be in the tree?

## Approaches
- With parent links: align depths and walk up (like list intersection), or climb from p checking whether the newly uncovered sibling subtree covers q.
- Without links: branch toward the side containing both; the first node where they split is the answer (O(n) with repeated covers calls).
- Single pass: recursively return p, q, null or the ancestor; handle the case where only one node exists with a (node, isAncestor) result.

## Complexity
- O(n) time; O(depth) space.

## Edge cases
- p ancestor of q, node missing from tree.

## Hints
Not covered in the source.

## Related algorithms
[[lowest-common-ancestor]], [[tree-traversal]], [[recursion]]

## Variants


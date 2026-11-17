---
title: Binary tree traversal (in-order, pre-order, post-order)
type: algorithm
aliases: [inorder, preorder, postorder]
sources: [Cracking the Coding Interview 6th ed., ch. 17 Hard (pp. 186-191, solutions pp. 530-627); Cracking the Coding Interview 6th ed., ch. 4 (book p. 103)]
---

# Binary tree traversal

## Definition
Visit every node recursively: in-order = left, node, right; pre-order = node, left, right; post-order = left, right, node.

## When to use it
In-order on a BST yields sorted order (validate BST, successor); pre-order starts at root (serialization: with null markers it uniquely identifies a tree; used for subtree check); post-order for bottom-up computations (heights, deletions, DFS topological ordering). Level-order is BFS with a queue.

## How it works
Recurse on children, passing extra state (level, min/max range, running sum) as parameters. Returning multiple values (node and boolean, height or error code) is common.

## BST to doubly linked list (CtCI 17.12)
Recursively convert the left and right subtrees into lists and join: left tail -> root -> right head. Returning head and tail can use a pair object, recomputing the tail by walking (O(N^2) because each node is re-walked once per ancestor), or returning circular lists so tail = head.prev (O(N)); break the circle at the end.

## Complexity
O(N) time; O(H) stack space (H = height; log N balanced, N degenerate).

## Common pitfalls
In-order alone cannot distinguish duplicates or different structures with equal values; missing null base case.

## Appears in
[[binode-bst-to-linked-list]], [[bst-successor]], [[check-balanced-tree]], [[check-subtree]], [[first-common-ancestor]], [[list-of-depths]], [[validate-bst]]

## See also
[[binary-search-tree]], [[depth-first-search]], [[breadth-first-search]]

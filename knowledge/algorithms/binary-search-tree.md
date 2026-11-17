---
title: Binary tree, binary search tree and balanced trees
type: algorithm
aliases: [BST, balanced tree, complete tree, full tree, perfect tree, AVL, red-black]
sources: [Cracking the Coding Interview 6th ed., ch. 4 (book pp. 100-102); ch. 10 Sorting and Searching, Rank from Stream (p. 151, solution pp. 410-412)]
---

# Binary search tree and tree terminology

## Definition
Tree: nodes with children, no cycles, usually a root. Binary tree: at most 2 children. BST: for every node, all left descendants <= n < all right descendants (duplicate policy varies: ask). Leaf: no children.

## When to use it
Ordered data with O(log N) insert/find when balanced; in-order successor; range checks.

## How it works
- Balanced = "not terribly imbalanced" so ops are O(log N) (red-black, AVL are common types). Subtrees need not be equal size.
- Complete: all levels full except possibly last, filled left to right. Full: every node has 0 or 2 children. Perfect: full and complete, exactly 2^k - 1 nodes; rare.
- Ask: binary tree vs BST? balanced? duplicates?
- Useful patterns: build minimal-height BST from sorted array via middle element; augment nodes with subtree size for random/ranked access; validate with narrowing (min, max) ranges.

- Rank (order statistic) tree: store left-subtree size in each node. Insert goes left on d <= node (increment left_size) else right. rank(x): equal -> left_size; go left -> rank in left; go right -> left_size + 1 + rank in right; return -1 if absent. O(log n) balanced, O(n) unbalanced. A sorted array gives O(log n) rank but O(n) insert.

## Complexity
Balanced: O(log N) find/insert/delete; degenerate: O(N).

## Common pitfalls
Checking only parent-child ordering (not all descendants); assuming a tree is a BST or perfect.

## Appears in
[[bst-sequences]], [[bst-successor]], [[minimal-tree]], [[random-node]], [[rank-from-stream]], [[validate-bst]]

## See also
[[tree-traversal]], [[binary-heap]], [[trie]]

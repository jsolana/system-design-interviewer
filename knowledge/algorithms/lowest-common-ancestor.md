---
title: Lowest (first) common ancestor
type: algorithm
aliases: [LCA, first common ancestor]
sources: [Cracking the Coding Interview 6th ed., ch. 4 solution 4.8]
---

# Lowest common ancestor

## Definition
The deepest node that has both p and q in its subtree.

## When to use it
Tree relationship queries; "first common ancestor" of two nodes in a (not necessarily search) tree.

## How it works
- With parent links: treat the two paths to the root like intersecting linked lists (align by depth), O(d). Or climb from p checking whether the sibling subtree covers q.
- Without parent links, top-down: if p and q are on the same side of the node, go that way; otherwise the node is the answer. O(n) but repeatedly re-searches subtrees.
- Optimized single pass: return p if the subtree contains p only, q if q only, null if neither, else the ancestor. Bug: if only one of p,q is in the tree it wrongly returns it; fix by returning (node, isAncestor) or pre-checking both exist.

## Complexity
O(n) time, O(h) space (single pass).

## Common pitfalls
Nodes not in the tree; p being ancestor of q.

## Appears in
[[first-common-ancestor]]

## See also
[[tree-traversal]], [[linked-list]]

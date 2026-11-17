---
title: BiNode (BST to Doubly Linked List)
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.12, solution p. 561]
algorithms: [tree-traversal, recursion]
difficulty: high
---

# BiNode (BST to Doubly Linked List)

## Prompt
BiNode has two node pointers and can represent both a binary tree and a doubly linked list. Convert a BST into a doubly linked list in place, keeping order.

## Examples
Not covered in the source.

## Constraints and clarifying questions
In place; values stay in order.

## Approaches
1. Recursively convert left and right subtrees and join left-list tail, root, right-list head.
2. Returning head and tail: a pair object; or recompute the tail by walking (O(N^2)); or return circular lists so tail = head.node1, then break the circle (O(N)).

## Complexity
O(N) time.

## Edge cases
Empty tree; subtrees missing on one side.

## Hints
Subtrees' lists are consecutive parts of the final list.

## Related algorithms
[[tree-traversal]] [[recursion]]

## Variants
Not covered in the source.

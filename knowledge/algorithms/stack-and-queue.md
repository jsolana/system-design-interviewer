---
title: Stack and queue
type: algorithm
aliases: [LIFO, FIFO, stack, queue]
sources: [Cracking the Coding Interview 6th ed., ch. 3 Stacks and Queues (book pp. 96-99)]
---

# Stack and queue

## Definition
Stack: LIFO with push, pop, peek, isEmpty. Queue: FIFO with add, remove, peek, isEmpty. Both can be linked-list based (stack adds/removes at the same end, queue at opposite ends).

## When to use it
Stack: backtracking, reversing, iterative version of recursion, matching, undo, tracking prior state (e.g. running min). Queue: BFS, caches, processing in arrival order.

## How it works
- Stack node holds `next`; `top` pointer. Push sets `t.next = top; top = t`.
- Queue keeps `first` and `last`; when removing the last element set `last = null`; when adding to an empty queue set `first = last`. Easy to get wrong.
- Constant-time add/remove but no O(1) access to the ith item.
- Implementations/tricks: one array for several stacks, auxiliary min stack, two stacks as a queue (lazy transfer), insertion-sort via a temp stack, separate queues + timestamps.

## Complexity
O(1) push/pop/add/remove.

## Common pitfalls
Updating first/last; empty-structure exceptions; reversing cost when transferring stacks repeatedly.

## Appears in
[[animal-shelter]], [[calculator]], [[palindrome-linked-list]], [[queue-via-stacks]], [[sort-stack]], [[stack-min]], [[stack-of-plates]], [[three-stacks-in-one-array]]

## See also
[[breadth-first-search]], [[depth-first-search]], [[linked-list]]

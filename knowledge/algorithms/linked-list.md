---
title: Linked list
type: algorithm
aliases: [singly linked list, doubly linked list]
sources: [Cracking the Coding Interview 6th ed., ch. 2 Linked Lists (book pp. 92-95)]
---

# Linked list

## Definition
Sequence of nodes where each node points to the next (singly) and optionally the previous (doubly).

## When to use it
Frequent insert/delete at the ends or at a known node; splitting and merging sequences without shifting; problems stating "singly linked list" with O(1)-space constraints.

## How it works
- No index access: finding the kth element is O(k).
- Add/remove at the head is O(1). Delete node n: find prev, set `prev.next = n.next` (doubly: also fix `n.next.prev`). Check for null and update head/tail.
- Access via head reference only means head changes are not seen by other holders; wrap in a LinkedList class to avoid it.
- Typical techniques: [[runner-technique]], recursion (O(depth) stack), dummy/two-list partitioning, reversing, hash set of seen nodes.
- Clarify singly vs doubly.

## Complexity
Access O(n); insert/delete at known position O(1); search O(n).

## Common pitfalls
Null pointers, losing the head, forgetting tail updates, recursion using O(n) space.

## Appears in
[[animal-shelter]], [[delete-middle-node]], [[kth-to-last-element]], [[linked-list-intersection]], [[list-of-depths]], [[loop-detection]], [[palindrome-linked-list]], [[partition-linked-list]], [[remove-duplicates-linked-list]], [[sum-lists]]

## See also
[[runner-technique]], [[floyd-cycle-detection]], [[stack-and-queue]]

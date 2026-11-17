---
title: Runner technique (fast/slow pointers)
type: algorithm
aliases: [two pointers on linked list, slow and fast pointer]
sources: [Cracking the Coding Interview 6th ed., ch. 2 (book p. 93, solutions 2.2, 2.6, 2.1)]
---

# Runner technique

## Definition
Iterate a linked list with two pointers simultaneously: a fixed gap apart, or moving at different speeds.

## When to use it
Kth from last; find the middle; palindrome check without length; interleave two halves; unknown length; remove duplicates without buffer (runner scans ahead of current).

## How it works
- Fixed gap: advance p1 k nodes, then move both until p1 hits the end; p2 is kth from last.
- 2x speed: when fast reaches the end, slow is at the midpoint (push slow's values on a stack to compare against the second half).
- Weave a1..an,b1..bn into a1,b1,a2,b2...: fast finds midpoint, then insert.

## Complexity
O(n) time, O(1) space.

## Common pitfalls
Odd vs even length; off-by-one in k definition (k=1 is last).

## Appears in
[[kth-to-last-element]], [[loop-detection]], [[palindrome-linked-list]], [[remove-duplicates-linked-list]]

## See also
[[linked-list]], [[floyd-cycle-detection]]

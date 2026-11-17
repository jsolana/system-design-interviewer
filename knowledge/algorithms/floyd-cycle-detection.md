---
title: Floyd cycle detection (tortoise and hare)
type: algorithm
aliases: [loop detection, fast and slow runner cycle]
sources: [Cracking the Coding Interview 6th ed., ch. 2 solution 2.8 (book p. 95)]
---

# Floyd cycle detection

## Definition
Detect (and locate the start of) a cycle in a linked list using a slow pointer (1 step) and a fast pointer (2 steps).

## When to use it
"Circular/corrupt linked list", find loop start, detect repeated state with O(1) space.

## How it works
1. Fast and slow start at head; they must meet if a loop exists (fast cannot jump over slow: one step before, they would have collided).
2. If the non-loop prefix has k nodes, when slow enters the loop fast is k mod LOOP_SIZE ahead; they meet LOOP_SIZE - K steps later, i.e. K nodes before the loop start (K = k mod LOOP_SIZE).
3. Move slow back to head, keep fast at the meeting point; advance both one step at a time: both are k nodes from loop start, so they meet at the loop start.

## Complexity
O(n) time, O(1) space.

## Common pitfalls
Null checks on fast.next; returning the meeting point instead of the loop start.

## Appears in
[[loop-detection]]

## See also
[[runner-technique]], [[linked-list]]

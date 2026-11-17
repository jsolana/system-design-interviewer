---
title: Return Kth to Last
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 2 Linked Lists, problem 2.2]
algorithms: [linked-list, runner-technique, recursion]
difficulty: low
---

# Return Kth to Last

## Prompt
Find the kth to last element of a singly linked list.

## Examples
- k=1 returns the last element

## Constraints and clarifying questions
- Define k (book: k=1 is last).

## Approaches
- If length known: element at index length-k.
- Recursive: recurse to the end, return a counter incremented on unwind; when it equals k that node is the answer (needs a wrapper to return both counter and node). O(n) space.
- Iterative two pointers: advance p1 k nodes, then move p1 and p2 together; when p1 ends, p2 is the answer. O(n) time, O(1) space.

## Complexity
- Iterative O(n)/O(1); recursive O(n) space.

## Edge cases
- k greater than length, k = 0.

## Hints
Not covered in the source.

## Related algorithms
[[linked-list]], [[runner-technique]], [[recursion]]

## Variants


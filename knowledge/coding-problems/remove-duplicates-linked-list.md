---
title: Remove Duplicates from Linked List
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 2 Linked Lists, problem 2.1]
algorithms: [linked-list, hash-table, runner-technique]
difficulty: low
---

# Remove Duplicates from Linked List

## Prompt
Remove duplicates from an unsorted linked list. Follow-up: no temporary buffer.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Singly or doubly linked?

## Approaches
- Hash set of seen values; unlink nodes already seen, single pass.
- No buffer: two pointers: current plus a runner that removes later nodes equal to current. O(N^2) time, O(1) space.

## Complexity
- Hash: O(N) time, O(N) space. Runner: O(N^2), O(1).

## Edge cases
- Empty list, all equal values.

## Hints
Not covered in the source.

## Related algorithms
[[linked-list]], [[hash-table]], [[runner-technique]]

## Variants


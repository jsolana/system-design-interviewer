---
title: Partition Linked List
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 2 Linked Lists, problem 2.4]
algorithms: [linked-list]
difficulty: medium
---

# Partition Linked List

## Prompt
Partition a linked list around value x so that nodes < x come before nodes >= x.

## Examples
- 3->5->8->5->10->2->1, x=5 -> 3->1->2->10->5->5->8

## Constraints and clarifying questions
- Stability not required.

## Approaches
- Build two lists (before / after) while iterating and concatenate: stable.
- Without stability: grow a new list at the head for small elements and at the tail for large elements, then return the new head.

## Complexity
- O(N) time, O(1) extra space.

## Edge cases
- All elements on one side; x absent.

## Hints
Not covered in the source.

## Related algorithms
[[linked-list]]

## Variants


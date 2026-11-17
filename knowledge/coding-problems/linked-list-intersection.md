---
title: Intersection of Two Linked Lists
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 2 Linked Lists, problem 2.7]
algorithms: [linked-list]
difficulty: medium
---

# Intersection of Two Linked Lists

## Prompt
Determine whether two singly linked lists intersect (by reference) and return the intersecting node.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Intersection by reference, not value.

## Approaches
- Hash set of node references (O(A) space).
- Two intersecting lists share the same last node: traverse both to get lengths and tails; if tails differ, no intersection. Advance the pointer of the longer list by the length difference, then move both until the pointers are equal.

## Complexity
- O(A+B) time, O(1) space.

## Edge cases
- Different lengths, no intersection, one list empty.

## Hints
Not covered in the source.

## Related algorithms
[[linked-list]]

## Variants


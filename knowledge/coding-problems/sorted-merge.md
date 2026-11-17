---
title: Sorted Merge (In Place)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 10 Sorting and Searching, problem 10.1 (p. 149, solution p. 396)]
algorithms: [two-pointers,sorting-algorithms]
difficulty: low
---

# Sorted Merge (In Place)

## Prompt
Sorted arrays A and B; A has a buffer at its end large enough for B. Merge B into A in sorted order.

## Examples
Not covered in the source.

## Constraints and clarifying questions
No extra array allowed.

## Approaches
- Inserting at the front of A would shift elements. Instead merge from the back: compare the last elements and place the larger at the last free slot of A, moving the pointers backward.
- Stop when B is exhausted; leftover A elements are already in place.

## Complexity
O(a+b) time, O(1) space.

## Edge cases
A empty; B shorter or longer.

## Hints
Fill from the back.

## Related algorithms
- [[two-pointers]]
- [[sorting-algorithms]]

## Variants
Not covered in the source.

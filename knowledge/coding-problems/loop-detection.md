---
title: Loop Detection (start of cycle)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 2 Linked Lists, problem 2.8]
algorithms: [floyd-cycle-detection, linked-list, runner-technique]
difficulty: high
---

# Loop Detection (start of cycle)

## Prompt
Given a circular (corrupt) linked list, return the node at the beginning of the loop.

## Examples
- A->B->C->D->E->C returns C

## Constraints and clarifying questions
- Not covered in the source.

## Approaches
- Fast pointer (2 steps) and slow pointer (1 step) meet inside the loop if one exists. They meet K = k mod LOOP_SIZE nodes before the loop start, where k is the length of the non-looped prefix.
- Move slow to head, keep fast at the meeting point, advance both 1 step: they meet at the loop start.

## Complexity
- O(n) time, O(1) space.

## Edge cases
- No loop (fast hits null), loop containing the whole list.

## Hints
Not covered in the source.

## Related algorithms
[[floyd-cycle-detection]], [[linked-list]], [[runner-technique]]

## Variants


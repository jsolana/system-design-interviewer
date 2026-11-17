---
title: Stack Min
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 3 Stacks and Queues, problem 3.2]
algorithms: [stack-and-queue]
difficulty: low
---

# Stack Min

## Prompt
Design a stack with push, pop and min all in O(1).

## Examples
- push 5,6,3,7: min 3; pop 7, pop 3: min 5

## Constraints and clarifying questions
- Not covered in the source.

## Approaches
- Single minValue breaks when the minimum is popped (needs a search).
- Each node stores the minimum beneath it: O(n) extra space.
- Separate min stack: push onto it only when value <= current min, pop it when the main stack pops its min value. Saves space when the minimum rarely changes.

## Complexity
- O(1) per operation.

## Edge cases
- Duplicate minimums (push on <=), empty stack.

## Hints
Not covered in the source.

## Related algorithms
[[stack-and-queue]]

## Variants


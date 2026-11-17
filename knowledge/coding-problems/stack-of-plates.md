---
title: Stack of Plates (SetOfStacks)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 3 Stacks and Queues, problem 3.3]
algorithms: [stack-and-queue]
difficulty: medium
---

# Stack of Plates (SetOfStacks)

## Prompt
Implement SetOfStacks, composed of several stacks, each with a capacity threshold; push/pop behave like one stack. Follow-up: popAt(index).

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Not covered in the source.

## Approaches
- Keep a list of stacks; push to the last stack, creating a new one at capacity; pop from the last stack and remove it when empty.
- popAt(index): "roll over" by removing the bottom of the next stack and pushing it onto the previous one, cascading; or allow non-full stacks (cheaper, trade-off to discuss).

## Complexity
- push/pop O(1); popAt with rollover O(number of stacks).

## Edge cases
- Empty sub-stacks, invalid index.

## Hints
Not covered in the source.

## Related algorithms
[[stack-and-queue]]

## Variants


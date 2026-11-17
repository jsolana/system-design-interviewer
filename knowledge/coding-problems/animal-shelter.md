---
title: Animal Shelter
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 3 Stacks and Queues, problem 3.6]
algorithms: [stack-and-queue, linked-list]
difficulty: medium
---

# Animal Shelter

## Prompt
Dogs and cats adopted strictly FIFO: dequeueAny gives the oldest overall, or choose dequeueDog / dequeueCat for the oldest of that type.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Animals cannot be chosen individually.

## Approaches
- One queue: dequeueAny easy, type-specific needs iteration (slow).
- Two queues (dogs, cats) in a wrapper, each animal stamped with an order/timestamp; dequeueAny compares the heads of both queues and removes the older.

## Complexity
- O(1) per operation.

## Edge cases
- One queue empty, ties in timestamp.

## Hints
Not covered in the source.

## Related algorithms
[[stack-and-queue]], [[linked-list]]

## Variants


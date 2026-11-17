---
title: Queue via Stacks
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 3 Stacks and Queues, problem 3.4]
algorithms: [stack-and-queue]
difficulty: medium
---

# Queue via Stacks

## Prompt
Implement a queue using two stacks.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Not covered in the source.

## Approaches
- Move everything between stacks on each operation (wasteful).
- Lazy: push onto stackNewest; on peek/remove, if stackOldest is empty pour all of stackNewest into it (reversing order), then pop/peek stackOldest.

## Complexity
- Amortized O(1) per operation.

## Edge cases
- Empty queue.

## Hints
Not covered in the source.

## Related algorithms
[[stack-and-queue]]

## Variants


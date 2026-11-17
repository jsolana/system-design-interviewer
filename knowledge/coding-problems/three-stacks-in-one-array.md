---
title: Three in One (three stacks in one array)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 3 Stacks and Queues, problem 3.1]
algorithms: [stack-and-queue]
difficulty: medium
---

# Three in One (three stacks in one array)

## Prompt
Use a single array to implement three stacks.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- How flexible must space allocation be?

## Approaches
- Fixed division: stack i uses [i*cap, (i+1)*cap); track sizes[]; top index = offset + size - 1. Simple but a stack can overflow while others are empty.
- Flexible division: stack blocks of variable capacity within a circular array; when a stack is full shift the next stack(s) over and expand; need per-stack metadata (start, size, capacity) and wrap-around index math (use ((i % n) + n) % n). Far too long to code fully in an interview.

## Complexity
- O(1) push/pop for fixed division; shifting costs O(n) for flexible.

## Edge cases
- Overflow, pop on empty stack.

## Hints
Not covered in the source.

## Related algorithms
[[stack-and-queue]]

## Variants


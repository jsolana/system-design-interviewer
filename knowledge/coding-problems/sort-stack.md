---
title: Sort Stack
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 3 Stacks and Queues, problem 3.5]
algorithms: [stack-and-queue, sorting-algorithms]
difficulty: medium
---

# Sort Stack

## Prompt
Sort a stack so the smallest items are on top using at most one additional stack.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Only push, pop, peek, isEmpty; no arrays.

## Approaches
- Selection with two extra stacks (not allowed).
- Insertion sort: pop each element tmp from s1; while s2 top is greater than tmp, move it back to s1; push tmp on s2; finally copy s2 back (or keep it reversed).
- With unlimited stacks: merge sort or quicksort using two extra stacks per recursion level.

## Complexity
- O(N^2) time, O(N) space.

## Edge cases
- Empty stack, duplicates.

## Hints
Not covered in the source.

## Related algorithms
[[stack-and-queue]], [[sorting-algorithms]]

## Variants


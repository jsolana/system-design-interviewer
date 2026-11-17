---
title: Running Median
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 17 problem 17.20 (p. 190, solution p. 596); Cracking the Coding Interview 6th ed., ch. VII Technical Questions / VI Big O (introductory examples), Data Structure Brainstorm (book p. 72)]
algorithms: [binary-heap, problem-solving-techniques]
difficulty: high
---

# Running Median

## Prompt
Numbers are generated randomly and stored in an expanding array. Track the median.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Even count: median is the average of the two middle elements.

## Approaches
- Brainstorm: linked list (poor), sorted array (expensive), balanced BST (top might be median, even-case awkward), heaps.
- Two heaps: max-heap for the smaller half, min-heap for the larger half; roots are the median candidates; rebalance by moving a root when sizes differ by more than 1.

## Complexity
- Insert O(log n), median O(1).

## Edge cases
- One element, even/odd count.

## Hints
Not covered in the source.

## Related algorithms
[[binary-heap]], [[problem-solving-techniques]]

## Variants
- **CtCI 17.20 Continuous Median (ch. 17 Hard)**: same problem posed as numbers passed to a method; solution is two heaps (max heap for the lower half holding at most one extra element, min heap for the upper half). New value goes to the max heap if it is at most the current median, else to the min heap; then rebalance by moving a top. Median is the top of the larger heap or the average of both tops; O(log n) insert, O(1) median.


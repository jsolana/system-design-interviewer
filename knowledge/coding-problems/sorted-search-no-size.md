---
title: Sorted Search, No Size
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 10 Sorting and Searching, problem 10.4 (p. 150, solution pp. 400-401)]
algorithms: [binary-search]
difficulty: medium
---

# Sorted Search, No Size

## Prompt
A Listy structure has no size method; elementAt(i) is O(1) and returns -1 past the end. Contains sorted positive integers; find index of x.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Only positive ints because -1 is the sentinel.

## Approaches
- Find an upper bound by doubling the index 1,2,4,8... until elementAt is -1 or larger than x: O(log n).
- Binary search between index/2 and index, treating -1 as too big.

## Complexity
O(log n) overall.

## Edge cases
Value beyond the end.

## Hints
Back off exponentially, not linearly.

## Related algorithms
- [[binary-search]]

## Variants
Not covered in the source.

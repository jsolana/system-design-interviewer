---
title: Search in Rotated Sorted Array
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 10 Sorting and Searching, problem 10.3 (p. 150, solution pp. 398-400)]
algorithms: [binary-search]
difficulty: medium
---

# Search in Rotated Sorted Array

## Prompt
A sorted array was rotated an unknown number of times; find an element.

## Examples
find 5 in {15,16,19,20,25,1,3,4,5,7,10,14} returns 8.

## Constraints and clarifying questions
Originally increasing order.

## Approaches
- Binary search where at least one half is normally ordered: if a[left] < a[mid] the left is ordered; check whether x lies in it, else go right. If a[mid] < a[left] the right is ordered; same check.
- If a[left]==a[mid] the half may be all repeats: if a[mid] != a[right] search right, otherwise search both halves.

## Complexity
O(log n) with distinct values; O(n) with many duplicates.

## Edge cases
Duplicates like {2,2,2,3,4,2}; off-by-one errors.

## Hints
Compare x to the ordered half.

## Related algorithms
- [[binary-search]]

## Variants
Not covered in the source.

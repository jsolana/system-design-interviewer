---
title: Smallest K
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.14, solution p. 570]
algorithms: [binary-heap, quickselect, sorting-algorithms]
difficulty: medium
---

# Smallest K

## Prompt
Find the smallest K numbers in an array.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Ask whether the array may be modified (otherwise clone) and about duplicates.

## Approaches
1. Sort and take the first K: O(n log n).
2. Max heap of size K: O(n log K).
3. Selection rank (quickselect): find the Kth smallest in expected O(n), then collect smaller elements; with duplicates partition into less/equal/greater and fill with equal elements last.

## Complexity
Sort O(n log n); heap O(n log K); quickselect expected O(n).

## Edge cases
Duplicates around the threshold; K = 0 or K >= n.

## Hints
Three standard options: sort, heap, partition.

## Related algorithms
[[binary-heap]] [[quickselect]] [[sorting-algorithms]]

## Variants
Not covered in the source.

---
title: Peaks and Valleys
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 10 Sorting and Searching, problem 10.11 (p. 151, solution pp. 413-416)]
algorithms: [sorting-algorithms,two-pointers]
difficulty: medium
---

# Peaks and Valleys

## Prompt
Rearrange an integer array into alternating peaks (>= neighbors) and valleys (<= neighbors).

## Examples
{5,3,1,2,3} becomes {5,1,3,2,3}.

## Constraints and clarifying questions
Any valid arrangement.

## Approaches
- Sort, then swap each pair starting at index 1 stepping by 2: O(n log n).
- Optimal: for each odd index i, swap a[i] with the largest of a[i-1], a[i], a[i+1]. A swap puts a smaller value in a valley so earlier work is not broken. O(n).

## Complexity
O(n).

## Edge cases
Ends of the array.

## Hints
Make peaks right and valleys follow.

## Related algorithms
- [[sorting-algorithms]]
- [[two-pointers]]

## Variants
Not covered in the source.

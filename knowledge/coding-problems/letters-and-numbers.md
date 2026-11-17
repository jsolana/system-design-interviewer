---
title: Letters and Numbers
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.5, solution p. 535]
algorithms: [prefix-sum-hash-map, hash-table]
difficulty: medium
---

# Letters and Numbers

## Prompt
Given an array of letters and digits, find the longest subarray with equal numbers of letters and digits.

## Examples
[A,B,A,A,A,B,B,B,A,B,A,A,B,B,A,A,A,A,A,A] treating letters and numbers as A/B.

## Constraints and clarifying questions
Letters are all alike, numbers are all alike.

## Approaches
1. Brute force: all subarrays, count each, O(N^2) (start with the longest and stop at the first success).
2. Track the running difference (letters - numbers). Whenever the same difference appears at two indices, the elements between are balanced. Keep a hash map difference -> first index; the answer is the farthest pair.

## Complexity
O(N) time and space.

## Edge cases
No balanced subarray; entire array balanced (difference 0 at index -1).

## Hints
Two equal differences mean the slice between them adds equal amounts of each.

## Related algorithms
[[prefix-sum-hash-map]] [[hash-table]]

## Variants
Not covered in the source.

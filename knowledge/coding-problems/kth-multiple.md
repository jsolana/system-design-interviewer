---
title: Kth Multiple of 3, 5, 7
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.9, solution p. 549]
algorithms: [multi-queue-merge]
difficulty: high
---

# Kth Multiple of 3, 5, 7

## Prompt
Find the kth number whose only prime factors are 3, 5 and 7 (not all required). Sequence starts 1, 3, 5, 7, 9, 15, 21.

## Examples
Not covered in the source.

## Constraints and clarifying questions
k-th in sorted order, 1 counts as the first.

## Approaches
1. Brute force: generate 3^a 5^b 7^c for a,b,c up to k, sort: O(k^3 log k).
2. Each term is 3, 5 or 7 times an earlier term; scanning all earlier terms is O(k^2).
3. Three queues: push multiples of earlier terms into queues for 3, 5 and 7; pop the smallest head x; if from the 3-queue add x*3, x*5, x*7; from the 5-queue add x*5, x*7; from the 7-queue add x*7 (this avoids duplicates).

## Complexity
O(k).

## Edge cases
k = 1 (result 1); integer overflow for big k.

## Hints
Think of each value as "pushing" three future values.

## Related algorithms
[[multi-queue-merge]]

## Variants
Not covered in the source.

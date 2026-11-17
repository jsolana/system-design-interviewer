---
title: Shortest Supersequence
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.18, solution p. 595]
algorithms: [precomputation-tables, binary-heap]
difficulty: high
---

# Shortest Supersequence

## Prompt
Given a short array of distinct elements and a long array, find the shortest subarray of the long array containing all short elements in any order.

## Examples
{1,5,9} in {7,5,9,0,2,1,3,5,7,9,1,1,5,8,8,9,7} -> [7, 10].

## Constraints and clarifying questions
Not covered in the source.

## Approaches
1. Brute force: at each start index find the next occurrence of each element (the "closure" is the largest); O(S B^2).
2. Backwards sweeps per needed element give next-occurrence tables: O(SB); keep only a running min row to use O(B) space.
3. Alternative: lists of occurrences per element; repeatedly take min and max of the heads as a candidate range, then advance the list that held the min; a min heap makes that O(B log S).

## Complexity
O(SB) or O(B log S).

## Edge cases
Element missing from the long array; shorter array of size 1.

## Hints
Precompute the next occurrence of every needed value.

## Related algorithms
[[precomputation-tables]] [[binary-heap]]

## Variants
Not covered in the source.

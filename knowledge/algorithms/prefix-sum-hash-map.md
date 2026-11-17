---
title: Prefix counts with a hash map
type: algorithm
aliases: [running difference, balance trick, cumulative difference]
sources: [Cracking the Coding Interview, 6th ed., ch. 17 pp. 186-191 / solutions pp. 530-627]
---

# Prefix counts with a hash map

## Definition
Track a running quantity (count difference or sum) and store the first index where each value occurred; equal values at two indices mean the slice between them has zero net change.

## When to use it
- Longest/shortest subarray with equal counts of two kinds or with a target sum.

## How it works
Walk the array, keeping (count of A - count of B). Store the first index of each difference in a hash map. When a difference repeats at index j and first occurred at i, the subarray i+1..j is balanced; keep the longest.

## Complexity
O(n) time, O(n) space (versus O(n^2) brute force over all subarrays).

## Common pitfalls
- The subarray starts one after the stored index.
- Seed the map with difference 0 at index -1.

## Appears in
[[letters-and-numbers]]

## See also
[[hash-table]], [[recursion]]

---
title: Prefix (running) sum with hash map
type: algorithm
aliases: [running sum, subarray sum equals k, cumulative sum]
sources: [Cracking the Coding Interview 6th ed., ch. 4 solution 4.12]
---

# Prefix sum with hash map

## Definition
Track the running sum along a sequence/path; a contiguous segment ending at y sums to target iff some earlier prefix equals runningSum_y - target.

## When to use it
Count subarrays/paths with a given sum, including negative values.

## How it works
Map runningSum -> count seen. At each element: add `map[run - target]` to the answer; if run == target add 1 (empty prefix); then record run. On trees do DFS and decrement the entry after leaving the node (back out of the change so sibling branches do not see it).

## Complexity
O(N) time; O(N) space (O(log N) for hash table on balanced tree).

## Common pitfalls
Forgetting to undo the map entry on tree backtracking; forgetting the empty prefix.

## Appears in
[[paths-with-sum]]

## See also
[[hash-table]], [[depth-first-search]]

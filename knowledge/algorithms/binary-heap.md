---
title: Binary heap (min-heap / max-heap)
type: algorithm
aliases: [priority queue, min-heap, max-heap]
sources: [Cracking the Coding Interview 6th ed., ch. 17 Hard (pp. 186-191, solutions pp. 530-627); Cracking the Coding Interview 6th ed., ch. 4 (book pp. 103-104); ch. VII data structure brainstorm]
---

# Binary heap

## Definition
Complete binary tree in which every node is smaller (min-heap) or larger (max-heap) than its children; root is the extremum.

## When to use it
Repeated min/max extraction, top-K, running median (max-heap for the lower half, min-heap for the upper half, rebalance sizes by moving a root).

## How it works
- Insert: place at the rightmost bottom spot, bubble up swapping with parent.
- Extract min: remove root, move last element to root, bubble down swapping with the smaller child.
- Peek min O(1).

## Additional uses (CtCI ch. 17)
- Smallest K of n numbers: max heap of size K; if an element is smaller than the root, insert it and remove the root; O(n log K). (Alternatives: sort, quickselect.)
- Running median: max heap holds the lower half, min heap the upper half, max heap may have one extra; new value goes to the max heap if at most the current median, else the min heap; rebalance by moving one element; median = top of the larger heap, or average of both tops.
- Merge-like scans: keep the head of each of S lists in a min heap, pop the min, push the next element of that list (needs list id with the element); makes the shortest-range-covering-all-lists search O(B log S).
- Default priority queues are often min heaps; reverse the comparator for a max heap.

## Complexity
Insert and extract O(log n); peek O(1).

## Common pitfalls
Swapping with the larger child in a min-heap; assuming left/right ordering.

## Appears in
[[running-median]], [[shortest-supersequence]], [[smallest-k]]

## See also
[[binary-search-tree]], [[problem-solving-techniques]]

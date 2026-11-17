---
title: Selection rank (quickselect)
type: algorithm
aliases: [selection rank, kth smallest, partition]
sources: [Cracking the Coding Interview, 6th ed., ch. 17 pp. 186-191 / solutions pp. 530-627]
---

# Selection rank (quickselect)

## Definition
Find the i-th smallest element in expected O(n) by partitioning around a pivot like quicksort but recursing on one side only.

## When to use it
- K smallest elements, kth element, without full sort.

## How it works
Pick a random pivot, partition (with duplicates use three zones: less, equal, greater). If the left side has exactly i elements return; if larger recurse left; else recurse right with i reduced by left and middle sizes. After finding the threshold value copy elements below it first and fill the rest with elements equal to it.

## Complexity
Expected O(n), worst case O(n^2); modifies the array (clone if not allowed).

## Common pitfalls
- Duplicates break the two-way partition.
- Filling the output with equal elements before smaller ones.

## Appears in
[[smallest-k]]

## See also
[[binary-heap]], [[recursion]]

---
title: Dynamic array (ArrayList, resizable array)
type: algorithm
aliases: [ArrayList, vector, resizable array]
sources: [Cracking the Coding Interview 6th ed., ch. 1 (book p. 89)]
---

# Dynamic array

## Definition
Array that grows automatically: when full, allocate a new array of double capacity and copy elements.

## When to use it
Default list structure when size is unknown and random access is needed.

## How it works
Each doubling copies n/2 + n/4 + ... + 1 < n elements, so N inserts cost O(N) total.

## Complexity
Access O(1); append O(1) amortized (O(N) worst case on resize); insert/delete in the middle O(N).

## Common pitfalls
Calling append that copies the whole array each time (O(n^2) overall). Resize factor and name vary by language.

## Appears in
None yet.

## See also
[[big-o-analysis]], [[string-builder]]

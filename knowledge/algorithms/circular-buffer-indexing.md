---
title: Circular array with rotation offset
type: algorithm
aliases: [rotating array, ring buffer indexing]
sources: [Cracking the Coding Interview, 6th ed., ch. 17 pp. 186-191 / solutions pp. 530-627]
---

# Circular array with rotation offset

## Definition
Represent an array that can be rotated in O(1) by storing a head offset instead of moving elements.

## When to use it
- Efficient rotation; iteration over a rotated view.

## How it works
Keep head index. Logical index i maps to (head + i) mod length. Rotating right by k changes head by -k (add length to avoid negative mod results). All methods go through a single convert function. For iteration implement an iterator that visits convert(0..n-1).

## Complexity
Rotate O(1), access O(1), iterate O(n).

## Common pitfalls
- Negative values with the % operator.
- Generic array creation limitations in Java.
- hasNext/next order in for-each loops.

## Appears in
[[circular-array]]

## See also
[[recursion]]

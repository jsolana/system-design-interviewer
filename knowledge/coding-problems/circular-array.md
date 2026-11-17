---
title: Circular Array
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 7 OOD (pp. 125-129), solutions pp. 329-341 (problem 7.9)]
algorithms: [circular-buffer-indexing]
difficulty: medium
---

# Circular Array

## Prompt
Implement a generic CircularArray that can be rotated efficiently and supports for-each iteration. Problem 7.9.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Generic type; iteration via the standard for (Obj o : circularArray) notation.

## Approaches
1. Shifting all elements on each rotate costs O(n).
2. Keep a head offset: logical index i is physical (head + i) mod length; rotate just changes head. Route every access through one convert function (add length when the offset is negative, since % can return negatives).
3. Iteration: make the class iterable and write an iterator walking convert(0..n-1); mind that for-each calls hasNext before next.

## Complexity
Rotate and get O(1); full iteration O(n).

## Edge cases
Rotation larger than the length or negative; empty array; generic arrays cannot be created directly in Java (cast or use List<T>).

## Hints
Never move elements; move the notion of "start".

## Related algorithms
[[circular-buffer-indexing]]

## Variants
Not covered in the source.

---
title: Fisher-Yates shuffle (perfect shuffle)
type: algorithm
aliases: [random permutation, in-place shuffle]
sources: [Cracking the Coding Interview, 6th ed., ch. 17 pp. 186-191 / solutions pp. 530-627]
---

# Fisher-Yates shuffle (perfect shuffle)

## Definition
In-place algorithm producing every permutation of an array with equal probability.

## When to use it
- "Shuffle a deck so all 52! orderings are equally likely."
- Placing K items randomly in a grid without retries (shuffle then take the first K).

## How it works
Base case and build: if you can shuffle the first n-1 elements, shuffle them, then swap element n-1 with a random index in [0, n-1]. Iteratively: for i from 0 to n-1, swap array[i] with array[random(0..i)] (or random between i and n-1 going forward).

## Complexity
O(n) time, O(1) extra space (assuming a perfect random generator).

## Common pitfalls
- Picking the random index over the whole array each time biases the result.
- Off-by-one in inclusive ranges.

## Appears in
[[shuffle-a-deck]]

## See also
[[reservoir-sampling]], [[recursion]]

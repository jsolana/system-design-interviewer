---
title: Multi-queue merge generation
type: algorithm
aliases: [k-way ordered generation, ugly numbers style generation]
sources: [Cracking the Coding Interview, 6th ed., ch. 17 pp. 186-191 / solutions pp. 530-627]
---

# Multi-queue merge generation

## Definition
Generate an ordered sequence in which each new element is a constant multiple of an earlier element, using one FIFO queue per multiplier.

## When to use it
- "kth number whose only prime factors are 3, 5, 7."

## How it works
Every term is 3, 5 or 7 times an earlier term. Keep queues Q3, Q5, Q7 seeded with 3, 5, 7. Repeatedly take the smallest head x; append x*3, x*5, x*7 to Q3, Q5, Q7 if x came from Q3; only x*5 and x*7 if it came from Q5; only x*7 if from Q7. This avoids duplicates, since the omitted products were already inserted via a different path. Stop after k terms.

## Complexity
O(k) time and space (versus O(k^3 log k) brute force and O(k^2) pull-from-all).

## Common pitfalls
- Duplicates (3*5 vs 5*3) unless the queue-skipping rule is applied.
- Integer overflow for large k.

## Appears in
[[kth-multiple]]

## See also
[[binary-heap]], [[recursion]]

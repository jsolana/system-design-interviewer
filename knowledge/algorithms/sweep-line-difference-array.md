---
title: Difference Array / Sweep Line over Events
type: algorithm
aliases: [prefix sum of deltas, event counting]
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate (pp. 181-185, solutions)]
---

# Difference Array / Sweep Line over Events

## Definition
Record +1/-1 events at interval endpoints and take a running sum to know how many intervals overlap at each point.

## When to use it
Max number of overlapping intervals, e.g. year with most people alive.

## How it works
Increment delta[birth], decrement delta[death+1] (death year is inclusive), then running sum; max over years. Alternative: sort births and deaths and merge-walk, counting a birth before a death in the same year.

## Complexity
O(P + R) with a difference array (R = range); O(P log P) with sorting.

## Common pitfalls
Using death instead of death+1; array size max-min+1 (101 for 1900-2000, plus one for death+1).

## Appears in
[[living-people]]

## See also
- [[sorting-algorithms]]

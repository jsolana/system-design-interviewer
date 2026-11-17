---
title: Boyer-Moore majority vote
type: algorithm
aliases: [majority element, candidate and counter]
sources: [Cracking the Coding Interview, 6th ed., ch. 17 pp. 186-191 / solutions pp. 530-627]
---

# Boyer-Moore majority vote

## Definition
Find an element appearing more than half the time in O(n) time and O(1) space with one counter.

## When to use it
- Majority element with O(1) space.

## How it works
Pass 1: keep a candidate and count; if count is 0 take the current element as candidate; increment on equal, decrement on different. Any prefix where the candidate stops being a majority contains no majority and can be discarded without changing the overall majority. Pass 2: validate the candidate by counting it (there may be no majority).

## Complexity
O(n) time, O(1) space.

## Common pitfalls
- Forgetting the validation pass when a majority may not exist.

## Appears in
[[majority-element]]

## See also
[[two-pointers]], [[recursion]]

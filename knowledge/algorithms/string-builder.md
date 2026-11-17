---
title: StringBuilder (efficient string concatenation)
type: algorithm
aliases: [string buffer, string joining]
sources: [Cracking the Coding Interview 6th ed., ch. 1 (book pp. 89-90)]
---

# StringBuilder

## Definition
A resizable buffer for building strings so that concatenation does not copy the whole string every time.

## When to use it
Building a string in a loop (compression, joining words, URL encoding).

## How it works
Naive `s = s + w` copies the growing string each iteration: x + 2x + ... + nx = O(x*n^2) for n strings of length x. A StringBuilder appends into a [[dynamic-array]] of characters and copies once at the end: O(total length). Pre-sizing capacity avoids resize doubling.

## Complexity
O(total length) vs O(x*n^2) naive.

## Common pitfalls
Strings immutable in many languages; hidden quadratic cost in loops.

## Appears in
[[string-compression]]

## See also
[[dynamic-array]], [[big-o-analysis]]

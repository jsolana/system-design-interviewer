---
title: Random subset selection (reservoir-style)
type: algorithm
aliases: [random sample of m from n, random set]
sources: [Cracking the Coding Interview, 6th ed., ch. 17 pp. 186-191 / solutions pp. 530-627]
---

# Random subset selection (reservoir-style)

## Definition
Choose m elements from n so each element has the same probability m/n, using a single pass.

## When to use it
- "Randomly generate a set of m integers from an array of size n, each equally likely."

## How it works
Fill the subset with the first m elements. For each later index i (m to n-1) pick random k in [0, i]; if k < m replace subset[k] with array[i]. Justification by induction: a subset of size m from the first n-1, then array[n] enters with probability m/(n+1), evicting a random member.

## Complexity
O(n) time, O(m) space.

## Common pitfalls
- Using random(0, i) exclusive vs inclusive.
- Not copying the first m elements before the loop.

## Appears in
[[random-subset]]

## See also
[[fisher-yates-shuffle]], [[recursion]]

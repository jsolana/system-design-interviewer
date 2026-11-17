---
title: Multi Search
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.17, solution p. 578]
algorithms: [trie]
difficulty: high
---

# Multi Search

## Prompt
Given a string b and an array T of smaller strings, find all occurrences of each small string in b.

## Examples
b = mississippi, T = {is, ppi, hi, sis, i, ssippi}

## Constraints and clarifying questions
Not covered in the source.

## Approaches
1. Search each small string at each offset: O(kbt).
2. Build a suffix trie of b: O(b^2) to build, O(kt) to query.
3. Put the small strings into a trie and, for each start index of b, walk the trie, recording each terminal node: O(kt + bk).

## Complexity
O(kt + bk) best (k longest small string, t strings, b length of b).

## Edge cases
Overlapping matches; small string longer than b.

## Hints
Search all small strings at once.

## Related algorithms
[[trie]]

## Variants
Not covered in the source.

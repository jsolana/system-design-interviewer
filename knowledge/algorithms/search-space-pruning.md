---
title: Brute Force to Optimized: Pruning the Search Space
type: algorithm
aliases: [reduce enumeration]
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate (pp. 181-185, solutions)]
---

# Brute Force to Optimized: Pruning the Search Space

## Definition
Start from brute force, then use constraints to determine unknowns instead of iterating them.

## When to use it
String pattern matching with two unknown substrings, diving board, similar enumerations.

## How it works
Pattern matching 'aabab' against a string: brute force tries all substrings for a and b (O(n^4) candidates, O(n^5) with comparison). Once a's length is chosen, b's length is determined from remaining length / count of b, and its position from the first b in the pattern, so only O(n) choices remain: O(n^2) total; compare in place to short-circuit early. Diving board: only the count of each plank type matters, K+1 combinations, O(K).

## Complexity
See problems.

## Common pitfalls
Forgetting patterns with only one letter (zero count) or empty strings.

## Appears in
[[diving-board]], [[pattern-matching]]

## See also
- [[hash-table]]

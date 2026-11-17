---
title: Pattern Matching (a/b Pattern)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.18 (p. 183)]
algorithms: [search-space-pruning,hash-table]
difficulty: high
---

# Pattern Matching (a/b Pattern)

## Prompt
Given pattern of a and b and a value string, decide if value can be formed by substituting strings for a and b consistently.

## Examples
catcatgocatgo matches aabab (a=cat, b=go) and also a, ab, b.

## Constraints and clarifying questions
Pattern may consist of a single letter.

## Approaches
- Brute force over all substrings for a and b: O(n^5) with the build/compare; fixing a to start at index 0 gives O(n^4).
- Choose length of the main string; the alternate length is then determined by remaining length / count of alternate; so O(n) candidates, each built and compared in O(n): O(n^2).
- Compare in place instead of building a string to short-circuit on failure.

## Complexity
O(n^2).

## Edge cases
Only one letter used; empty pattern.

## Hints
Once a is chosen, b is determined.

## Related algorithms
- [[search-space-pruning]]
- [[hash-table]]

## Variants
Not covered in the source.

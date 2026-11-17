---
title: Check Permutation
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 1 Arrays and Strings, problem 1.2]
algorithms: [character-counting, sorting-algorithms]
difficulty: low
---

# Check Permutation

## Prompt
Given two strings, decide whether one is a permutation of the other.

## Examples
- "god" vs "dog" -> true; case-sensitive "God" vs "dog" -> false (assumed)

## Constraints and clarifying questions
- Case sensitive? Whitespace significant? (book assumes yes to both). Charset size.

## Approaches
- Different lengths -> false immediately.
- Sort both and compare: clean, O(n log n).
- Count characters of one string in an array; decrement for the other and fail on negative: O(n).

## Complexity
- Sort: O(n log n); count array: O(n) time, O(c) space.

## Edge cases
- Different lengths, empty strings.

## Hints
Not covered in the source.

## Related algorithms
[[character-counting]], [[sorting-algorithms]]

## Variants


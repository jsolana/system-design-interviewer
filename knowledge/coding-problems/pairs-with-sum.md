---
title: Pairs with Sum
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.24 (p. 185)]
algorithms: [hash-table,two-pointers,sorting-algorithms]
difficulty: medium
---

# Pairs with Sum

## Prompt
Find all pairs of integers in an array that sum to a value.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Duplicates: should the same pair print twice? Clarify.

## Approaches
- Brute force O(N^2).
- Hash map of unpaired counts: for x look for complement sum - x with count > 0, pair and decrement, else increment x. O(N) time and space.
- Sort and two pointers from both ends: O(N log N), O(1) extra.

## Complexity
O(N) or O(N log N).

## Edge cases
Duplicates reuse.

## Hints
Complement = target - x.

## Related algorithms
- [[hash-table]]
- [[two-pointers]]
- [[sorting-algorithms]]

## Variants
Not covered in the source.

---
title: Diving Board
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.11 (p. 182)]
algorithms: [recursion,dynamic-programming,search-space-pruning]
difficulty: low
---

# Diving Board

## Prompt
Use exactly K planks, each shorter or longer; produce all possible lengths.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Two plank lengths.

## Approaches
- Recurse over K choices: O(2^K).
- Memoize on (planks used, total) - not total alone: O(K^2).
- Only the count of each type matters: for i in 0..K of shorter planks, length = i*shorter + (K-i)*longer. O(K).

## Complexity
O(K).

## Edge cases
shorter equals longer gives one length.

## Hints
Order does not matter.

## Related algorithms
- [[recursion]]
- [[dynamic-programming]]
- [[search-space-pruning]]

## Variants
Not covered in the source.

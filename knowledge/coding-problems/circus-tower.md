---
title: Circus Tower
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.8, solution p. 546]
algorithms: [dynamic-programming, sorting-algorithms]
difficulty: high
---

# Circus Tower

## Prompt
People must stack so each is both shorter and lighter than the one below. Given heights and weights compute the largest tower.

## Examples
(65,100) (70,150) (56,90) (75,190) (60,95) (68,110) -> 6 people.

## Constraints and clarifying questions
Strictly smaller in both dimensions.

## Approaches
1. Sort by height, so the problem becomes the longest increasing subsequence on weight.
2. Brute force take/skip recursion: O(2^n); memoize to speed up.
3. Better: for each element keep the longest valid sequence ending there (extend the best earlier compatible one): O(n^2). An O(n log n) algorithm exists but is unlikely to be derived in an interview.

## Complexity
O(n^2) time.

## Edge cases
Ties in height (sort tie-break); all equal.

## Hints
Sort on one attribute, then you only handle the other.

## Related algorithms
[[dynamic-programming]] [[sorting-algorithms]]

## Variants
Not covered in the source.

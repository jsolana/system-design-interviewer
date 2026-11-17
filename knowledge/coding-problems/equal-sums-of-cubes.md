---
title: Equal Sums of Cubes (a^3+b^3 = c^3+d^3)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. VII Technical Questions / VI Big O (introductory examples), BUD example (book pp. 68-69)]
algorithms: [hash-table, problem-solving-techniques]
difficulty: medium
---

# Equal Sums of Cubes (a^3+b^3 = c^3+d^3)

## Prompt
Print all positive integer solutions of a^3 + b^3 = c^3 + d^3 where a,b,c,d are in 1..n.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- n = 1000 in the example.

## Approaches
- Brute force 4 nested loops: O(N^4).
- Unnecessary work: break after finding d; better compute d = cbrt(a^3+b^3-c^3) and validate: O(N^3).
- Duplicated work: precompute all (c,d) pairs in a hash map keyed by c^3+d^3; for each (a,b) look up the list: O(N^2). Even simpler: for each key, pair every two pairs in its list.

## Complexity
- O(N^2) time and space.

## Edge cases
- Validate the rounded cube root.

## Hints
Not covered in the source.

## Related algorithms
[[hash-table]], [[problem-solving-techniques]]

## Variants


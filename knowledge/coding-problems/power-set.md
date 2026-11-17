---
title: Power Set (All Subsets)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 8 Recursion and Dynamic Programming, problem 8.4 (p. 135, solution pp. 347-349)]
algorithms: [recursion,backtracking,bit-manipulation]
difficulty: medium
---

# Power Set (All Subsets)

## Prompt
Return all subsets of a set.

## Examples
{a1,a2,a3} gives {}, {a1}, {a2}, {a3}, {a1,a2}, {a1,a3}, {a2,a3}, {a1,a2,a3}.

## Constraints and clarifying questions
Not covered in the source.

## Approaches
- Output size: 2^n subsets, n*2^(n-1) elements in total, so O(n*2^n) is the lower bound.
- Recursion (base case and build): P(0)={{}}; P(n) = P(n-1) plus a copy of each subset with element n added.
- Combinatorial: each element is in or out, so subsets correspond to binary numbers 0..2^n-1; map set bits to elements.

## Complexity
O(n*2^n) time and space.

## Edge cases
Empty set must be included.

## Hints
P(3)-P(2) are the subsets containing a3.

## Related algorithms
- [[recursion]]
- [[backtracking]]
- [[bit-manipulation]]

## Variants
Not covered in the source.

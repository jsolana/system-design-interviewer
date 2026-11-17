---
title: Random Set of m Integers
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.3, solution p. 532]
algorithms: [reservoir-sampling, recursion]
difficulty: medium
---

# Random Set of m Integers

## Prompt
Randomly generate a set of m integers from an array of size n, with every element equally likely to be chosen.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Equal probability for each element.

## Approaches
1. Recursive: take a random m-subset of the first n-1 elements; pick k in 0..n; if k < m replace subset[k] with the nth element.
2. Iterative: copy the first m elements, then for each later i pick k in 0..i and replace subset[k] when k < m.

## Complexity
O(n) time, O(m) space.

## Edge cases
m = n; m = 0.

## Hints
Same structure as the shuffle problem.

## Related algorithms
[[reservoir-sampling]] [[recursion]]

## Variants
Not covered in the source.

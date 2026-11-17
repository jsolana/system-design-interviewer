---
title: Max Black Square
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.23, solution p. 603]
algorithms: [precomputation-tables]
difficulty: high
---

# Max Black Square

## Prompt
In an NxN matrix of black/white pixels find the largest subsquare whose four borders are all black.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Only the border has to be black.

## Approaches
1. Try sizes from N downward; for each placement check the border in O(N): O(N^4).
2. Precompute for each cell the count of consecutive black cells to the right and below (bottom-right sweep); a candidate's four edges are then validated in O(1): O(N^3).

## Complexity
O(N^3).

## Edge cases
No black pixel; whole matrix black.

## Hints
Make the "is this a valid square" check constant time.

## Related algorithms
[[precomputation-tables]]

## Variants
Not covered in the source.

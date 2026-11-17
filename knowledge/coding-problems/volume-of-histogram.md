---
title: Volume of Histogram (Trapping Rain Water)
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.21, solution p. 596]
algorithms: [precomputation-tables]
difficulty: high
---

# Volume of Histogram (Trapping Rain Water)

## Prompt
Given a histogram of bars of width 1, compute the volume of water it holds if poured on top.

## Examples
{0,0,4,0,0,6,0,0,3,0,5,0,1,0,0,0} -> 26

## Constraints and clarifying questions
Not covered in the source.

## Approaches
1. Recursive by tallest bar: water to the left/right controlled by the second tallest, O(N^2).
2. Precompute for each index the max to its left and right: O(N).
3. Simplest: water above bar i = min(leftMax, rightMax) - height[i]; one forward sweep for left maxes, one backward sweep tracking the right max while summing.

## Complexity
O(N) time.

## Edge cases
Monotone bars; fewer than 3 bars (no water).

## Hints
Water at a bar is determined by the shorter of the tallest bars on each side.

## Related algorithms
[[precomputation-tables]]

## Variants
Not covered in the source.

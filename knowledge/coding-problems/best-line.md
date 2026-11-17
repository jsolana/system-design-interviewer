---
title: Best Line
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.14 (p. 183)]
algorithms: [hash-table,computational-geometry]
difficulty: high
---

# Best Line

## Prompt
Given points on a plane, find a line that passes through the most points.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Float precision.

## Approaches
- For every pair of points compute the line (slope, intercept), count equal lines in a hash map: O(N^2). Because floating-point equality is unreliable, key by slope floored to an epsilon and check the neighboring buckets.

## Complexity
O(N^2).

## Edge cases
Vertical lines (flag infinite slope, use x-intercept).

## Hints
Not covered in the source.

## Related algorithms
- [[hash-table]]
- [[computational-geometry]]

## Variants
Not covered in the source.

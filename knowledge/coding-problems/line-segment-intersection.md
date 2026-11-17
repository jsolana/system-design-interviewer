---
title: Line Segment Intersection
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.3 (p. 181)]
algorithms: [computational-geometry]
difficulty: medium
---

# Line Segment Intersection

## Prompt
Given two line segments (start and end points), find their intersection point, if any.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Vertical and parallel segments.

## Approaches
- Order endpoints by x. Compute slope and y-intercept for each. Different slopes: intersection x = (b2-b1)/(m1-m2); check the point lies within both segments. Same slope: need the same intercept and overlap (start2 between start1 and end1).

## Complexity
O(1).

## Edge cases
Vertical lines, parallel overlapping segments.

## Hints
Not covered in the source.

## Related algorithms
- [[computational-geometry]]

## Variants
Not covered in the source.

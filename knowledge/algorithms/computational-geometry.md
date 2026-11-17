---
title: Computational Geometry Basics
type: algorithm
aliases: [line intersection, slopes]
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate (pp. 181-185, solutions)]
---

# Computational Geometry Basics

## Definition
Handling lines and segments with slope, intercept and boundary checks.

## When to use it
Segment intersection, bisecting shapes, lines through the most points.

## How it works
Two infinite lines intersect iff slopes differ (or same slope and same intercept = same line). For segments also check the intersection lies within both ranges; for collinear segments check overlap after ordering by x. Vertical lines have infinite slope (flag separately; use x-intercept). Two squares are bisected by the line through their centers; extend it to each square's edge depending on whether slope is steep or shallow. Best line: O(N^2) pairs counted in a hash map using epsilon-floored slopes, checking neighboring buckets.

## Complexity
O(1) per pair; best line O(N^2).

## Common pitfalls
Floating-point equality (use epsilon), division by zero for vertical lines, same-center squares.

## Appears in
[[best-line]], [[bisect-squares]], [[line-segment-intersection]]

## See also
- [[hash-table]]

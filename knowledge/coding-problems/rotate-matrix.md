---
title: Rotate Matrix
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 1 Arrays and Strings, problem 1.7]
algorithms: [in-place-matrix-operations]
difficulty: medium
---

# Rotate Matrix

## Prompt
Rotate an NxN image (4 bytes per pixel) by 90 degrees, ideally in place.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Direction of rotation; in place?

## Approaches
- Rotate layer by layer: for each layer, for each offset do a 4-way cyclic swap (save top; left->top, bottom->left, right->bottom, saved top->right). No extra array.

## Complexity
- O(N^2) time (optimal: every cell moves), O(1) space.

## Edge cases
- N = 1, odd N (center fixed), non-square (invalid).

## Hints
Not covered in the source.

## Related algorithms
[[in-place-matrix-operations]]

## Variants


---
title: Check Balanced
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 4 Trees and Graphs, problem 4.4]
algorithms: [recursion, tree-traversal]
difficulty: low
---

# Check Balanced

## Prompt
Check whether a binary tree is balanced: heights of the two subtrees of any node differ by at most one.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Not covered in the source.

## Approaches
- Compute heights recursively at every node: O(N log N) because getHeight repeats work.
- Combine: checkHeight returns the height or an error sentinel (Integer.MIN_VALUE; null height is -1) if unbalanced; abort immediately on error.

## Complexity
- O(N) time, O(H) space.

## Edge cases
- Empty tree, skewed tree.

## Hints
Not covered in the source.

## Related algorithms
[[recursion]], [[tree-traversal]]

## Variants


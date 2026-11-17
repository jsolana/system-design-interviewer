---
title: Check Subtree
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 4 Trees and Graphs, problem 4.10]
algorithms: [tree-traversal, recursion]
difficulty: medium
---

# Check Subtree

## Prompt
T1 is huge, T2 is smaller. Check whether T2 is a subtree of T1 (some node of T1 has an identical subtree).

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Memory matters for huge trees.

## Approaches
- Pre-order serialization with null markers (e.g. X) uniquely identifies a tree; T2 is a subtree iff its string is a substring of T1 string. In-order alone does not work. O(n+m) time and space.
- Search T1 for nodes equal to T2 root and run a matchTree comparison: O(n + k*m) time, O(log n + log m) space (k = occurrences of the root value).

## Complexity
- See approaches.

## Edge cases
- Empty T2 (always subtree), repeated values.

## Hints
Not covered in the source.

## Related algorithms
[[tree-traversal]], [[recursion]]

## Variants


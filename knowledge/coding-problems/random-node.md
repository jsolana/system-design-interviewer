---
title: Random Node in BST
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 4 Trees and Graphs, problem 4.11]
algorithms: [binary-search-tree, recursion]
difficulty: high
---

# Random Node in BST

## Prompt
Implement a binary tree class with insert, find, delete and getRandomNode (all nodes equally likely).

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- You control the class internals.

## Approaches
- Copy to array each call: O(N). Maintain an array: delete O(N). Index labels: O(N) updates.
- Wrong: random depth, or random walk with equal 1/3 odds (not uniform).
- Correct: store subtree size in every node. Pick i in [0, size); if i < leftSize go left; if i == leftSize return node; else go right with i - leftSize - 1. A single random call suffices. O(depth).

## Complexity
- O(log N) balanced, O(D) in general.

## Edge cases
- Empty tree, size upkeep on delete.

## Hints
Not covered in the source.

## Related algorithms
[[binary-search-tree]], [[recursion]]

## Variants


---
title: Paths with Sum
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 4 Trees and Graphs, problem 4.12]
algorithms: [prefix-sum, hash-table, depth-first-search]
difficulty: high
---

# Paths with Sum

## Prompt
Count downward paths (any start/end node, parent to child only) in a binary tree whose node values sum to a target. Values can be negative.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Paths need not start at root or end at leaf.

## Approaches
- Brute force: from every node, try all downward paths: O(N log N) balanced, O(N^2) skewed.
- Optimized: running sum from the root; map of running sums seen on the current root-to-node path; at each node add map[run - target] (+1 if run == target); recurse; then remove this node run sum from the map.

## Complexity
- O(N) time; O(log N) space balanced, O(N) skewed.

## Edge cases
- Negative values, target zero.

## Hints
Not covered in the source.

## Related algorithms
[[prefix-sum]], [[hash-table]], [[depth-first-search]]

## Variants


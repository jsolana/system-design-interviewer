---
title: Build Order
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 4 Trees and Graphs, problem 4.7]
algorithms: [topological-sort, graph-representations, depth-first-search]
difficulty: medium
---

# Build Order

## Prompt
Given projects and dependency pairs (a, d) meaning d depends on a, find a valid build order or report an error.

## Examples
- projects a..f, deps (a,d),(f,b),(b,d),(f,a),(d,c) -> f, e, a, b, d, c

## Constraints and clarifying questions
- Cycle means no valid order. Include projects without dependencies.

## Approaches
- Kahn: build graph with in-degree counts; repeatedly add zero-in-degree nodes to the order and decrement children; leftover nodes mean a cycle.
- DFS: finish a node after its children, adding it to the front of the order; states BLANK/PARTIAL/COMPLETE detect cycles.

## Complexity
- O(P + D).

## Edge cases
- Cycle, isolated projects, multiple valid orders.

## Hints
Not covered in the source.

## Related algorithms
[[topological-sort]], [[graph-representations]], [[depth-first-search]]

## Variants


---
title: Route Between Nodes
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 4 Trees and Graphs, problem 4.1]
algorithms: [breadth-first-search, depth-first-search, graph-representations]
difficulty: low
---

# Route Between Nodes

## Prompt
Given a directed graph, find whether there is a route between two nodes.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Directed edges; cycles possible.

## Approaches
- Traverse from one node with BFS or DFS, marking visited nodes, until the other is found. DFS is simpler (recursion); BFS finds shortest paths.
- Bidirectional search is an option for long routes.

## Complexity
- O(V+E).

## Edge cases
- Same node, disconnected graph, cycles.

## Hints
Not covered in the source.

## Related algorithms
[[breadth-first-search]], [[depth-first-search]], [[graph-representations]]

## Variants


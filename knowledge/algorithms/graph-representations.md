---
title: Graph representations (adjacency list and matrix)
type: algorithm
aliases: [graph, adjacency list, adjacency matrix]
sources: [Cracking the Coding Interview 6th ed., ch. 4 (book pp. 105-107)]
---

# Graph representations

## Definition
A graph is nodes with edges (directed or undirected, possibly several components, cyclic or acyclic). A tree is a connected acyclic graph. "Connected" means a path exists between every pair of vertices.

## When to use it
Dependencies, networks, routes, social links; any "relationships between items" problem.

## How it works
- **Adjacency list** (most common): each node stores its neighbors (node class, or array/hash of lists). Undirected edge stored twice. Needs a Graph class since not all nodes are reachable from one node.
- **Adjacency matrix**: NxN booleans, `m[i][j]` = edge i->j; symmetric if undirected. Finding neighbors needs scanning a row.

## Complexity
List: O(V+E) space, neighbor iteration O(deg). Matrix: O(V^2) space, neighbors O(V).

## Common pitfalls
Direction of arrows (be explicit: A->B means A must come first); forgetting visited flags (infinite loops).

## Appears in
[[build-order]], [[route-between-nodes]]

## See also
[[depth-first-search]], [[breadth-first-search]], [[topological-sort]]

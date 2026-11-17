---
title: Breadth-first search (BFS)
type: algorithm
aliases: [BFS, level-order traversal]
sources: [Cracking the Coding Interview 6th ed., ch. 4 (book pp. 107-108)]
---

# Breadth-first search

## Definition
Visit all neighbors of a node before their children; uses a queue (it is not recursive).

## When to use it
Shortest path (unweighted), any path between two nodes, closest-first exploration, level-order tree traversal (e.g. list of nodes per depth).

## How it works
Mark root, enqueue. While queue not empty: dequeue r; for each unmarked neighbor: mark, enqueue. Mark when enqueuing to avoid duplicates. For levels, process level i-1's children to get level i.

## Complexity
O(V+E) time; O(V) queue space.

## Common pitfalls
Trying to implement recursively; forgetting visited.

## Appears in
[[list-of-depths]], [[route-between-nodes]], [[word-transformer]]

## See also
[[depth-first-search]], [[bidirectional-search]], [[stack-and-queue]]

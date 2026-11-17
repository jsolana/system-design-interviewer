---
title: Doubly Linked List
type: algorithm
aliases: [linked list with prev pointers]
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate (pp. 181-185, solutions)]
---

# Doubly Linked List

## Definition
List nodes with next and prev pointers allowing O(1) removal of a known node from the middle.

## When to use it
Need quick reordering plus quick access by key (LRU cache: list for recency order, hash map for lookup).

## How it works
Insert at head, remove node by relinking neighbors, update head/tail; the map stores node references so moving a node to the front needs no map update.

## Complexity
O(1) insert/remove given the node.

## Common pitfalls
Forgetting head/tail updates on removal; forgetting to remove the evicted key from the map.

## Appears in
[[lru-cache]]

## See also
- [[hash-table]]

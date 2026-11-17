---
title: LRU Cache
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.25 (p. 185)]
algorithms: [hash-table,doubly-linked-list]
difficulty: high
---

# LRU Cache

## Prompt
Design a least-recently-used cache mapping integer keys to string values with a max size.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Operations: insert, get, evict LRU when full.

## Approaches
- Hash map alone cannot find the LRU; list alone cannot look up by key.
- Combine: hash map key -> node of a doubly linked list ordered by recency. get: lookup node, move to front. set: remove old key, evict tail if full (remove from map too), insert at head. All O(1).

## Complexity
O(1) per operation.

## Edge cases
Updating existing key; capacity one.

## Hints
Keep head and tail updated.

## Related algorithms
- [[hash-table]]
- [[doubly-linked-list]]

## Variants
Not covered in the source.

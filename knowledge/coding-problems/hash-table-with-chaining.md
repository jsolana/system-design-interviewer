---
title: Hash Table with Chaining
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 7 OOD (pp. 125-129), solutions pp. 329-341 (problem 7.12)]
algorithms: [hash-table]
difficulty: medium
---

# Hash Table with Chaining

## Prompt
Design and implement a hash table that handles collisions with chaining (linked lists). Problem 7.12.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Generic key and value types Hash<K, V>.

## Approaches
1. An array of linked lists holding only values fails: after a collision (two keys mapping to the same index) you cannot tell which value belongs to which key.
2. Store a cell pairing key and value in each list node; index = hash(key) mod capacity; put replaces an existing key or appends; get scans the chain comparing keys; remove unlinks a cell.
3. Alternative: use a balanced binary search tree as the backing store: O(log n) lookups but no need for a very large array.

## Complexity
Average O(1) put/get/remove; worst O(n) when many keys collide.

## Edge cases
Null keys; negative hash codes; resizing the array (rehash).

## Hints
What do you need to store in each node to resolve a collision?

## Related algorithms
[[hash-table]]

## Variants
Not covered in the source.

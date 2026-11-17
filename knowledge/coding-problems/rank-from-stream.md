---
title: Rank from Stream
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 10 Sorting and Searching, problem 10.10 (p. 151, solution pp. 410-412)]
algorithms: [binary-search-tree]
difficulty: medium
---

# Rank from Stream

## Prompt
Numbers arrive in a stream. Implement track(x) and getRankOfNumber(x) returning the count of values <= x (excluding x itself).

## Examples
Stream 5,1,4,4,5,9,7,13,3: rank(1)=0, rank(3)=1, rank(4)=3.

## Constraints and clarifying questions
Rank of an unseen value returns -1 in the book's version.

## Approaches
- Sorted array with binary search: fast rank, O(n) insert.
- Binary search tree with left-subtree sizes: track is an insert, rank accumulates left_size+1 when going right.

## Complexity
O(log n) balanced, O(n) unbalanced.

## Edge cases
Value absent; duplicates.

## Hints
Store left size at each node.

## Related algorithms
- [[binary-search-tree]]

## Variants
Not covered in the source.

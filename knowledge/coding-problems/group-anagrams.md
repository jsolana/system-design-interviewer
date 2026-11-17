---
title: Group Anagrams
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 10 Sorting and Searching, problem 10.2 (p. 150, solution pp. 397-398)]
algorithms: [hash-table,sorting-algorithms]
difficulty: low
---

# Group Anagrams

## Prompt
Sort an array of strings so anagrams are adjacent.

## Examples
acre, race, care are grouped.

## Constraints and clarifying questions
Only grouping needed, not total order.

## Approaches
- Sort with a comparator comparing the sorted characters of each string: O(n log n) comparisons (times word length costs).
- Better: hash map from sorted-characters key to list of words, then write lists back; a bucket-sort style approach.

## Complexity
O(n * L log L) with the map.

## Edge cases
Empty strings; case.

## Hints
You do not need a full sort.

## Related algorithms
- [[hash-table]]
- [[sorting-algorithms]]

## Variants
Not covered in the source.

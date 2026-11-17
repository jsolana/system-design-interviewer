---
title: Sort a Big File
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 10 Sorting and Searching, problem 10.6 (p. 150, solution p. 403)]
algorithms: [external-sort,sorting-algorithms]
difficulty: medium
---

# Sort a Big File

## Prompt
A 20 GB file with one string per line; explain how to sort it.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Memory is smaller than the file.

## Approaches
- External sort: split into chunks that fit in memory, sort each, write back, then merge the chunks.

## Complexity
O(n log n) compute, sequential I/O.

## Edge cases
Not covered in the source.

## Hints
The size hint means do not load it all.

## Related algorithms
- [[external-sort]]
- [[sorting-algorithms]]

## Variants
Not covered in the source.

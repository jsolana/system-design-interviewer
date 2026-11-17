---
title: External Sort
type: algorithm
aliases: [sorting data larger than memory]
sources: [Cracking the Coding Interview 6th ed., ch. 10 Sorting and Searching (pp. 146-151, solutions pp. 396-416)]
---

# External Sort

## Definition
Sort a dataset too large for memory by sorting chunks that fit in memory and then merging them.

## When to use it
A size hint such as '20 GB file' implies the data cannot be loaded at once.

## How it works
Split the file into chunks of x MB (x = available memory), sort each chunk in memory and write it back, then k-way merge the sorted chunks into the final file.

## Complexity
O(n log n) comparisons plus sequential disk I/O; extra disk space for chunks.

## Common pitfalls
Choosing chunk size larger than memory; random disk access during the merge.

## Appears in
[[sort-big-file]]

## See also
- [[sorting-algorithms]]
- [[bit-vector]]

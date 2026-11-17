---
title: Common Sorting Algorithms
type: algorithm
aliases: [merge sort, quick sort, bucket sort, radix sort, bubble sort, selection sort]
sources: [Cracking the Coding Interview 6th ed., ch. 10 Sorting and Searching (pp. 146-151, solutions pp. 396-416)]
---

# Common Sorting Algorithms

## Definition
Algorithms that order elements; the book stresses knowing merge sort, quick sort and bucket sort.

## When to use it
When asked to sort or when a problem is a tweak of a known sort; scan the algorithms and ask which fits the data (e.g. sorting a huge array of people by age: values in a small range -> bucket/radix sort with one bucket per year).

## How it works
| Algorithm | Time | Memory | Idea |
|---|---|---|---|
| Bubble | O(n^2) avg/worst | O(1) | sweep, swap adjacent out-of-order pairs |
| Selection | O(n^2) | O(1) | repeatedly move the smallest remaining to front |
| Merge | O(n log n) | O(n) with helper array | sort halves, merge; right-half leftovers are already in place |
| Quick | O(n log n) avg, O(n^2) worst | O(log n) | partition around a pivot; bad pivots cause worst case |
| Radix | O(kn) | | group by each digit/bit pass; k = number of passes; beats comparison bound |
| Bucket | | | spread into buckets by value range, sort each; grouping anagrams by sorted key is a bucket-sort variant |
Peak/valley note: sorting then swapping pairs works; see problems.

## Complexity
Comparison sorts cannot beat O(n log n) on average.

## Common pitfalls
Pivot choice; choosing a full sort when only grouping is needed (a hash table keyed by sorted word groups anagrams in less than a full sort).

## Appears in
[[check-permutation]], [[circus-tower]], [[group-anagrams]], [[is-unique]], [[living-people]], [[pairs-with-sum]], [[peaks-and-valleys]], [[smallest-difference]], [[smallest-k]], [[sort-big-file]], [[sort-stack]], [[sorted-merge]]

## See also
- [[external-sort]]
- [[binary-search]]
- [[hash-table]]

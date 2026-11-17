---
title: Sparse Similarity
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.26, solution p. 608]
algorithms: [inverted-index-counting, hash-table]
difficulty: high
---

# Sparse Similarity

## Prompt
Document similarity = |intersection| / |union|. Given many documents where most pairs have similarity 0, list pairs with similarity above 0.

## Examples
13: {14,15,100,9,3}; 16: {32,1,9,3,5}; 19: {15,29,2,6,8,7}; 24: {7,10} -> (13,19,0.1) (13,16,0.25) (19,24,0.142857...).

## Constraints and clarifying questions
Empty documents are not printed; only positive similarity.

## Approaches
1. Brute force: compare every pair via a hash set intersection; union = |A| + |B| - intersection; O(A) per pair after hashing.
2. Sort-based comparison O(A + B) per pair.
3. Build word -> documents; for each word, increment a counter for every pair of documents in its list; only overlapping pairs are touched.
4. Variant: tag words with doc ID and sort, then pair up equal runs.

## Complexity
Proportional to the number of overlapping pairs (worst case as brute force).

## Edge cases
Empty documents; identical documents (similarity 1).

## Hints
Do not look at pairs that share nothing.

## Related algorithms
[[inverted-index-counting]] [[hash-table]]

## Variants
Not covered in the source.

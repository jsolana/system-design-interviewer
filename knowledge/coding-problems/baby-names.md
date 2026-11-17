---
title: Baby Names (Merge Synonyms)
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.7, solution p. 541]
algorithms: [depth-first-search, hash-table]
difficulty: high
---

# Baby Names (Merge Synonyms)

## Prompt
Given name frequencies and a list of pairs of equivalent names (symmetric and transitive), print the true frequency of each name, using any name from a group as its representative.

## Examples
Names: John 15, Jon 12, Chris 13, Kris 4, Christopher 19; Synonyms: (Jon, John), (John, Johnny), (Chris, Kris), (Chris, Christopher) -> John 27, Kris 36 (group sums).

## Constraints and clarifying questions
10,000 names; synonym pairs may chain.

## Approaches
1. Maintain equivalence classes in hash maps; merge sets by copying the smaller into the larger and updating pointers: O(N log N) worst case.
2. Better: build a graph (edge per synonym pair) and sum frequencies per connected component with DFS/BFS using a visited set.

## Complexity
O(B + P) with B names and P pairs (optimal: must read the input).

## Edge cases
Names with no synonyms; names appearing only in the synonym list.

## Hints
Think of the synonym pairs as edges, not as merge operations.

## Related algorithms
[[depth-first-search]] [[hash-table]]

## Variants
Not covered in the source.

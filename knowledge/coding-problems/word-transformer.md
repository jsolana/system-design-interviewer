---
title: Word Transformer (Word Ladder)
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.22, solution p. 602]
algorithms: [breadth-first-search, bidirectional-search]
difficulty: high
---

# Word Transformer (Word Ladder)

## Prompt
Transform one dictionary word into another of equal length by changing one letter at a time, each step being a dictionary word.

## Examples
DAMP -> LAMP -> LIMP -> LIME -> LIKE

## Constraints and clarifying questions
Not covered in the source.

## Approaches
1. DFS over one-letter edits finds a path but not the shortest.
2. Precompute wildcard groups (b_ll -> ball, bill) so neighbors are found without testing all 26 letters at every position.
3. BFS for the shortest path.
4. Bidirectional BFS from both words, merging at the collision; about O(E^(D/2)).

## Complexity
About O(E^(D/2)) with E neighbors per word and distance D.

## Edge cases
Words with no path; identical words.

## Hints
Words are nodes, one-edit words are neighbors.

## Related algorithms
[[breadth-first-search]] [[bidirectional-search]]

## Variants
Not covered in the source.

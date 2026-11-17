---
title: T9 Words
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.20 (p. 184)]
algorithms: [trie,backtracking,hash-table]
difficulty: high
---

# T9 Words

## Prompt
Given a digit sequence and a dictionary, return all words matching the T9 keypad mapping (digits 2-9 map to 3-4 letters).

## Examples
8733 returns used, tree.

## Constraints and clarifying questions
Dictionary data structure is your choice.

## Approaches
- Brute force: recurse over letters of each digit, check each full string against a set: O(4^N).
- Prune with a trie: stop when the prefix is not in the dictionary.
- Precompute a hash map from digit sequence to words by converting every dictionary word; each query is a lookup, O(N).

## Complexity
Query O(N) after preprocessing.

## Edge cases
Digits 0 and 1.

## Hints
Preprocessing is acceptable.

## Related algorithms
- [[trie]]
- [[backtracking]]
- [[hash-table]]

## Variants
Not covered in the source.

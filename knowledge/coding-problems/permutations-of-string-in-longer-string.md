---
title: Find Permutations of a Short String Within a Longer String
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. VII Technical Questions / VI Big O (introductory examples), DIY example (book pp. 69-70)]
algorithms: [two-pointers, problem-solving-techniques, hash-table]
difficulty: medium
---

# Find Permutations of a Short String Within a Longer String

## Prompt
Given shorter string s and longer string b, find (print the location of) all permutations of s within b (contiguous).

## Examples
- s=abbc, b=cbabadcbbabbcbabaabccbabc

## Constraints and clarifying questions
- Permutations must be contiguous.

## Approaches
- Generate all S! permutations and search each: O(S! * B), horrible.
- Slide a window of length |s| over b, test each window as a permutation (count compare): O(B*S) or O(B*S log S).
- The source notes an O(B) solution exists (incremental window counts); not derived there.

## Complexity
- O(B) optimal (stated, not derived).

## Edge cases
- s longer than b.

## Hints
- Solve a big example by hand and reverse-engineer what you did.

## Related algorithms
[[two-pointers]], [[problem-solving-techniques]], [[hash-table]]

## Variants
- Technique: DIY.

---
title: Ransom Note
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. VII Technical Questions / VI Big O (introductory examples), Simplify and Generalize (book p. 71)]
algorithms: [hash-table, character-counting, problem-solving-techniques]
difficulty: low
---

# Ransom Note

## Prompt
Can a ransom note (string) be formed by cutting words out of a magazine (string)?

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Words are cut as units.

## Approaches
- Simplify to characters: count note characters in an array, scan magazine and decrement.
- Generalize to words: hash map word -> frequency.

## Complexity
- O(N+M) time, O(distinct words) space.

## Edge cases
- Empty note.

## Hints
Not covered in the source.

## Related algorithms
[[hash-table]], [[character-counting]], [[problem-solving-techniques]]

## Variants


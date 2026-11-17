---
title: URLify
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 1 Arrays and Strings, problem 1.3]
algorithms: [two-pointers, character-counting]
difficulty: low
---

# URLify

## Prompt
Replace all spaces in a character array with "%20" in place. The array has enough room at the end and you are given the true length.

## Examples
- Input "Mr John Smith    ", 13 -> "Mr%20John%20Smith"

## Constraints and clarifying questions
- Use a char array (strings immutable in Java).

## Approaches
- Edit from the end: pass 1 counts spaces; new length = trueLength + 2*spaces. Pass 2 walks backwards copying chars or writing "%20" so nothing unread is overwritten.

## Complexity
- O(n) time, O(1) extra space (one pass if allowed to return a new string).

## Edge cases
- Trailing spaces beyond true length, no spaces.

## Hints
Not covered in the source.

## Related algorithms
[[two-pointers]], [[character-counting]]

## Variants


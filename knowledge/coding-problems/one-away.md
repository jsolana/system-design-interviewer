---
title: One Away
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 1 Arrays and Strings, problem 1.5]
algorithms: [two-pointers]
difficulty: medium
---

# One Away

## Prompt
Given two strings, check if they are zero or one edit apart (insert, remove or replace one character).

## Examples
- pale, ple -> true
- pales, pale -> true
- pale, bale -> true
- pale, bake -> false

## Constraints and clarifying questions
- Lengths differing by more than 1 -> false immediately.

## Approaches
- Brute force: try all edits (too slow).
- Reason about the meaning: replace = differ in exactly one position; insert/remove = same except for a shift. Length difference decides which check.
- Single merged method: walk both strings, on the first mismatch flag it and advance the longer string pointer (insert/remove) or both (replace); a second mismatch fails.

## Complexity
- O(n), n = length of the shorter string.

## Edge cases
- Both empty, lengths differing by one at the end.

## Hints
Not covered in the source.

## Related algorithms
[[two-pointers]]

## Variants
- Separate oneEditReplace/oneEditInsert is clearer; merged version avoids duplicate code (trade-off to discuss).

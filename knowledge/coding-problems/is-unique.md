---
title: Is Unique
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 1 Arrays and Strings, problem 1.1]
algorithms: [character-counting, bit-vector, sorting-algorithms]
difficulty: low
---

# Is Unique

## Prompt
Determine whether a string has all unique characters. Follow-up: do it without additional data structures.

## Examples
- "abca" -> false; "abc" -> true (Note: illustrative)

## Constraints and clarifying questions
- ASCII (128) or extended ASCII (256) or Unicode? Clarify the charset.

## Approaches
- Boolean array of charset size; return false on the first repeat. Also return false immediately if length > charset size (pigeonhole).
- Bit vector in one int when only a-z: 8x less space.
- No extra structures: compare every pair (O(n^2) time, O(1) space), or sort (if input may be modified; beware sort space) and check neighbors in O(n log n).

## Complexity
- Boolean array: O(n) time (effectively O(1) since n <= charset size), O(1) space (O(c) for charset c).
- Pairwise: O(n^2) time, O(1) space.
- Sort: O(n log n).

## Edge cases
- Empty string, length greater than charset.

## Hints
- Fixed alphabet makes bounds constant.

## Related algorithms
[[character-counting]], [[bit-vector]], [[sorting-algorithms]]

## Variants
- Unicode: increase storage or use a hash set.

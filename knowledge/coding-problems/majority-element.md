---
title: Majority Element
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.10, solution p. 554]
algorithms: [boyer-moore-majority-vote]
difficulty: medium
---

# Majority Element

## Prompt
In an array of positive integers find the element making up more than half of the items, or return -1; O(N) time, O(1) space.

## Examples
1 2 5 9 5 9 5 5 5 -> 5

## Constraints and clarifying questions
Space is O(1).

## Approaches
1. Relax time: check each element, O(N^2).
2. Observation: when a candidate stops being a majority of a prefix (counts equal), that prefix has no majority and can be discarded.
3. One pass with a candidate and counter (zero -> new candidate, equal -> +1, different -> -1), then a second pass to validate the candidate.

## Complexity
O(N) time, O(1) space.

## Edge cases
No majority (validation fails); single element.

## Hints
If the majority loses early, it must be more frequent later.

## Related algorithms
[[boyer-moore-majority-vote]]

## Variants
Not covered in the source.

---
title: String Rotation
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 1 Arrays and Strings, problem 1.9]
algorithms: [problem-solving-techniques]
difficulty: low
---

# String Rotation

## Prompt
Given a method isSubstring, check whether s2 is a rotation of s1 using only one call.

## Examples
- "waterbottle" and "erbottlewat" -> true

## Constraints and clarifying questions
- Equal length and non-empty required.

## Approaches
- If s1 = xy and s2 = yx, then s2 is always a substring of xyxy = s1+s1. So check lengths equal and isSubstring(s1+s1, s2).

## Complexity
- O(N) if isSubstring is linear.

## Edge cases
- Different lengths, empty strings.

## Hints
Not covered in the source.

## Related algorithms
[[problem-solving-techniques]]

## Variants


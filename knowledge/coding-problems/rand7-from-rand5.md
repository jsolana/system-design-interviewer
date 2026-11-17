---
title: Rand7 from Rand5
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.23 (p. 186)]
algorithms: [rejection-sampling]
difficulty: high
---

# Rand7 from Rand5

## Prompt
Implement rand7() (0..6) using rand5() (0..4), uniformly.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Equal probability.

## Approaches
- rand5()+rand5() mod 7 is biased.
- Fixed calls cannot work (5 and 7 coprime). Use 5*rand5()+rand5() uniform on 0..24; reject >= 21; return mod 7; loop.

## Complexity
Expected constant number of calls.

## Edge cases
Not covered in the source.

## Hints
Make a uniform larger range.

## Related algorithms
- [[rejection-sampling]]

## Variants
Not covered in the source.

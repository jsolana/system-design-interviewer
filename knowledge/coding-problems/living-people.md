---
title: Living People (Year with Most Alive)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.10 (p. 182)]
algorithms: [sweep-line-difference-array,sorting-algorithms]
difficulty: medium
---

# Living People (Year with Most Alive)

## Prompt
Given birth and death years (1900-2000 inclusive), find the year with the most people alive; a person is alive in both birth and death year.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Range given as min/max parameters.

## Approaches
- Brute force: for each year count the alive people: O(R*P).
- Year array incremented across each lifespan: O(P*Y + R).
- Sort births and deaths separately and walk both; count the birth before the death when years tie: O(P log P).
- Delta array: +1 at birth, -1 at death+1; running sum; O(R+P).

## Complexity
O(R+P).

## Edge cases
Death in the birth year; array size max-min+1 (101), plus one for death+1.

## Hints
Births and deaths need not be matched.

## Related algorithms
- [[sweep-line-difference-array]]
- [[sorting-algorithms]]

## Variants
Not covered in the source.

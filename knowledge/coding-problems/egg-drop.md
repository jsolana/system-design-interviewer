---
title: Egg Drop (Two Eggs, 100 Floors)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 6 Math and Logic Puzzles, problem 6.8 (p. 124, solution p. 296)]
algorithms: [worst-case-balancing,number-theory]
difficulty: medium
---

# Egg Drop (Two Eggs, 100 Floors)

## Prompt
A 100-floor building: an egg dropped from floor N or above breaks, from below survives. With two eggs find N minimizing the worst-case number of drops.

## Examples
Dropping egg 1 every 10 floors costs at most 19 drops (floors 10..100, then 91..99).

## Constraints and clarifying questions
Eggs can be reused until they break.

## Approaches
- Egg 2 must do a linear scan between the last safe floor and the breaking floor of egg 1.
- Balance the worst case: make drops(egg1)+drops(egg2) constant. If egg 1 starts at floor X and each later step shrinks by one (X, X+(X-1), ...), the total is always X.
- Solve X(X+1)/2 >= 100 -> X about 13.65; round up to 14: floors 14, 27, 39, ... worst case 14 drops. Rounding down to 13 leaves floors 92-100 uncovered.

## Complexity
O(sqrt(floors)) drops; general building: solve x(x+1)/2 = floors with the quadratic formula.

## Edge cases
Egg 1 never breaks: need a final check at floor 100 (the book returns -1 when the egg never breaks).

## Hints
Think about what egg 2 must do after egg 1 breaks.

## Related algorithms
- [[worst-case-balancing]]
- [[number-theory]]

## Variants
Not covered in the source.

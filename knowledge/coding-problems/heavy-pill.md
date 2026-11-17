---
title: Heavy Pill Bottle
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 6 Math and Logic Puzzles, problem 6.1 (p. 122, solution p. 289)]
algorithms: [number-theory]
difficulty: low
---

# Heavy Pill Bottle

## Prompt
20 bottles of pills; 19 hold 1.0 g pills, one holds 1.1 g pills. Use a scale (exact reading) once to find the heavy bottle.

## Examples
If the weighing reads 211.3 g, bottle 13 is heavy.

## Constraints and clarifying questions
One weighing only.

## Approaches
- Take i pills from bottle i (1..20). Expected weight is 1+2+...+20 = 210 g. The excess over 210 divided by 0.1 g is the bottle number.

## Complexity
O(n).

## Edge cases
Take different pill counts from each bottle.

## Hints
Make each bottle contribute a distinguishable amount.

## Related algorithms
- [[number-theory]]

## Variants
Not covered in the source.

---
title: Factorial Zeros
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.5 (p. 181)]
algorithms: [number-theory]
difficulty: medium
---

# Factorial Zeros

## Prompt
Count trailing zeros in n!.

## Examples
19! has 3 trailing zeros.

## Constraints and clarifying questions
Do not compute the factorial (overflow).

## Approaches
- Each 10 needs a 2 and a 5; 2s are more plentiful so count 5s.
- Loop 2..n counting factors of 5 per number, or directly: floor(n/5)+floor(n/25)+floor(n/125)+...

## Complexity
O(log_5 n) with the direct formula.

## Edge cases
Negative n.

## Hints
25 gives two 5s.

## Related algorithms
- [[number-theory]]

## Variants
Not covered in the source.

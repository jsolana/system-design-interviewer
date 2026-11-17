---
title: Generate Valid Parentheses
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 8 Recursion and Dynamic Programming, problem 8.9 (p. 136, solution pp. 358-360)]
algorithms: [recursion,backtracking]
difficulty: medium
---

# Generate Valid Parentheses

## Prompt
Print all valid combinations of n pairs of parentheses.

## Examples
n=3: ((())), (()()), (())(), ()(()), ()()().

## Constraints and clarifying questions
Not covered in the source.

## Approaches
- Build from n-1 by inserting '()' after each '(' and at the start; this creates duplicates, so use a set.
- Better: build char by char with counts of remaining left and right parens. Add '(' if any remain; add ')' if more ')' remain than '(' (i.e. more '(' in use than ')'). Each string is unique.

## Complexity
Output-bound (Catalan number).

## Edge cases
n=0 gives the empty string.

## Hints
When is a right paren legal?

## Related algorithms
- [[recursion]]
- [[backtracking]]

## Variants
Not covered in the source.

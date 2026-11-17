---
title: Arithmetic Expression Evaluation
type: algorithm
aliases: [calculator, operator precedence, two stacks]
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate (pp. 181-185, solutions)]
---

# Arithmetic Expression Evaluation

## Definition
Evaluate +,-,*,/ expressions without parentheses respecting precedence.

## When to use it
Parsing and calculating arithmetic strings.

## How it works
Option 1: scan left to right keeping a 'processing' term for the current multiply/divide cluster and a result; when the next operator is + or -, fold processing into result. Option 2: two stacks (numbers, operators); on a new operator, while its priority <= priority of the top operator, collapse (pop two numbers and an operator, push result); finally collapse everything. Both O(N).

## Complexity
O(N) time, O(N) space for stacks.

## Common pitfalls
Evaluating strictly left to right (3+6*2 would give 18 instead of 15); subtraction/division ordering; malformed input.

## Appears in
[[calculator]]

## See also
- [[doubly-linked-list]]

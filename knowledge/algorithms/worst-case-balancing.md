---
title: Worst-Case Balancing
type: algorithm
aliases: [load balancing the worst case]
sources: [Cracking the Coding Interview 6th ed., ch. 6 Math and Logic Puzzles (pp. 117-124, solutions pp. 289-300)]
---

# Worst-Case Balancing

## Definition
When minimizing the worst-case number of attempts, adjust early choices so all branches cost the same in the worst case.

## When to use it
Brainteasers with 'at most k tries' (eggs, weighings).

## How it works
Nine balls, find heavy in two weighings: use groups of 3, not 4+4+1. Egg drop with 2 eggs and 100 floors: drop first egg at floor X, then X+(X-1), X+(X-1)+(X-2)... so drops of egg 1 plus egg 2 stay constant; solve X(X+1)/2 >= 100 -> X ~ 13.65, round up to 14 (floors 14, 27, 39, ...); worst case 14 drops.

## Complexity
Egg drop O(sqrt(n)) drops.

## Common pitfalls
Rounding down X leaves floors uncovered.

## Appears in
[[egg-drop]]

## See also
- [[number-theory]]

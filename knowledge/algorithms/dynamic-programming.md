---
title: Dynamic Programming and Memoization
type: algorithm
aliases: [DP, memoization, top-down DP, bottom-up DP]
sources: [Cracking the Coding Interview 6th ed., ch. 17 Hard (pp. 186-191, solutions pp. 530-627); Cracking the Coding Interview 6th ed., ch. 8 Recursion and Dynamic Programming (pp. 130-136, solutions pp. 342-380)]
---

# Dynamic Programming and Memoization

## Definition
Take a recursive algorithm, find the overlapping subproblems (repeated calls) and cache their results. The book does not distinguish memoization (top-down) from DP (bottom-up); both are called DP.

## When to use it
A naive recursion repeats the same calls (recursion tree has identical nodes); counting ways, max/min over choices, 'number of paths', and exponential brute force over choices with few distinct states.

## How it works
1. Write the plain recursive solution. 2. Cache results keyed by the parameters that define a subproblem (top-down), or iterate from base cases upward filling a table (bottom-up). 3. Often only the last few table entries are needed, so the table shrinks to a few variables (Fibonacci keeps just two). Runtime = number of distinct states x work per state. Tip: if unsure about the runtime, expand the recursion tree breadth-first, treating cached calls as leaves.

## More examples (CtCI ch. 17)
- Circus tower (17.8): sort by one attribute, then longest increasing subsequence on the other; best chain ending at each element, O(n^2) (O(n log n) exists).
- Re-space (17.13): best(start) = min over split points of unrecognized characters; the start index is the memo key; O(n^2) with memoization versus O(2^n) brute force; short-circuit on a zero-invalid parse.
- Longest word made of other words (17.15): sort by length descending; canBuild(word) tries each prefix that is in the set and recurses on the rest, memoizing; bypass the cache for the word itself.
- Masseuse (17.16): best(i) = max(a[i] + best(i+2), best(i+1)); iterate backwards with two variables for O(n) time, O(1) space.

## Complexity
Fibonacci: O(2^n) naive -> O(n) memoized. Grid paths: O(2^(r+c)) -> O(r*c).

## Common pitfalls
The memo key must capture the whole state: for the diving board, caching on total alone is wrong, the key is (total, planks remaining). Keep the read and write of the cache symmetric. Integer overflow in counting problems (triple step overflows an int at n=37).

## Appears in
[[boolean-evaluation]], [[circus-tower]], [[coin-change-ways]], [[diving-board]], [[longest-word]], [[re-space]], [[recursive-multiply]], [[robot-in-grid]], [[stack-of-boxes]], [[the-masseuse]], [[triple-step]]

## See also
- [[recursion]]
- [[backtracking]]

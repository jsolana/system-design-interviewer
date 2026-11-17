---
title: Recursion
type: algorithm
aliases: [recursive approach]
sources: [Cracking the Coding Interview 6th ed., ch. 17 Hard (pp. 186-191, solutions pp. 530-627); Cracking the Coding Interview 6th ed., ch. 8 Recursion and Dynamic Programming (pp. 130-136, solutions pp. 342-380)]
---

# Recursion

## Definition
A function that solves a problem by calling itself on smaller subproblems until it reaches a base case.

## When to use it
Statements such as 'compute the nth...', 'list the first n...', 'implement a method to compute all...'; the answer can be built from answers to subproblems. Note: the book says intuition about 'this is recursive' is right only about half the time.

## How it works
Three ways to split a problem: bottom-up (solve for 1 element, then 2, then build on the previous case; 'base case and build'), top-down (divide case N into subproblems, watch for overlap) and half-and-half (binary search, merge sort). Draw the recursion tree to count calls: each call doing O(1) work means runtime = number of nodes (naive Fibonacci is about O(2^n), more precisely about 1.6^n).

## Base case and build (CtCI 17.2, 17.3)
Assume the problem is solved for n-1 and extend: shuffle first n-1 elements then swap element n with a random index in 0..n; or pick an m-subset of the first n-1 and insert element n at a random slot k < m. Both have clean iterative forms ([[fisher-yates-shuffle]], [[reservoir-sampling]]).

## Complexity
Each level uses stack space, so depth n costs at least O(n) memory. Every recursive algorithm can be written iteratively, usually with more complex code; discuss the trade-off.

## Common pitfalls
Overlapping subproblems (fix with memoization); wrong base case (e.g. is countWays(0) 0 or 1; 1 is easier); integer overflow in counting problems.

## Appears in
[[binode-bst-to-linked-list]], [[boolean-evaluation]], [[bst-sequences]], [[check-balanced-tree]], [[check-subtree]], [[coin-change-ways]], [[diving-board]], [[eight-queens]], [[first-common-ancestor]], [[generate-parentheses]], [[kth-to-last-element]], [[magic-index]], [[minimal-tree]], [[paint-fill]], [[palindrome-linked-list]], [[permutations]], [[power-set]], [[print-all-permutations]], [[random-node]], [[random-subset]], [[re-space]], [[recursive-multiply]], [[robot-in-grid]], [[shuffle-a-deck]], [[stack-of-boxes]], [[sum-lists]], [[the-masseuse]], [[towers-of-hanoi]], [[triple-step]], [[validate-bst]]

## See also
- [[dynamic-programming]]
- [[backtracking]]
- [[depth-first-search]]

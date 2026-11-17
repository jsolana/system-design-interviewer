---
title: Big O analysis (time and space complexity)
type: algorithm
aliases: [big O, asymptotic analysis, amortized time, complexity analysis]
sources: [Cracking the Coding Interview 6th ed., ch. VI Big O (book pp. 38-59)]
---

# Big O analysis (time and space complexity)

## Definition
Big O describes how an algorithm's runtime (or memory) scales with input size. Academically O = upper bound, Omega = lower bound, Theta = tight bound; in industry/interviews "O" means the tightest bound. Best/worst/expected case are a separate axis (scenarios), unrelated to O/Omega/Theta.

## When to use it
Always: state time and space for brute force and every improvement; use it to judge whether an optimization matters.

## How it works
- **Drop constants** (two sequential loops = O(N)) and **non-dominant terms** (O(N^2 + N) = O(N^2); O(2^N + N^100) = O(2^N)). O(A + B) cannot be reduced without knowing A vs B.
- **Add vs multiply**: "do this, then that" = add; "do this for each time you do that" = multiply.
- **Different inputs, different variables**: nested loops over two arrays are O(a*b), not O(N^2). Avoid reusing N for two meanings (e.g. sorting an array of `a` strings of length `s`: O(a*s*(log a + log s)), because each comparison costs O(s)).
- **Amortized time**: a doubling dynamic array has O(N) worst-case insert but O(1) amortized, since copies total 1+2+4+...+N/2 < N.
- **Log N**: appears when the problem space halves each step (binary search, balanced BST lookup). Log base is irrelevant (constant factor); exponent base is not (2^N vs 8^N).
- **Recursive runtimes**: with multiple branches, roughly O(branches^depth) (two calls per level, depth N -> O(2^N)); naive Fibonacci is O(2^N) (really ~1.6^N); with memoization it becomes O(N). Permutation generation is O(n^2 * n!) upper bound.
- **Space**: includes recursion stack depth. N recursive calls that are not simultaneously on the stack use O(1).
- **Sum over a loop**: `for j from i+1` pattern = N(N-1)/2 = O(N^2). A loop `x*x <= n` is O(sqrt n). Digit-count loops are O(log n). Iterating a balanced BST fully is O(N), not O(log N).

## Complexity
Common orders: O(1) < O(log N) < O(N) < O(N log N) < O(N^2) < O(2^N) < O(N!).

## Common pitfalls
- Assuming "two calls -> N^2" (it is exponential), or "BST -> log" for a full traversal.
- Expressing runtime of number-valued input in the value rather than the bit/digit count.
- Treating runtime as multiple choice: derive it, do not guess.
- Appending to an array by copying each time (O(n^2) total); repeated string concatenation (O(x*n^2)).

## Appears in
None yet.

## See also
[[problem-solving-techniques]], [[dynamic-array]], [[string-builder]], [[binary-heap]]

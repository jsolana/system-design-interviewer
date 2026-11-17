---
title: Interview problem-solving techniques (BUD, DIY, BCR, base case and build...)
type: algorithm
aliases: [BUD, best conceivable runtime, BCR, base case and build, simplify and generalize, data structure brainstorm]
sources: [Cracking the Coding Interview 6th ed., ch. VII Technical Questions (book pp. 60-77)]
---

# Interview problem-solving techniques

## Definition
A workflow and a toolbox for deriving and optimizing algorithm solutions: Listen, Example, Brute force, Optimize, Walk through, Implement, Test.

## When to use it
Whenever the optimal approach is not obvious. Use the toolbox in order when stuck on the brute force.

## How it works
- **Listen**: every detail in the statement is probably needed (e.g. "sorted", "run repeatedly on a server" -> precompute/cache).
- **Draw an example**: specific (real values), sufficiently large (most are ~50% too small), not a special case (not perfectly balanced, etc.).
- **State a brute force** with its complexity, then optimize.
- **Optimization toolbox**: unused information; fresh example; solve it "incorrectly" first; time-space trade-off; precompute/reorganize (sort); hash table; best conceivable runtime.
- **BUD**: look for Bottlenecks (one-time step dominating, or repeated work like searching), Unnecessary work (e.g. break after the only valid d; compute d = cbrt(a^3+b^3-c^3) instead of looping), Duplicated work (precompute (c,d) sums in a hash map keyed by sum).
- **DIY**: solve a big example by hand intuitively, then reverse-engineer what you did (e.g. sliding windows when finding permutations of s in b).
- **Simplify and generalize**: solve a simpler variant (characters instead of words for ransom note), then generalize (array counts -> hash map).
- **Base case and build**: solve n=1, 2, 3, then build n from n-1 (permutations: insert new char in all positions). Yields natural recursion.
- **Data structure brainstorm**: run through list, array, tree, heap, hash table... (running median -> two heaps).
- **Best Conceivable Runtime (BCR)**: the lower bound implied by the problem's inputs/outputs (e.g. must touch every element -> O(A+B)); unrelated to best-case of an algorithm. Work at or below BCR is "free" (e.g. O(N) precomputation); once BCR reached, optimize space; if BCR and O(1) space reached, you are done.
- **Test** order: conceptual read-through, odd-looking code, hot spots (base cases, integer division, null nodes, loop ends), small cases, special/edge cases.
- Rough memory table: 2^10 = 1 thousand (1KB), 2^20 = 1 million (1MB), 2^30 = 1 billion (1GB), 2^32 = 4GB, 2^40 = 1TB. A bit vector over all 32-bit ints needs 2^29 bytes (~512MB).

## Complexity
Not applicable.

## Common pitfalls
Jumping to code before walking through the algorithm; guessing runtime by elimination; claiming BCR from what your algorithm does rather than from the problem.

## Appears in
[[common-elements-of-sorted-arrays]], [[count-pairs-with-difference-k]], [[equal-sums-of-cubes]], [[permutations-of-string-in-longer-string]], [[ransom-note]], [[running-median]], [[string-rotation]]

## See also
[[big-o-analysis]], [[hash-table]], [[binary-heap]], [[recursion]]

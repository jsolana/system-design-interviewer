---
title: Rejection Sampling
type: algorithm
aliases: [uniform random from another generator]
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate (pp. 181-185, solutions)]
---

# Rejection Sampling

## Definition
Generate uniform random numbers in a target range by drawing from a bigger uniform range and discarding values outside a multiple of the target size.

## When to use it
Building randX from randY; fairness requirements.

## How it works
rand7 from rand5: v = 5*rand5()+rand5() is uniform on 0..24; reject v >= 21; return v mod 7. Each outcome has exactly one way to appear. A fixed number of calls cannot work because powers of 5 never sum to 1/7, so the loop has unbounded (but finite expected) calls. 2*rand5()+rand5() is not uniform.

## Complexity
Expected constant calls.

## Common pitfalls
Combining with weights that make some outcomes more likely; modulo bias without discarding.

## Appears in
[[rand7-from-rand5]]

## See also
- [[number-theory]]

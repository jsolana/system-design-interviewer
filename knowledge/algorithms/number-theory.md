---
title: Number Theory and Math Tricks for Interviews
type: algorithm
aliases: [gcd, lcm, factors, probability basics]
sources: [Cracking the Coding Interview 6th ed., ch. 6 Math and Logic Puzzles (pp. 117-124, solutions pp. 289-300)]
---

# Number Theory and Math Tricks for Interviews

## Definition
Small mathematical facts that turn puzzles into closed formulas.

## When to use it
Counting factors, trailing zeros, parity/coloring arguments, probability questions, simulation checks.

## How it works
- Factors: a number n has an odd number of divisors iff it is a perfect square (divisors pair up as (d, n/d); the pair (s,s) counts once). Used for the 100 lockers puzzle: 10 open lockers.
- Trailing zeros of n!: each 10 needs a 2 and a 5; there are more 2s, so count factors of 5: floor(n/5)+floor(n/25)+floor(n/125)+...
- Two jugs of relatively prime sizes can measure any amount from 1 to their sum.
- Coloring/parity argument: a domino covers one black and one white square, so a board with two same-colored corners removed cannot be tiled.
- Probability: P(A and B)=P(B|A)P(A); Bayes P(A|B)=P(B|A)P(A)/P(B); P(A or B)=P(A)+P(B)-P(A and B); independent events multiply; mutually exclusive events add; non-zero-probability events cannot be both independent and mutually exclusive.
- n ants on an n-gon walking randomly avoid collision only if all go the same direction: P(collision)=1-(1/2)^(n-1).
- Gender-ratio puzzle: stopping rules do not change a 50/50 birth process, so ratio stays 1:1.
- Best-case thinking: derive rules, then combine (rope-burning puzzle: light one rope at both ends and the other at one end).

## Complexity
Closed forms, O(log n) or O(1).

## Common pitfalls
Computing n! directly overflows; counting only multiples of 5 misses 25, 125 (multiple factors of 5); confusing independence with mutual exclusivity.

## Appears in
[[egg-drop]], [[factorial-zeros]], [[heavy-pill]], [[lockers-perfect-squares]]

## See also
- [[sieve-of-eratosthenes]]

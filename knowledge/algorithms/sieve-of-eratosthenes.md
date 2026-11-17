---
title: Sieve of Eratosthenes and Primality Testing
type: algorithm
aliases: [primes, primality]
sources: [Cracking the Coding Interview 6th ed., ch. 6 Math and Logic Puzzles (pp. 117-124, solutions pp. 289-300)]
---

# Sieve of Eratosthenes and Primality Testing

## Definition
Generate all primes up to max by crossing off multiples of each prime. Also covers the simple primality test.

## When to use it
List primes up to n, or test many numbers for primality.

## How it works
Primality: trial division from 2 to n-1 is naive; iterate only to sqrt(n) because each divisor a has a complement b=n/a with min(a,b) <= sqrt(n). Sieve: flags[2..max]=true; take the next true value p, cross off p*p, p*p+p, ... (smaller multiples were already crossed off by smaller primes); stop when p > sqrt(max). Optimization: store only odd numbers to halve memory. Prime factorization view: every integer is a product of primes, x divides y iff every prime exponent of x <= that of y; gcd uses min of exponents, lcm uses max, so gcd*lcm = x*y.

## Complexity
Trial division O(sqrt n); sieve about O(max log log max) time, O(max) space.

## Common pitfalls
Starting the inner loop at 2*p instead of p*p (correct but slower); forgetting 0 and 1 are not prime.

## Appears in
None yet.

## See also
- [[number-theory]]

---
title: Bit manipulation
type: algorithm
aliases: [bitwise operations, bit tricks, two's complement]
sources: [Cracking the Coding Interview 6th ed., ch. 17 Hard (pp. 186-191, solutions pp. 530-627); Cracking the Coding Interview 6th ed., ch. 5 Bit Manipulation (book pp. 112-116); ch. 6 poison puzzle and ch. 16 Moderate (Number Swapper, Number Max, Operations)]
---

# Bit manipulation

## Definition
Operating directly on binary representations with AND, OR, XOR, NOT and shifts.

## When to use it
Explicit bit problems; compact sets/flags (bit vectors); parity; power-of-two checks; counting differing bits; swapping bit groups; optimizing multiplication/division by powers of two.

## How it works
- Identities (bitwise, so valid for sequences): x^0s = x, x^1s = ~x, x^x = 0; x&0s = 0, x&1s = x, x&x = x; x|0s = x, x|1s = 1s, x|x = x.
- Shifts: `<<k` multiplies by 2^k. Logical right shift (>>>) fills with 0; arithmetic (>>) fills with the sign bit (about divide by 2). Shifting a negative int repeatedly: logical -> 0, arithmetic -> -1.
- Two's complement: -K stored as the complement of K w.r.t. 2^(N-1) (invert bits and add 1). All-ones = -1.
- Common tasks: get bit `(n & (1<<i)) != 0`; set `n | (1<<i)`; clear `n & ~(1<<i)`; clear MSB through i `n & ((1<<i)-1)`; clear i through 0 `n & (-1 << (i+1))`; update bit: clear then OR `(v<<i)`.
- `n & (n-1)` clears the lowest set bit: zero iff n is a power of two (or 0); looping it counts set bits.
- `n & -n` isolates the lowest set bit (derived from two's complement; Note: not stated explicitly in source).
- Swap odd/even bits: `((n & 0xAAAAAAAA) >>> 1) | ((n & 0x55555555) << 1)`.
- Fractions in binary: multiply by 2, emit 1 when result >= 1 (or compare to .5, .25, ...).

- Arithmetic tricks (ch. 16): swap in place with XOR (x^=y; y^=x; x^=y) or with sum/difference; max without comparison: k = sign bit of (a-b) turned into 0/1, result a*k + b*(1-k), but a-b can overflow when signs differ, so use sign(a) in that case. Multiply by halving: product(s,b) = 2*product(s>>1,b), plus b if s is odd, O(log s). With only addition: negate by adding +/-1 (O(k)) or with doubling steps O((log a)^2); subtract = add negation; multiply = repeated addition; divide = count how many times the divisor fits.
- Subsets as bitmasks: integers 0..2^n-1, bit i set = element i included.
- Binary encoding for tests (poison puzzle, 1000 bottles, 10 strips): strip i gets a drop of every bottle whose bit i is 1; the positive strips spell the bottle number in one 7-day round.

## Add without plus and bitwise elimination (CtCI 17.1, 17.4)
- Add without + : XOR = sum without carry, (a AND b) << 1 = carry; repeat with the two results until carry is 0.
- Missing number when only "fetch bit j of A[i]" is allowed: examine the least significant bit of all remaining numbers; in a complete 0..n list count(0s) equals count(1s) or exceeds it by one, so the removed value's bit is the one that breaks the pattern; keep only numbers sharing that bit and move to the next bit. Total work n + n/2 + ... = O(n).

## Complexity
Mostly O(1) per op, O(b) over b bits.

## Common pitfalls
Off-by-one in masks; sign extension with arithmetic shift; do not memorize, derive masks; complexity should be in bits b, not the value n.

## Appears in
[[add-without-plus]], [[arithmetic-with-add-only]], [[binary-to-string]], [[bit-conversion]], [[bit-insertion]], [[draw-line]], [[flip-bit-to-win]], [[missing-int]], [[missing-number-bit-access]], [[next-number-same-bit-count]], [[number-max]], [[number-swapper]], [[pairwise-swap-bits]], [[poison-bottles]], [[power-of-two-check]], [[power-set]], [[recursive-multiply]]

## See also
[[character-counting]], [[big-o-analysis]]

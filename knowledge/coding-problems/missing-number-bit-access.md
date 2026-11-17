---
title: Missing Number with Bit Access
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.4, solution p. 533]
algorithms: [bit-manipulation]
difficulty: high
---

# Missing Number with Bit Access

## Prompt
An array contains all integers from 0 to n except one. You cannot read a whole element; the only operation is "fetch the j-th bit of A[i]" in constant time. Find the missing integer, ideally in O(n).

## Examples
Not covered in the source.

## Constraints and clarifying questions
Elements are in binary; n elements, log n bits each.

## Approaches
1. Sum approach needs whole numbers: reconstructing each number costs O(n log n).
2. Bit-by-bit elimination: for the least significant bit count 0s and 1s; a complete list has equal counts (n odd) or one extra 0; the removed number's bit is 0 if count(0) <= count(1) else 1. Discard numbers whose bit differs, recurse on the next bit with the shrunken list; empty list means remaining bits are 0.

## Complexity
O(n): n + n/2 + n/4 ...

## Edge cases
Missing value 0; missing the highest value.

## Hints
Look at one bit position at a time and the expected balance of 0s and 1s.

## Related algorithms
[[bit-manipulation]]

## Variants
Not covered in the source.

---
title: Number Swapper
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.1 (p. 181)]
algorithms: [bit-manipulation]
difficulty: low
---

# Number Swapper

## Prompt
Swap two numbers in place without a temporary variable.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Integers.

## Approaches
- Arithmetic: a = a-b; b = a+b (now old a); a = b-a (old b).
- XOR: a^=b; b=a^b; a^=b. XOR with 1 flips a bit, with 0 leaves it, so each bit swaps correctly.

## Complexity
O(1).

## Edge cases
a and b the same variable/reference.

## Hints
Think bitwise.

## Related algorithms
- [[bit-manipulation]]

## Variants
Not covered in the source.

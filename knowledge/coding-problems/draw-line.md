---
title: Draw Line on a Monochrome Screen
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 5 Bit Manipulation, problem 5.8]
algorithms: [bit-manipulation]
difficulty: high
---

# Draw Line on a Monochrome Screen

## Prompt
The screen is an array of bytes (8 pixels per byte), width w divisible by 8. Implement drawLine(screen, width, x1, x2, y) for a horizontal line.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Width divisible by 8 so no byte spans rows.

## Approaches
- Naive: set each pixel from x1 to x2.
- Better: set full bytes in between to 0xFF; use masks for the partial first and last bytes; handle x1 and x2 in the same byte separately.

## Complexity
- O((x2-x1)/8).

## Edge cases
- x1 and x2 in the same byte, x1 and x2 byte-aligned, x1 == x2.

## Hints
Not covered in the source.

## Related algorithms
[[bit-manipulation]]

## Variants


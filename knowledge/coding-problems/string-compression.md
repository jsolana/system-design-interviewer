---
title: String Compression
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 1 Arrays and Strings, problem 1.6]
algorithms: [string-builder]
difficulty: low
---

# String Compression

## Prompt
Compress runs of repeated characters (aabcccccaaa -> a2b1c5a3); return the original if the compressed string is not shorter.

## Examples
- aabcccccaaa -> a2b1c5a3

## Constraints and clarifying questions
- Only letters a-z/A-Z.

## Approaches
- Scan counting consecutive repeats, append char+count when the next char differs. Using plain string concatenation is O(p + k^2) (k = number of runs); use a StringBuilder.
- Optionally precompute the compressed length first to return early and size the builder.

## Complexity
- O(n) time with a builder; O(n) space.

## Edge cases
- Single-character string, no repeats, last run flush.

## Hints
Not covered in the source.

## Related algorithms
[[string-builder]]

## Variants


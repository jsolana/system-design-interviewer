---
title: Master Mind
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.15 (p. 183)]
algorithms: [hash-table]
difficulty: medium
---

# Master Mind

## Prompt
Four slots with colors R,Y,G,B. Given guess and solution count hits (right color and slot) and pseudo-hits (right color elsewhere; a hit never counts as a pseudo-hit).

## Examples
Solution RGBY, guess GGRR: 1 hit, 1 pseudo-hit.

## Constraints and clarifying questions
Equal lengths.

## Approaches
- First pass: count hits; for non-hits tally solution colors in a frequency array.
- Second pass: for each non-hit guess slot, if its color has frequency > 0 count a pseudo-hit and decrement.

## Complexity
O(n).

## Edge cases
Repeated colors.

## Hints
Not covered in the source.

## Related algorithms
- [[hash-table]]

## Variants
Not covered in the source.

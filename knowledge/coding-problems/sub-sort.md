---
title: Sub Sort (Minimal Unsorted Window)
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 16 Moderate, problem 16.16 (p. 183)]
algorithms: [two-pointers]
difficulty: high
---

# Sub Sort (Minimal Unsorted Window)

## Prompt
Find indices m and n such that sorting only elements m..n sorts the entire array; minimize n-m.

## Examples
{1,2,4,7,10,11,7,12,6,7,16,18,19} gives (3,9).

## Constraints and clarifying questions
Not covered in the source.

## Approaches
- Find the end of the sorted prefix and the start of the sorted suffix; the middle is what is out of order.
- Let min and max be those of the middle. Shrink the left part left until a[i] <= min and extend the right part until a[i] >= max.
Result is the range after shrinking.

## Complexity
O(n).

## Edge cases
Already sorted array.

## Hints
Not covered in the source.

## Related algorithms
- [[two-pointers]]

## Variants
Not covered in the source.

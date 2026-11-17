---
title: Sum Lists
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 2 Linked Lists, problem 2.5]
algorithms: [linked-list, recursion]
difficulty: medium
---

# Sum Lists

## Prompt
Two numbers are stored as linked lists of digits. Add them and return the sum as a list.

## Examples
- Reverse order: (7->1->6)+(5->9->2) = 2->1->9 (617+295=912)
- Forward order follow-up: (6->1->7)+(2->9->5) = 9->1->2

## Constraints and clarifying questions
- Different lengths.

## Approaches
- Reverse order (ones digit first): add digit by digit with carry, recursively or iteratively; keep going while either list has nodes or carry != 0.
- Forward order: pad the shorter list with leading zeros to equal length; recurse to the end and return (partial sum node, carry), inserting each digit at the front of the result; add a final carry node.

## Complexity
- O(max(len1, len2)).

## Edge cases
- Different lengths, final carry, empty list.

## Hints
Not covered in the source.

## Related algorithms
[[linked-list]], [[recursion]]

## Variants


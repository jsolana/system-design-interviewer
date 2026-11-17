---
title: Palindrome Linked List
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 2 Linked Lists, problem 2.6]
algorithms: [linked-list, runner-technique, stack-and-queue, recursion]
difficulty: medium
---

# Palindrome Linked List

## Prompt
Check if a linked list is a palindrome.

## Examples
- Not covered in the source.

## Constraints and clarifying questions
- Not covered in the source.

## Approaches
- Reverse a copy and compare the first half.
- Fast/slow runner: push first half onto a stack; at the end of the list, compare the second half with popped values (skip the middle when odd length).
- Recursive: pass length; base cases length 0 or 1; each frame compares its head with the node returned from the inner call, returning that node.next up the stack (needs a result wrapper holding node and boolean).

## Complexity
- O(n) time; O(n) space (stack/recursion/copy).

## Edge cases
- Odd/even length, one node.

## Hints
Not covered in the source.

## Related algorithms
[[linked-list]], [[runner-technique]], [[stack-and-queue]], [[recursion]]

## Variants


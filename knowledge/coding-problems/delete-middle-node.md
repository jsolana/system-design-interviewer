---
title: Delete Middle Node
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 2 Linked Lists, problem 2.3]
algorithms: [linked-list]
difficulty: low
---

# Delete Middle Node

## Prompt
Delete a node in the middle of a singly linked list given only access to that node.

## Examples
- Delete c from a->b->c->d->e->f gives a->b->d->e->f

## Constraints and clarifying questions
- Cannot work for the last node; point it out.

## Approaches
- Copy the next node data into the current node and unlink the next node.

## Complexity
- O(1).

## Edge cases
- Last node (cannot do; mark as dummy), null.

## Hints
Not covered in the source.

## Related algorithms
[[linked-list]]

## Variants


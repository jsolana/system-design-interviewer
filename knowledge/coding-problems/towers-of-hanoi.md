---
title: Towers of Hanoi
type: coding-problem
sources: [Cracking the Coding Interview 6th ed., ch. 8 Recursion and Dynamic Programming, problem 8.6 (p. 135, solution pp. 351-353)]
algorithms: [recursion]
difficulty: medium
---

# Towers of Hanoi

## Prompt
Move N disks (ascending size top to bottom) from tower 1 to tower 3 using stacks, moving one disk at a time and never placing a disk on a smaller one.

## Examples
n=2: move disk1 to tower2, disk2 to tower3, disk1 to tower3.

## Constraints and clarifying questions
Three towers.

## Approaches
- Base case and build: to move n disks, move the top n-1 to the buffer tower, move the largest to the destination, then move the n-1 disks from the buffer to the destination.
- Pseudocode: move(n, from, to, via): if n==0 return; move(n-1, from, via, to); move top from -> to; move(n-1, via, to, from).
- Model towers as stacks.

## Complexity
2^n - 1 moves; O(n) stack depth.

## Edge cases
n = 0.

## Hints
Labels of the two non-source towers are interchangeable.

## Related algorithms
- [[recursion]]

## Variants
Not covered in the source.

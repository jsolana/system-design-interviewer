---
title: Shuffle a Deck (Perfect Shuffle)
type: coding-problem
sources: [Cracking the Coding Interview, 6th ed., ch. 17 Hard (pp. 186-191), problem 17.2, solution p. 531]
algorithms: [fisher-yates-shuffle, recursion]
difficulty: medium
---

# Shuffle a Deck (Perfect Shuffle)

## Prompt
Shuffle a deck of cards so that each of the 52! permutations is equally likely, given a perfect random number generator.

## Examples
Not covered in the source.

## Constraints and clarifying questions
Random generator is assumed perfect.

## Approaches
1. Base case and build: shuffle the first n-1 cards, then swap card n with a random position in 0..n.
2. Iterative form: for i in 0..n-1, swap a[i] with a[random(0..i)].

## Complexity
O(n) time, O(1) space.

## Edge cases
Deck of 0 or 1 card.

## Hints
Suppose a shuffle works for n-1 elements; how do you place the nth?

## Related algorithms
[[fisher-yates-shuffle]] [[recursion]]

## Variants
Not covered in the source.

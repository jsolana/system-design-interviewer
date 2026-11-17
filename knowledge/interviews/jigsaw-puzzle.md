---
title: Jigsaw Puzzle (NxN)
type: interview
sources: [Cracking the Coding Interview, 6th ed., ch. 7 pp. 125-129 and solutions pp. 305-341 (problem 7.6)]
concepts: [object-oriented-design]
difficulty: medium
---

# Jigsaw Puzzle (NxN)

## Prompt
Implement an NxN jigsaw: design the data structures and explain an algorithm to solve it, given fitsWith(edge) that tells whether two edges belong together.

## Functional requirements
- Traditional grid puzzle; each piece has four edges: inner, outer or flat.
- Solve and store each piece's position.

## Non-functional requirements
Not covered in the source (object-oriented design; ask clarifying questions first).

## Estimations
Not covered in the source.

## API
fitsWith(edge), isCorner(), isBorder(), rotate pieces, solve().

## Data model
Puzzle (list of pieces, NxN solution grid), Piece (map orientation -> edge, may be rotated), Edge (shape and back pointer to its piece, no orientation), enums Shape (INNER, OUTER, FLAT) and Orientation (LEFT, TOP, RIGHT, BOTTOM). Absolute positions are stored (alternative: relative neighbors).

## Architecture (high-level design)
Group pieces into corners, borders and inners. Put a corner at the top-left, then fill in row order; at each slot search the right group for a piece whose edges fit the neighbors, rotating it to the needed orientation.

## Deep dives
Absolute vs relative position of pieces.

## Trade-offs and decisions
Not covered in the source.

## Related concepts
[[object-oriented-design]]

## Follow-up questions
Not covered in the source.

## Variants


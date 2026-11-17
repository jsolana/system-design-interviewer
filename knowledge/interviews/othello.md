---
title: Othello
type: interview
sources: [Cracking the Coding Interview, 6th ed., ch. 7 pp. 125-129 and solutions pp. 305-341 (problem 7.8)]
concepts: [object-oriented-design]
difficulty: medium
---

# Othello

## Prompt
Implement the object-oriented design for Othello: pieces are white on one side and black on the other; a piece surrounded by opponents on both left/right or top/bottom is captured and flips. A move must capture at least one piece; the game ends when either player has no valid move; most pieces wins.

## Functional requirements
- Initialize a board with 2 black and 2 white pieces in the centre.
- Place a piece, flip captured lines, update scores, detect the end.

## Non-functional requirements
Not covered in the source (object-oriented design; ask clarifying questions first).

## Estimations
Not covered in the source.

## API
Board.initialize, placeColor(row, col, color), flipSection(row, col, color, direction), getScoreForColor, updateScore; Game and Player methods (Player.getScore calls Game).

## Data model
Game, Board, Piece (single class with a color flag), Player, Color and Direction enums.

## Architecture (high-level design)
Board manages pieces and score counts (colorChanged/colorAdded); Game handles flow and times; Player holds little state.

## Deep dives
- One Piece class with a color flag, not BlackPiece/WhitePiece, because pieces flip often.
- Separate Game and Board: logical separation vs extra layer of delegation.
- Score kept in Board (groups logically).
- Game as a Singleton only if exactly one game is acceptable (discuss it). What matters is why you chose, not what.

## Trade-offs and decisions
Board vs Game ownership of scores; Singleton or not.

## Related concepts
[[object-oriented-design]]

## Follow-up questions
Not covered in the source.

## Variants
Not covered in the source.

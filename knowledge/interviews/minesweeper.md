---
title: Minesweeper
type: interview
sources: [Cracking the Coding Interview, 6th ed., ch. 7 pp. 125-129 and solutions pp. 305-341 (problem 7.10)]
concepts: [object-oriented-design]
difficulty: medium
---

# Minesweeper

## Prompt
Design and implement a text-based Minesweeper: NxN grid with B hidden mines, other cells blank or a number of adjacent mines. Uncovering a mine loses; a number exposes it; a blank cell exposes it and adjacent blanks (up to the numbers). Win when all non-bombs are exposed. Players can flag guesses.

## Functional requirements
- Uncover/flag cells, flood-expose blank regions, win and lose detection.

## Non-functional requirements
Not covered in the source (object-oriented design; ask clarifying questions first).

## Estimations
Not covered in the source.

## API
Game.initialize/start/playGame; Board.flipCell(GamePlay) returning a GamePlayResult (successful flag plus state won/lost/playing); GamePlay (row, column, isGuess).

## Data model
Cell (row, col, isBomb, number where blank = 0, isExposed, isGuess), Board (2D cell array, bomb count, unexposed counter), Game (state, input), GamePlay, GamePlayResult, GameState.

## Architecture (high-level design)
Board holds cells and basic moves; Game holds state and user input. Interesting algorithms: placing bombs, setting numbers, expanding blank areas.

## Deep dives
- Place bombs: put K bombs in the first K cells then shuffle the grid (Fisher-Yates style, convert index to row and column) instead of random retries that slow down with many bombs.
- Numbers: for each bomb increment its 8 neighbors, rather than counting around every cell.
- Expand blanks: BFS with a queue (or recursion); exposing a blank adds its blank neighbors to the queue.
- No Cell subclasses for exposed/unexposed (references would break); BLANK is just NUMBER 0.

## Trade-offs and decisions
Flags vs subclasses for cell state; two result values (success, state).

## Related concepts
[[object-oriented-design]]

## Follow-up questions
Not covered in the source.

## Variants
Not covered in the source.

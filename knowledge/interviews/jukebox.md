---
title: Jukebox
type: interview
sources: [Cracking the Coding Interview, 6th ed., ch. 7 pp. 125-129 and solutions pp. 305-341 (problem 7.3)]
concepts: [object-oriented-design]
difficulty: low
---

# Jukebox

## Prompt
Design a musical jukebox using object-oriented principles.

## Functional requirements
- Assumed: computer simulation of a physical jukebox, free to use, plays CDs.
- Playlist creation (add, delete, shuffle), get next song, display, user selection.

## Non-functional requirements
Not covered in the source (object-oriented design; ask clarifying questions first).

## Estimations
Not covered in the source.

## API
Jukebox methods mediate between user, CD player, playlist and display.

## Data model
Jukebox, CDPlayer (one CD at a time; others stored in the jukebox), CD, Song, Playlist (wrapper around a queue with convenience methods), User, Display.

## Architecture (high-level design)
Jukebox is the body of the program; interactions between components and between user and system go through it. Each component maps to an object, each action to a method.

## Deep dives
Questions to ask: CDs, records or MP3s? Simulation or physical? Money and change? The answers shape the classes.

## Trade-offs and decisions
How to extend for paid play or other media.

## Related concepts
[[object-oriented-design]]

## Follow-up questions
Not covered in the source.

## Variants


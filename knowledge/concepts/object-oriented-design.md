---
title: Object-oriented design (interview approach and patterns)
type: concept
aliases: [OOD, class design, singleton, factory method]
sources: [Cracking the Coding Interview, 6th ed., ch. 7 pp. 125-129]
---

# Object-oriented design (interview approach and patterns)

## Definition
Sketching classes, relationships and methods for a real-world object or technical task. Tests whether you can produce elegant, maintainable code, not whether you recite design patterns.

## Why it matters
Poor performance on OOD questions can be a red flag about coding style. The problems are deliberately vague.

## How it works
Four steps:
1. **Handle ambiguity**: ask who uses it and how (the "six Ws": who, what, where, when, how, why). A coffee maker may be an industrial multi-product machine or a simple one for the elderly.
2. **Define core objects** (restaurant: Table, Guest, Party, Order, Meal, Employee, Server, Host).
3. **Analyze relationships**: members, inheritance, one-to-many vs many-to-many (Party has Guests; Server and Host inherit Employee; a Table may hold several Parties in communal-table restaurants, so ask how general to be).
4. **Investigate actions**: walk key flows (party arrives, host looks up reservation, assigns table or queues; leaving frees the table) and fix forgotten objects.

## Variants and techniques
- **Singleton**: one instance with a global access point (private static instance, protected constructor, getInstance lazily creates). Often disliked as an anti-pattern since it hinders unit testing.
- **Factory method**: an interface/static method creates instances and decides the concrete class (e.g. createCardGame(type) returning Poker or BlackJack).
- Do not hunt for "the right" pattern; design for the problem.
- Recurrent judgement calls in the worked solutions: abstract class vs concrete (card values depend on the game), a flag instead of subclasses when instances change state often (a piece flipping color, a cell exposed or not), separate Board and Game objects (logic of pieces vs flow), splitting a big controller into UserManager/Library/Display, a Singleton Game only if one game per program is acceptable, design for long-term flexibility but state assumptions.

## Trade-offs
Flexibility vs complexity: over-generalizing leads to hopelessly complex designs; make it reasonably flexible and state constraints. More classes give organization but add indirection.

## When to use it / when not to
For low-level design interviews. For distributed architectures use the system design concepts instead ([[system-design-interview-framework]]).

## Appears in
[[call-center]], [[deck-of-cards]], [[in-memory-file-system]], [[jigsaw-puzzle]], [[jukebox]], [[minesweeper]], [[online-book-reader]], [[othello]], [[parking-lot]]

## See also
[[system-design-interview-framework]], [[thread-synchronization-and-deadlocks]]

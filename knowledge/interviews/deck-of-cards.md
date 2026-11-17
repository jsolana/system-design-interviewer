---
title: Deck of Cards (and Blackjack)
type: interview
sources: [Cracking the Coding Interview, 6th ed., ch. 7 pp. 125-129 and solutions pp. 305-341 (problem 7.1)]
concepts: [object-oriented-design]
difficulty: low
---

# Deck of Cards (and Blackjack)

## Prompt
Design the data structures for a generic deck of cards and explain how to subclass them for blackjack.

## Functional requirements
- Standard 52-card deck (after clarifying what 'generic' means: poker-like deck vs Uno or baseball cards).
- Deal/shuffle cards; blackjack scoring of a hand.

## Non-functional requirements
Not covered in the source (object-oriented design; ask clarifying questions first).

## Estimations
Not covered in the source.

## API
Deck, Hand and Card methods (deal, shuffle, remaining cards, score); not detailed.

## Data model
Suit enum; Card (abstract) with suit and face value; Deck<T extends Card>; Hand<T extends Card>; BlackJackCard extends Card; BlackJackHand extends Hand.

## Architecture (high-level design)
- Card is abstract because value() depends on the game; Deck is generic restricted to Card.
- BlackJackCard: face cards are 10, ace is 1 or 11.
- BlackJackHand computes all possible scores (each ace counted as 1 or 11), picks the max score not above 21 (or the min above 21), and exposes busted(), is21(), isBlackJack().

## Deep dives
- Ace handling: logic in Hand (possible scores) rather than a special Ace subclass (alternative).
- Could argue Card should have a default poker value() instead of being abstract.

## Trade-offs and decisions
- Ace as 1/11 in the hand evaluator vs an Ace class.
- Abstract Card vs default poker rules.

## Related concepts
[[object-oriented-design]]

## Follow-up questions
Not covered in the source.

## Variants
Not covered in the source.

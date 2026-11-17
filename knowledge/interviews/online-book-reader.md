---
title: Online Book Reader
type: interview
sources: [Cracking the Coding Interview, 6th ed., ch. 7 pp. 125-129 and solutions pp. 305-341 (problem 7.5)]
concepts: [object-oriented-design]
difficulty: low
---

# Online Book Reader

## Prompt
Design the data structures for an online book reader system.

## Functional requirements
- User membership creation and extension.
- Search the book database.
- Assumed one active user and one active book at a time.

## Non-functional requirements
Not covered in the source (object-oriented design; ask clarifying questions first).

## Estimations
Not covered in the source.

## API
get/set/update methods; not detailed.

## Data model
User, Book, Library (book collection and search), UserManager, Display (refreshUsername, refreshTitle, refreshDetails, refreshPage), OnlineReaderSystem (main class).

## Architecture (high-level design)
OnlineReaderSystem coordinates; Library, UserManager and Display are split out. User and Book mostly hold data.

## Deep dives
Splitting components out adds complexity in a tiny system but stops the main class from becoming huge as it grows.

## Trade-offs and decisions
Splitting responsibilities vs a single class.

## Related concepts
[[object-oriented-design]]

## Follow-up questions
Not covered in the source.

## Variants
Not covered in the source.

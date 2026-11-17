---
title: In-Memory File System
type: interview
sources: [Cracking the Coding Interview, 6th ed., ch. 7 pp. 125-129 and solutions pp. 305-341 (problem 7.11)]
concepts: [object-oriented-design]
difficulty: medium
---

# In-Memory File System

## Prompt
Explain the data structures and algorithms for an in-memory file system, with code where possible.

## Functional requirements
- Files and directories; directories contain files and directories.

## Non-functional requirements
Not covered in the source (object-oriented design; ask clarifying questions first).

## Estimations
Not covered in the source.

## API
Entry operations: delete, getFullPath, rename, size; Directory: numberOfFiles, addEntry.

## Data model
Entry (abstract: name, created, last updated, last accessed, parent), File extends Entry (content, size), Directory extends Entry (list of Entries).

## Architecture (high-level design)
Files and directories share most attributes, so both inherit from Entry; Directory holds a single list of entries and computes size recursively.

## Deep dives
Alternative: separate lists for files and subdirectories (numberOfFiles cleaner, no instanceof) but sorting by date or name across both gets harder.

## Trade-offs and decisions
Single mixed list vs two lists.

## Related concepts
[[object-oriented-design]]

## Follow-up questions
Not covered in the source.

## Variants
Not covered in the source.

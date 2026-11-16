---
title: Google Docs
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/google-docs]
concepts: [websockets]
difficulty: high
---

# Google Docs

> Note: mostly paywalled page; only the intro, functional requirements and section titles were readable. Tagged topic: Real-time Updates; difficulty "hard".

## Prompt
A collaborative document editor in the browser: rich text and real-time collaboration. Websockets and collaborative editing systems are the key areas.

## Functional requirements
- Create documents.
- Concurrent editing of the same document by several users.
- See other people's changes in real time.
- See cursors and presence of other users.
- Out of scope: sophisticated structure (simple text editor), permissions, history/versioning.

## Non-functional requirements
Not covered in the source.

## Estimations
Not covered in the source.

## API
Not covered in the source.

## Data model
Not covered in the source.

## Architecture (high-level design)
Titles only: create documents; concurrent editing ("Collaborative Edits Breakdown"); real-time changes (when loading the document and when there are updates); cursor and presence.

## Deep dives
Titles only: scale to millions of websocket connections; keep storage under control; additional deep dives.

## Trade-offs and decisions
Not covered in the source.

## Related concepts
[[websockets]]

## Follow-up questions
Not covered in the source.

## Variants
Not covered in the source.

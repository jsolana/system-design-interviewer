---
title: Google Docs
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/google-docs, https://dropbox.tech/application/how-dropbox-replay-keeps-everyone-in-sync]
concepts: [websockets, logical-clocks-and-causality]
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
- **Dropbox Replay live review (shared video playback)**, source: https://dropbox.tech/application/how-dropbox-replay-keeps-everyone-in-sync. Differs from document co-editing: the shared state is small (frame int64 + rate float32), so no OT/CRDT is used. Clients hold WebSockets to a Go server (Gorilla, Protocol Buffers); the server serializes playback messages under a mutex, using arrival order as a logical clock, broadcasts each update and echoes it back to the sender; a client that is awaiting the echo of its own change ignores incoming state that arrives first (it was ordered earlier). Single-client state (cursor, drawings) is simply echoed. No numbers given. See [[logical-clocks-and-causality]].

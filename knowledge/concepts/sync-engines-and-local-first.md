---
title: Sync engines and local-first software
type: concept
aliases: [local-first, offline-first, sync engine, real-time collaboration, CRDT, operational transformation]
sources: [Designing Data-Intensive Applications, 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 6 (pp. 220-229)]
---

# Sync engines and local-first software

## Definition
*2nd edition (new section).* A sync engine is a library that keeps a persistent local replica on each device/browser and replicates changes in the background: multi-leader replication taken to the extreme (each device is a "region" with an unreliable link). **Offline-first** apps work while disconnected; **local-first** apps keep working even if the vendor shuts down its services (open sync protocol with several providers; Git is an example).

## Why it matters
Used for calendars, Google Docs/Sheets, Figma, Linear. UI reacts instantly (target <16 ms/frame), offline equals "very large network delay", and the frontend model gets simpler because local reads/writes almost never fail.

## How it works
- Capture local edits, send them when online, receive others' edits, merge into the local copy, update the UI (often with reactive programming).
- Concurrent edits need conflict resolution: **OT** (operations with indexes transformed against concurrent ones; used by Google Docs, ShareDB) or **CRDTs** (each element gets a unique ID, insertions refer to the ID of the preceding element; Automerge, Yjs; also Riak, Redis Enterprise, Cosmos DB). See [[conflict-resolution]].
- Examples: Firestore, Realm, Ditto (proprietary backends); PouchDB/CouchDB, Automerge, Yjs (open).

## Variants and techniques
Game netcode solves a similar problem with game-specific techniques (out of scope).

## Trade-offs
Not suitable when the user can access huge data volumes (download everything up front); merging cannot enforce invariants such as "max five items" (some writes must be dropped).

## When to use it / when not to
Collaborative or offline-capable apps with per-user-sized data; not for large shared catalogs.

## Appears in
None yet.

## See also
[[replication]], [[conflict-resolution]], [[google-docs]], [[websockets]]

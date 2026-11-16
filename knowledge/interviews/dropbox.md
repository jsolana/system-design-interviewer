---
title: Dropbox (file storage and synchronization)
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/dropbox, Grokking the System Design Interview (PDF), "Designing Dropbox" pp. 48-59, System Design Interview Vol.1 (Alex Xu) ch. 15 (Google Drive)]
concepts: [presigned-urls, chunked-multipart-upload, cdn-edge-computing, caching, server-sent-events, long-polling, data-deduplication, database-replication, database-partitioning, load-balancer, message-queues, conflict-resolution, sql-vs-nosql, stateless-architecture, database-indexing, websockets]
difficulty: medium
---

# Dropbox

## Prompt
Design a cloud file storage and sharing service (upload, download, share and sync across devices). The source labels it as easy, topic "Handling Large Blobs".

## Functional requirements
- Upload a file from any device.
- Download it from any device.
- Share with other users and see what has been shared with you.
- Automatic synchronization across devices.
- Out of scope: editing, preview, quotas, versioning, antivirus.

## Non-functional requirements
- High availability (takes priority over consistency; eventual consistency acceptable).
- Files up to 50 GB.
- Secure and reliable (recovery from loss/corruption).
- Low latency for upload, download and sync.

## Estimations
- 50 GB at 100 Mbps: 50 x 8 / 100 = 4,000 s (~1.11 h) -> justifies chunking and progress tracking.
- Typical chunks of 5-10 MB. API Gateway payload limit ~10 MB: prevents uploading in a single request.

## API
- `POST /files/presigned-url` (stores metadata in "uploading" state), `GET /files/{id}/presigned-url`.
- `POST /files/{id}/share` (list of users), `GET /files/changes?since=ts` (created/updated/deleted events).
- `PATCH /files/{id}/chunks` (chunk status; evolved into server-side verification).
- Identity comes from the token/JWT, never from a userId sent by the client.

## Data model
- **FileMetadata**: id (UUID), name, size, mimeType, uploadedBy, status (uploading/uploaded), chunks[{id,status}], fingerprint.
- **SharedFiles**: partition key `userId`, sort key `fileId`.
- Entities: File (bytes), FileMetadata, User. DynamoDB suggested, PostgreSQL equally valid.

## Architecture (high-level design)
- Client (web/mobile/desktop) -> LB + API Gateway -> **File Service** (control plane: metadata and URL signing; does not touch bytes) -> Metadata DB; bytes in **S3**; downloads via **CDN**.
- Upload: bad = server disk; good = server forwards to S3 (double upload); excellent = [[presigned-urls]] (client uploads directly to S3, S3 notification moves the state to "uploaded").
- Download: bad = via server; good = presigned URL; excellent = CDN with signed URLs ([[cdn-edge-computing]]).
- Sharing: bad = list of userIds in metadata (scan everything); good = cache of the inverse mapping (must be kept in sync); excellent = normalized SharedFiles table.
- Local->remote sync: client agent with OS events (FSEvents, FileSystemWatcher), change queue, last-write-wins. Remote->local: hybrid of push over one connection per device (WebSocket/[[server-sent-events]]) + periodic polling of `/files/changes` as a safety net.

## Deep dives
1. **Large files** ([[chunked-multipart-upload]]): chunking on the client (not on the server), 5-10 MB, parallel, per-chunk progress, resumable. Chunk state: client PATCH (trusts the client) vs server-side verification with ETags + S3 ListParts. SHA-256 fingerprint of file and chunks to identify/resume/deduplicate (the fileId is a separate UUID). Flow: chunk+hash -> check whether it exists -> CreateMultipartUpload + per-part URLs -> upload -> verify -> CompleteMultipartUpload. Downloads: HTTP Range.
2. **Speed**: CDN; parallel chunks and adaptive size; delta sync with Content-Defined Chunking (rolling hash/Rabin) because with fixed chunks inserting one byte shifts everything; client-side compression (Gzip, Brotli, Zstandard; do not compress already-compressed media; compress before encrypting).
3. **Security**: HTTPS, encryption at rest (S3 SSE), SharedFiles as ACL, short-lived signed URLs (~5 min; they are bearer tokens: IP binding or auth cookies as reinforcement).

## Trade-offs and decisions
- Presigned URLs: faster/cheaper but the backend loses control of the data flow (must verify).
- CDN: low latency at the cost of money; requires Cache-Control and invalidation.
- SharedFiles table: indexed query somewhat slower but without sync problems.
- Polling vs push: they are combined.

## Related concepts
[[presigned-urls]], [[chunked-multipart-upload]], [[cdn-edge-computing]], [[caching]], [[server-sent-events]], [[database-indexing]]

## Follow-up questions
- You are uploading the file twice, how do you avoid it?
- How do you show progress and allow resuming?
- Malicious client that marks chunks as uploaded; delta sync with fixed chunks; misuse of shared links.
- Expectations: mid = API/data and functional HLD; senior = go deep on large files; staff = practical configuration and real trade-offs.

## Variants
- **System Design Interview Vol. 1 (Alex Xu), ch. 15 "Design Google Drive", pp. 244-262**: upload/download, sync across devices, revisions, sharing and notifications; any file type, encryption at rest, max 10 GB, 10M DAU. Out of scope: Google Docs-style collaborative editing. NFRs: reliability (no losses), fast sync, low bandwidth, scalability and high availability.
  - Estimations: 50M registered users, 10M DAU, 10 GB free -> **500 PB** allocated; 2 uploads/day of 500 KB, read:write ratio 1:1; upload QPS ≈ 10M x 2 / 86,400 ≈ 240 (peak 480).
  - Didactic approach: start with a single server (Apache + MySQL + `drive/` directory with per-user namespaces) and scale: sharding by `user_id` -> **Amazon S3** with same-region and cross-region replication -> LB, addable web servers, metadata DB moved out with replication/sharding ([[database-replication]], [[database-partitioning]]).
  - API: simple and **resumable** upload (`uploadType=resumable`: request a resumable URL, upload while monitoring status, resume), `download` (by path) and `list_revisions` (path, limit); all with authentication and HTTPS.
  - **Sync conflicts**: the first version processed wins; the second gets a conflict and both copies (local and server) are shown so it can merge or overwrite ([[conflict-resolution]]).
  - Components: **block servers** (split the file into blocks of up to 4 MB as Dropbox does, each with a unique hash; compress and encrypt each block; **delta sync** = only modified blocks are uploaded), cloud storage, **cold storage** (inactive data, e.g. S3 Glacier), LB, API servers, metadata DB, metadata cache, **notification service** (pub/sub) and **offline backup queue** (pending changes for offline clients).
  - **Strong consistency** of metadata: invalidate the cache on every write and keep cache replicas consistent with the master; a relational DB is chosen for native ACID (in NoSQL it would have to be programmed; [[sql-vs-nosql]]).
  - Metadata schema: User, Device (push_id), Namespace (user root), File (latest version), File_version (read-only, history), Block (order to reconstruct any version).
  - Upload flow: in parallel (1) add metadata with "pending" state and notify; (2) upload to block servers -> compressed/encrypted blocks to cloud storage -> completion callback to API servers -> "uploaded" state -> notify other clients. Download flow: the notification service notifies (or the offline client pulls on reconnect), requests metadata from API servers and downloads the blocks via block servers to reconstruct the file.
  - **Notification service**: long polling (chosen: Dropbox uses it; unidirectional server->client communication and infrequent notifications) vs WebSocket (bidirectional; [[long-polling]], [[websockets]]).
  - **Space savings**: deduplicate blocks by hash at account level ([[data-deduplication]]), limit on versions/keep only the valuable ones (more weight on recent ones), move cold data to cold storage.
  - **Failures**: secondary LB with heartbeat; block server -> others pick up pending jobs; S3 replicated across regions; stateless API; replicated cache; Metadata DB master/slave with promotion; notification server down (more than 1M connections per machine at Dropbox in 2012: reconnecting is slow); replicated offline backup queue.
  - Wrap-up: alternative of uploading directly to cloud storage from the client (faster, but duplicates chunking/compression/encryption logic across iOS/Android/Web and client-side encryption is tamperable); split out a presence service.
  - Differs from the base design: block servers centralize chunking, compression and encryption (vs direct presigned URLs to S3 in the base design), with relational metadata and strong consistency.

- **Grokking the System Design Interview (PDF), pp. 48-59** (Medium difficulty): emphasis on client components and messaging.
  - Requirements: upload/download from any device, sharing, automatic synchronization, files up to GB, ACID, offline editing; extended: snapshots/versions.
  - Estimations: 500 M users, 100 M DAU, 200 files/user = 100 B files x 100 KB = 10 PB.
  - 4 MB chunks (retry only the failed chunk, send only modified chunks, diffs), local metadata on the client.
  - Client in four parts: Internal Metadata DB, **Chunker**, **Watcher** and **Indexer**; exponential backoff on a slow server; on mobile sync on demand.
  - Listening for changes: **HTTP long polling** ([[long-polling]]) instead of polling.
  - Relational Metadata DB (native ACID) or NoSQL with ACID in the Synchronization Service; objects: chunks, files, users, devices, workspaces.
  - Synchronization Service + **Message Queuing Service** with a global Request Queue and one Response Queue per subscribed client (the message is deleted when read); Cloud/Block Storage separated from metadata.
  - Flow: A uploads chunks -> updates metadata -> notifications to B and C -> they download chunks; offline clients receive from their response queue when they reconnect.
  - Inline vs post-process deduplication by chunk hash ([[data-deduplication]]).
  - Metadata partitioning: vertical, by range (first letter of the path) or by hash (+ consistent hashing); block cache (a 144 GB server caches ~36K chunks) with LRU; LB between clients and block/metadata servers; permissions in the metadata DB.

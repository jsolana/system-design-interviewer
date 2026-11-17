---
title: WhatsApp (messaging)
type: interview
sources: [Cracking the Coding Interview ch. 7.7, https://www.hellointerview.com/learn/system-design/problem-breakdowns/whatsapp, Grokking the System Design Interview (PDF), "Designing Facebook Messenger" pp. 60-71, System Design Interview Vol.1 (Alex Xu) ch. 12]
concepts: [websockets, pub-sub, consistent-hashing, presigned-urls, message-queues, database-indexing, long-polling, service-discovery, online-presence, sql-vs-nosql, unique-id-generation, lsm-trees]
difficulty: high
---

# WhatsApp

## Prompt
Messaging app with groups, offline messages and media (calls out of scope). WhatsApp is famously built on Erlang.

## Functional requirements
- Group chats (limit 100); send/receive messages; receive messages sent while offline (up to 30 days); send/receive media.
- Out of scope: calls, business, registration/profile.

## Non-functional requirements
- Delivery < 500 ms to available users; guaranteed delivery.
- Billions of users, high throughput.
- Messages on central servers only for as long as needed.
- Resilience to component failures.

## Estimations
- 200M active x ~20 msg/day = 4B/day ≈ 40K msg/s; writes ~100K/s (Message + Inbox and groups).
- 1B users, ~200M connected; 1-2M users per host -> hundreds of Chat Servers.
- Heartbeat every 10 s: 20M ping/pong per s. Polling every 30 s: ~7M queries/s.
- Kafka with a topic per user: ~50 KB/topic -> 50 TB+ for 1B.
- Reference: 100K updates/s on a Redis host (Canva) at 27%.

## API
Bidirectional WebSocket over TLS: `createChat`, `sendMessage`, `createAttachment`/`getAttachmentTarget` (presigned URL), `modifyChatParticipants`, `getLastSeen`/`updateLastSeen`; server push `chatUpdate`, `newMessage` with client ack (`RECEIVED`), which allows deleting from the Inbox.

## Data model
DynamoDB: **Chat** (chatId); **ChatParticipant** (PK chatId, SK participantId, inverse GSI); **Message** (TTL); **Inbox** per recipient/client (TTL); **Clients** per user; **LastSeen** per user.

## Architecture (high-level design)
- Chat Servers behind an L4 LB with an in-memory userId -> WebSocket map ([[websockets]]).
- Create chat: DynamoDB transaction (batches near 100 participants).
- Offline: write Message + each recipient's Inbox, push to those connected, ack -> delete from the Inbox; on connect the Inbox is drained; TTLs clean up.
- Media: bad = in the DB; good = via the Chat Server to blob storage with a 30 d TTL; excellent = direct upload with [[presigned-urls]] and an opaque URL in the message (expiring media after download remains unresolved).

## Deep dives
1. **Billions of simultaneous users** (host confusion): bad = scale naively; bad = Kafka topic per user; good = [[consistent-hashing]] of Chat Servers with a registry (ZooKeeper/etcd), with connections between servers and careful draining; excellent = [[pub-sub]] (Redis) with a channel per user, at-most-once (durability via the prior Inbox), shard by userId. Partition by user (1:1) vs by chat (large groups); senior improvement: adaptive, per-chat channels above ~25 users with double publishing during the transition.
2. **Multiple clients per user**: Clients table, Inbox per client, Pub/Sub by userId, limit (~3).
3. **WebSocket failures**: bad = TCP timeouts; good = ACK timeout of 500-2000 ms with retry and socket close; excellent = application heartbeats (ping 10-30 s, pong within ~5 s; detection ≈15 s).
4. **Pub/Sub failures**: polling every 30-60 s (~7M qps); per-chat sequence numbers with gap detection (Redis INCR); excellent = global per-user sequence in the heartbeat. In production they are combined.
5. **Out-of-order delivery**: no strict ordering; server receive timestamp (NTP) and the client sorts; messages may "jump" upward.
6. **Last seen**: bad = write on every heartbeat; excellent = write only on disconnect (DynamoDB conditional writes) and ask the target user via Pub/Sub whether they are ONLINE.

## Trade-offs and decisions
- Pub/Sub adds ms of latency and server-shard connections, but avoids the mesh between servers.
- Heartbeats: ping cost vs bounded detection.
- Tolerating apparent disorder versus reordering logic.

## Related concepts
[[websockets]], [[pub-sub]], [[consistent-hashing]], [[presigned-urls]], [[message-queues]]

## Follow-up questions
Partition by chat vs user; regionalization and cell-based architecture (staff). Expectations: mid = HLD and WebSockets; senior = consistent hashing and trade-offs; staff = failure modes.

## Variants
- **System Design Interview Vol. 1 (Alex Xu), ch. 12, pp. 178-199 ("Design a chat system", Messenger-style)**: 1-1 with low latency, small groups (max. 100), presence, multi-device, push; text only (< 100,000 characters), 50M DAU, history forever, E2E out of scope.
  - Protocols: HTTP with keep-alive for the sender; the receiver needs to simulate push: **polling** (expensive, almost always empty), **[[long-polling]]** (sender and receiver may land on different servers with round robin, does not detect disconnections, inefficient if there is little activity) and **[[websockets]]** (bidirectional, persistent, upgrade from HTTP, ports 80/443). WebSocket is used to send and receive; the rest (login, signup, profile) stays as HTTP request/response.
  - Components: **stateless** services (behind an LB; login, profile; includes [[service-discovery]] with ZooKeeper), a **stateful** service (chat servers with a persistent connection), third-party integration (push notifications). Servers: chat, presence, API, notification, key-value store.
  - Scale: 1M concurrent users x ~10 KB/connection ≈ 10 GB, would fit on one server but that would be a SPOF and a red flag; you can start that way and tell the interviewer.
  - Storage: generic data (profile, settings, friends) in relational with replication and sharding; **history in a key-value store** (Messenger uses HBase, Discord Cassandra) for horizontal scaling, low latency and because relational databases handle the long tail with large indexes poorly ([[sql-vs-nosql]]). Pattern: 60,000M messages/day across Messenger and WhatsApp, reads:writes ≈ 1:1 in 1-1, mostly recent data is read except for searches/mentions/jumps.
  - Model: 1-1 table with PK `message_id` (not `created_at`, because of ties); group with composite PK `(channel_id, message_id)` and `channel_id` as the partition key. `message_id` unique and sortable by time: auto_increment does not exist in NoSQL; options: a global Snowflake-style generator ([[unique-id-generator]]) or a **local per-channel sequence** (simpler; sorting within a channel/chat is enough).
  - 1-1 flow: A -> chat server 1 -> ID generator -> message sync queue ([[message-queues]]) -> KV store; if B is online it is forwarded to their chat server 2 and over WebSocket; otherwise, push notification.
  - Multi-device: each device stores `cur_max_message_id`; new messages are the recipient's with a greater id.
  - Small groups: copy of the message in **each member's inbox (message sync queue)**; simplifies synchronization and is affordable with few members (WeChat limits to 500); infeasible for large groups.
  - Presence: [[online-presence]] (login, logout, heartbeat every 5 s with a 30 s window, pub/sub fanout per friend pair).
  - Wrap-up: media (compression, cloud storage, thumbnails), end-to-end encryption, client-side message cache, geo-distributed network (Slack Flannel), errors (if a chat server fails, service discovery provides another), resend with retries and queues.
  - Differs from the base: per-user sync queues + KV store and service discovery to assign a server, instead of routing with consistent hashing/pub-sub between chat servers.

- **Grokking the System Design Interview (PDF), pp. 60-71 (Facebook Messenger)**: 1:1 chat with presence and persistent history; groups and push as an extension.
  - NFR: low latency and **high consistency** (same history on all devices), even at the cost of availability.
  - Estimates: 500 M DAU x 40 messages = 20 B messages/day x 100 B = 2 TB/day -> 3.6 PB in 5 years; 25 MB/s ingress and the same egress.
  - Flow with acks: A -> server (ack) -> stores and sends to B -> B confirms -> server notifies A of delivery.
  - Push (open connection, long polling or WebSockets, see [[long-polling]]) vs pull; hash table userId -> connection; ~50K connections/server -> ~10K servers for 500 M concurrent users; LB that maps UserID -> chat server; message to an offline user: error to the sender or retry.
  - **Message ordering**: the server timestamp is not enough; a per-user/client sequence number is used.
  - Persistence with a separate thread or asynchronous request; retries and failure log; wide-column DB **HBase** (in-memory buffer, fast small writes, range scans), not MySQL/MongoDB because of latency and the load of reading/writing row by row.
  - Presence: do not broadcast every change; the client queries statuses on startup or when opening a chat, the server delays the "online" broadcast by a few seconds and only emits to relevant users.
  - Partitioning by UserID (hash, logical partitions -> physical servers) and not by MessageID; cache of the last ~15 messages of recent conversations on the same machine as the shard; if a chat server fails the client reconnects; message replication (or Reed-Solomon).
  - Groups: group objects identified by GroupChatID on the chat servers, groups table partitioned by GroupChatID; push notifications via a Notification server for offline users.
- **Cracking the Coding Interview (problem 7.7 Chat Server, pp. 128, 322-326)**: object-oriented slice of a chat server (users, add requests, status, private/group conversations), not networking.
  - Actions: sign on/off, send/accept/reject add requests (mutual friendship), status message, create private and group chats, add messages.
  - Classes: UserManager (addUser, approve/reject AddRequest, userSignedOn/Off), User (sentAddRequest/receivedAddRequest), abstract Conversation with GroupChat and PrivateChat, AddRequest (from, to, date, status), UserStatus.
  - Components: DB for long-term data (SQL, or Bigtable-like for scale), clients, a set of servers; XML between client and servers (readable, easy to debug, not compact); data split across machines with replication to cut lookups; no single point of failure (e.g. one machine handling all sign-ins).
  - Hardest problems: really knowing a user is online (ping/heartbeat the client), in-memory vs DB state getting out of sync, scaling the server (splitting data raises consistency problems), denial-of-service from clients.

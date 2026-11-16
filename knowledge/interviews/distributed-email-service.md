---
title: Distributed Email Service
type: interview
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 8 Distributed Email Service, pp. 225-251]
concepts: [message-queues, websockets, long-polling, full-text-search, inverted-index, lsm-trees, database-partitioning, multi-data-center, cap-theorem, caching, sql-vs-nosql, data-deduplication]
difficulty: high
---

# Distributed Email Service

## Prompt
A large-scale email service like Gmail/Outlook/Yahoo Mail (Gmail 1,800 M active users in 2020; Outlook 400 M).

## Functional requirements
- Send and receive emails; fetch all emails (by folder).
- Filter by read/unread; search by subject, sender and body.
- Anti-spam and antivirus; attachments.
- Client-server over HTTP (the SMTP/POP/IMAP protocols are considered legacy). Authentication out of scope.

## Non-functional requirements
- Reliability: do not lose emails.
- Availability: replication across nodes; keep working in the face of partial failures.
- Scalability without degrading performance.
- Flexibility and extensibility (POP/IMAP are very limited; custom protocols may be needed).

## Estimations
- 1,000 M users; 10 emails sent/user/day -> send QPS = 10^9 x 10 / 10^5 = **100,000**.
- 40 emails received/day, 50 KB of metadata: 1,000 M x 40 x 365 x 50 KB = **730 PB/year**.
- 20% with an attachment of ~500 KB: 1,000 M x 40 x 365 x 20% x 500 KB = **1,460 PB/year**.
- Storage-intensive application -> distributed DB.

## API
HTTP webmail (simplified, with pagination in reality):
- `POST /v1/messages` (To/Cc/Bcc recipients).
- `GET /v1/folders` (id, name, user_id; default RFC 6154 folders: All, Archive, Drafts, Flagged, Junk, Sent, Trash).
- `GET /v1/folders/{folder_id}/messages`.
- `GET /v1/messages/{message_id}` (user_id, from, to, subject, body, is_read, attachments...).

## Data model
NoSQL-style DB with **partition key user_id** (a user's entire mailbox in one shard; messages are not shared between users) and a clustering key for ordering:
- `folders_by_user`: user_id (partition), folder_id, folder_name.
- `emails_by_folder`: composite partition key (user_id, folder_id); clustering `email_id` TIMEUUID (chronological order); subject, preview, is_read.
- `emails_by_user` (detail) and `attachments` (email_id + filename, listing `LIST<filename|size>`).
- Read/unread query: NoSQL only queries by partition/clustering key, so it is **denormalized** into `read_emails` and `unread_emails`; marking as read = delete from one and insert into the other (more complex application but fast reads).
- **Conversation threads** (bonus): JWZ algorithm with the `Message-Id`, `In-Reply-To` and `References` headers.

## Architecture (high-level design)
- Background knowledge: SMTP (server to server), POP (downloads and deletes from the server), IMAP (downloads on demand, multi-device, good with slow connections), HTTPS/ActiveSync; DNS with **MX** records with priority (lower number = preferred, retries with the next one); attachments in Base64/MIME with limits (Outlook 20 MB, Gmail 25 MB).
- Traditional server (a single server, Maildir with one file per email): disk I/O and backup become infeasible; does not meet availability or reliability.
- Distributed: webmail -> **web servers** (login, profile, mail API), **real-time servers** (stateful; WebSocket with long polling as a fallback; e.g. Apache James with JMAP over WebSocket), **metadata DB**, **attachment store** (S3; Cassandra does not work: practical blobs < 1 MB and it does not allow a row cache), **distributed cache** (Redis, recent emails), **search store** (inverted index).
- **Send flow**: LB (rate limit) -> web servers validate (size...); if the recipient is on the same domain, spam/virus is checked and it is inserted directly into Sent/Inbox; otherwise, to the **outgoing queue** (large attachments in the object store with a reference) or to the **error queue**; **SMTP outgoing workers** check spam/virus, save in Sent and send to the destination server. Monitor the queue size (recipient down -> retries with **exponential backoff**; too few consumers -> scale).
- **Receive flow**: SMTP load balancer -> SMTP servers (acceptance policy at connection; bounces invalid ones) -> large attachments to S3 -> **incoming queue** (decouples and buffers spikes) -> mail processing workers (spam, virus) -> saves to storage/cache/object store -> if the user is online, push via real-time servers (WebSocket); otherwise, they retrieve it via REST when they return.

## Deep dives
**Metadata**: headers are small and heavily accessed; the body is of variable size and rarely accessed (read once); operations isolated per user; recency rules (82% of reads on data less than 16 days old); high reliability. **DB choice**: relational (indexes, but poor for blobs/emails of >100 KB), pure object storage (backup, but hard for read state/search/threads), NoSQL (Bigtable is used by Gmail; Cassandra possible). Large providers build custom DBs; requirements: columns of several MB, **strong consistency**, minimize disk I/O, high availability, incremental backups.

**Consistency vs availability**: a single primary per mailbox is preferred; on failover the mailbox is not accessible and synchronization is paused (availability is sacrificed for consistency).

**Deliverability** (reaching the inbox, >50% of the world's email is spam): dedicated IPs, classify emails by type/IP (do not mix marketing with important mail), **warm up** new IPs for 2-6 weeks, ban spammers quickly, **feedback loops** with ISPs (separate queues for soft bounces, hard bounces and complaints), **SPF, DKIM, DMARC** authentication (against phishing, 93% of breaches according to Verizon 2018).

**Search**: more writes (reindexing on every send/receive/delete) than reads; scope = own mailbox, ordering by attributes, near real-time and exact indexing (unlike Google). Option 1: **Elasticsearch** with partitioning by user_id, asynchronous reindexing via Kafka; hard to keep in sync with the primary store (two copies), but the index can be rebuilt; good at small/medium scale. Option 2: custom engine embedded in the DB (large providers): a single copy and one system, but a large effort; bottleneck = disk I/O, index written with an **LSM tree** (sequential writes, separate data that changes (folders) from immutable data (mail)).

**Scalability and availability**: independent access patterns per user -> components scale horizontally; multi-data-center replication, user to the nearest one, reachable from another DC during a network partition.

## Trade-offs and decisions
- Outgoing/incoming queue to decouple and absorb spikes versus synchronous processing.
- Denormalization (read/unread) vs simple queries.
- Elasticsearch vs custom engine (complexity and consistency vs engineering effort).
- Strong consistency per mailbox at the cost of availability during failover.
- WebSocket with fallback to long polling for browser compatibility.

## Related concepts
[[message-queues]], [[websockets]], [[long-polling]], [[full-text-search]], [[inverted-index]], [[lsm-trees]], [[database-partitioning]], [[multi-data-center]], [[cap-theorem]], [[caching]], [[sql-vs-nosql]], [[data-deduplication]]

## Follow-up questions
- Fault tolerance (nodes, network, event delays).
- Compliance (European PII/GDPR, legal intercept) and security (phishing, encryption, confidential mode).
- Optimization: the same attachment sent to many recipients is stored several times in S3 -> check for existence before saving.

## Variants
Not covered in the source.

---
title: FB Live Comments
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-live-comments]
concepts: [server-sent-events, pub-sub, websockets, consistent-hashing, cdn-edge-computing, caching, cursor-pagination]
difficulty: medium
---

# FB Live Comments

## Prompt
Comments on a live video: viewers post, see new comments in near real time, and also see the ones posted before they joined.

## Functional requirements
- Post comments on a live; see them while watching; see those from before joining.
- Out of scope: replies and reactions.

## Non-functional requirements
- Millions of concurrent lives, thousands of comments/s per video.
- Availability over consistency (eventual).
- Latency < 200 ms end to end.
- Out of scope: security/authorization, content integrity (spam, hate).

## Estimations
No dedicated section: ~100k SSE connections per server as typical capacity; example mega-stream: 5,000 comments/s with 4-word comments. The 65,535-port limit is not the real ceiling: CPU, memory and file descriptors dominate.

## API
- `POST /comments/:liveVideoId` {message} (userId from JWT/session).
- `GET /comments/:liveVideoId?cursor=&pageSize=10&sort=desc` (history); `since={last_comment_id}` for polling/catch-up.

## Data model
DynamoDB (Postgres/MySQL viable): comments table with `liveVideoId` as partition key and `commentId` as sort key; query with `commentId < cursor`, descending and with a limit.

## Architecture (high-level design)
- Posting: client -> Comment Management Service -> DynamoDB.
- Distribution: polling with `since` (discarded: DB load, useless requests, no millisecond freshness).
- History: offset (bad: slow, unstable under inserts/deletes) vs **[[cursor-pagination]]** (chosen: efficient with an index and stable).

## Deep dives
1. **Real-time broadcast**: polling (no); WebSockets (bidirectional but the load is almost read-only); **SSE** ([[server-sent-events]]) with regular POSTs for writing. Challenges: proxies/LBs that buffer, SSE connection limit per domain, monitoring of long-lived connections.
2. **Millions of concurrent viewers**:
   - Coordination between servers: naive pub/sub (every server processes everything; inefficient); **partitioned pub/sub with co-location** (`hash(liveVideoId) % N`, L7 LB with consistent hashing on liveVideoId or Zookeeper); **Dispatcher Service** with a video -> servers map (heartbeats, Zookeeper/etcd). Kafka handles dynamic subscriptions poorly; Redis pub/sub fits; fire-and-forget is acceptable because there is persistence and catch-up. The author would choose pub/sub with co-location (simpler edge cases).
   - Mega-streams (e.g. World Cup final): at that rate nobody reads individual comments (a general "vibe" is perceived). Good = adaptive representative sampling (50% at 100/s, 1-2% at 5,000/s; prioritize followed, reacted-to, verified); excellent = CDN with snapshots: ring buffer of 100-200 comments, per-second snapshot to Redis/CDN origin, clients poll the CDN and animate. Latency 1-2 s, local optimistic insertion, hysteresis to switch SSE<->CDN (e.g. 100k viewers or 500 comments/s).
3. **Disconnections**: ignoring them (bad); excellent = SSE `Last-Event-ID` + local ID of the last comment and catch-up `since&limit=100`; "you missed N comments" UX; mobile: disconnect in background; bounded replay (e.g. 5 min); shared Redis cache because you reconnect to a different server; deduplicate SSE and HTTP catch-up.

## Trade-offs and decisions
- SSE vs WebSockets: unidirectional and simple in exchange for proxy/browser limits.
- Co-location per video: efficient but subscriptions must be synchronized when scaling.
- Mega-streams: fewer guarantees/more latency in exchange for bounded cost.

## Related concepts
[[server-sent-events]], [[pub-sub]], [[websockets]], [[consistent-hashing]], [[cdn-edge-computing]], [[caching]], [[cursor-pagination]]

## Follow-up questions
No explicit list; the deep dive questions. Expectations: mid = push and pub/sub with hints; senior = pub/sub and leading the scaling discussion; staff = reliability limits and technologies.

## Variants
Not covered in the source.

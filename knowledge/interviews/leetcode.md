---
title: LeetCode
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/leetcode]
concepts: [sandboxed-code-execution, redis-sorted-sets, message-queues, caching]
difficulty: medium
---

# LeetCode

## Prompt
A coding platform: list and view problems, write solutions in several languages, submit them with immediate feedback and see a live competition leaderboard. Small scale (hundreds of thousands of users, ~4,000 problems).

## Functional requirements
- List problems; view a problem and code in several languages; submit and receive a result; live leaderboard.
- Out of scope: auth, profiles, payments, analytics, social, fault tolerance, CI/CD, backups.

## Non-functional requirements
- Availability over consistency.
- Isolated and secure code execution.
- Result in < 5 s.
- Competitions of 100,000 users.

## Estimations
- 90-minute competition, 10 problems, 100k users (solved problems score; ties broken by time).
- Worst case: 10k concurrent submissions x ~100 tests x 100 ms = 1M executions ≈ 100,000 s of CPU -> ~1,667 cores to clear it in 1 min; vertical scaling does not work (machines with a few hundred vCPUs).

## API
- `GET /problems?page&limit`; `GET /problems/:id?language=` (with code stub); `POST /problems/:id/submit` {code, language} (userId from the session); `GET /leaderboard/:competitionId?page&limit`.
- Never trust the client's userId or timestamps.

## Data model
- **Problem** (NoSQL, DynamoDB): id, title, question, level, tags, codeStubs per language (manual or LLM-generated), testCases[{type,input,output}] as a subdocument.
- **Submission**: userId, problemId, competitionId, passed, submittedAt (no explicit schema in the source).

## Architecture (high-level design)
Monolith (API server) + DB; Monaco editor on the client. Submission: API -> worker/container per language -> result in DB -> client. Leaderboard: query of correct submissions grouped by user, ordered by problems solved and then time (in DynamoDB, GSI by competitionId and in-memory aggregation); the client refreshes every ~5 s.

Code execution ([[sandboxed-code-execution]]): on the API server (bad); VM (good: strong isolation, heavy); Docker container (chosen: lightweight, fast startup, weaker isolation -> hardening); serverless (cold starts and limits).

## Deep dives
1. **Isolation and security**: read-only filesystem, output to a deleted temp, CPU/memory limits, timeout (~5 s), no network (VPC SG/NACL), seccomp.
2. **Efficient leaderboard** ([[redis-sorted-sets]]): bad = DB polling; good = Redis cache refreshed every ~30 s (stale); excellent = sorted set (`ZADD` per processed submission, reverse range read) with 5 s polling, top ~1,000 and pagination. WebSockets ruled out as overkill.
3. **Scale to 100k**: vertical (bad); horizontal autoscaling of containers per language (ECS); or a queue (SQS, [[message-queues]]) that absorbs spikes and allows retries -> asynchronous system, the client polls `GET /check/:id` every second.
4. **Multi-language tests**: one test set per problem, standard serialization of inputs/outputs and a harness per language (e.g. binary trees in level order `[3,9,20,null,null,15,7]`).

## Trade-offs and decisions
- Container vs VM vs serverless (startup/isolation/cost).
- A queue is perhaps excessive at this volume, but it adds reliability.
- 5 s polling versus WebSockets.

## Related concepts
[[sandboxed-code-execution]], [[redis-sorted-sets]], [[message-queues]], [[caching]]

## Follow-up questions
There is no list; expectations: mid = API/data and awareness of isolation; senior = secure execution and comparing options; staff = simple design with a scaling path.

## Variants
Not covered in the source. *Note*: the source names the leaderboard endpoint in two different ways.

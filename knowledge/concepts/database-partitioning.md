---
title: Database partitioning
type: concept
aliases: [sharding, partitioning, particionado]
sources: [https://www.figma.com/blog/how-figmas-databases-team-lived-to-tell-the-scale/, Cracking the Coding Interview, ch. 9 pp. 140-141, https://www.hellointerview.com/learn/system-design/problem-breakdowns/gopuff, System Design Interview Vol.1 (Alex Xu), ch. 1, Grokking the System Design Interview (PDF), "Sharding or Data Partitioning" pp. 178-181, Designing Data-Intensive Applications (Kleppmann), ch. 6, DDIA 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 7 (pp. 251-271)]
---

# Database partitioning

## Definition
Dividing a DB's data into subsets (partitions/shards) according to a key, to spread load and storage.

## Why it matters
It lets you scale reads/writes and makes most queries touch only a few partitions.

## How it works
- Choose a partition key aligned with the queries (e.g. region = first 3 digits of the zip in [[gopuff]]).
- Combine with read replicas for reads that tolerate staleness; writes go to the leader.

## Variants and techniques
By region/range, by hash; replicas per partition.

## Trade-offs
Partitions must be balanced (hot partitions) and replicas sized; multi-partition transactions are harder.

## When to use it / when not to
When a single instance can't handle the volume and the queries have a natural locality key.

## Additional detail (Xu Vol. 1, ch. 1)
- Sharding = horizontal DB scaling: shards with the same schema and different data; example `user_id % 4` to pick the shard. The most important thing is the **sharding key** (partition key), which must distribute the data evenly.
- Problems: **resharding** (full shard or uneven distribution; mitigation: [[consistent-hashing]]); **celebrity / hotspot key** (assign one shard per celebrity, even sub-partition; see [[hot-keys]]); **joins and denormalization** (joins across shards are hard; data is denormalized).
- Part of the non-relational functionality is moved to NoSQL to relieve load ([[sql-vs-nosql]]). Context: [[horizontal-vs-vertical-scaling]].

## Additional detail (Grokking, pp. 178-181)
- **Methods**: horizontal/range-based (risk of imbalance, e.g. Manhattan zip codes), vertical (tables per feature on different servers; easy, but a feature may still not fit and cross joins are expensive), **directory-based** (lookup service that abstracts the schema; makes rebalancing easier at the cost of complexity and a new SPOF).
- **Criteria**: hash/key-based (uniform distribution but fixes the number of servers -> [[consistent-hashing]]), list partitioning (e.g. Nordic countries), round-robin (i mod n), composite (consistent hashing = hash + list).
- **Problems**: joins and denormalization, referential integrity (no FKs across servers; cleanup jobs), rebalancing without downtime.
- **Logical partitions**: create many logical partitions over few physical servers and move them by updating a configuration file ([[instagram]], Messenger in [[whatsapp]]).
- Schemes per problem: URL by range/key hash ([[url-shortener]]), tweets by UserID/TweetID/time ([[twitter]]), index by word or by tweet ([[twitter-search]]), trie by capacity ([[typeahead]]), shows by ShowID ([[ticketmaster]]).

## Additional detail (DDIA, ch. 6)
- **Strategies**: *key-range* (sorted ranges; allows range scans but risks hot spots, e.g. key = timestamp -> prefix by sensor/entity) vs *key hash* (spreads evenly, loses range queries; in MongoDB hash-sharding, range queries go to all partitions). Cassandra compromise: **compound key**, the first column is hashed (partition) and the rest sorts (SSTables) -> `(user_id, timestamp)` model for one-to-many.
- **Hot keys/skew**: hashing doesn't fix a single hot key (celebrity); technique: add a random suffix (e.g. 2 digits = 100 keys) when writing and read from all of them and combine; only for the few hot keys ([[hot-keys]]).
- **Secondary indexes**: *local / document-partitioned* (each partition indexes its own documents; write to one partition, but **scatter/gather** read from all, with tail latency amplification; used by MongoDB, Cassandra, Elasticsearch) vs *global / term-partitioned* (index partitioned by term: efficient reads from one partition and range scans, but writes that touch several partitions and are usually updated asynchronously, like DynamoDB GSI).
- **Rebalancing**: goals = fair distribution, keep serving during the process, and move the minimum of data. `hash mod N` is a bad idea (moves almost everything). Options: (1) **fixed number of partitions** (many more than nodes, e.g. 1000 on 10 nodes; only whole partitions move; Riak, Elasticsearch, Couchbase); (2) **dynamic partitioning** (split when they exceed a size, merge when they empty; HBase, MongoDB; starts with a single partition, mitigable with pre-splitting); (3) **proportional to nodes** (fixed number of partitions per node; Cassandra). Automatic rebalancing + failure detection can cause cascades: human approval is preferable.
- **Request routing / service discovery**: three approaches (any node forwards; routing layer; client knows the assignment); usually delegated to a coordination service (ZooKeeper, [[consensus]]) or *gossip* (Cassandra) to learn the partition->node assignment.
- Partitioning + [[replication]]: each partition is replicated; multi-partition transactions require [[two-phase-commit]] or avoiding them.

## Additional detail (DDIA 2nd edition, ch. 7)
*2nd edition note*: "partitioning" is renamed **sharding** (ch. 7).
- Sharding is heavyweight: only needed when data volume or **write** throughput exceeds one node (read scaling can use replicas). Needs a partition key; cross-shard writes need distributed transactions. Some systems shard inside one machine (one process per core: Redis, VoltDB, FoundationDB).
- **Hash-range sharding**: assign ranges of the hash space to shards that can split/merge (YugabyteDB, DynamoDB, optional in MongoDB). Cassandra/ScyllaDB use many ranges with random boundaries per node (16 per node in Cassandra, 256 in ScyllaDB). Compound keys: hash the first column, range-scan the rest (BigQuery partition + cluster columns, Snowflake micro-partitions, Delta Lake). Language built-in hash functions (Java hashCode, Ruby hash) are unsuitable (vary per process).
- **Fixed number of shards** (Citus, Riak, Elasticsearch, Couchbase): choose a count divisible by many numbers (e.g. 1,000) and give stronger nodes more; resharding is costly if the guess is wrong.
- **Hot keys**: append a random 2-digit suffix to a hot key to spread writes over 100 keys (reads must gather all; track which keys are split). Cloud services automate this (Amazon heat management / adaptive capacity). Rebalancing automatic vs manual (Couchbase/Riak suggest and an admin commits).
- Multitenancy via sharding: [[multitenancy-and-cell-based-architecture]].

## Additional detail (Figma, https://www.figma.com/blog/how-figmas-databases-team-lived-to-tell-the-scale/)
Production story: Postgres on the largest RDS instance, ~100x growth 2020-2024; vacuum and write IOPS limits hit on multi-TB tables.
- **Phase 1, vertical partitioning**: groups of related tables moved to their own DBs (a dozen by end of 2022); quick win but a single table is the smallest unit.
- **Phase 2, horizontal sharding** of tables with hashed routing on the shard key (UserID, FileID, OrgID) to avoid hot spots from auto-increment/Snowflake-style IDs; related tables are **colos** sharing a key so joins/transactions stay in one shard. First sharded table shipped Sept 2023 (~9 months of work).
- **DBProxy** (Go) between app and PgBouncer: parser -> logical planner (logical shard IDs) -> physical planner (maps to physical DBs, rewrites queries); query language covers ~90% of production queries; queries without the shard key become scatter-gather.
- **Logical before physical**: Postgres views expose per-shard subsets on the unsharded DB, rolled out by percentage feature flag (rollback = config change); only then copy data to N physical DBs. Shadow planning/reads de-risked decisions. Failover ~10 s partial availability; topology updates < 1 s; views < 10% overhead.
- Rejected NewSQL (CockroachDB, TiDB, Spanner, Vitess) and NoSQL because of migration risk and rewrite cost; built a narrower in-house solution.
- Costs: no atomic cross-shard transactions, no cross-shard FKs/unique indexes, coordinated schema changes, inefficient range scans on hashed keys.

## Additional detail (Cracking the Coding Interview, ch. 9)
- Vertical partitioning: by feature (profiles, messages); a table that grows huge needs repartitioning.
- Key/hash-based: server = mod(key, N); N is effectively fixed, adding servers reshuffles all data.
- Directory-based: lookup table makes adding servers easy but is a single point of failure and a performance hit.
- Real systems usually combine schemes. Related design drill ("scale an algorithm"): ask questions, pretend all data fits on one machine, get real (how to split data, how does a machine know where to look), then solve those issues iteratively. Example: find documents containing all words from a list, by splitting the inverted index by keyword ranges (small lookup table, expensive shifts when data grows) or by document; see [[inverted-index]].

## Appears in
[[digital-wallet]], [[distributed-cache]], [[distributed-email-service]], [[distributed-message-queue]], [[distributed-rate-limiter]], [[dropbox]], [[duplicate-url-detection]], [[fb-post-search]], [[gaming-leaderboard]], [[git-repository-hosting]], [[gopuff]], [[hotel-reservation]], [[nearby-friends]], [[pastebin]], [[proximity-service]], [[s3-object-storage]], [[search-query-cache]], [[social-network-shortest-path]], [[tinder]], [[top-k]], [[twitter]], [[twitter-search]], [[typeahead]], [[uber]], [[unique-id-generator]], [[web-crawler]], [[youtube]]

## See also
[[caching]], [[database-indexing]]

---
title: SQL vs NoSQL
type: concept
aliases: [relational vs non-relational databases]
sources: [Grokking the System Design Interview (PDF), "SQL vs. NoSQL" pp. 185-188, System Design Interview Vol.1 (Alex Xu), ch. 1]
---

# SQL vs NoSQL

## Definition
Two major families of databases: relational (tables, fixed schema, SQL) and non-relational (dynamic schema, different storage models).

## Why it matters
The choice shapes scaling, consistency and modeling; in an interview it must be justified with the characteristics of the data (volume, relationships, access pattern).

## How it works
**NoSQL types**
- Key-value: Redis, Voldemort, Dynamo.
- Document: MongoDB, CouchDB.
- Wide-column: Cassandra, HBase (column families; rows with different numbers of columns; good for large volumes).
- Graph: Neo4j, InfiniteGraph.

**Differences**
| Aspect | SQL | NoSQL |
|---|---|---|
| Storage | Tables, rows = entities | key-value, document, graph, columnar |
| Schema | Fixed, changing it is costly/offline | Dynamic |
| Queries | SQL, powerful | Collection-centric; own syntax |
| Scaling | Vertical (horizontal scaling is hard) | Horizontal, commodity hardware, often auto-distribution |
| ACID | Mostly ACID | Usually sacrificed for performance/scale |

## Variants and techniques
Many systems use both (polyglot persistence).

## Trade-offs
- Reasons for SQL: need for ACID (e-commerce, financial), structured and stable data, joins.
- Reasons for NoSQL: large volumes with little structure, multi-datacenter scaling in the cloud with cheap hardware, fast development with a changing schema.
- If NoSQL is chosen where ACID is needed (e.g. [[dropbox]] metadata), ACID has to be implemented in application logic.

## When to use it / when not to
Examples in the source: URLs/pastes (billions of small objects without relationships) -> key-value NoSQL; video/user metadata -> MySQL; chat messages (many small writes + range scans) -> wide-column HBase; user-photo/follower relationships -> Cassandra; reservations with ACID -> SQL.

## Additional detail (Xu Vol. 1, ch. 1)
The book's criterion: relational is the default option (more than 40 years of maturity, joins with SQL). Consider NoSQL (CouchDB, Neo4j, Cassandra, HBase, DynamoDB) if: very low latency is needed; the data is unstructured or non-relational; you only need to serialize/deserialize (JSON, XML, YAML); or you need to store massive amounts. The four families: key-value ([[key-value-store]]), graph, column and document; generally without joins.

## Appears in
[[distributed-email-service]], [[dropbox]], [[gaming-leaderboard]], [[key-value-store]], [[pastebin]], [[twitter]], [[whatsapp]]

## See also
[[cap-theorem]], [[database-partitioning]], [[database-indexing]]

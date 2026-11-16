---
title: Data models (relational, document, graph)
type: concept
aliases: [relational model, document model, graph model, NoSQL, schema-on-read, impedance mismatch, SQL vs NoSQL, normalization, polyglot persistence]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 2 (pp. 27-70)]
---

# Data models

## Definition
Data models determine how the problem is thought about and which queries are natural: relational (tables and joins), document (hierarchical JSON) and graph (vertices and edges).

## Why it matters
Choosing the right model simplifies code and queries; a wrong choice leads to manual joins or rigid schemas.

## How it works
- **Relacional**: tables, joins, normalization, strong support for many-to-one/many-to-many joins.
- **Documento** (MongoDB, CouchDB): self-contained JSON documents; better **locality** (the whole profile in one read) and less *impedance mismatch*; natural one-to-many (tree). Weak at many-to-many and joins (done in the application). References by ID. The whole document is updated (small changes rewrite everything).
- **Schema-on-write** (relacional) vs **schema-on-read** (document: "schemaless" = implicit, useful with heterogeneous data).
- **Normalization vs denormalization**: store IDs (a name changes in one place) vs duplicate (fast reads, costlier writes); Twitter timeline example.
- **Grafos**: property graph (Neo4j, cypher), triple-store (RDF, SPARQL), Datalog. For highly connected many-to-many relationships and variable-length (recursive) queries, which are hard in SQL.
- Lenguajes: **declarative** (SQL, CSS) lets the optimizer parallelize and change the plan, vs imperative; MapReduce as a mix.

## Variants and techniques
- Converging models: PostgreSQL/MySQL with JSON, document databases with joins.
- **Analytical models**: star schema (fact table + dimensions), snowflake ([[olap-columnar-stores]]).
- Event/derived views ([[event-sourcing]]).

## Trade-offs
| Model | Strong | Weak |
|---|---|---|
| Relational | joins, many-to-many, integrity | impedance mismatch, rigid schema |
| Document | locality, flexibility | joins, partial writes |
| Graph | arbitrary relationships | general use |

## When to use it / when not to
Tree-shaped data read as a whole -> document; highly interrelated data -> relational or graph. Combining systems is common (polyglot persistence).

## Appears in


## See also
[[database-indexing]], [[database-partitioning]], [[encoding-and-schema-evolution]], [[lsm-trees]], [[b-trees]]

---
title: Encoding and schema evolution
type: concept
aliases: [serialization, Protocol Buffers, Thrift, Avro, JSON, forward compatibility, backward compatibility, dataflow through services, REST, RPC]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 4 (pp. 111-152)]
---

# Encoding and schema evolution

## Definition
How to translate in-memory structures into bytes (serialization) to store them or send them over the network, and how to evolve the format without breaking readers/writers of different versions.

## Why it matters
In rolling upgrades, new and old code coexist, as do old and new data. **Backward compatibility** (new code reads old data) and **forward compatibility** (old code reads new data) are needed.

## How it works
- Language-specific formats (Java serialization, pickle): avoid (coupled, insecure, unversioned).
- JSON/XML/CSV: human-readable, ambiguity with numbers (large ints >2^53), no native binary support.
- Binary formats with a schema: **Thrift** and **Protocol Buffers** use *field tags* (numbers) instead of names: you can rename fields, add new optional fields or ones with a default (forward-compat: old readers ignore unknown tags), never reuse tags; only optional fields can be removed.
- **Avro**: no tags; uses a *writer's schema* and a *reader's schema* and reconciles them by field name; compatibility by adding/removing fields with defaults; ideal for generating the schema dynamically (e.g. a DB dump). The writer's schema is included in the file (Hadoop), with a version number (DB) or negotiated on connection (RPC).
- Advantages of schemas: compact, always up-to-date documentation, compatibility checking.

## Variants and techniques
- Dataflow through a **DB** ("data outlives code"; beware of losing unknown fields when rewriting), through **REST/RPC services** (RPC "location transparency" is a mistake: unreliable network, variable latencies, retries -> [[idempotency]]; servers are upgraded before clients, so backward compatibility on requests and forward compatibility on responses) and through **asynchronous messaging** ([[message-queues]]; the broker decouples, retries, buffers).
- Actor model: the same evolution challenges in messages.

## Trade-offs
Text (readable, flexible) vs binary with a schema (compact, fast, controlled evolution). Tags (Protobuf) vs names (Avro).

## When to use it / when not to
Public APIs: JSON/REST; high-volume internal services and data pipelines (Kafka, Hadoop): Avro/Protobuf.

## Appears in


## See also
[[message-queues]], [[change-data-capture]], [[idempotency]]

---
title: Encoding and schema evolution
type: concept
aliases: [serialization, Protocol Buffers, Thrift, Avro, JSON, forward compatibility, backward compatibility, dataflow through services, REST, RPC]
sources: [Designing Data-Intensive Applications (Kleppmann), full PDF, ch. 4 (pp. 111-152), DDIA 2nd ed. (Kleppmann & Riccomini), full PDF, ch. 5 (pp. 161-191)]
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

## Additional detail (DDIA 2nd edition, ch. 5)
*Verification note:* the 1st-edition entry holds up against the 2nd edition (now ch. 5 "Encoding and Evolution"). Corrections/additions:
- **Protocol Buffers / Avro** (Thrift is only mentioned): in the 2nd edition removing a field is handled by *reserving its tag*, never reusing it; the old "required vs optional" distinction is not used. Protobuf has no list type, `repeated` is used; varints (1337 in 2 bytes; -64..63 in 1 byte). Changing int32->int64 is safe forward only if values fit.
- Size comparison for the same record: JSON text 81 bytes, MessagePack 66, Protobuf 33, Avro 32 (no tags or types in the data; reader needs the exact writer schema). Avro: nulls need a union type (`["null","long"]`, default null first); field renames via aliases; schemas have IDL and JSON forms.
- **JSON Schema** (new emphasis): used in OpenAPI, schema registries (Confluent, Apicurio); open vs closed content models (`additionalProperties`), conditional logic; very powerful but hard to evolve. Base64 for binary adds ~33%. Large IDs (>2^53) as in X's 64-bit IDs need string copies. Zero-copy formats exist.
- Language-specific serialization: also a security problem (deserializing arbitrary classes, CWE-502).
- **Services**: REST vs RPC, IDLs (OpenAPI/Swagger, gRPC/Protobuf), frameworks (Spring Boot, FastAPI, gRPC). **Service discovery and load balancing** options: hardware LB, software LB, DNS, discovery systems (etcd/ZooKeeper with heartbeats), service mesh/sidecars (Istio, Linkerd). API versioning: URL, Accept header, or stored per API key.
- **New: durable execution and workflows** ([[workflow-orchestration]]): orchestrator + executor; engines like Airflow/Dagster (ETL), Camunda/Orkes (BPMN), Temporal/Restate (durable execution). Durable execution logs RPCs and state changes (like a WAL) so a retried task skips completed calls: exactly-once for workflows if the external services are idempotent; code must be deterministic and call order must not change (version workflows separately).
- **New: event-driven architectures**: message brokers buffer, redeliver, decouple and avoid service discovery; queue vs topic delivery; schema registries and AsyncAPI; distributed **actor** frameworks (Akka, Orleans, Erlang/OTP) where location transparency works better because message loss is assumed.

## Appears in
None yet.

## See also
[[message-queues]], [[change-data-capture]], [[idempotency]]

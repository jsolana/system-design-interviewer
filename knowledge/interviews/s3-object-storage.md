---
title: S3-like Object Storage
type: interview
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 9 S3-like Object Storage, pp. 253-285]
concepts: [object-storage, erasure-coding, replication, consistent-hashing, consensus, database-partitioning, chunked-multipart-upload, write-ahead-log, multi-data-center, database-indexing]
difficulty: high
---

# S3-like Object Storage

## Prompt
Design an object storage service like Amazon S3 (launched in 2006; 100 trillion objects in 2021): buckets, uploading/downloading objects, versioning and listing.

## Functional requirements
- Create buckets.
- Upload and download objects.
- Object versioning.
- List the objects in a bucket (like `aws s3 ls`).
- Massive objects (GBs or more) and many small objects (tens of KB).

## Non-functional requirements
- 100 PB of data per year.
- Durability of 6 nines (99.9999%); availability of 4 nines (99.99%).
- Storage efficiency: low cost with high reliability and performance.

## Estimations
- Bottlenecks: disk capacity and IOPS (a 7200 rpm SATA disk: 100-150 random seeks/s).
- Distribution: 20% small objects (<1 MB), 60% medium (1-64 MB), 20% large (>64 MB); medians 0.5 MB, 32 MB and 200 MB; storage usage of 40%.
- Number of objects = 10^11 MB x 0.4 / (0.2x0.5 + 0.6x32 + 0.2x200) MB ~ **0.68 trillion**; with 1 KB of metadata per object, ~**0.68 TB** of metadata.

## API
- `PUT /bucket/object` (headers Host, Date, Authorization, Content-Type, Content-Length, `x-amz-meta-*`), `GET /bucket/object`; create bucket with PUT; listing by prefix (3 uses: list buckets, list objects of one level with roll-up of common prefixes, recursive listing).
- Multipart: initiate (returns uploadID), upload parts with uploadID (returns ETag), complete with the list of parts+ETags.

## Data model
- **bucket**: bucket_name, bucket_id, owner_id, enable_versioning. Small table (1M customers x 10 buckets x 1 KB = 10 GB): fits on one server; read replicas if needed.
- **object**: bucket_name, object_name, object_version (TIMEUUID), object_id (UUID). The current version is the one with the highest TIMEUUID; deletion with versioning inserts a *delete marker* (GET returns 404).
- **object_mapping** (inside each data node): object_id, file_name, start_offset, object_size; in local SQLite per node (fast reads with a B+ tree; RocksDB is faster at writes but slower at reads, and the pattern is write-once/read-many).
- Sharding of `object`: by bucket_id creates hotspots (a bucket can have trillions of objects); by object_id prevents lookup by URI; chosen **hash(bucket_name, object_name)**.

## Architecture (high-level design)
- Load balancer -> **API service** (stateless; orchestrates IAM, metadata and data store) -> **IAM** (authentication and authorization) -> **metadata service / metadata store** (metadata DB) and **data store** (data by object_id/UUID).
- **Upload**: create bucket (API, IAM verifies WRITE, entry in the metadata DB); then PUT object: IAM, data to the data store (returns UUID), and the metadata row (object_id, bucket_id, object_name) is inserted.
- **Download**: IAM verifies READ, the UUID is obtained from the metadata store by name, the data is read from the data store and returned. There is no real hierarchy: "folders" are by prefix in the name.

## Deep dives
**Data store** = *data routing service* (stateless, gRPC/REST; queries the placement service, reads/writes on data nodes) + **placement service** + **data nodes**.
- *Placement service*: maintains the **virtual cluster map** (physical topology; physically separated replicas); detects failures through heartbeats (a node is "down" if it does not respond within 15 s); critical, so it is deployed as a cluster of 5 or 7 nodes with **Paxos/Raft** (tolerates 3 failures out of 7). Choosing the replication group of a UUID must be deterministic and robust to additions/removals: [[consistent-hashing]].
- *Data node*: service daemon that sends heartbeats (number of disks and data per disk); on the first heartbeat it receives an ID, the cluster map and where to replicate.
- *Write flow*: the routing service generates the UUID, the placement service returns the primary, the primary stores and replicates to 2 secondaries and responds when all confirm (strong consistency; latency is that of the slowest replica). Alternatives: acknowledge with primary + 1 secondary (medium) or only the primary (worse consistency, lower latency); the last two are eventual consistency.
- *Data organization*: one file per object wastes blocks (4 KB) and exhausts inodes; solution: **append to a large read-write file** (like a WAL), which becomes read-only once it reaches a few GB; writes to the active file are serialized, so one read-write file is given per core. Lookup with the object_mapping table.
- **Durability**: 3 replicas with an annual disk failure rate of 0.81% -> 1 - 0.0081^3 ~ 0.999999 (6 nines). **Failure domains** (node, rack, AZ/data center): replicate across AZs. **[[erasure-coding]]** (8+4: 11 nines, 50% overhead versus 200%, but more compute and slower reads); the design focuses on replication.
- **Correctness verification**: checksum (MD5, SHA1, HMAC) at the end of each object and of the whole file before marking it read-only; on read it is compared and if it fails, data is read from other failure domains.

**Metadata and listing**: with a single DB, `WHERE bucket_id=... AND object_name LIKE 'abc/%'` and roll-up in the application. With a sharded DB, all shards must be queried and results aggregated; cursor pagination is complex (one offset per shard). Since listing is not a priority in object storage, a **listing table sharded by bucket_id is denormalized** (a single DB per query).

**Versioning**: new row with the same bucket and object_name but new object_id and object_version; old versions are not marked deleted.

**Multipart upload** ([[chunked-multipart-upload]]): split (e.g. 1.6 GB into 8 parts of 200 MB), upload each part with uploadID, the ETag (MD5) validates each part, complete by reassembling by part number (can take minutes). Leftover parts are cleaned up by the garbage collector.

**Garbage collection**: lazily deleted objects, orphaned data (incomplete uploads) and corrupted data. Cleaned periodically through **compaction**: copy live objects from read-only files into a new file, update object_mapping (file_name, start_offset) in a transaction and wait until many files accumulate to avoid creating many small ones; it also reclaims space on replicas (or on all 12 nodes with 8+4).

## Trade-offs and decisions
- Separate metadata (mutable) and data (immutable) to optimize them separately.
- Replication (simple, fast) vs erasure coding (cheap, more durable, complex).
- Strong consistency on write (all replicas) vs latency.
- Small objects grouped into large files vs one file per object.
- Shard by hash(bucket_name, object_name) and a denormalized listing table.
- Local SQLite for object_mapping vs shared DB or RocksDB.

## Related concepts
[[object-storage]], [[erasure-coding]], [[replication]], [[consistent-hashing]], [[consensus]], [[database-partitioning]], [[chunked-multipart-upload]], [[write-ahead-log]], [[multi-data-center]], [[database-indexing]]

## Follow-up questions
- How to avoid data corruption in memory and between processes (checksums).
- How to distribute replicas across failure domains.

## Variants
Not covered in the source.

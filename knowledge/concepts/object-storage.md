---
title: Object storage
type: concept
aliases: [object storage, blob storage, S3]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF), ch. 9 S3-like Object Storage, pp. 253-285]
---

# Object storage

## Definition
Storing data as **objects** (payload + metadata) in a flat structure of **buckets**, accessible through a REST API (S3, Google Cloud Storage, Azure Blob). It trades performance for durability, vast scale and low cost; aimed at "cold" data (archive, backup, unstructured binaries).

## Why it matters
It is the storage layer for attachments, videos, images, map tiles, backups... in almost any system design.

## How it works
- **Block vs file vs object**: block storage (disks, raw volume; flexible and high-performance: VMs, databases); file storage (on top of block, directory hierarchy, SMB/NFS; general purpose); object storage (flat, RESTful, vast scale, not mutable: versioning; strong consistency; low-to-medium performance).
- Concepts: bucket (globally unique name), object (data + key-value metadata), versioning (bucket-level), URI, SLA (S3 Standard-IA: 11 nines of durability, 99.9% availability).
- Properties: **immutable** objects (replaced, not edited), accessed as key-value (URI -> data), write once/read many (95% reads according to LinkedIn), both small and huge objects.
- Analogy with the UNIX file system: metadata store = inodes, data store = disk; separating them allows optimizing each (immutable data vs mutable metadata).
- Detailed design in [[s3-object-storage]].

## Variants and techniques
Simulated hierarchy with *prefixes* in the object name; multipart upload ([[chunked-multipart-upload]]); presigned URLs ([[presigned-urls]]); durability through replication or [[erasure-coding]].

## Trade-offs
Very durable and cheap, but slow and with no in-place update or efficient listing.

## When to use it / when not to
Large binaries and rarely changing data. Not for transactional databases or low-latency random access (use block storage).

## Appears in
[[s3-object-storage]]

## See also
[[erasure-coding]], [[s3-object-storage]], [[cdn-edge-computing]], [[write-ahead-log]]

---
title: Chunked / multipart upload
type: concept
aliases: [chunking, resumable upload, content-defined chunking, delta sync]
sources: [System Design Interview Vol. 2 (Xu & Lam, PDF) ch. 9 pp. 282-284, https://www.hellointerview.com/learn/system-design/problem-breakdowns/dropbox, System Design Interview Vol.1 (Alex Xu), ch. 14 and 15]
---

# Chunked / multipart upload

## Definition
Splitting a large file into parts (5-10 MB) that are uploaded in parallel and in a resumable way.

## Why it matters
Avoids timeouts, size limits (API Gateway ~10 MB) and losses from network cuts, and allows showing progress.

## How it works
- Chunking is done by the **client**, not the server.
- Fingerprint (SHA-256) of the file and of each chunk to identify content, resume and deduplicate.
- S3: CreateMultipartUpload -> signed URLs per part -> direct upload -> server verifies ETags with ListParts -> CompleteMultipartUpload.
- Per-chunk state in metadata (uploading/uploaded).
- Downloads: HTTP Range for parallel/resumable transfers.

## Variants and techniques
- State reported by the client (trusting it) vs verified by the server.
- **Content-Defined Chunking** (rolling hash, Rabin) for delta sync: boundaries do not shift when bytes are inserted, unlike fixed chunks.
- Client-side compression (Zstandard/Brotli/Gzip), before encrypting and not on already-compressed media.

## Trade-offs
More complexity and API calls in exchange for robustness and speed.

## When to use it / when not to
Large files or unreliable networks; unnecessary for small files.

## Additional detail (Xu Vol. 1, chs. 14 and 15)
YouTube: the client splits the video by GOP for fast, resumable uploads. Google Drive: **simple** vs **resumable** upload (request a resumable URL, upload while monitoring state, resume if interrupted); block servers split files into blocks of up to 4 MB (Dropbox reference), compress and encrypt each one and upload only the modified ones (delta sync). See [[youtube]], [[dropbox]].

## Additional detail (Xu & Lam Vol. 2, ch. 9)
Multipart upload flow in object storage: initiate (returns `uploadID`), upload each part with the uploadID (the server returns an **ETag** = MD5 of the part), and complete by sending uploadID + list (part number, ETag); the server reassembles by part number (can take minutes for huge objects). Parts that were already reassembled or abandoned are reclaimed by a garbage collector. See [[s3-object-storage]].

## Appears in
[[dropbox]], [[s3-object-storage]], [[youtube]]

## See also
[[presigned-urls]]

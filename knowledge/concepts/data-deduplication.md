---
title: Data deduplication
type: concept
aliases: [deduplication, dedupe, video deduplication]
sources: [Grokking the System Design Interview (PDF), "Designing Dropbox" pp. 56-57, "Designing Youtube or Netflix" pp. 88-89, "Designing a Web Crawler" pp. 125-126, System Design Interview Vol.1 (Alex Xu), ch. 15]
---

# Data deduplication

## Definition
Eliminating duplicate copies of data to improve storage usage and reduce transferred bytes.

## Why it matters
Saves storage, bandwidth, cache and energy; for video it avoids duplicate results and slow starts.

## How it works
- **Dropbox (4 MB chunks)**: a hash (e.g. SHA-256) of each chunk is compared with the existing ones; if it already exists, only a reference is added in the metadata.
  - *Post-process*: it is stored first and analyzed afterwards; the client does not wait, but duplicates are temporarily stored and transferred.
  - *In-line*: hash computed in real time; optimal for network and storage, the client waits for the computation/lookup.
- **YouTube**: duplicates differ in aspect ratio, encoding, overlays, or are excerpts. Inline during upload is preferable, using video matching algorithms (block matching, phase correlation): if it already exists, cut the upload short or keep the higher-quality one; if it is a sub-part, upload only the missing pieces.
- **Web crawler**: dedupe of documents (64-bit checksum; 15B x 8 B = 120 GB) and of URLs (4 B checksum; 15B x 4 B = 60 GB), with a local LRU cache and persistent backing; [[bloom-filter]] option (false positives = pages never downloaded).

## Variants and techniques
Inline vs post-process; at the chunk, document or URL level.

## Trade-offs
Inline computation latency vs immediate savings; Bloom filter false positives vs memory.

## When to use it / when not to
Massive storage with high redundancy (file synchronization, video, crawling).

## Additional detail (Xu Vol. 1, ch. 15)
In Google Drive, redundant blocks are eliminated at the account level: two blocks are identical if they have the same hash. In addition, the number of stored versions is limited (prioritizing recent ones) and cold data moves to cold storage (S3 Glacier). See [[dropbox]].

## Appears in
[[distributed-email-service]], [[dropbox]], [[web-crawler]], [[youtube]]

## See also
[[chunked-multipart-upload]], [[bloom-filter]], [[dropbox]], [[youtube]], [[web-crawler]]

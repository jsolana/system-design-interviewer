---
title: YouTube
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/youtube, Grokking the System Design Interview (PDF), "Designing Youtube or Netflix" pp. 82-91, System Design Interview Vol.1 (Alex Xu) ch. 14]
concepts: [adaptive-bitrate-streaming, presigned-urls, chunked-multipart-upload, cdn-edge-computing, caching, message-queues, workflow-orchestration, data-deduplication, database-replication, database-partitioning, stateless-architecture, video-transcoding]
difficulty: medium
---

# YouTube

## Prompt
A video platform where users upload and others stream. Focus on the upload and playback flows.

## Functional requirements
- Upload videos; watch them (streaming).
- Out of scope: view counters, search, comments, recommendations, channels, subscriptions.

## Non-functional requirements
- High availability (over consistency).
- Videos of tens of GB.
- Low-latency streaming, also with low bandwidth.
- ~1M uploads/day and ~100M views/day.
- Resumable uploads.
- Out of scope: harmful content, bots, monitoring.

## Estimations
- 1M videos/day ≈ 365M metadata records per year; 100M views/day.
- 10 GB at 100 Mbps ≈ 13+ min of download -> motivates streaming.

## API
- `POST /presigned_url` (metadata only; returns S3 presigned URL).
- `GET /videos/{videoId}` -> VideoMetadata with playback URLs.
- `PATCH /videos/{id}/chunks` (chunk status, resumption).

## Data model
- **VideoMetadata** in Cassandra, partitioned by `videoId` (point reads): uploader, references to manifests, `chunks` [{fingerprint, status NotUploaded/Uploaded}].
- **S3**: original, segments in several formats and manifests. Entities: User, Video, VideoMetadata.

## Architecture (high-level design)
- Concepts: codec (H.264, VP9, AV1), container, bitrate, manifests (primary and media with segment URLs).
- Upload with [[presigned-urls]] + multipart directly to S3; an S3 event triggers processing.
- Storage: original only (bad); several formats (good, no partial download); **segments of a few seconds transcoded per format** (great).
- Playback: full download (bad); segments in sequence (good, does not adapt to bandwidth); **[[adaptive-bitrate-streaming]]** with manifest and quality switching per segment (great).

## Deep dives
1. **Processing for ABR**: split into segments (ffmpeg), transcode each segment and generate audio/transcripts in parallel, create manifests, mark complete. It is an orchestrated DAG with a workflow engine such as Temporal ([[workflow-orchestration]]); intermediate data in S3 passing URLs. Waits for the full upload (starting earlier would require segmenting on the client, with incomplete segments).
2. **Resumable uploads** ([[chunked-multipart-upload]]): 5-10 MB chunks with fingerprint, registered as NotUploaded; after each upload the client sends partNumber+ETag and the backend verifies; CompleteMultipartUpload emits a single event. On resume, completed chunks are skipped.
3. **Scale**: stateless Video Service behind an LB; Cassandra (leaderless replication, consistent hashing) with hot videos -> replicate popular partitions and a distributed LRU cache by videoId; processing service with an internal queue ([[message-queues]]) whose depth drives autoscaling; regional S3 -> [[cdn-edge-computing]] for segments and manifests.
4. Suggested extras: faster upload (client-side segmentation in a pipeline), resume playback (progress per user/video), exact vs estimated view counters.

## Trade-offs and decisions
- Segmenting adds pipeline complexity but enables ABR.
- Waiting for the full upload simplifies but delays availability.

## Related concepts
[[adaptive-bitrate-streaming]], [[presigned-urls]], [[chunked-multipart-upload]], [[cdn-edge-computing]], [[caching]], [[message-queues]], [[workflow-orchestration]]

## Follow-up questions
No list; expectations: mid = API/data, upload and playback with multipart and segments; senior = post-processing and upload mechanics; staff = trade-offs and bottlenecks.

## Variants
- **System Design Interview Vol. 1 (Alex Xu), ch. 14, pp. 220-242**: upload and watch videos, mobile/web/smart TV, 5M DAU, 30 min/day on average, international users, videos up to 1 GB, encryption, leverage cloud (CDN + blob storage). Goals: fast upload, smooth streaming, quality switching, low cost, high availability.
  - Estimations: 5M DAU x 10% upload 1 video of 300 MB = **150 TB/day**; CDN cost: 5M x 5 videos x 0.3 GB x $0.02/GB = **$150,000/day**.
  - Components: client, CDN (streaming) and API servers (everything else). Rationale for using managed services: Netflix uses AWS and Facebook uses Akamai's CDN; in the interview it is enough to name the blob storage.
  - **Upload flow**: LB -> API servers; Metadata DB (sharded and replicated) + metadata cache; **original storage** (blob) -> transcoding servers -> **transcoded storage** -> CDN; **completion queue** + completion handler (workers) update metadata/cache. Two parallel processes: (a) uploading the video; (b) updating metadata.
  - **Streaming flow**: streaming (not full download) from the nearest edge with an appropriate protocol (MPEG-DASH, Apple HLS, Microsoft Smooth Streaming, Adobe HDS); see [[adaptive-bitrate-streaming]].
  - **Transcoding** ([[video-transcoding]]): container (.mp4, .mov, .avi) + codecs (H.264, VP9, HEVC); reasons: save space, compatibility, quality based on bandwidth and quality switching. **DAG** model (inspired by Facebook's video engine) with tasks: inspection, encodings, thumbnail, watermark. Architecture: preprocessor (split by GOP, generates the DAG from configuration files, stores GOPs/metadata in temporary storage for retries), DAG scheduler (splits into stages), resource manager (task queue, worker queue, running queue + task scheduler), task workers and temporary storage; output e.g. `funny_720p.mp4` ([[workflow-orchestration]]).
  - **Optimizations**: speed (client-side upload in GOP chunks, resumable; nearby upload centers using the CDN; parallelism with message queues to decouple download->encoding->upload, [[message-queues]]); security (pre-signed upload URL, [[presigned-urls]]; content protection with DRM: FairPlay, Widevine, PlayReady; AES encryption; visual watermark); **cost** (long-tail distribution: only popular videos on the CDN, the rest from own servers; encode less popular ones on demand; do not distribute to regions without audience; own CDN with ISPs like Netflix).
  - **Errors**: recoverable (retries) vs non-recoverable (malformed format: stop tasks and return a code); playbook: upload retry, server-side split for old clients, transcoding retry, preprocessor regenerates DAG, scheduler reschedules, resource manager queue with replica, failed worker retries on another, stateless API, replicated cache, master/slave failover in Metadata DB.
  - Wrap-up: scale API and DB (replication/sharding), **live streaming** (more demanding latency, different protocol, less parallelism, fast errors), takedowns.
  - Differs from the base: detailed DAG transcoding architecture, CDN cost estimation and long-tail-based optimizations.

- **Grokking the System Design Interview (PDF), pp. 82-91** (difficulty Medium): version without recommendations, channels or subscriptions.
  - Requirements: upload/watch/share/search by title, statistics (likes, views) and comments; reliable, available (consistency can be sacrificed) and lag-free.
  - Estimations: 1.5 B users, 800 M DAU, 5 videos/day = 46K views/s; 200:1 ratio -> 230 uploads/s; 500 h of video/min x 60 x 50 MB = 25 GB/s storage; ingress 5 GB/s; egress ~1 TB/s.
  - API: upload returns HTTP 202 and the user is notified when encoding finishes; `streamVideo(video_id, offset, codec, resolution)` (offset on the server to resume on another device).
  - Components: processing queue, encoder (multiple formats), thumbnails generator, video storage (HDFS/GlusterFS), thumbnails in **Bigtable** (small files of ~5 KB, read-heavy), metadata and comments in MySQL with master-slave (ms-level staleness acceptable); resumable uploads.
  - Metadata sharding by UserID (popular users) or by VideoID (with a cache of hot videos).
  - Inline video deduplication during upload ([[data-deduplication]]).
  - Distribution: consistent hashing across caches, dynamic HTTP redirects to balance (at the cost of extra RTT), geographic caches and CDN for popular videos; videos with 1-20 views/day from own data centers. See [[dropbox]] for large blob uploads.

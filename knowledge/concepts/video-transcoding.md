---
title: Video transcoding (DAG pipeline)
type: concept
aliases: [video encoding, video processing DAG]
sources: [System Design Interview (Alex Xu), Vol. 1, ch. 14 (pp. 229-236)]
---

# Video transcoding (DAG pipeline)

## Definition
Converting the original video into other formats, resolutions and bitrates compatible with different devices and network conditions. A format consists of a **container** (.avi, .mov, .mp4: video + audio + metadata) and a **codec** (H.264, VP9, HEVC).

## Why it matters
- Raw video takes a lot of space (one hour of HD at 60 fps can take hundreds of GB).
- Many devices only support certain formats.
- Allows serving higher resolution to those with bandwidth and lower to those without, and switching quality as the network varies ([[adaptive-bitrate-streaming]]).

## How it works
It is costly and each creator has different needs (watermark, own thumbnails, HD), so it is modeled with a **DAG** (like Facebook's video engine) that defines tasks in sequential or parallel stages. Tasks: inspection (quality/malformation), encodings (resolution, codec, bitrate), thumbnail (uploaded or generated), watermark.
Architecture with six components:
1. **Preprocessor**: splits the video into GOPs (Group of Pictures; playable chunks of a few seconds), generates the DAG from configuration files and stores GOPs and metadata in temporary storage (retries). For old clients that do not split the video, the server does it.
2. **DAG scheduler**: splits the DAG into stages and puts them in the task queue.
3. **Resource manager**: task queue (priority), worker queue (utilization), running queue and task scheduler (picks the optimal task/worker).
4. **Task workers**: run the DAG tasks (different worker types).
5. **Temporary storage**: metadata in memory/cache; video and audio in blob storage; freed when finished.
6. **Encoded video**: final output (e.g. `funny_720p.mp4`).

## Variants and techniques
Completion event queue + completion handler to update metadata and cache; decoupling with [[message-queues]] between download, encoding and upload to parallelize. Generic orchestration: [[workflow-orchestration]].

## Trade-offs
Many encoded versions = more storage and CDN; for less popular content it can be encoded on demand.

## When to use it / when not to
Always on video-on-demand platforms; in live streaming there is less parallelism because chunks are processed in real time.

## Appears in
[[youtube]]

## See also
[[adaptive-bitrate-streaming]], [[presigned-urls]], [[cdn-edge-computing]], [[chunked-multipart-upload]]

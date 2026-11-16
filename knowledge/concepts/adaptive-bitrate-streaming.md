---
title: Adaptive bitrate streaming
type: concept
aliases: [ABR, HLS, DASH, video segmentation, transcoding]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/youtube, System Design Interview Vol.1 (Alex Xu), ch. 14]
---

# Adaptive bitrate streaming

## Definition
Video playback in short segments, at several quality levels, where the client picks the quality of each segment based on the network.

## Why it matters
Avoids downloading the whole file (10 GB at 100 Mbps ≈ 13 min) and reduces buffering when bandwidth varies.

## How it works
- Concepts: codec (H.264, VP9, AV1), container, bitrate, primary manifest (versions) and media manifests (segment URLs).
- Pipeline: segment (ffmpeg) -> transcode each segment per format + audio/transcripts in parallel -> generate manifests -> mark complete. An orchestrated DAG ([[workflow-orchestration]]).
- The client reads the manifest and switches quality per segment. Segments and manifests are served through a CDN.

## Variants and techniques
Earlier steps: full download (bad) and segments in a single quality (good).

## Trade-offs
Pipeline complexity and multiple copies in storage vs a smooth experience. Waiting for the full upload vs segmenting on the client.

## When to use it / when not to
Video on demand at scale and with heterogeneous networks.

## Additional detail (Xu Vol. 1, ch. 14)
Streaming = the device continuously receives the video and loads a little at a time (no full download). Protocols: MPEG-DASH, Apple HLS, Microsoft Smooth Streaming, Adobe HDS; each supports certain encodings and players, so you choose based on your clients. The video is served from the nearest edge. Generating the variants: [[video-transcoding]].

## Appears in
[[youtube]]

## See also
[[cdn-edge-computing]], [[chunked-multipart-upload]]

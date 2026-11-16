---
title: Presigned URLs
type: concept
aliases: [signed urls, presigned urls]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/dropbox, System Design Interview Vol.1 (Alex Xu), ch. 14]
---

# Presigned URLs

## Definition
Temporary URLs signed by the backend that give direct access to an object in blob storage (S3) or a CDN, without going through the application servers.

## Why it matters
Takes the bytes off the backend's data path: avoids double transfer, saves cost and bandwidth and scales better.

## How it works
- The backend signs a URL locally (without calling S3) with a short expiry (~5 min).
- Upload: client requests URL -> backend stores metadata as "uploading" -> client does PUT to S3 -> S3 notification marks it "uploaded".
- Download: signed URL from S3 or from a CDN (CloudFront validates with a registered public key).

## Variants and techniques
One URL per part in multipart ([[chunked-multipart-upload]]); IP binding or authentication cookies.

## Trade-offs
They are bearer tokens: whoever has the URL gets access. The backend loses visibility of what the client uploads (it must be verified).

## When to use it / when not to
Large/medium files. Not for small payloads that already fit in the API.

## Additional detail (Xu Vol. 1, ch. 14)
Secure video upload flow: the client asks the API server for a pre-signed URL (permission on a specific object), receives it and uploads the video directly to that URL. Azure calls it Shared Access Signature. See [[youtube]].

## Appears in
[[dropbox]], [[whatsapp]], [[youtube]]

## See also
[[cdn-edge-computing]]

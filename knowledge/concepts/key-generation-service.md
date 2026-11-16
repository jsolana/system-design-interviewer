---
title: Key Generation Service (KGS)
type: concept
aliases: [KGS, key-DB, offline key generation]
sources: [Grokking the System Design Interview (PDF), "Designing a URL Shortening service" pp. 17-22 and "Designing Pastebin" pp. 35-36]
---

# Key Generation Service (KGS)

## Definition
Standalone service that generates unique random keys in advance (e.g. 6 base64 characters) and stores them in a key-DB so app servers can consume them without computing hashes or handling collisions.

## Why it matters
It avoids collisions, duplicates from identical or differently encoded URLs, and the cost of retries; it makes creation simple and fast.

## How it works
- Problem with the hash approach (MD5/SHA-256 + base64, taking the first 6-8 characters): the same URL from different users gives the same key, equivalent URLs with different URL-encoding, collisions when truncating. Patches: append an increasing sequence (overflow? hurts performance) or a user ID (requires login), and retry until unique.
- The KGS uses two tables: unused keys and used keys. When handing keys to a server it moves them to "used"; it can load a batch into memory and mark it as used right away (if the KGS goes down those keys are wasted; acceptable).
- **Concurrency**: synchronize/lock the structure holding the keys before handing them out so the same one isn't given to two servers.
- **Size**: 6 base64 characters = 64^6 ≈ 68.7 B keys; 6 B x 68.7 B ≈ 412 GB. (8 characters: ≈ 281 trillion.)
- **SPOF**: standby replica of the KGS. App servers can cache batches of keys (if they die, they lose the unused ones).
- After a link expires, the key can be returned to the key-DB.

## Variants and techniques
Alternatives: hash + check; distributed counter/ID ([[unique-id-generation]]) with [[base62-encoding]]. In Pastebin, generating a random key on the app server and retrying on a duplicate (error) is compared against the KGS.

## Trade-offs
Simple and collision-free, but an extra stateful component that must be replicated; lost keys are acceptable given the large space.

## When to use it / when not to
When short, unpredictable, collision-free keys are needed at large scale.

## Appears in
[[pastebin]], [[url-shortener]]

## See also
[[unique-id-generation]], [[base62-encoding]], [[url-shortener]], [[pastebin]]

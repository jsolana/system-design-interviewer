---
title: Discord voice and video on an edge network
type: interview
sources: [https://discord.com/blog/how-we-moved-discord-voice-to-the-edge]
concepts: [cdn-edge-computing, service-discovery, multi-data-center, observability-and-monitoring, network-latency-and-bandwidth]
difficulty: high
---

# Discord voice and video on an edge network

## Prompt
Real-world case study: reduce latency of group voice/video calls by moving media servers (SFUs) from about 30 hyperscaler cities to an edge network with 300+ PoPs.

## Functional requirements
- Host a call on one SFU instance; all participants connect to it for the call duration. Control plane stateful (membership, mute, stream routing); media plane stateless UDP.

## Non-functional requirements
- Low latency and packet loss globally (users in e.g. Reykjavik, Auckland suffered); hosts are recyclable containers managed by the edge provider.

## Estimations
- 80%+ of voice/video traffic ends up on the edge provider; about 25,000 voice hosts when etcd strained.
- Frankfurt: ping -34%, loss -42%; Europe/LatAm loss down 20-60%; Iceland-only calls ping -9% but mixed-region calls 2.7x worse ping (host placement matters).

## API
Not covered in the source.

## Data model
- Discovery records in Valkey with 10-minute TTL (hosts register on startup, re-register periodically, unregister on shutdown).

## Architecture (high-level design)
- Edge-hosted worker containers (2-8 workers per host), discovery service, deployer that recreates outdated hosts, passive eBPF probe timestamping health-check packets at the NIC.

## Deep dives
- **Recreate, not restart**: shutdown signals delayed 5 minutes so replacements come up first, avoiding reconnect storms.
- **etcd -> Valkey** for discovery at 25k hosts, with double-writes then migration.
- **Tokio poll-budget fix**: always-ready recv future starved the flush timer; a 9 ms rule disables recv when a flush is overdue.
- **CPU/IRQ**: pin workers away from the vCPU handling receive IRQs; Receive Packet Steering.
- Other: 25 s hangs from page-cache flush on new disks; futex stalls up to 860 ms.

## Trade-offs and decisions
- Coverage vs placement (nearest PoP can hurt mixed-region calls); density vs availability (8 -> 2 workers per host due to shared NIC queues); speed vs safety (region-by-region ramps gated on metrics and ISP peering headroom); platform built for short-lived workloads needed extra discovery/drain logic. Peering/transit can dominate geography.

## Related concepts
[[cdn-edge-computing]], [[service-discovery]], [[multi-data-center]], [[observability-and-monitoring]], [[network-latency-and-bandwidth]]

## Follow-up questions
Not covered in the source.

## Variants
Not covered in the source.

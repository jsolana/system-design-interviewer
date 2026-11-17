---
title: Network latency and bandwidth
type: concept
aliases: [latency vs bandwidth, network performance]
sources: [Cracking the Coding Interview, ch. 9 pp. 141-142, Programming Interviews Exposed, 3rd ed., ch. 16 "Network Performance" (pp. 247-248)]
---

# Network latency and bandwidth

## Definition
The two main measures of network performance. **Latency**: time for a bit to travel from one point to another. **Bandwidth**: rate at which data flows once communication is established. Pipe analogy: length is latency, width is bandwidth.

## Why it matters
"Speed" is not one number; a link can be good on one axis and bad on the other (satellite: high bandwidth, high latency). Which one matters depends on the workload.

## How it works
- Latency-sensitive: voice/video calls (VoIP), interactive apps, small request/response chains. Little bandwidth needed.
- Bandwidth-sensitive: HD video streaming; latency only delays playback start.

## Variants and techniques
Not covered in the source (see [[cdn-edge-computing]] for reducing latency and [[caching]]).

## Trade-offs
Optimizing one does not improve the other; choose techniques per workload.

## When to use it / when not to
Use as the first question when reasoning about a network-bound design: is it latency- or throughput-bound?

## Additional detail (Cracking the Coding Interview, ch. 9)
Conveyor-belt analogy: bandwidth = max items per unit time in the best case; throughput = actual items per unit time; latency = time for one item to cross. A wider belt raises bandwidth/throughput but not latency; a shorter belt lowers latency only; a faster belt changes all three. Compression can raise effective throughput but there is often little to do about latency (matters for online games).

## Appears in
[[discord-voice-infrastructure]]

## See also
[[cdn-edge-computing]], [[caching]], [[back-of-the-envelope-estimation]]

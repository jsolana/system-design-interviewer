---
title: Service discovery
type: concept
aliases: [descubrimiento de servicios, ZooKeeper, registro de servicios]
sources: [System Design Interview (Alex Xu), Vol. 1, ch. 12 (pp. 184-185, 190)]
---

# Service discovery

## Definition
Component that registers the available servers and recommends the best one to each client according to predefined criteria (geographic location, server capacity...). Open-source example: Apache ZooKeeper.

## Why it matters
In stateful services (e.g. chat servers with persistent connections) the client must know which server to connect to without overloading any; it also provides the next server if one goes down.

## How it works
Flow in a chat: 1) the user logs in; 2) the load balancer sends the request to the API servers; 3) after authenticating, service discovery picks the best chat server and returns its info to the client; 4) the client opens a WebSocket connection with that server.

## Variants and techniques
Registering all servers in ZooKeeper and selecting by rules (geography, capacity). If a chat server goes down, service discovery provides a new one to reconnect to.

## Trade-offs
It is an additional piece that must be highly available; the client stays on its server while it is alive (affinity).

## When to use it / when not to
Stateful services with persistent connections ([[websockets]]). For stateless services a [[load-balancer]] is enough.

## Appears in
[[digital-wallet]], [[distributed-message-queue]], [[metrics-monitoring]], [[nearby-friends]], [[whatsapp]]

## See also
[[websockets]], [[load-balancer]], [[stateless-architecture]]

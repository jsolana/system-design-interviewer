---
title: Load balancer
type: concept
aliases: [load balancing, sticky sessions]
sources: [System Design Interview (Alex Xu), Vol. 1, ch. 1 (pp. 10-11, 20-21), Grokking the System Design Interview (PDF), "Load Balancing" pp. 173-175]
---

# Load balancer

## Definition
Component that distributes incoming traffic among the servers of a pool (load-balanced set). Clients only see its public IP; web servers communicate with it over private IPs.

## Why it matters
- Eliminates the SPOF of the web tier: if a server goes down, traffic goes to the others.
- Simple horizontal scaling: add servers to the pool and the LB starts sending them requests.
- Security: servers are not directly reachable from the internet.

## How it works
- DNS returns the LB's IP; the LB routes each HTTP request to a healthy server.
- If a server goes down it is removed from the pool and a new healthy one is added.
- With a stateless web tier ([[stateless-architecture]]) any server can serve any request.

## Variants and techniques
- **Sticky sessions**: the LB always sends the same client to the same server (required with a stateful architecture); adds overhead and makes adding/removing servers and handling failures harder.
- Autoscaling of the pool based on load.
- With several data centers, [[multi-data-center]] (geoDNS) distributes across regions.

### Layers and algorithms (Grokking the System Design Interview, pp. 173-175)
- You can balance at each layer: user -> web servers; web -> internal layer (app/cache servers); internal layer -> database.
- **Health checks**: the LB periodically queries the backends; one that fails is removed until it responds again.

| Algorithm | Idea | Useful when |
|---|---|---|
| Round Robin | Cycles through the list | Identical servers, few persistent connections |
| Weighted Round Robin | Weight per capacity | Heterogeneous servers |
| Least Connection | Fewest active connections | Many uneven persistent connections |
| Least Response Time | Fewest connections + lowest average latency | Variable latency |
| Least Bandwidth | Fewest Mbps served | Very uneven traffic sizes |
| IP Hash | Hash of client IP -> server | Client-server affinity |

- **Redundant LBs**: a second LB in a cluster monitors the first and takes over if it fails.
- Simple Round Robin ignores actual load (a slow server keeps receiving requests); alternative: an LB that periodically queries load. With [[consistent-hashing]] cache/video is balanced, but dynamic HTTP redirects to balance add RTT and may jump to distant caches ([[youtube]]).
- In chat, the LB (or routing layer) maps UserID -> chat server that holds the connection.

## Trade-offs
The LB itself can be a SPOF (requires redundancy). Sticky sessions simplify local state at the cost of elasticity.

## When to use it / when not to
Whenever there is more than one server in a tier. Avoid sticky sessions if state can be externalized.

## Appears in
[[dropbox]], [[pastebin]], [[twitter]], [[twitter-search]], [[typeahead]], [[web-crawler]]

## See also
[[stateless-architecture]], [[database-replication]], [[horizontal-vs-vertical-scaling]]

---
title: Load balancer
type: concept
aliases: [load balancing, sticky sessions]
sources: [System Design Interview (Alex Xu), Vol. 1, ch. 1 (pp. 10-11, 20-21), Grokking the System Design Interview (PDF), "Load Balancing" pp. 173-175, https://sre.google/sre-book/load-balancing-frontend/, https://sre.google/sre-book/load-balancing-datacenter/]
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

## Additional detail (Google SRE Book, ch. 19-20)
- **Frontend**: DNS balancing returns several A/AAAA records but gives weak control (clients pick arbitrarily, resolvers hide client location, EDNS0 client-subnet helps, 512-byte reply cap, cached answers cannot be flushed and some resolvers ignore low TTLs). Anycast gets queries to the nearest DNS server. Next layer is a **VIP** served by network load balancers; combine DNS and VIP levels.
- **Backend selection and forwarding**: least-loaded needs per-connection state; simple hashing remaps almost everything when backends change; **consistent hashing** keeps mappings stable and works as a stateless fallback (e.g. under DoS). NAT needs a connection table; L2 rewriting/DSR requires one broadcast domain; **GRE encapsulation** lifts that at ~24 bytes overhead per packet (fragmentation unless MTU raised).
- **Datacenter**: clients keep long-lived connections to a **subset** of 20-100 backends. Random subsetting is uneven (300 clients/300 backends, 30% subsets: least-loaded backend 63% of average, most-loaded 121%; 10% subsets: 50%-150%); **deterministic subsetting** shuffles the backend list per round with a seed and gives every backend equal connections.
- **Policies**: simple round robin can leave a 2x CPU spread (query cost varies up to 1000x, noisy neighbors ~20%); least-loaded round robin still ~2x spread (count recent errors as active to avoid sinkholing); **weighted round robin** uses backend-reported rate, error and utilization and narrows the gap sharply.
- **Health**: healthy / refusing / **lame duck** (listening but asks clients to stop; drain 10-150 s); client flow control around 100 active requests per backend. Source: https://sre.google/sre-book/load-balancing-frontend/ and /load-balancing-datacenter/. See also [[load-shedding-and-overload-handling]].

## Appears in
[[airbnb-search-ranking]], [[dropbox]], [[pastebin]], [[search-query-cache]], [[twitter]], [[twitter-search]], [[typeahead]], [[web-crawler]]

## See also
[[stateless-architecture]], [[replication]], [[horizontal-vs-vertical-scaling]]

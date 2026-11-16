---
title: Long polling (Ajax polling vs long-polling vs WebSockets vs SSE)
type: concept
aliases: [HTTP long-polling, ajax polling]
sources: [Grokking the System Design Interview (PDF), "Long-Polling vs WebSockets vs Server-Sent Events" pp. 193-196, System Design Interview Vol.1 (Alex Xu), ch. 12]
---

# Long polling

## Definition
A variant of polling in which the server holds the request open until it has data (or a timeout), instead of returning an empty response.

## Why it matters
Allows simulating push over HTTP with low latency without maintaining a bidirectional channel; it is the base mechanism the source uses to notify changes (Dropbox, Messenger, feeds, Uber, waits in Ticketmaster).

## How it works
**Comparison of client-server communication techniques**
| Technique | How it works | Problem / use |
|---|---|---|
| Ajax polling | Client asks at intervals (e.g. 0.5 s) | Many empty responses, HTTP overhead |
| Long-polling | Server holds the request until there is data; the client re-requests upon receiving a response | Each request has a timeout -> periodic reconnection; the server almost always has a request waiting |
| [[websockets]] | Persistent full-duplex channel over a TCP connection after a handshake | Bidirectional, low overhead; chat, real time |
| [[server-sent-events]] | Long connection, server -> client only; sending client -> server requires another protocol | Continuous events from the server |

Long-polling cycle: (1) initial request; (2) the server delays until there is an update or a timeout; (3) full response; (4) the client resends immediately or after a pause; (5) reconnection after a timeout.

In chat, the server keeps a hash table userId -> connection object to deliver messages on the open request.

## Variants and techniques
See the table. For push to offline devices: push notifications via the manufacturer's servers.

## Trade-offs
More efficient than polling, but each client occupies an open connection on the server (a server ~50K concurrent connections in the Messenger estimate) and the timeout forces reconnection.

## When to use it / when not to
When WebSockets is not available or notifications are sporadic; WebSockets for bidirectional chat; SSE for server -> client streams.

## Additional detail (Xu Vol. 1, ch. 12)
Compared to polling (periodic asking, almost always with no answer), the client keeps the request open until there are messages or a timeout expires, and immediately sends another. Drawbacks: with stateless HTTP servers and round robin, the sender and the receiver may not share a server; the server does not detect client disconnection well; it is inefficient with low-activity users. See [[whatsapp]].

## Appears in
[[distributed-email-service]], [[distributed-message-queue]], [[dropbox]], [[google-maps]], [[ticketmaster]], [[whatsapp]]

## See also
[[websockets]], [[server-sent-events]], [[pub-sub]]

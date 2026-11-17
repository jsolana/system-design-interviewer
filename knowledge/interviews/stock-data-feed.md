---
title: Stock Data Feed Service
type: interview
sources: [Cracking the Coding Interview, 6th ed. (G. Laakmann McDowell), ch. 9 pp. 137-145 and solutions pp. 372-395 (problem 9.1)]
concepts: [sql-vs-nosql, database-normalization-and-denormalization, horizontal-vs-vertical-scaling]
difficulty: low
---

# Stock Data Feed Service

## Prompt
Up to 1,000 client applications need simple end-of-day stock data (open, close, high, low). The data already exists and can be stored in any format. Design the client-facing service, including development, rollout, monitoring and maintenance. Compare the options considered and recommend one.

## Functional requirements
- Clients retrieve end-of-day open/close/high/low per company and date.
- Any distribution mechanism and technology is allowed.

## Non-functional requirements
Evaluation axes given by the source:
- Client ease of use.
- Ease of implementation and maintenance for us.
- Flexibility for future demands (new fields, new query types).
- Scalability and efficiency.

## Estimations
Not covered in the source (only the 1,000-client figure).

## API
Optionally a web service layer (the source mentions SOAP) in front of any storage choice. No concrete endpoints.

## Data model
Fixed-format, fixed-size record: company name, date, open, high, low, closing price.

## Architecture (high-level design)
Three storage/distribution proposals are compared:
| Option | Pros | Cons |
|---|---|---|
| Text files over FTP | Easy to view and back up | Parsing is hard; adding columns can break client parsers; no querying |
| SQL database exposed to clients | Rich queries (e.g. open > N and close < M), built-in backup/rollback/security, standard client integration | Heavyweight for such a small feed; not human-readable without an extra layer; clients can run expensive queries; security must be tight |
| XML files | Human- and machine-readable, widely supported parsers, new nodes do not break parsers, existing backup tools | Sends everything even if client wants a part; any query needs parsing the whole file |
A web service in front adds security and integration ease but restricts clients to the access patterns we expose.

## Deep dives
- Web service layer: pro (control, security) and con (clients cannot do unanticipated queries).
- Rollout and monitoring are asked for but not detailed in the source.

## Trade-offs and decisions
There is no single correct answer. Plain text is probably the worst; SQL or XML (with or without a web service) are both defensible. The point is evaluating trade-offs.

## Related concepts
[[sql-vs-nosql]], [[database-normalization-and-denormalization]]

## Follow-up questions
Not covered in the source.

## Variants
Not covered in the source.

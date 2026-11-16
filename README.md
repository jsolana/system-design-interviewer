# system-design-interviewer

A system that helps candidates prepare for system design interviews.

The idea is to build a structured knowledge base from books and online sources, and use it to practice: study concepts, review classic interview problems and rehearse answers.

## Structure

- `knowledge/concepts/`: one file per technical concept (caching, consistent hashing, quorum, etc.), with definition, how it works, trade-offs and the interviews it appears in.
- `knowledge/interviews/`: one file per interview problem (URL shortener, Ticketmaster, chat, etc.), with requirements, estimations, API, architecture, deep dives and links to its concepts.
- `docs/`: source documents (PDF) the knowledge is extracted from.
- `.claude/agents/`: Claude Code agents, including `knowledge-extractor`, which writes the content of a document or URL into `knowledge/`.
- `TODO.md`: list of candidate books to process.

## How it is fed

Run the `knowledge-extractor` agent with a document path or a URL (and, optionally, a page or chapter range). The agent creates or merges concepts and interviews. Each interview lists its concepts in its header (`concepts:`), and that header is the source of truth for the interview-concept relationship.

## Sources

The problems and concepts come from the Hello Interview *problem breakdowns*, *Designing Data-Intensive Applications*, *System Design Interview* (Alex Xu, vol. 1 and 2) and *Grokking the System Design Interview*. The log of what has been processed is in `knowledge/_sources.md`.

All content is written in English.

---
title: Social Network Data Structures and Shortest Path
type: interview
sources: [Cracking the Coding Interview, 6th ed. (G. Laakmann McDowell), ch. 9 pp. 137-145 and solutions pp. 372-395 (problem 9.2)]
concepts: [database-partitioning, caching]
difficulty: medium
---

# Social Network Data Structures and Shortest Path

## Prompt
Design the data structures for a very large social network (Facebook/LinkedIn) and an algorithm that shows the shortest path between two people (Me -> Bob -> Susan -> Jason -> You).

## Functional requirements
- Store people and friendship relations.
- Given two users, return the shortest chain of friends.

## Non-functional requirements
Millions of users: data cannot live on one machine; searches must tolerate multiple machines and concurrent searches.

## Estimations
Branching analysis: with k friends per person and path length q, plain BFS visits O(k^q) nodes; bidirectional BFS visits O(k^(q/2)). Example: path A-B-C-D-E with 100 friends each: 100^4 = 100M nodes vs 2 x 100^2 = 20,000.

## API
Not covered in the source (internal methods: find path(source, destination)).

## Data model
- Graph: person = node, friendship = undirected edge.
- Person holds ID, info and a list of friend IDs (IDs, not object references, because friends may live on other machines).
- A lookup maps personID -> machineID; each machine has a hash table personID -> Person.

## Architecture (high-level design)
1. Simplified, single-machine version: BFS from the source. DFS is wrong: it finds only some path, not the shortest, and may explore millions of nodes while the target is a direct friend.
2. Better: **bidirectional BFS** (two BFS, from source and destination, advancing one level at a time; they collide at a shared person; merge the two paths). Needs both endpoints known.
3. Multi-machine version: for each friend ID, look up the machine, jump to it, fetch the person.

## Deep dives
- Reduce machine jumps: batch lookups (friends on the same machine are fetched together).
- Smart partitioning: group people by country, city, state to keep friends co-located.
- Visited marking: do not set a flag on the node (several searches run concurrently); keep a per-search hash table of visited IDs.
- Other follow-ups: server failures, caching, when to give up in an unbounded search, starting from high-degree people (more friends of friends).

## Trade-offs and decisions
- Bidirectional BFS is much faster but requires the destination to be known.
- Locality-aware partitioning reduces hops but needs a smarter assignment than random hashing.

## Related concepts
Algorithms: [[breadth-first-search]], [[bidirectional-search]]. [[database-partitioning]], [[caching]]

## Follow-up questions
Failures, caching, search depth cutoff, using node popularity to choose traversal start.

## Variants
Not covered in the source.

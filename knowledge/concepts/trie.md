---
title: Trie (prefix tree)
type: concept
aliases: [prefix tree]
sources: [Grokking the System Design Interview (PDF), "Designing Typeahead Suggestion" pp. 92-99, System Design Interview Vol.1 (Alex Xu), ch. 13]
---

# Trie (prefix tree)

## Definition
A tree in which each node stores one character of a phrase and the paths from the root form prefixes; it makes it possible to find all terms that start with a given prefix.

## Why it matters
It is the base structure for typeahead/autocomplete: prefix lookup in time proportional to the prefix length (plus the cost of choosing the best results).

## How it works
- Nodes with a single branch can be merged to save space; case-insensitivity is usually assumed.
- Ranking: store the search counter on each terminal node. Walking the subtree of a prefix to get the top-N is too slow with a huge tree (the source cites about 30 levels of depth).
- **Optimization**: store each node's top-10 suggestions (more storage, immediate read). To save space, store only references to the terminal nodes (walk up to the parent to rebuild the phrase) plus the frequency.
- **Bottom-up construction**: each parent combines the top-N of its children.
- **Update**: do not update online for every query (~60K QPS). Log queries (or sample 1 in 1000), process with MapReduce at regular intervals (e.g. hours) and replace: offline copy of the trie and switch, or master-slave (update the slave, promote it). For frequencies, apply differences or an exponential moving average (EMA) instead of recounting; when a term goes up, walk the ancestors updating their top-N.
- **Removing terms** (legal/hate/piracy): remove in the regular update and, in the meantime, a filter on each server.
- **Persistence**: periodic snapshot to a file, traversing level by level (character + number of children); allows rebuilding after a restart. With top-N per node it must be recomputed during construction.

## Variants and techniques
Partitioning: by range (first letter, unbalanced), by maximum server capacity (cut the subtree when it no longer fits, with an LB that keeps the map), or by hash of the term (requires querying all servers and aggregating).

## Trade-offs
Lots of memory vs. minimal latency; deferred updates (suggestions not immediate) vs. write cost.

## When to use it / when not to
Prefix search with strict latency constraints (< 200 ms). For full-text search use [[inverted-index]].

## Additional detail (Xu Vol. 1, ch. 13)
Trie with 26 children per node (root = empty string). Top-k for a prefix: find the prefix O(p), traverse the subtree O(c), sort O(c log c). Optimizations: limit the maximum prefix length (~50, O(1)) and **store the k most frequent queries on each node** (e.g. node "be": best 35, bet 29, bee 20, be 15, beer 10), at a space cost. A frequency change forces updating the node and all its ancestors; that is why it is rebuilt in batches (weekly) rather than in real time. Persistence: serialized snapshot in a document store, or hash table (prefix -> node) in a key-value store. Sharding by first letter with uneven distribution, correctable with a shard map manager. See [[typeahead]].

## Appears in
[[typeahead]]

## See also
[[typeahead]], [[inverted-index]], [[caching]], [[database-partitioning]]

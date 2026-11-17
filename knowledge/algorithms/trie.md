---
title: Trie (prefix tree)
type: algorithm
aliases: [prefix tree]
sources: [Cracking the Coding Interview 6th ed., ch. 17 Hard (pp. 186-191, solutions pp. 530-627); Cracking the Coding Interview 6th ed., ch. 4 (book p. 105); ch. 16 Moderate, T9 (p. 184)]
---

# Trie

## Definition
n-ary tree where each node holds a character; a root-to-node path spells a prefix; terminal markers (* node or boolean flag) denote complete words.

## When to use it
Prefix lookups over a dictionary, word-list problems (boggle-like), autocomplete. A hash table can say whether a word exists but not whether a string is a prefix.

## How it works
Each node has up to ALPHABET_SIZE children. When searching related prefixes (M, MA, MAN...), pass the current node instead of restarting from the root.

Pruning use (T9): while recursively generating letter combinations for a digit string, only descend into a child that exists in the trie so dead prefixes are abandoned early. If the dictionary is fixed, an even faster option is a precomputed hash table from digit string to words.

## Multi-search and word rectangles (CtCI 17.17, 17.25)
Insert the small strings into a trie, then start a walk at every index of the big string and record every terminal node hit: O(kt + bk) versus O(kbt) naive or O(b^2 + kt) with a suffix trie. For the largest word rectangle keep a trie per word length and prune a partial rectangle as soon as a column prefix is not a dictionary prefix.

## Complexity
Prefix/word check O(K), K = string length (same as a hash table really costs).

## Common pitfalls
Forgetting the word-terminator flag.

## Appears in
[[multi-search]], [[t9-words]], [[word-rectangle]]

## See also
[[hash-table]], [[binary-search-tree]]

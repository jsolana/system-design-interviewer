---
title: Data integrity and backups
type: concept
aliases: [backups, soft deletion, point-in-time recovery, out-of-band validation, restore testing]
sources: [https://sre.google/sre-book/data-integrity/, https://sre.google/sre-book/managing-critical-state/]
---

# Data integrity and backups

## Definition
Data integrity means users can access their data accurately and consistently. It is separate from uptime: data unavailable too long (24 hours is the suggested starting threshold) effectively counts as lost.

## Why it matters
Replication copies corruption and accidental deletes to every replica, so redundancy alone is not recoverability. Most data-loss events come from software bugs and human error, not hardware.

## How it works
- **Plan for 24 failure combinations**: root cause x scope x rate of loss.
- **Defense in depth**:
  1. **Soft deletion**: hide, keep 15-60 days (Gmail trash: 30 days) so deletions are reversible.
  2. **Tiered backups**: frequent fast-restoring local snapshots plus slower, remote copies (tape) for site-level failures; typical retention 30-90 days. Point-in-time recovery is valuable but hard across all stores.
  3. **Replication** with diverse media and redundancy schemes ([[replication]], [[erasure-coding]]).
  4. **Early detection**: out-of-band validators check invariants continuously, aiming to catch serious problems within 24 hours; rate-limit them; shard verification (a single task verifying 700 PB would take decades) and verify immutable "trust points".
- **Backups vs archives**: backups can be restored into an application; archives serve audit/compliance and can restore slowly.
- **The goal is restores, not backups**: set frequency and retention from recovery time and tolerable data loss; continuously and automatically test restores end to end, alert when the test stops succeeding.
- **Case studies**: Gmail 2011 recovered from offline tape (GTape) with rehearsed plans, over 99% restored ahead of estimate; Google Music 2012 deletion-pipeline race condition removed audio references for ~21,000 users, ~436,000 of ~600,000 tracks recovered from tape (5,000+ tapes, ~1.5 PB).
- **Corruption maths**: 99.99% "good bytes" in a 2 GB artifact can still mean up to 200 KB corrupted.
- Consensus systems still need backups: bugs and human error are failure domains replicas cannot protect against.

## Variants and techniques
Snapshots, WAL archiving ([[write-ahead-log]]), versioned object storage ([[object-storage]]), checksums and [[merkle-tree]] verification, [[reconciliation]].

## Trade-offs
Backup frequency vs cost and write overhead; long retention vs privacy/deletion obligations (Note: not discussed in source); validators cost I/O at scale.

## When to use it / when not to
Every stateful system; archives are enough only where slow recovery is acceptable.

## Note: what a senior/staff candidate should say
State RPO/RTO (Note: terms are common practice, the chapter speaks of recovery time and acceptable data loss), "replication is not a backup", soft delete plus tiered backups plus restore drills, and invariant validators for critical data like ledgers ([[double-entry-ledger]]).

## Appears in
[[payment-system]]

## See also
[[disaster-recovery]], [[replication]], [[reconciliation]], [[incident-management-and-postmortems]]

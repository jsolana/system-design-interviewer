---
title: Sandboxed code execution
type: concept
aliases: [secure code execution, code sandbox]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/leetcode]
---

# Sandboxed code execution

## Definition
Running untrusted user code isolated from the rest of the system.

## Why it matters
Prevents security leaks, CPU contention and server crashes.

## How it works
Options: on the API server (bad); VM (strong isolation, heavy, slow startup); Docker container (lightweight, fast, weaker isolation); serverless (autoscaling, cold starts, resource limits).
Hardening: read-only filesystem with an ephemeral temp directory, CPU/memory limits, timeout, no network (VPC SG/NACL), seccomp to restrict syscalls.

## Variants and techniques
Container pools per language with autoscaling (ECS) and/or a queue; per-language harness with standard test serialization.

## Trade-offs
Isolation vs startup/cost. Containers: chosen with steady load; serverless if it is very spiky.

## When to use it / when not to
Whenever third-party code is executed.

## Appears in
[[leetcode]]

## See also
[[message-queues]]

---
title: Thread synchronization and deadlocks
type: concept
aliases: [concurrency, monitors, semaphores, mutex, deadlock, livelock, busy waiting, producer-consumer, dining philosophers]
sources: [Cracking the Coding Interview, ch. 15 pp. 174-180 / solutions pp. 447-461, Programming Interviews Exposed, 3rd ed., ch. 9 (pp. 145-158), ch. 12 pp. 182-183 (transactions)]
---

# Thread synchronization and deadlocks

## Definition
Single-machine concurrency primitives that coordinate threads sharing memory: mutexes, semaphores and monitors, plus the failure modes they introduce (race conditions, deadlock, livelock, starvation, busy waiting). The distributed counterpart is [[distributed-lock]].

## Why it matters
- Threads share memory by default, so unsynchronized access corrupts data and causes intermittent, hard-to-reproduce bugs.
- Classic example: two ATM threads withdraw 100 each from the same account. Both read balance 500; one write overwrites the other, and the bank loses 100 (a lost update, the same anomaly as in [[transactions-and-isolation-levels]]).
- Foundation for reasoning about worker pools, queues and locks in service design.

## How it works
- **Thread**: unit of execution with its own stack, shared heap and file handles. Native (kernel) threads are preemptive: the OS context-switches between them at any point. Green threads (VM level) cannot use several cores well.
- **Monitor**: a set of routines guarded by a mutual-exclusion lock; only one thread runs inside at a time; threads can wait and be notified (Java synchronized, wait/notifyAll). Acquires/releases locks automatically.
- **Semaphore**: a lock the caller must acquire and release explicitly (easy to forget on error paths). Types: mutex (binary), counting (max n holders), event (notify one or all waiters).
- Narrow the critical section (synchronize only the code touching shared state) for efficiency. Locks cost time; hence thread-safe and non-thread-safe variants of classes. Use lock timeouts to report errors and retry.
- **Busy waiting**: a thread loops checking a condition and burns CPU. Avoid it by sleeping on a monitor/semaphore until notified. Spinlocks are acceptable only when the wait is shorter than a normal lock acquisition (kernel code) or in HPC with one thread per core.
- **Producer/consumer (bounded buffer)**: naive version busy-waits and has no access control. Making methods synchronized alone is worse: a producer spinning on a full buffer holds the lock, so the consumer can never run. Correct: producer `wait()`s when full, consumer `wait()`s when empty, each calls `notifyAll()` after changing state (re-check the condition in a loop).
- **Deadlock**: threads each hold a lock the other needs (typically locks acquired in different orders). Best prevention: always acquire multiple locks in one global order and release in reverse. Detection/breaking mechanisms exist but are unsatisfying.
- **Dining philosophers**: everyone grabbing the left fork first can deadlock. A timeout/retry does not fix it and can cause **livelock** (starvation). Fix: impose a lock order (one philosopher takes the right fork first). That is correct but unfair (one philosopher ate about 100x more often in the author's tests); a rule such as "odd-numbered fork before even-numbered fork" keeps ordering with fairer sharing.

## Variants and techniques
- Mutex vs counting semaphore vs event semaphore; monitor vs raw semaphore.
- Lock ordering, lock timeouts, try-lock (deadlock avoidance).
- Blocking queue (bounded buffer) as the standard hand-off between threads; the distributed equivalent is a [[message-queues]] with back-pressure.

## Trade-offs
| Choice | Pro | Con |
|---|---|---|
| Coarse lock (whole method) | Simple | Contention, lower throughput |
| Fine-grained lock | Higher concurrency | More deadlock risk, harder to reason about |
| Busy wait / spinlock | Lowest wake-up latency | Wastes CPU |
| Timeout and retry | Breaks some stalls | Can livelock, unfair |

## When to use it / when not to
Use in-process locks for state shared between threads of one process. Across machines they do not work; use [[distributed-lock]], [[optimistic-concurrency-control]] or database transactions. Many servers keep request handlers single-threaded or stateless to avoid this complexity.

## Additional detail (Cracking the Coding Interview, ch. 15)
- **Process vs thread**: a process is a program instance with its own address space and resources; other processes are reached via IPC (pipes, files, sockets). Threads live in a process and share its heap; each has its own stack and registers. A change by one thread is immediately visible to siblings.
- **Creating threads (Java)**: implement Runnable (preferred: Java has no multiple inheritance and Thread carries overhead) or extend Thread.
- **synchronized**: restricts a block/method to one thread per object instance; two threads with different instances can both run it. Static synchronized methods lock the class, so two different static synchronized methods cannot run together. A non-synchronized method B can always run concurrently with synchronized A.
- **Explicit locks** (e.g. ReentrantLock) give finer control; always unlock (finally). A lock is owned by the thread that locked it, so it cannot be released by another thread.
- **Four deadlock conditions (Coffman)**: mutual exclusion, hold and wait, no preemption, circular wait. Prevention removes one; most algorithms attack circular wait.
- **Dining philosophers fixes**: (1) all-or-nothing with tryLock (put the left chopstick back if the right is unavailable; risk: perfectly synchronized philosophers repeat forever); (2) number the chopsticks and always take the lower first, so no cycle can form.
- **Deadlock-free lock class**: require each process to declare up front the order in which it will request locks; build a directed graph with an edge (v, w) when w is requested right after v; run DFS cycle detection (fresh/visiting/visited states); if the new declaration creates a cycle, remove its edges and reject. At lock time verify the process follows its declared order.
- **Call in order** (first, second, third on three threads): use semaphores (initialized/acquired to 0 permits) released at the end of each step and acquired by the next; plain locks fail because only the owner thread may unlock.
- **Multithreaded FizzBuzz**: four threads (Fizz, Buzz, FizzBuzz, number) share a counter under one lock; each checks the bound first, then its divisibility predicate, prints and increments; check "divisible by 3 and 5" before the single cases.
- **Measuring context-switch time**: two processes pass a token over a pipe (ping-pong), each read blocks and forces a switch; round trip T = 2 * (Td + Tc + Tr). Measure Td + Tr by a process sending to itself (no switch), subtract, repeat many times and take the minimum to filter kernel noise. The result is only an approximation dependent on the scheduler.

## Appears in
None yet.

## See also
[[distributed-lock]], [[optimistic-concurrency-control]], [[transactions-and-isolation-levels]], [[message-queues]]

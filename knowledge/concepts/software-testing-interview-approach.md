---
title: Software testing interview approach
type: concept
aliases: [testing questions, test a pen, test plan, troubleshooting questions]
sources: [Cracking the Coding Interview, 6th ed., ch. 11 pp. 152-157, solutions pp. 417-421]
---

# Software testing interview approach

## Definition
A structured method for the four kinds of testing questions: (1) test a real-world object (pen, paperclip), (2) test a piece of software, (3) write test code for a function, (4) troubleshoot an existing issue. Assume neither input nor user will play nice.

## Why it matters
Interviewers look for big-picture understanding (prioritize payments over image placement in an e-commerce system), knowing how pieces fit in an ecosystem (spreadsheet integration with mail and plug-ins), organization (categories, not a random list) and practicality (reinstalling is not a plan).

## How it works
**Real-world object** (5 steps): who uses it and why; use cases; bounds of use (capacity, temperature); stress/failure conditions (what failure is acceptable, never a fire or flood); how to perform the testing (define "normal use", automate usage). Ask many who/what/where questions first; the problem often turns out different (a washable felt-tip pen for 5-10 year-olds drawing on clothing). Components for the pen: fact check, intended use (drawing), washing (hot/warm/cold), safety (non-toxic), unintended uses (other surfaces, stomping, throwing).

**Software** (6 steps): black-box or white-box; users; use cases; bounds of use; stress/failure conditions; test cases and how to run them. Manual vs automated: manual covers qualitative judgement and unexpected issues; automation covers known scenarios and heavy repetition. Structure the test cases by main components.

**Function**: define test cases (normal case incl. odd/even sizes; extremes such as empty, one element, huge; null and illegal input such as negative n; strange input such as already sorted or reverse sorted), define expected results (also that the original is untouched), write the test code.

**Troubleshooting**: understand the scenario (version, OS, frequency, error report), break the flow into testable steps (e.g. launch icon, start, load settings, HTTP request, response, parse, display), create specific steps the user can realistically perform.

## Variants and techniques
- Chess canMoveTo(x, y): extreme-case validation (negative or out-of-board x/y, full/empty board, lopsided colors; decide return false vs exception) plus general testing (each piece against each other piece type or empty, in every direction).
- Load testing a page without tools: define response time, throughput, resource utilization and max load; write a multithreaded program simulating thousands of virtual users and measure; compare to accepted values.
- ATM in a distributed bank: clarify users, uses, tooling; components login, withdraw, deposit, balance, transfer; manual error cases plus automated scenarios and race conditions on a closed system with fake accounts; prioritize security and reliability (money is always accounted for).
- Random crash causes in a single-threaded C program: random variables, uninitialized variables, memory corruption/leaks, external dependencies; investigate by elimination and tools.
- Unsigned loop bug: `for (unsigned i = 100; i >= 0; --i)` never ends because an unsigned value is always >= 0; use `i > 0` (and %u).

## Trade-offs
Exhaustive coverage is impossible; focus on essential areas. Automation is powerful but misses qualitative issues.

## When to use it / when not to
Use for any testing-flavored question. For distributed system testing see [[distributed-systems-testing]]; for experiments see [[ab-testing]].

## Appears in
None yet.

## See also
[[distributed-systems-testing]], [[ab-testing]], [[thread-synchronization-and-deadlocks]]

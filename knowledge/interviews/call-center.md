---
title: Call Center
type: interview
sources: [Cracking the Coding Interview, 6th ed., ch. 7 pp. 125-129 and solutions pp. 305-341 (problem 7.2)]
concepts: [object-oriented-design]
difficulty: medium
---

# Call Center

## Prompt
A call center has respondents, managers and directors. A call goes first to a free respondent; if they cannot handle it, it is escalated to a manager, then to a director. Design classes and implement dispatchCall() assigning to the first available employee.

## Functional requirements
- Three employee levels with escalation.
- Queue the call if nobody suitable is free.

## Non-functional requirements
Not covered in the source (object-oriented design; ask clarifying questions first).

## Estimations
Not covered in the source.

## API
dispatchCall(call), getHandlerForCall(call), employee.receiveCall / callCompleted / escalateAndReassign, call.reply, call.incrementRank, call.disconnect.

## Data model
Employee (abstract: name, address, title, age, rank, current call, free flag), Respondent/Manager/Director subclasses, Call (caller, minimum rank, assigned handler), Rank enum, CallHandler (employee lists per level, per-rank call queues).

## Architecture (high-level design)
- CallHandler is the single entry point: it routes to the lowest-ranked free employee able to take the call, else puts the call in the queue for that rank with a 'please wait' message.
- Role-specific behavior lives in each subclass; common fields in abstract Employee.
- A call carries a minimum rank that increments on escalation.

## Deep dives
- Design for long-term flexibility; there are many equally good designs.
- The amount of code shown is more than an interview would require.

## Trade-offs and decisions
How to handle an employee becoming free while calls are queued; escalation policy.

## Related concepts
[[object-oriented-design]]

## Follow-up questions
Not covered in the source.

## Variants


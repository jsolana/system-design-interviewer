---
title: Personal Financial Manager (Mint-style)
type: interview
sources: [Cracking the Coding Interview, 6th ed. (G. Laakmann McDowell), ch. 9 pp. 137-145 and solutions pp. 372-395 (problem 9.7)]
concepts: [message-queues, batch-processing, caching, sql-vs-nosql]
difficulty: medium
---

# Personal Financial Manager (Mint-style)

## Prompt
Design a personal financial manager like Mint.com: connect to bank accounts, analyze spending habits and recommend.

## Functional requirements
- Create account, add multiple bank accounts (also later).
- Pull financial history: outgoing, incoming, current balances/investments.
- Each transaction has a category (from a data source; user can override).
- Recommendations from typical-user budgets, overridable by custom budgets (not the main focus).
- Website; email notifications (regular or on thresholds / budget exceeded).
- No user-defined categorization rules.

## Non-functional requirements
- Adding/removing accounts is rare; write-heavy (several transactions per day, site visited weekly at most).
- Banks do not push: system pulls.
- Alerts may be up to 24 h late.
- Categories are never reassigned behind the scenes (avoid confusing users).

## Estimations
Not covered in the source.

## API
Not covered in the source.

## Data model
Raw transactions, categorized transactions, per-user budget per category (current totals per category to check thresholds quickly).

## Architecture (high-level design)
Bank data synchronizer -> raw transaction store -> categorizer -> categorized transactions -> budget analyzer -> budget data; the frontend reads categorized transactions and budgets and writes user changes (budget, category overrides).

## Deep dives
- Asynchronous task queue (with priorities, no starvation of low priority, retries) for pulling bank data, categorizing, re-analyzing budgets. Sync frequency depends on user activity; deprioritize or drop inactive users.
- Alerts: enqueue a task when a transaction might exceed a budget instead of scanning all users daily.
- Categorizer: transactions are independent; categories depend on seller name, so group raw transaction files by seller (many duplicates), apply the category once per seller (cache popular sellers), then regroup by user; budget analyzer merges by user and category. Use flat log files for intermediate steps; only final results go to the database.
- User override: update the categorized store and adjust budget (decrement old, increment new) or recompute from the last weeks.

## Trade-offs and decisions
Flat files + batch vs database joins for heavy ingestion; delayed alerts for scalability.

## Related concepts
[[message-queues]], [[batch-processing]], [[caching]]

## Follow-up questions
Mobile app, category assignment design, recommended budgets, user-defined rules.

## Variants
Not covered in the source.

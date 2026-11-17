---
title: Database normalization and denormalization
type: concept
aliases: [denormalization, normalized schema, small database design]
sources: [Cracking the Coding Interview, 6th ed., ch. 14 pp. 169-173, solutions pp. 441-446, ch. 9 pp. 140]
---

# Database normalization and denormalization

## Definition
Normalized databases minimize redundancy (each fact stored once, linked by foreign keys). Denormalized databases add redundant data to speed up reads by avoiding joins.

## Why it matters
Joins get slow as tables grow, so scalable systems avoid them. Large-scale designs almost always use a mix of normalized and denormalized data.

## How it works
- Normalized: Courses(CourseID, CourseName, TeacherID) + Teachers(TeacherID, TeacherName); listing courses with teacher name needs a join, but a teacher rename updates one row.
- Denormalized: store TeacherName in Courses too; reads need no join.
- Small database design steps (same flow as object-oriented design): (1) handle ambiguity (e.g. one location or many? can a person rent two apartments?), (2) define core objects (each becomes a table), (3) analyze relationships (one-to-many via foreign key; many-to-many via a link table such as TenantApartments), (4) investigate actions (leases, payments, move-out add tables/columns).
- Large database design: expect to duplicate data across tables because joins are too slow.
- Entity-relationship modelling: ISA (inheritance, e.g. Professional is a Person), multi-valued attributes (phone numbers), relationship attributes (start date, salary on "Works For").

## Variants and techniques
Denormalized column copies, one row per (product, category) instead of joining, NoSQL stores without joins ([[sql-vs-nosql]]), [[materialized-views]].

## Trade-offs
| Normalized | Denormalized |
|---|---|
| Less storage, single place to update, consistent | Faster reads, simpler read queries (fewer bugs) |
| Reads need joins | Inserts/updates slower and harder to code; data may become inconsistent (which copy is right?); more storage |

## When to use it / when not to
Normalize by default for correctness; denormalize the hot read paths when joins become the bottleneck. In design questions, state assumptions (e.g. one professor per course) and weigh flexibility against complexity.

## Appears in
[[stock-data-feed]]

## See also
[[sql-vs-nosql]], [[database-partitioning]], [[materialized-views]], [[sql-queries-and-joins]]

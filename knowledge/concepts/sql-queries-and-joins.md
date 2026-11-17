---
title: SQL queries and joins
type: concept
aliases: [SQL joins, GROUP BY, HAVING, outer join]
sources: [Cracking the Coding Interview, 6th ed., ch. 14 pp. 169-173, solutions pp. 441-446]
---

# SQL queries and joins

## Definition
Core SQL interview material: join types, aggregation with GROUP BY/HAVING, subqueries and updates with WHERE. Examples in the source are written for Microsoft SQL Server; syntax varies by dialect.

## Why it matters
Frequently asked in database questions; mistakes in joins and aggregation silently drop or duplicate rows.

## How it works
- **Joins** (match rows through a shared field): INNER (only matching rows); LEFT OUTER (all left rows, NULLs when no match); RIGHT OUTER (mirror; A LEFT JOIN B equals B RIGHT JOIN A); FULL OUTER (union of left and right; NULLs on both sides). Implicit (comma + WHERE) and explicit (JOIN ... ON) forms are equivalent.
- **Counting per group with zero groups**: use LEFT JOIN so entities without children appear, count a column of the child table (count(*) would give 1 for an empty group), and convert NULL to 0 (ISNULL/COALESCE).
- **GROUP BY rule**: every selected column must be in GROUP BY or inside an aggregate. Fixes for selecting a name when grouping by ID: wrap in a subquery and join back, add the name to GROUP BY, or apply an aggregate such as max(name).
- **HAVING** filters groups after aggregation, e.g. tenants renting more than one apartment: group the link table by TenantID having count(*) > 1, then join to Tenants.
- Open requests per building: join Requests to Apartments with WHERE Status = 'Open', group by BuildingID, then LEFT JOIN from Buildings with NULL -> 0.
- UPDATE with a subquery: close requests of building 11 with WHERE AptID IN (SELECT AptID FROM Apartments WHERE BuildingID = 11).
- Top 10 percent by GPA: TOP 10 PERCENT returns literally 10% of rows and cuts ties. Compute the GPA cutoff first (min GPA within the top 10%), then select students with GPA >= cutoff so ties are included.
- Test subqueries from the inside out.

## Variants and techniques
Subquery in FROM, correlated vs uncorrelated subqueries, grade database with Students, Courses, CourseEnrollment(Grade, Term).

## Trade-offs
Joins are normalized and flexible but slow at scale; see [[database-normalization-and-denormalization]].

## When to use it / when not to
Relational stores with moderate scale; at very large scale prefer denormalized or NoSQL models ([[sql-vs-nosql]]).

## Appears in
None yet.

## See also
[[database-normalization-and-denormalization]], [[database-indexing]], [[transactions-and-isolation-levels]]

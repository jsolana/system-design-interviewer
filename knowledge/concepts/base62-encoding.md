---
title: Base62 encoding
type: concept
aliases: [base62]
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly, System Design Interview Vol.1 (Alex Xu), ch. 8]
---

# Base62 encoding

## Definition
Encoding of numbers/bytes with 62 symbols (a-z, A-Z, 0-9), suitable for URLs.

## Why it matters
Produces short codes that are safe in paths/queries. Preferred over base64 because `/` is a path separator and `+` can be interpreted as a space in query strings.

## How it works
Capacity by length: 62^6 ≈ 56B, 62^7 ≈ 3.5T, 62^8 ≈ 218T. 1B URLs fit in 6 characters.

## Variants and techniques
Applicable to a counter (reversible) or to a truncated hash. See [[unique-id-generation]].

## Trade-offs
More characters = fewer collisions but less brevity.

## When to use it / when not to
Short public identifiers. It is not encryption: sequential codes are enumerable.

## Additional detail (Xu Vol. 1, ch. 8)
Mapping 0-9 -> 0-9, 10-35 -> a-z, 36-61 -> A-Z. Example: 11157 = 2x62^2 + 55x62 + 59 = [2,55,59] = "2TX". Length 7 (62^7 ≈ 3.5 trillion) covers 365,000M URLs (10 years at 100M/day).

## Appears in
[[pastebin]], [[url-shortener]]

## See also
[[unique-id-generation]]

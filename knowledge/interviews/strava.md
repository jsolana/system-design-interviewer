---
title: Strava
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/strava]
concepts: [redis-sorted-sets]
difficulty: medium
---

# Strava

> Note: paywalled article after the "Final Design" heading; only the prompt, requirements and deep dive questions are readable. Patterns tagged by the source: Scaling Writes and Real-time Updates.

## Prompt
Fitness app to record and share activities (running and cycling) with the user's network, with analytics and route details.

## Functional requirements
- Start, pause, stop and save runs/rides.
- See route, distance and time during the activity.
- View details of own and friends' activities.
- Out of scope: friend management, auth, comments/likes.

## Non-functional requirements
- High availability (over consistency).
- Work without connectivity (remote areas).
- Accurate, up-to-date local statistics during the activity.
- 10M concurrent activities.

## Estimations
Only the target of 10M concurrent activities.

## API
Not covered in the source.

## Data model
Not covered in the source.

## Architecture (high-level design)
Not covered in the source.

## Deep dives
Questions only: offline tracking; scaling to 10M concurrent; sharing activities with friends in real time; leaderboard of top athletes (*Note*: cf. [[redis-sorted-sets]] as a ranking technique seen in [[leetcode]], not confirmed for Strava).

## Trade-offs and decisions
Not covered in the source.

## Related concepts
[[redis-sorted-sets]] (indicative)

## Follow-up questions
Not covered in the source.

## Variants
Not covered in the source.

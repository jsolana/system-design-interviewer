---
title: Online Chess
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/online-chess]
concepts: [websockets, redis-sorted-sets]
difficulty: high
---

# Online Chess

> Note: the page is mostly paywalled; the prompt, functional requirements, scale and deep dive titles are readable.

## Prompt
Online chess platform like Chess.com/Lichess: skill-based matchmaking, real-time game with a clock per player and a global leaderboard. The server validates every move and owns both clocks. Scope: 3-minute blitz only (3 min total per player, the clock runs on their turn, no increment). Rating goes up with wins and down with losses and feeds matchmaking and ranking.

## Functional requirements
- Find an opponent via skill-based matchmaking and start a game.
- Play in real time.
- View the global leaderboard and one's own rank, updated shortly after games end.
- Out of scope: spectators, chat/friends, puzzles/analysis/replays, tournaments, anti-cheat (revisited at the end, paywalled).

## Non-functional requirements
Scale: 10M registered players, 500K concurrent games at peak. Explicit NFR list not covered in the source (paywalled).

## Estimations
500K games x 2 players = 1M concurrent connections; validate every move and two clocks per game.

## API
Not covered in the source.

## Data model
Not covered in the source.

## Architecture (high-level design)
Only three flows: matchmaking and start, real-time play, leaderboard.

## Deep dives
Titles only: prevent a player from entering two games (and what if matchmaking outgrows Postgres?); scale game servers to 500K games; fair clocks with uneven latency; correct and fast leaderboard with 10M players.

## Trade-offs and decisions
Not covered in the source.

## Related concepts
[[websockets]], [[redis-sorted-sets]] (*Note*: indicative).

## Follow-up questions
Matchmaking beyond Postgres; anti-cheat and tournament integrity (paywalled).

## Variants
Not covered in the source.

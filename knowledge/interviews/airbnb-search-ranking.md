---
title: Airbnb Rental Search Ranking
type: interview
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 7 pp. 196-207]
concepts: [ml-evaluation-metrics, feature-engineering-for-ml, embeddings, imbalanced-data-and-sampling, ml-model-serving, training-serving-skew-and-feature-store, geospatial-indexing, message-queues, load-balancer]
difficulty: medium
---

# Airbnb Rental Search Ranking

## Prompt
Given a search (location, dates), sort the available homes so those most likely to be booked appear first. A hand-made score (e.g., text similarity) does not guarantee bookings, so train a binary classifier on booking likelihood.

## Functional requirements
- Rank thousands of candidate listings by booking probability for the user/query.
- Log recommended candidates as future training data.

## Non-functional requirements
- Latency: top results from thousands of matches within 200 ms (ranking 50-100 ms).
- Handle new listings with little data (under-prediction) and unseen listing IDs.
- Time-based train/validation split.

## Estimations
- 100M monthly active users; 5 bookings/user/year; ~30 listings seen per booking -> 5 x 30 x 10^8 = 15 B samples/year = 1.25 B/month.
- 500 B/row -> ~625 GB/month. Keep 6-12 months in the data lake. Support 150M users.

## API
Not covered in the source.

## Data model
Per-sample row: user, query, listing features plus booking label; search/view/booking history.

## Architecture (high-level design)
App server -> search service (looks up an index DB for candidates) -> ranking service (ML model scores booking probability) -> search service sorts -> app server. Scale: more app/search/ranking instances behind load balancers; search service logs candidates to cloud storage or Kafka for training.
- Model: two-tower architecture, input user data + query + listing, output booked/not.

## Deep dives
- **Features**: raw lat/long is noisy; take log of distance from map center per axis; encode map grid cells to keep neighborhood locality; listing ID embedding; listing features (bedrooms, amenities, city); search query text embedding; user features (scaled), previous bookings/stays; time features ([[feature-engineering-for-ml]]).
- **Metrics**: offline DCG/nDCG; online conversion rate (bookings per search results per session) and revenue lift ([[ml-evaluation-metrics]]).
- **Training data length**: decide by experiments across periods comparing accuracy vs training time.

## Trade-offs and decisions
Booking likelihood target vs text similarity; listing ID embeddings are weak (only millions of IDs, few bookings each) -> use feature hashing/other features; thousands of new listings daily -> unseen IDs. Multi-output network (view time + booking) if dwell time correlates with booking. Retrain frequency balances online metrics and training time.

## Related concepts
[[embeddings]], [[imbalanced-data-and-sampling]] (non-bookings far outnumber bookings), [[ml-model-serving]], [[geospatial-indexing]].

## Follow-up questions
Cons of listing ID embeddings; handling unseen IDs; redesign with view_time; retrain cadence.

## Variants
<!-- One entry per variant: source + how it differs from the base design -->

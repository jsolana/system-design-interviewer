---
title: Food Delivery Time Estimation (ML)
type: interview
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 8 pp. 209-218]
concepts: [ml-loss-functions, ml-evaluation-metrics, model-retraining, feature-engineering-for-ml, message-queues, stream-processing, training-serving-skew-and-feature-store, ml-model-serving, olap-columnar-stores]
difficulty: medium
---

# Food Delivery Time Estimation (ML)

## Prompt
Estimate total delivery time for an order: `Delivery = Pickup time + Point-to-point time + Drop-off time`. Batching of orders is ignored. Inputs: order details, market conditions, traffic.

## Functional requirements
- Estimate at order time and update whenever order status changes (restaurant starts preparing, driver starts driving) and push updates to customers.

## Non-functional requirements
- Estimates should be within ~10-15 minutes; over-estimation reduces orders, under-estimation causes unhappy customers.
- Retrain several times a day; low inference latency (100-200 ms). (The source text copies "100 videos" from the YouTube chapter here; clearly a leftover.)

## Estimations
20M monthly active users, 2M active, 300k restaurants, 200k drivers, 20M deliveries/year; ~2M deliveries/month x 500 B = 1 GB (the book writes "1TB"; arithmetic gives 1 GB).

## API
Not covered in the source.

## Data model
Six months of historical deliveries: delivery and actual duration, store, order, customer, location, parking data. Features: order (subtotal, cuisine, type group/catering), items, merchant, store ID + embedding, real-time (orders, dashers, traffic, travel estimates), time (lunch/dinner, weekday, holiday), historical aggregates (past X weeks per store/city/market/time of day), parking-time averages/variance, driving time between restaurant and customer.

## Architecture (high-level design)
- Inference: event-driven with Kafka; status service and notification service handle real-time updates, estimate-delivery-time service runs the model; feature pipeline reads Kafka, aggregates near-real-time stats into a key-value feature store (DynamoDB). Predictions are pushed via Kafka (push not poll).
- Training: data prep from delivery order DB -> Parquet in S3 -> Spark training data; scheduler retrains every few hours -> model storage.
- Scale: scale out services behind load balancers; Kafka for notifications and predictions.

## Deep dives
- **Model**: gradient boosted decision trees on `actual = estimate + error`; RMSE metric treats over- and under-estimation equally (two models with equal RMSE can differ in business impact).
- **Quantile regression** `h_q = z*(q - I[z<0])`; q = 0.05 and 0.95 give a 90% interval; evaluate % of predictions inside the interval and mean estimate; tune q for retention ([[ml-loss-functions]]).
- Retrain often because of traffic/weather/game-day effects ([[model-retraining]]).

## Trade-offs and decisions
RMSE (simple) vs quantile loss (asymmetric business cost); push vs poll; Parquet for throughput.

## Related concepts
[[stream-processing]], [[message-queues]], [[training-serving-skew-and-feature-store]].

## Follow-up questions
Not covered in the source.

## Variants
<!-- One entry per variant: source + how it differs from the base design -->

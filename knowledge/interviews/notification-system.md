---
title: Notification System
type: interview
sources: [https://www.hellointerview.com/learn/system-design/problem-breakdowns/notification-system, System Design Interview Vol.1 (Alex Xu) ch. 10, https://slack.engineering/how-slack-rebuilt-notifications/]
concepts: [queue-backlog-management, retries-timeouts-and-backoff, message-queues, idempotency, rate-limiting, stateless-architecture, online-data-migration]
difficulty: medium
---

# Notification System

> Note: the page is paywalled after the list of deep dives; only the prompt, requirements and questions are readable.

## Prompt
Internal notification platform so other teams can send messages by push, email and SMS. The clients are engineering teams (e.g. an auth service with OTP, marketing with a promo to 1M users).

## Functional requirements
- Send a notification to a user by push/email/SMS, immediate or scheduled.
- Send campaigns (one message to a segment), immediate or scheduled.
- User preferences: per-channel opt-out and quiet hours.
- Out of scope: templates, delivery analytics, in-app feeds/badges, frequency capping.

## Non-functional requirements
- Sustained load: 10M/day (~100/s). Peak: 1M in 5 min (> 3,000/s). Design target: 5,000/s (~50x the sustained load).

## Estimations
The figures above.

## API
Not covered in the source.

## Data model
Not covered in the source.

## Architecture (high-level design)
Not covered in the source (only the outline of three requirements).

## Deep dives
Questions only: guarantee that an accepted notification is not lost; deliver high-priority ones in < 5 s during a campaign; avoid duplicates with at-least-once delivery.

## Trade-offs and decisions
Not covered in the source.

## Related concepts
[[message-queues]], [[idempotency]] (*Note*: indicative).

## Follow-up questions
The three deep dives.

## Variants
- **System Design Interview Vol. 1 (Alex Xu), ch. 10, pp. 151-165**: push notification system (iOS/Android), SMS and email, soft real-time.
  - Requirements: iOS, Android and desktop devices; triggered by clients or scheduled on the server; opt-out; daily scale: 10M push + 1M SMS + 5M email.
  - Providers: iOS -> provider + APNS (device token + JSON payload); Android -> FCM (not available in China: JPush, PushY...); SMS -> Twilio/Nexmo; email -> Sendgrid/Mailchimp. Extensibility to plug/unplug providers.
  - Data: `user` tables (email, phone) and `device` (several device tokens per user); contact info collected when installing the app or signing up. Settings table (`user_id`, `channel`, `opt_in`).
  - The initial design (a single notification server) has a SPOF, is hard to scale and is a bottleneck; improved: DB and cache moved out of the server, more servers with autoscaling, **one queue per notification type** ([[message-queues]]) to isolate a provider's outages, and workers that send to third parties. Flow: service -> server API -> cache/DB metadata -> queue -> workers -> provider -> device.
  - Reliability: do not lose data (persist in a notification log + retries; delay or reordering is accepted, never loss); exactly-once delivery is impossible, duplication is reduced with **dedupe by event ID** ([[idempotency]]).
  - Extras: notification templates, user settings, per-user [[rate-limiting]] (frequency capping), retries by re-enqueueing and alerting if it persists, security with appKey/appSecret, monitoring the number of queued notifications (more workers), event tracking (open rate, click rate).
  - Differs from the base design (internal platform with campaigns and quiet hours): this chapter is a classic architecture with external providers, without scheduling or campaigns.
- **Slack notification preferences rebuild**, source: https://slack.engineering/how-slack-rebuilt-notifications/. Differs: about the preference model, not the delivery pipeline. Four conflicting preference systems (desktop/mobile, "what" coupled to "how") for millions of users were merged into one model: what to notify about (all / mentions and DMs / mute) decoupled from push delivery (desktop+mobile / one / disabled). Migration used read-time interpretation of legacy values and a backfilled push flag so rollback was safe; settings engagement rose 5x. See [[online-data-migration]].

# Processed sources

## Hello Interview - Problem Breakdowns
Index: https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview (the URL with a trailing slash returned 404; the index was read at `/overview`, 32 breakdowns). Accessed: 2026-11-16.

Base URL of each breakdown: https://www.hellointerview.com/learn/system-design/problem-breakdowns/{slug}

### Fully processed (readable content)
- bitly -> interviews/url-shortener.md
- ticketmaster -> interviews/ticketmaster.md
- dropbox -> interviews/dropbox.md
- gopuff -> interviews/gopuff.md
- fb-news-feed -> interviews/fb-news-feed.md
- tinder -> interviews/tinder.md
- leetcode -> interviews/leetcode.md
- whatsapp -> interviews/whatsapp.md
- distributed-rate-limiter -> interviews/distributed-rate-limiter.md
- youtube -> interviews/youtube.md
- fb-live-comments -> interviews/fb-live-comments.md
- top-k -> interviews/top-k.md
- uber -> interviews/uber.md
- web-crawler -> interviews/web-crawler.md
- ad-click-aggregator -> interviews/ad-click-aggregator.md
- fb-post-search -> interviews/fb-post-search.md

### Partially processed (Premium paywall; only the problem statement, requirements and deep dive titles; the rest marked "Not covered in the source")
yelp, instagram, strava, distributed-cache, online-auction, job-scheduler, google-news, camelcamelcamel, notification-system, robinhood, google-docs, payment-system, metrics-monitoring, online-chess, chatgpt, flash-sale -> interviews/{slug}.md

### Concepts created (this pass)
presigned-urls, chunked-multipart-upload, database-partitioning, fan-out, hot-keys, message-queues, geospatial-indexing, bloom-filter, sandboxed-code-execution, redis-sorted-sets, websockets, pub-sub, consistent-hashing, rate-limiting, adaptive-bitrate-streaming, workflow-orchestration, cursor-pagination, stream-processing, count-min-sketch, olap-columnar-stores, inverted-index.
Earlier concepts (Bitly/Ticketmaster): unique-id-generation, base62-encoding, http-redirects, database-indexing, caching, cdn-edge-computing, distributed-lock, optimistic-concurrency-control, server-sent-events, virtual-waiting-queue, full-text-search, change-data-capture, idempotency.

### Expanded concepts
caching, cdn-edge-computing, http-redirects, idempotency, database-indexing (Appears in and sources), distributed-lock (Uber, Gopuff), server-sent-events (Live Comments), full-text-search (variant without an engine), geospatial-indexing and stream-processing (expanded after being created).

### Discarded
Nothing out of scope. Diagrams, videos, quizzes and comments on the pages are not readable as text.

## Pending
- Revisit with Premium access the 16 partial breakdowns listed above (API sections, data model, HLD, deep dives with options and trade-offs). Only their problem statements and requirements are read; nothing was completed from memory.
- Concept links in the partial interviews marked "indicative" are not confirmed by the source.
- Source inconsistencies noted: Tinder (100 vs 200 swipes/user/day), Distributed Rate Limiter (10M vs 100M users), LeetCode (two leaderboard routes), FB Post Search (mention of Elasticsearch despite the restriction).

## Books (docs/)

| Book | Coverage | Notes |
|---|---|---|
| Designing Data-Intensive Applications (Kleppmann) | Ch. 1-12 | No interview problems; 20 new concepts and variants in `payment-system` and `fb-news-feed`. Ch. 3, 5, 6, 7, 9 read in detail; ch. 8, 11, 12 only in fragments; ch. 2, 4, 10 mostly written from prior knowledge (review `data-models`, `encoding-and-schema-evolution`, `batch-processing`). |
| System Design Interview Vol. 1 (Xu) | Ch. 1-16 | Tables (powers of 2, latencies, availability nines, ch. 6 summary) were not extractable. Ch. 16 (reading list) discarded. |
| System Design Interview Vol. 2 (Xu & Lam) | Ch. 1-13 | Scanned PDF read with OCR; some tables and figures illegible. CDN traffic figure in `google-maps` is ambiguous. |
| Grokking the System Design Interview | Intro, 15 problems, System Design Basics (pp. 1-196) | Text extracted from PDF streams; a few phrases truncated. |
| Cracking the Coding Interview, 6th ed. (McDowell) | Big O (ch. VI), technical questions (ch. VII), ch. 1-11, 14, 15, 16, 17 (pdf p. = book p. + 12) | Processed in 3 parts. Coding material goes to `algorithms/` and `coding-problems/`; system design, OO design, databases, threads and testing go to `concepts/` and `interviews/`. Skipped: pp. 76-86 of ch. VII (interview-process advice), ch. 12 (C/C++), ch. 13 (Java), behavioral parts, Hints section, and brain teasers 6.2-6.7, 16.8, 16.12. Solutions text for 8.1 and 16.1 partly cut; difficulty ratings are estimates. `permutations` (ch. 8) and `print-all-permutations` (ch. VII) are distinct problems that overlap. |
| Designing Data-Intensive Applications, 2nd ed. (Kleppmann & Riccomini) | 14 chapters; ch. 1-3, 5-8, 10, 11 read in depth, 4, 9, 12, 13 in part; ch. 14 (ethics) out of scope | 6 new concepts and 22 updated with 'Additional detail (DDIA 2nd edition)'; chapters renumbered vs the 1st edition. Verified the 1st-edition `data-models`, `encoding-and-schema-evolution`, `batch-processing` entries against this text; `batch-processing` keeps some 1st-edition-only details (marked). |
| Programming Interviews Exposed, 3rd ed. (Mongan et al.) | Ch. 9 (concurrency), ch. 12 (transactions only), ch. 16 (network performance only) | Mostly a coding-interview book. In scope (little): `thread-synchronization-and-deadlocks` (new), `network-latency-and-bandwidth` (new), ACID note added to `transactions-and-isolation-levels`. No interview problems created. PDF read via pypdf text extraction. |
| Machine Learning Design Interview (Khang Pham, 2022; file `dokumen.pub_machine-learning-design-interview-...pdf`) | Ch. 1-9 (all, 236 pp.) | ML-system-design book. Read via pypdf text extraction; formulas partly garbled, figures not extractable. 17 new ML concepts (`feature-engineering-for-ml`, `embeddings`, `recommendation-system-pipeline`, `collaborative-filtering`, `learning-to-rank`, `ml-loss-functions`, `ml-evaluation-metrics`, `imbalanced-data-and-sampling`, `model-retraining`, `training-serving-skew-and-feature-store`, `ab-testing`, `model-calibration`, `approximate-nearest-neighbor-search`, `ml-model-serving`, `exploration-exploitation`, `deep-learning-recsys-architectures`). 8 new interviews (`ad-click-prediction`, `airbnb-search-ranking`, `food-delivery-time-estimation`, `airbnb-room-classification`, `linkedin-talent-search`, `linkedin-people-you-may-know`, `linkedin-course-recommendation`, `uber-eta-prediction`). Variants added to `youtube` (ch. 5), `fb-news-feed` (LinkedIn feed ranking, ch. 6), `instagram` (non-friend recommendations, ch. 3). |
| Generative AI System Design Interview (Aminian & Sheng, 2024; file `dokumen.pub_generative-ai-system-design-interview-1.pdf`) | Ch. 1-11 (all, 351 pp.) | Scanned PDF read with macOS Vision OCR; figures, formulas and tables mostly illegible. Interviews: gmail-smart-compose, google-translate, image-captioning, chatpdf-rag, realistic-face-generation, high-resolution-image-synthesis, text-to-image-generation, personalized-headshot-generation, text-to-video-generation; ch. 4 (ChatGPT) added as a variant of `chatgpt`. New concepts: genai-system-design-framework, tokenization, transformer-architecture, llm-training-stages, text-generation-sampling, text-generation-metrics, llm-evaluation, distributed-training-parallelism, vision-transformer, retrieval-augmented-generation, prompt-engineering, rag-evaluation, image-generation-approaches, gan-training, image-generation-evaluation, image-tokenization-vq-vae, latent-diffusion-text-to-image, parameter-efficient-finetuning, generative-ai-system-pipelines; `approximate-nearest-neighbor-search` extended with ANN categories. Appears in regenerated for all concepts. |
| Google SRE Book (free online, https://sre.google/sre-book/table-of-contents/) | Ch. 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26 (read 2026-11-17 via WebFetch summaries) | Concepts only. New: slos-slis-and-error-budgets, observability-and-monitoring, alerting-strategy, cascading-failures, graceful-degradation, capacity-planning, data-integrity-and-backups, disaster-recovery (compiled, no dedicated DR chapter), on-call-and-toil, distributed-periodic-scheduling; release-engineering-and-canary-deployments and incident-management-and-postmortems (also enriched by another extractor with Workbook material). Enriched: load-balancer, consensus, overload-and-metastable-failures, distributed-systems-testing, load-shedding-and-overload-handling and retries-timeouts-and-backoff (both created concurrently by another extractor from AWS sources; SRE sections appended). `concepts:` headers extended in payment-system, distributed-rate-limiter, youtube, uber, metrics-monitoring, job-scheduler, distributed-message-queue. Out of scope: ch. 1-2, 7 (automation history), 25 (data pipelines, not read), 27 (launches), 28-34 (hiring/onboarding/interrupts/engagement/communication/other industries). Notes: pages were read as summaries, so formulas shown only as images (client throttling probability) are not reproduced. |

## Known issues
- `database-replication` was merged into `replication` (aliases kept; links rewritten).
- Possible overlaps to review: `observability-and-monitoring` / `alerting-strategy` / `slo-burn-rate-alerting`; `capacity-planning` / `autoscaling-and-load-management`; `release-engineering-and-canary-deployments` / `safe-deployments-and-rollbacks`; `multitenancy-and-cell-based-architecture` / `multi-tenancy-and-fairness` / `shuffle-sharding-and-cell-based-architecture` (cross-linked, different angles).
- `sql-vs-nosql` was overwritten twice by parallel extractors; check for lost content.
- 40 concepts/algorithms appear in no interview or coding problem (mostly theory and production-operations notes such as SLOs, disaster recovery, tail latency). Earlier list of theory-only concepts: `b-trees`, `serializability`, `linearizability`, `data-models`, `proxies`, `batch-processing`, `back-of-the-envelope-estimation`, `encoding-and-schema-evolution`, `logical-clocks-and-causality`, `distributed-system-faults`, `distributed-systems-characteristics`, `horizontal-vs-vertical-scaling`, `system-design-interview-framework`.

### Programming Interviews Exposed: discarded
Ch. 1-2 (job search, application process), 3 (problem approaches), 4 linked lists, 5 trees/graphs, 6 arrays/strings, 7 recursion, 8 sorting, 10 OOP, 11 design patterns, 13 graphics/bit manipulation, 14-15 puzzles, 17 nontechnical: out of scope. Ch. 12 SQL syntax (SELECT, joins, GROUP BY, schema exercises) discarded as query-writing, not system design. Ch. 16 other items (C++ vs Java, macros, GC, 32/64-bit, web security/SQL injection, cryptography, hash tables vs BSTs) discarded. Ch. 9 Java code samples not reproduced.


### Machine Learning Design Interview: discarded / notes
- Front matter (success stories), ch. 9 assessment quizzes (generic ML, SQL, coding, DL diagnosis) and chapter-end quizzes: out of scope or not design content (a few quiz facts were used inline). Interview exercise lists (ch. 1-2: ~12 prompts such as Facebook events attendance, contraband detection, TikTok hashtags) have no solutions and were not turned into files.
- Source inconsistencies: ad click chapter says 50 bytes and 500 bytes per record; food delivery says "1TB" for 10^9 B and reuses "100 videos" text from the YouTube chapter; LinkedIn feed says 60 TB and 12 TB.
- `## Appears in` sections not touched (to be regenerated).

### Generative AI System Design Interview: notes
- Ch. 8 and ch. 9/10/11 requirement dialogues were only partially readable; `high-resolution-image-synthesis` requirements are inferred from the chapter text (marked as such). Ch. 1 content distributed into framework/training/parallelism concepts. Monitoring deliberately not covered by the book.
- Doubts: the OCR garbled some formulas/numbers (e.g. DreamBooth 15 min, 512x latent compression kept as read); per-chapter follow-up lists were summarized.

## Google SRE Workbook (https://sre.google/workbook/table-of-contents/), accessed 2026-11-17
| Chapter (URL under https://sre.google/workbook/) | Result |
|---|---|
| implementing-slos, slo-engineering-case-studies | `slos-slis-and-error-budgets` enriched |
| monitoring | `observability-and-monitoring` enriched |
| alerting-on-slos | new `slo-burn-rate-alerting`; `alerting-strategy` enriched |
| canarying-releases | `release-engineering-and-canary-deployments` enriched |
| incident-response, postmortem-culture | `incident-management-and-postmortems` enriched |
| configuration-design, configuration-specifics | new `configuration-management-and-safe-config-changes` |
| data-processing | new `data-pipeline-reliability` |
| managing-load | new `autoscaling-and-load-management`; `overload-and-metastable-failures` enriched |
| non-abstract-design | new `non-abstract-large-system-design` |
- Interview `concepts:` headers extended: `metrics-monitoring` (+slo-burn-rate-alerting), `distributed-rate-limiter` (+autoscaling-and-load-management), `ad-click-aggregator` (+data-pipeline-reliability).
- Out of scope / skipped: ch. 1 (SRE vs DevOps), 6 toil, 7 simplicity, 8 on-call, 17 (is human operational overload, not system overload), 18-21 (engagement model, reaching beyond, team lifecycles, organizational change). "Reliable Product Launches at Scale" is not in the Workbook ToC, so no `reliable-launch-checklist` was created.
- Notes: the fetched non-abstract-design page uses an AdWords CTR example (not Shakespeare); managing-load has Pokemon GO but no Snapchat. Source's low-traffic burn-rate figure (1,000x) is inconsistent; ~100x used.

## Engineering blogs - batch 2
Accessed 2026-11-17.
- https://www.figma.com/blog/how-figmas-databases-team-lived-to-tell-the-scale/ : updated `database-partitioning` (vertical then horizontal Postgres sharding, DBProxy, logical vs physical sharding).
- https://www.figma.com/blog/livegraph-real-time-data-at-scale/ : updated `caching` (invalidation-based read-through cache, edge/cache/invalidator split).
- https://www.figma.com/blog/figmas-next-generation-data-caching-platform/ : updated `caching`, `proxies` (FigCache Redis proxy).
- https://highscalability.com/brief-history-of-scaling-uber/ : variant in `uber`.
- https://highscalability.com/capturing-a-billion-emo-j-i-ons/ : variant in `fb-live-comments` (Hotstar emoji pipeline).
- https://www.confluent.io/blog/10x-apache-kafka-elasticity/ : created `tiered-storage`; updated `message-queues`, `distributed-message-queue` (concepts header). Vendor post; its "954%" figure is inconsistent and was omitted.
- Pending / failed: doordash.engineering (302 redirect to careers page, then 403), medium.com/airbnb-engineering (403), lyft.com/blog/engineering (403), blog.grab.com and engineering.atlassian.com (DNS not found), pinterest.com/engineering (content truncated, no links), cockroachlabs.com/blog (index only had a podcast recap and a release note, no internals articles; /tag/engineering 404), aws.amazon.com/blogs/architecture (index only had AI/regression-testing customer posts, none read), confluent.io/blog (index had releases/marketing; only the elasticity post used). Not read to save scope: Figma OpenSearch/data pipeline/sandboxes posts, highscalability S3 and Presto posts.


### AWS Builders' Library (selected articles, accessed 2026-11-17)
Index https://aws.amazon.com/builders-library/ redirects (301) to builder.aws.com and its article list is JS-rendered (no links extractable), so the 14 articles were fetched by their known aws.amazon.com/builders-library/<slug>/ URLs (each 301-redirected to builder.aws.com/content/...). All processed; `sources` cite the aws.amazon.com URLs.
- Articles: timeouts-retries-and-backoff-with-jitter, avoiding-fallback-in-distributed-systems, static-stability-using-availability-zones, workload-isolation-using-shuffle-sharding, using-load-shedding-to-avoid-overload, fairness-in-multi-tenant-systems, avoiding-insurmountable-queue-backlogs, implementing-health-checks, automating-safe-hands-off-deployments, caching-challenges-and-strategies, leader-election-in-distributed-systems, challenges-with-distributed-systems, ensuring-rollback-safety-during-deployments, reliability-and-constant-work (= "Reliability, constant work, and a good cup of coffee").
- Created concepts: `avoiding-fallback-in-distributed-systems`, `static-stability`, `shuffle-sharding-and-cell-based-architecture`, `multi-tenancy-and-fairness`, `queue-backlog-management`, `health-checks`, `safe-deployments-and-rollbacks`, `constant-work-pattern`, `leader-election`; `retries-timeouts-and-backoff` and `load-shedding-and-overload-handling` were created by this pass but concurrently written by other extractors (merged; verify nothing lost).
- Updated: `caching` (new section), `distributed-system-faults` (new section), `overload-and-metastable-failures`, `multitenancy-and-cell-based-architecture`, `consensus` (see-also); `concepts:` headers of interviews `distributed-rate-limiter`, `distributed-message-queue`, `notification-system`, `job-scheduler`.
- Not covered: multi-region architecture (no such article in the selection; `multi-data-center` untouched). Skipped: non-technical articles.

## Engineering blogs - batch 1
Accessed 2026-11-17. One line per article read.
- https://discord.com/blog/how-discord-automates-scylladb-clusters-at-scale -> `workflow-orchestration` (section)
- https://discord.com/blog/how-we-moved-discord-voice-to-the-edge -> new interview `discord-voice-infrastructure`
- https://slack.engineering/how-slack-rebuilt-notifications/ -> variant in `notification-system`; `online-data-migration`
- https://blog.cloudflare.com/choosing-quepaxa/ -> `consensus` (section)
- https://blog.cloudflare.com/origin-range-requests/ -> `cdn-edge-computing` (section)
- https://engineering.fb.com/2026/10/28/ml-applications/meta-andromeda-next-gen-ads-retrieval-gpu-co-design/ -> variant in `ad-click-prediction`
- https://www.uber.com/es/en/blog/introducing-shard-manager/ -> new concept `shard-rebalancing`
- https://www.uber.com/es/en/blog/high-performance-search-platform/ -> variant in `twitter-search`; `online-data-migration`
- https://dropbox.tech/infrastructure/improving-storage-efficiency-in-magic-pocket-our-immutable-blob-store -> new concept `storage-compaction`; variant in `s3-object-storage`
- https://dropbox.tech/application/how-dropbox-replay-keeps-everyone-in-sync -> variant in `google-docs`
- https://github.blog/engineering/architecture-optimization/inside-githubs-new-git-storage-architecture/ -> new interview `git-repository-hosting`
- https://github.blog/engineering/architecture-optimization/from-2500-requests-to-24-rebuilding-star-history-without-the-stargazers/ -> `cursor-pagination` (section)
- https://engineering.atspotify.com/2026/7/indexing-the-data-lake-for-online-point-queries -> new concept `data-lake-point-lookup`
- https://shopify.engineering/capturing-every-change-shopify-sharded-monolith -> `change-data-capture` (section)
- https://shopify.engineering/horizontally-scaling-the-rails-backend-of-shop-app-with-vitess -> `online-data-migration` (Vitess phases)
- https://stripe.dev/blog/ledger-stripe-system-for-tracking-and-validating-money-movement (stripe.com redirects 301 to stripe.dev) -> variant in `payment-system`
- https://stripe.dev/blog/how-stripes-document-databases-supported-99.999-uptime-with-zero-downtime-data-migrations -> `online-data-migration`, variant pointer in `payment-system`
- https://www.linkedin.com/blog/engineering/infrastructure/introducing-northguard-and-xinfra -> variant in `distributed-message-queue`; `shard-rebalancing`
- https://www.linkedin.com/blog/engineering/search/reimagining-linkedins-search-stack -> variant in `linkedin-talent-search`

### Pending / failed (batch 1)
- https://netflixtechblog.com/ : HTTP 403 on fetch; not read, nothing filed.
- https://engineering.linkedin.com/ : 403; worked via https://www.linkedin.com/blog/engineering (2 articles read).
- Meta (engineering.fb.com): only 1 article read (Andromeda); F3 Lightning, Intelligent Delivery, PrivacyLib not read.
- Unread candidates: Slack Shipyard, Slack AI multi-cloud; Cloudflare DNS targeted zone builds; Uber Velox, Translations at Scale, Ads marketplace; Dropbox Riviera; Spotify other posts; Shopify catalog clustering; Stripe payment-api-design, data plane proxy; GitHub agent-scale Git posts; Discord voice outage review.
### Notes


## Engineering blogs - batch 3
Accessed 2026-11-17. One line per page read.
- https://microservices.io/patterns/index.html (index) ; https://microservices.io/patterns/data/saga.html -> `saga` (section)
- https://microservices.io/patterns/data/transactional-outbox.html -> new `transactional-outbox`
- https://microservices.io/patterns/reliability/circuit-breaker.html -> new `circuit-breaker`
- https://microservices.io/patterns/apigateway.html -> new `api-gateway`
- https://microservices.io/patterns/microservices.html -> new `microservices-architecture`
- https://microservices.io/patterns/refactoring/strangler-application.html -> new `strangler-fig-migration` (page is thin)
- https://microservices.io/patterns/data/cqrs.html -> `cqrs` (section)
- https://martinfowler.com/articles/microservices.html, https://martinfowler.com/articles/microservice-trade-offs.html -> `microservices-architecture`
- https://martinfowler.com/bliki/CQRS.html -> `cqrs` (section)
- https://martinfowler.com/bliki/CircuitBreaker.html -> `circuit-breaker`
- https://martinfowler.com/bliki/StranglerFigApplication.html -> `strangler-fig-migration`
- https://brandur.org/idempotency-keys -> `idempotency` (section), `transactional-outbox`
- https://brandur.org/job-drain, https://brandur.org/postgres-queues -> `transactional-outbox` (Postgres-queue failure mode and numbers)
- https://jepsen.io/analyses (index), https://jepsen.io/consistency, https://jepsen.io/consistency/models, https://jepsen.io/analyses/postgresql-12.3, https://jepsen.io/analyses/mongodb-4.2.6, https://jepsen.io/analyses/etcd-3.4.3 -> new `consistency-anomalies-jepsen`; `distributed-lock` (etcd section)
- https://blog.acolyer.org/ (index), https://blog.acolyer.org/2020/11/23/elle/ -> `consistency-anomalies-jepsen`
- https://www.brendangregg.com/usemethod.html -> new `performance-analysis-methods`
- https://danluu.com/ (index), https://danluu.com/postmortem-lessons/, https://danluu.com/cache-incidents/ -> `incident-management-and-postmortems` (section)
- https://danluu.com/percentile-latency/ -> new `tail-latency`
- https://www.allthingsdistributed.com/2008/12/eventually_consistent.html, https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html -> new `eventual-consistency`; `tail-latency`
- https://blog.pragmaticengineer.com/ (index), /resiliency-in-distributed-systems/ -> `retries-timeouts-and-backoff` (section), `circuit-breaker`, `tail-latency`; /distributed-architecture-concepts-i-have-learned-while-building-payments-systems/ -> `idempotency` (section)
- Interview `concepts:` headers updated: `payment-system`, `digital-wallet` (+transactional-outbox), `key-value-store` (+eventual-consistency), `distributed-cache` (+tail-latency).

### Pending / failed (batch 3)
- https://danluu.com/tail-latency/ : 404 (guessed URL); used /percentile-latency/ instead.
- https://blog.bytebytego.com/ : index returned only the subscribe landing page (no post links); nothing read. Posts may be Substack-gated; Pending.
- https://www.infoq.com/architecture-design/ : listing had only two unrelated recent items (multi-agent LLM batch, OpenTelemetry queue observability); nothing read.
- https://jvns.ca/ : index read, no article fetched (candidates: consistency-vs-availability, log-structured-storage, service-discovery-at-stripe).
- Unread candidates: pragmaticengineer "typical-migration-approaches", "operating-a-high-scale-distributed-system"; Acolyer Delos/Seeing is believing; Jepsen MySQL/RDS PostgreSQL/TiDB analyses; Dan Luu p95-skill, limplock.
- Fowler "Event Sourcing" / Saga pages not fetched (existing `event-sourcing`, `saga` not enriched from Fowler).

### Level guides (authored)
`knowledge/levels/{system-design,coding,ml-design}.md` are authored calibration guides (expectations and probing questions per level, junior to staff+), not extracted from a single source. Used by the practice mode. Not official rubrics of any company.

### Production-readiness additions (this pass)
Sources: Google SRE Book, Google SRE Workbook, AWS Builders' Library (14 articles), engineering blogs (batches 1-3, see sections above). Blocked or unreadable blogs (Netflix, DoorDash, Airbnb/Medium, Lyft, Grab, Atlassian, ByteByteGo, InfoQ, Pinterest, Cockroach Labs, AWS Architecture blog index) are listed under Pending in their batch sections. Known gap: no dedicated multi-region architecture concept yet. Blog numbers are as reported by the authors and not verified.

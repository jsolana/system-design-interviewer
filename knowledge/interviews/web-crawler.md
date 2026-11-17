---
title: Web Crawler
type: interview
sources: [Cracking the Coding Interview ch. 9.3, https://www.hellointerview.com/learn/system-design/problem-breakdowns/web-crawler, System Design Interview Vol.1 (Alex Xu) ch. 9, Grokking the System Design Interview (PDF), "Designing a Web Crawler" pp. 119-127]
concepts: [message-queues, rate-limiting, distributed-lock, bloom-filter, caching, consistent-hashing, database-partitioning, stateless-architecture, load-balancer, data-deduplication]
difficulty: medium
---

# Web Crawler

## Prompt
A crawler that starts from seed URLs, downloads pages and extracts text to train an LLM (the output would also work for search indexing).

## Functional requirements
- Crawl the web from seeds; extract and store the text of each page.
- Out of scope: processing the text, non-text content, JS-rendered content, pages behind login.

## Non-functional requirements
- Fault tolerance (resume without losing progress).
- Politeness: respect robots.txt and do not overload servers.
- Efficiency: < 5 days.
- Scale: 10B pages.
- Out of scope: security, cost, compliance.

## Estimations
- 10B pages, ~2 MB per page (HTML alone ~30 KB), data ready in 5 days.
- Instance optimized for 200 Gbps network ≈ 12,500 pages/s at 2 MB; at 30% utilization ≈ 3,750 pages/s per machine.
- One machine ≈ 30.9 days; 8 machines ≈ 3.9 days. Approximate figures: they require load testing.

## API
Input: seed URLs. Output: extracted text. No REST.

## Data model
Metadata DB (DynamoDB, or PostgreSQL/MySQL): **URL** (state fetched/processed, link to the raw HTML blob and the text blob, content hash, depth) and **Domain** (last crawl, parsed robots.txt rules, per-domain lock/state). Text and HTML in S3.

## Architecture (high-level design)
Flow: URL from the frontier -> DNS -> fetch HTML -> extract text -> store -> extract links into the frontier -> repeat. Components: Frontier Queue (Kafka, Redis or SQS), Crawler, DNS, external websites, S3.

## Deep dives
1. **Fault tolerance**: staged pipeline (URL Fetcher that stores raw HTML in a blob + text and URL extraction); messages carry only IDs. Retries: in-memory timer (bad); Kafka with retry topic and exponential backoff (good, complex); **SQS** with exponential backoff via visibility timeout/ChangeMessageVisibility and a dead-letter queue after 5 attempts (chosen). Recovery: Kafka offsets after success; SQS keeps the message until it is deleted.
2. **Politeness**: download and parse robots.txt per domain and check Disallow (skip with ack); honor crawl-delay (non-standard, Googlebot ignores it) by deferring with ChangeMessageVisibility (DelaySeconds only applies to new messages); per-domain lock with Redis `SET NX` and TTL = crawl delay ([[distributed-lock]]); ~1 req/s per domain with a global sliding window counter in Redis and jitter ([[rate-limiting]]).
3. **Scale and efficiency**: ~8 high-bandwidth machines with thousands of concurrent connections across many domains; parser workers with autoscaling by queue depth (Lambda/ECS Fargate); **DNS** as a bottleneck (cache, several providers in round-robin; the Mercator paper reported up to 70% of thread time); URL dedup by querying the table before enqueuing; content dedup: hash indexed in the Metadata DB (preferred) or [[bloom-filter]] (RedisBloom BF.ADD/BF.EXISTS, considered overkill); crawler traps: maximum depth ~15-20 hops.

## Trade-offs and decisions
- SQS vs Kafka: native backoff and visibility timeouts vs greater control.
- Hash in DB vs Bloom filter: simplicity vs memory.
- Separating stages isolates failures and allows changing extraction without refetching.

## Related concepts
[[message-queues]], [[rate-limiting]], [[distributed-lock]], [[bloom-filter]], [[caching]]

## Follow-up questions
Dynamic content (headless browser, Puppeteer); monitoring (Datadog/New Relic); large files (HEAD and Content-Length, skip > ~10 MB); continuous updates (URL Scheduler by last visit/popularity); priority crawl (several SQS queues or topics by priority).

## Variants
- **System Design Interview Vol. 1 (Alex Xu), ch. 9, pp. 132-150**: search engine crawler, no practical interview time limit; component-oriented.
  - Scope: indexing for a search engine, 1,000M pages/month, HTML only, include new/edited pages, store HTML for up to 5 years, ignore duplicate content. Properties: scalability, robustness, politeness, extensibility.
  - Estimations: 1,000M/30/24/3600 ≈ 400 pages/s (peak 800); 500 KB/page -> 500 TB/month; 5 years ≈ 30 PB.
  - Components: Seed URLs (by locality or by topic), URL Frontier, HTML Downloader, DNS Resolver, Content Parser (separate so as not to slow the crawl), "Content Seen?" (29% of pages are duplicates; compare hashes), Content Storage (disk + memory for popular content), URL Extractor (relative to absolute), URL Filter, "URL Seen?" ([[bloom-filter]] or hash table) and URL Storage. 11-step workflow.
  - Deep dive: BFS with a FIFO queue (DFS discarded because of depth); **URL Frontier** = *front queues* (priority: PageRank, traffic, update frequency; biased selector) + *back queues* (politeness: one FIFO queue per host mapped to a worker, with delay between downloads, queue router and mapping table); freshness through recrawl based on change history and priority; hybrid storage (mostly on disk, in-memory buffers).
  - HTML Downloader: respect `robots.txt` (cached); distributed crawl (partition the URL space); DNS cache (10-200 ms, a synchronous resolver blocks threads); geographic locality; short timeouts.
  - Robustness: [[consistent-hashing]] across downloaders, saving crawl state, exception handling, data validation. Extensibility with pluggable modules (PNG downloader, web monitor).
  - Problematic content: duplicates (hash/checksum), spider traps (limit URL length, manual review/custom filters), noise (ads, spam).
  - Wrap-up: server-side/dynamic rendering for JS, anti-spam, replication and sharding, stateless web tier, analytics.
  - Differs from the base design: here the focus is the frontier with priority + politeness and PB-scale storage, not the work queue with retries.

- **Grokking the System Design Interview (PDF), pp. 119-127** (difficulty Hard): general crawler, extensible to other document types and protocols.
  - Estimations: 15 B pages in 4 weeks ≈ 6,200 pages/s; 15 B x (100 KB + 500 B) ≈ 1.5 PB (2.14 PB at 70% occupancy).
  - Algorithm: seed URLs -> BFS (DFS in certain cases); path-ascending crawling; respect robots.txt (with cache).
  - Components: URL frontier, HTTP fetcher, extractor, duplicate eliminator, datastore; multithreaded workers with protocol and MIME modules; **Document Input Stream** (documents < 64 KB in memory, the rest to file).
  - Distributed frontier with a **FIFO queue per worker and hashed hostname** to enforce politeness (one thread per web server); enqueue/dequeue buffers on disk (hundreds of millions of URLs).
  - Dedupe of documents (64-bit checksum, 120 GB) and of URLs (4 B, 60 GB) with LRU cache; **[[bloom-filter]]** as an alternative (false positives mean that page is never downloaded); URL filters; DNS with local cache (bottleneck); state checkpointing.
  - Fault tolerance with consistent hashing; the three classes of data (pending URLs, URL checksums and document checksums) reside on the same host according to hostname; **crawler traps** (loops, anti-spam traps).
- **Cracking the Coding Interview (problem 9.3, pp. 137-145, 378-379)**: only asks how to avoid infinite loops. Cycles in the link graph are avoided with a visited hash table over a BFS queue, but "same page" is ambiguous: by URL (parameters may or may not change the page) or by content (random content differs on each visit). Proposal: compute a signature from page content snippets plus URL; look it up in a DB of recently crawled signatures; if seen, re-insert the page at low priority, else crawl and insert its links. A minimum priority threshold lets crawling "finish" on a small web (e.g. an intranet).

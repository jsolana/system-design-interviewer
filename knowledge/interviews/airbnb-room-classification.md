---
title: Airbnb Room Classification
type: interview
sources: [Machine Learning Design Interview (Khang Pham, 2022), ch. 3 pp. 133-135]
concepts: [ml-evaluation-metrics, ml-model-serving, feature-engineering-for-ml]
difficulty: low
---

# Airbnb Room Classification

## Prompt
Classify listing photos/text into room types (bedroom, living room, gym...).

## Functional requirements
- Multi-class classifier on images plus captions/amenity/host description text.

## Non-functional requirements
- High precision (>= 95%); room types assumed not too imbalanced; batch inference is enough.

## Estimations
Not covered in the source.

## API
Not covered in the source.

## Data model
Listing images, amenities images, image descriptions, amenities, host description. Labels: third-party vendors (high quality) plus host-captured images.

## Architecture (high-level design)
Pretrained ResNet50 + two extra fully connected layers + softmax. Two training modes: **fine-tuning** (freeze base, train added layers; easy, decent) or retrain the whole network (harder, better). Serving by offline batch inference.

## Deep dives
Improvement: pretrained Faster R-CNN detects amenities in each image to improve label quality. Metrics: precision, recall, accuracy, F1.

## Trade-offs and decisions
Fine-tune vs full retrain; batch vs online inference.

## Related concepts
[[ml-evaluation-metrics]], [[ml-model-serving]], [[embeddings]] (visual embeddings reuse CNN last layers).

## Follow-up questions
How to collect labels; how to leverage pretrained CV models; use of captions.

## Variants
<!-- One entry per variant: source + how it differs from the base design -->

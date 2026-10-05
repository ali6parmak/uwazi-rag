# Retrieval eval results — `uwazi-rag eval` (Step 3.5)

Append-only scorecard log: every run appends one dated, labeled block below. The golden set is the committed `data/eval/golden.jsonl`; scores are *relative* (config A vs config B, shared self-echo bias), never absolute (see `data/eval/about.md`).

## 2026-10-01T12:57:18+00:00 — baseline — Step 2 defaults (max-chars 1800, overlap 0.15, header on), bge-m3 1024d

store: `data/naive_store.json` — 2,850 chunks, bge-m3 (1024d), built 2026-09-30T08:58:30+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 30.0% | 65.9% | 75.7% | 0.490 | 62.5% | 89.5% | 92.5% | 0.746 |
| en | 169 | 32.5% | 70.4% | 76.3% | 0.506 | 68.0% | 90.5% | 93.5% | 0.777 |
| es | 98 | 25.5% | 58.2% | 74.5% | 0.462 | 53.1% | 87.8% | 90.8% | 0.691 |
| synthetic | 255 | 30.0% | 65.9% | 75.7% | 0.492 | 62.0% | 89.4% | 92.5% | 0.742 |
| manual | 12 | 29.2% | 66.7% | 75.0% | 0.445 | 75.0% | 91.7% | 91.7% | 0.826 |
| cross-language | 65 | 23.1% | 62.3% | 71.5% | 0.436 | 58.5% | 93.8% | 98.5% | 0.729 |
| same-language | 202 | 32.2% | 67.1% | 77.0% | 0.508 | 63.9% | 88.1% | 90.6% | 0.751 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5081, m014 0.5040, m015 0.4606)


## 2026-10-01T15:14:05+00:00 — post-refactor sanity — baseline store re-run through the shared path

store: `data/naive_store.json` — 2,850 chunks, bge-m3 (1024d), built 2026-09-30T08:58:30+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 30.0% | 65.9% | 75.7% | 0.490 | 62.5% | 89.5% | 92.5% | 0.746 |
| en | 169 | 32.5% | 70.4% | 76.3% | 0.506 | 68.0% | 90.5% | 93.5% | 0.777 |
| es | 98 | 25.5% | 58.2% | 74.5% | 0.462 | 53.1% | 87.8% | 90.8% | 0.691 |
| synthetic | 255 | 30.0% | 65.9% | 75.7% | 0.492 | 62.0% | 89.4% | 92.5% | 0.742 |
| manual | 12 | 29.2% | 66.7% | 75.0% | 0.445 | 75.0% | 91.7% | 91.7% | 0.826 |
| cross-language | 65 | 23.1% | 62.3% | 71.5% | 0.436 | 58.5% | 93.8% | 98.5% | 0.729 |
| same-language | 202 | 32.2% | 67.1% | 77.0% | 0.508 | 63.9% | 88.1% | 90.6% | 0.751 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5081, m014 0.5040, m015 0.4606)


## 2026-10-01T15:14:44+00:00 — benchmark sweep1-chunking: baseline-1800-header

store: `data/naive_store.json` — 2,850 chunks, bge-m3 (1024d), built 2026-09-30T08:58:30+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 30.0% | 65.9% | 75.7% | 0.490 | 62.5% | 89.5% | 92.5% | 0.746 |
| en | 169 | 32.5% | 70.4% | 76.3% | 0.506 | 68.0% | 90.5% | 93.5% | 0.777 |
| es | 98 | 25.5% | 58.2% | 74.5% | 0.462 | 53.1% | 87.8% | 90.8% | 0.691 |
| synthetic | 255 | 30.0% | 65.9% | 75.7% | 0.492 | 62.0% | 89.4% | 92.5% | 0.742 |
| manual | 12 | 29.2% | 66.7% | 75.0% | 0.445 | 75.0% | 91.7% | 91.7% | 0.826 |
| cross-language | 65 | 23.1% | 62.3% | 71.5% | 0.436 | 58.5% | 93.8% | 98.5% | 0.729 |
| same-language | 202 | 32.2% | 67.1% | 77.0% | 0.508 | 63.9% | 88.1% | 90.6% | 0.751 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5081, m014 0.5040, m015 0.4606)


## 2026-10-01T15:14:47+00:00 — benchmark sweep1-chunking: merge-1200

store: `data/benchmark_stores/merge-1200.json` — 4,488 chunks, bge-m3 (1024d), built 2026-10-01T15:14:47+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.4% | 62.8% | 73.5% | 0.479 | 62.9% | 91.8% | 93.6% | 0.751 |
| en | 169 | 32.8% | 64.2% | 73.4% | 0.484 | 68.0% | 92.9% | 93.5% | 0.782 |
| es | 98 | 28.9% | 60.4% | 73.8% | 0.470 | 54.1% | 89.8% | 93.9% | 0.698 |
| synthetic | 255 | 31.3% | 62.6% | 73.1% | 0.479 | 62.4% | 91.4% | 93.3% | 0.747 |
| manual | 12 | 33.3% | 66.7% | 83.3% | 0.476 | 75.0% | 100.0% | 100.0% | 0.833 |
| cross-language | 65 | 23.6% | 53.3% | 70.0% | 0.412 | 55.4% | 92.3% | 95.4% | 0.701 |
| same-language | 202 | 33.9% | 65.8% | 74.7% | 0.500 | 65.3% | 91.6% | 93.1% | 0.767 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5359, m014 0.5081, m015 0.4582)


## 2026-10-01T15:15:32+00:00 — benchmark sweep1-chunking: merge-2400

store: `data/benchmark_stores/merge-2400.json` — 2,069 chunks, bge-m3 (1024d), built 2026-10-01T15:15:32+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 29.6% | 63.5% | 71.2% | 0.465 | 59.6% | 89.1% | 93.3% | 0.722 |
| en | 169 | 29.6% | 66.9% | 74.9% | 0.472 | 62.7% | 89.9% | 94.1% | 0.744 |
| es | 98 | 29.6% | 57.7% | 64.8% | 0.453 | 54.1% | 87.8% | 91.8% | 0.683 |
| synthetic | 255 | 29.8% | 64.1% | 72.2% | 0.469 | 58.8% | 89.0% | 92.9% | 0.717 |
| manual | 12 | 25.0% | 50.0% | 50.0% | 0.373 | 75.0% | 91.7% | 100.0% | 0.831 |
| cross-language | 65 | 25.4% | 66.2% | 73.8% | 0.448 | 53.8% | 93.8% | 98.5% | 0.694 |
| same-language | 202 | 30.9% | 62.6% | 70.3% | 0.470 | 61.4% | 87.6% | 91.6% | 0.731 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5167, m014 0.5154, m015 0.4686)


## 2026-10-01T15:16:03+00:00 — benchmark sweep1-chunking: merge-1800-noheader

store: `data/benchmark_stores/merge-1800-noheader.json` — 2,850 chunks, bge-m3 (1024d), built 2026-10-01T15:16:03+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header OFF

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.1% | 64.8% | 74.3% | 0.488 | 61.8% | 91.0% | 92.9% | 0.739 |
| en | 169 | 31.7% | 66.9% | 75.7% | 0.489 | 65.7% | 91.1% | 92.9% | 0.756 |
| es | 98 | 30.1% | 61.2% | 71.9% | 0.487 | 55.1% | 90.8% | 92.9% | 0.708 |
| synthetic | 255 | 31.6% | 64.9% | 74.3% | 0.492 | 61.2% | 91.0% | 92.5% | 0.734 |
| manual | 12 | 20.8% | 62.5% | 75.0% | 0.403 | 75.0% | 91.7% | 100.0% | 0.828 |
| cross-language | 65 | 23.1% | 57.7% | 70.8% | 0.417 | 55.4% | 92.3% | 96.9% | 0.693 |
| same-language | 202 | 33.7% | 67.1% | 75.5% | 0.511 | 63.9% | 90.6% | 91.6% | 0.753 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4983, m014 0.5066, m015 0.4675)


## 2026-10-01T15:16:35+00:00 — benchmark sweep1-chunking — comparison (4 experiments)

| experiment | model | chunk cfg | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline-1800-header | bge-m3 | 1800/0.15/on | 267 | 30.0% | 65.9% | 75.7% | 0.490 | 62.5% | 89.5% | 92.5% | 0.746 | 0/3 | reuse / 3.1s |
| merge-1200 | bge-m3 | 1200/0.15/on | 267 | 31.4% | 62.8% | 73.5% | 0.479 | 62.9% | 91.8% | 93.6% | 0.751 | 0/3 | 41s / 3.5s |
| merge-2400 | bge-m3 | 2400/0.15/on | 267 | 29.6% | 63.5% | 71.2% | 0.465 | 59.6% | 89.1% | 93.3% | 0.722 | 0/3 | 29s / 2.8s |
| merge-1800-noheader | bge-m3 | 1800/0.15/off | 267 | 31.1% | 64.8% | 74.3% | 0.488 | 61.8% | 91.0% | 92.9% | 0.739 | 0/3 | 28s / 3.1s |


## 2026-10-01T15:16:54+00:00 — benchmark sweep2-models: bge-m3-baseline

store: `data/naive_store.json` — 2,850 chunks, bge-m3 (1024d), built 2026-09-30T08:58:30+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 30.0% | 65.9% | 75.7% | 0.490 | 62.5% | 89.5% | 92.5% | 0.746 |
| en | 169 | 32.5% | 70.4% | 76.3% | 0.506 | 68.0% | 90.5% | 93.5% | 0.777 |
| es | 98 | 25.5% | 58.2% | 74.5% | 0.462 | 53.1% | 87.8% | 90.8% | 0.691 |
| synthetic | 255 | 30.0% | 65.9% | 75.7% | 0.492 | 62.0% | 89.4% | 92.5% | 0.742 |
| manual | 12 | 29.2% | 66.7% | 75.0% | 0.445 | 75.0% | 91.7% | 91.7% | 0.826 |
| cross-language | 65 | 23.1% | 62.3% | 71.5% | 0.436 | 58.5% | 93.8% | 98.5% | 0.729 |
| same-language | 202 | 32.2% | 67.1% | 77.0% | 0.508 | 63.9% | 88.1% | 90.6% | 0.751 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5081, m014 0.5040, m015 0.4606)


## 2026-10-01T15:16:57+00:00 — benchmark sweep2-models: qwen3-embedding-06b

store: `data/benchmark_stores/qwen3-06b.json` — 2,850 chunks, qwen3-embedding:0.6b (1024d), built 2026-10-01T15:17:16+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 29.8% | 62.2% | 74.2% | 0.483 | 59.9% | 88.8% | 93.6% | 0.722 |
| en | 169 | 29.6% | 61.2% | 73.1% | 0.469 | 59.8% | 87.0% | 92.9% | 0.716 |
| es | 98 | 30.1% | 63.8% | 76.0% | 0.506 | 60.2% | 91.8% | 94.9% | 0.733 |
| synthetic | 255 | 30.6% | 62.4% | 74.5% | 0.489 | 59.6% | 88.2% | 93.3% | 0.718 |
| manual | 12 | 12.5% | 58.3% | 66.7% | 0.343 | 66.7% | 100.0% | 100.0% | 0.819 |
| cross-language | 65 | 32.3% | 63.8% | 73.1% | 0.502 | 58.5% | 92.3% | 96.9% | 0.720 |
| same-language | 202 | 29.0% | 61.6% | 74.5% | 0.477 | 60.4% | 87.6% | 92.6% | 0.723 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4671, m014 0.4360, m015 0.3119)


## 2026-10-01T15:18:35+00:00 — benchmark sweep2-models: nomic-embed-v2-moe

store: `data/benchmark_stores/nomic-v2-moe.json` — 2,850 chunks, nomic-embed-text-v2-moe (768d), built 2026-10-01T15:18:43+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 33.0% | 65.7% | 78.3% | 0.508 | 63.3% | 88.4% | 95.1% | 0.745 |
| en | 169 | 35.2% | 67.8% | 79.3% | 0.523 | 66.3% | 88.2% | 94.1% | 0.755 |
| es | 98 | 29.1% | 62.2% | 76.5% | 0.483 | 58.2% | 88.8% | 96.9% | 0.728 |
| synthetic | 255 | 33.9% | 65.9% | 78.4% | 0.515 | 62.7% | 88.2% | 95.3% | 0.741 |
| manual | 12 | 12.5% | 62.5% | 75.0% | 0.354 | 75.0% | 91.7% | 91.7% | 0.833 |
| cross-language | 65 | 30.0% | 62.3% | 76.9% | 0.475 | 60.0% | 89.2% | 96.9% | 0.714 |
| same-language | 202 | 33.9% | 66.8% | 78.7% | 0.519 | 64.4% | 88.1% | 94.6% | 0.755 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5017, m014 0.4497, m015 0.4142)


## 2026-10-01T15:19:07+00:00 — benchmark sweep2-models — comparison (3 experiments)

| experiment | model | chunk cfg | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bge-m3-baseline | bge-m3 | 1800/0.15/on | 267 | 30.0% | 65.9% | 75.7% | 0.490 | 62.5% | 89.5% | 92.5% | 0.746 | 0/3 | reuse / 2.7s |
| qwen3-embedding-06b | qwen3-embedding:0.6b | 1800/0.15/on | 267 | 29.8% | 62.2% | 74.2% | 0.483 | 59.9% | 88.8% | 93.6% | 0.722 | 0/3 | 93s / 5.4s |
| nomic-embed-v2-moe | nomic-embed-text-v2-moe | 1800/0.15/on | 267 | 33.0% | 65.7% | 78.3% | 0.508 | 63.3% | 88.4% | 95.1% | 0.745 | 0/3 | 30s / 2.1s |


## 2026-10-01T15:26:38+00:00 — benchmark method-comparison: baseline-embedding

store: `data/naive_store.json` — 2,850 chunks, bge-m3 (1024d), built 2026-09-30T08:58:30+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 30.0% | 65.9% | 75.7% | 0.490 | 62.5% | 89.5% | 92.5% | 0.746 |
| en | 169 | 32.5% | 70.4% | 76.3% | 0.506 | 68.0% | 90.5% | 93.5% | 0.777 |
| es | 98 | 25.5% | 58.2% | 74.5% | 0.462 | 53.1% | 87.8% | 90.8% | 0.691 |
| synthetic | 255 | 30.0% | 65.9% | 75.7% | 0.492 | 62.0% | 89.4% | 92.5% | 0.742 |
| manual | 12 | 29.2% | 66.7% | 75.0% | 0.445 | 75.0% | 91.7% | 91.7% | 0.826 |
| cross-language | 65 | 23.1% | 62.3% | 71.5% | 0.436 | 58.5% | 93.8% | 98.5% | 0.729 |
| same-language | 202 | 32.2% | 67.1% | 77.0% | 0.508 | 63.9% | 88.1% | 90.6% | 0.751 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5081, m014 0.5040, m015 0.4606)


## 2026-10-01T15:26:43+00:00 — benchmark method-comparison: baseline-bm25

store: `data/naive_store.json` — 2,850 chunks, bge-m3 (1024d), built 2026-09-30T08:58:30+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.6% | 55.2% | 62.2% | 0.451 | 54.7% | 75.3% | 79.4% | 0.640 |
| en | 169 | 30.2% | 54.7% | 61.2% | 0.437 | 53.8% | 71.6% | 75.7% | 0.623 |
| es | 98 | 34.2% | 56.1% | 63.8% | 0.476 | 56.1% | 81.6% | 85.7% | 0.671 |
| synthetic | 255 | 32.4% | 56.7% | 63.1% | 0.461 | 53.7% | 74.9% | 78.8% | 0.634 |
| manual | 12 | 16.7% | 25.0% | 41.7% | 0.231 | 75.0% | 83.3% | 91.7% | 0.781 |
| cross-language | 65 | 4.6% | 12.3% | 14.6% | 0.085 | 10.8% | 26.2% | 29.2% | 0.173 |
| same-language | 202 | 40.3% | 69.1% | 77.5% | 0.569 | 68.8% | 91.1% | 95.5% | 0.791 |

Unanswerable: 3 rows — false-retrieval not measured (the ranking method's top-1 score is not cosine-calibrated)
note: false-retrieval is cosine-specific — retrieval 'bm25' scores on a different scale, so comparison cells read —


## 2026-10-01T15:26:44+00:00 — benchmark method-comparison: baseline-rrf

store: `data/naive_store.json` — 2,850 chunks, bge-m3 (1024d), built 2026-09-30T08:58:30+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.5% | 60.9% | 71.5% | 0.487 | 58.1% | 85.4% | 95.1% | 0.705 |
| en | 169 | 31.4% | 63.9% | 70.4% | 0.489 | 59.8% | 84.0% | 95.3% | 0.710 |
| es | 98 | 31.6% | 55.6% | 73.5% | 0.483 | 55.1% | 87.8% | 94.9% | 0.695 |
| synthetic | 255 | 32.5% | 61.8% | 72.0% | 0.497 | 57.6% | 84.7% | 94.9% | 0.700 |
| manual | 12 | 8.3% | 41.7% | 62.5% | 0.281 | 66.7% | 100.0% | 100.0% | 0.799 |
| cross-language | 65 | 10.8% | 21.5% | 34.6% | 0.197 | 21.5% | 63.1% | 89.2% | 0.379 |
| same-language | 202 | 38.1% | 73.5% | 83.4% | 0.580 | 69.8% | 92.6% | 97.0% | 0.809 |

Unanswerable: 3 rows — false-retrieval not measured (the ranking method's top-1 score is not cosine-calibrated)
note: false-retrieval is cosine-specific — retrieval 'rrf' scores on a different scale, so comparison cells read —


## 2026-10-01T15:26:47+00:00 — benchmark method-comparison: merge-2400-embedding

store: `data/benchmark_stores/merge-2400.json` — 2,069 chunks, bge-m3 (1024d), built 2026-10-01T15:15:32+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 29.6% | 63.5% | 71.2% | 0.465 | 59.6% | 89.1% | 93.3% | 0.722 |
| en | 169 | 29.6% | 66.9% | 74.9% | 0.472 | 62.7% | 89.9% | 94.1% | 0.744 |
| es | 98 | 29.6% | 57.7% | 64.8% | 0.453 | 54.1% | 87.8% | 91.8% | 0.683 |
| synthetic | 255 | 29.8% | 64.1% | 72.2% | 0.469 | 58.8% | 89.0% | 92.9% | 0.717 |
| manual | 12 | 25.0% | 50.0% | 50.0% | 0.373 | 75.0% | 91.7% | 100.0% | 0.831 |
| cross-language | 65 | 25.4% | 66.2% | 73.8% | 0.448 | 53.8% | 93.8% | 98.5% | 0.694 |
| same-language | 202 | 30.9% | 62.6% | 70.3% | 0.470 | 61.4% | 87.6% | 91.6% | 0.731 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5167, m014 0.5154, m015 0.4686)


## 2026-10-01T15:26:49+00:00 — benchmark method-comparison: merge-2400-bm25

store: `data/benchmark_stores/merge-2400.json` — 2,069 chunks, bge-m3 (1024d), built 2026-10-01T15:15:32+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 26.8% | 56.6% | 64.8% | 0.416 | 49.8% | 76.0% | 79.8% | 0.612 |
| en | 169 | 27.8% | 56.2% | 63.6% | 0.423 | 51.5% | 72.8% | 76.3% | 0.610 |
| es | 98 | 25.0% | 57.1% | 66.8% | 0.404 | 46.9% | 81.6% | 85.7% | 0.614 |
| synthetic | 255 | 27.3% | 58.0% | 65.9% | 0.424 | 48.6% | 75.7% | 79.2% | 0.603 |
| manual | 12 | 16.7% | 25.0% | 41.7% | 0.243 | 75.0% | 83.3% | 91.7% | 0.804 |
| cross-language | 65 | 1.5% | 13.1% | 15.4% | 0.073 | 7.7% | 26.2% | 29.2% | 0.155 |
| same-language | 202 | 34.9% | 70.5% | 80.7% | 0.526 | 63.4% | 92.1% | 96.0% | 0.759 |

Unanswerable: 3 rows — false-retrieval not measured (the ranking method's top-1 score is not cosine-calibrated)
note: false-retrieval is cosine-specific — retrieval 'bm25' scores on a different scale, so comparison cells read —


## 2026-10-01T15:26:50+00:00 — benchmark method-comparison: merge-2400-rrf

store: `data/benchmark_stores/merge-2400.json` — 2,069 chunks, bge-m3 (1024d), built 2026-10-01T15:15:32+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 29.8% | 59.4% | 71.2% | 0.462 | 56.2% | 84.3% | 94.8% | 0.693 |
| en | 169 | 29.9% | 60.9% | 71.0% | 0.466 | 56.8% | 82.2% | 94.7% | 0.691 |
| es | 98 | 29.6% | 56.6% | 71.4% | 0.455 | 55.1% | 87.8% | 94.9% | 0.697 |
| synthetic | 255 | 30.8% | 61.0% | 72.2% | 0.475 | 55.7% | 83.5% | 94.5% | 0.689 |
| manual | 12 | 8.3% | 25.0% | 50.0% | 0.179 | 66.7% | 100.0% | 100.0% | 0.792 |
| cross-language | 65 | 8.5% | 22.3% | 36.9% | 0.184 | 18.5% | 56.9% | 87.7% | 0.361 |
| same-language | 202 | 36.6% | 71.3% | 82.2% | 0.552 | 68.3% | 93.1% | 97.0% | 0.800 |

Unanswerable: 3 rows — false-retrieval not measured (the ranking method's top-1 score is not cosine-calibrated)
note: false-retrieval is cosine-specific — retrieval 'rrf' scores on a different scale, so comparison cells read —


## 2026-10-01T15:26:53+00:00 — benchmark method-comparison: merge-1200-embedding

store: `data/benchmark_stores/merge-1200.json` — 4,488 chunks, bge-m3 (1024d), built 2026-10-01T15:14:47+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.4% | 62.8% | 73.5% | 0.479 | 62.9% | 91.8% | 93.6% | 0.751 |
| en | 169 | 32.8% | 64.2% | 73.4% | 0.484 | 68.0% | 92.9% | 93.5% | 0.782 |
| es | 98 | 28.9% | 60.4% | 73.8% | 0.470 | 54.1% | 89.8% | 93.9% | 0.698 |
| synthetic | 255 | 31.3% | 62.6% | 73.1% | 0.479 | 62.4% | 91.4% | 93.3% | 0.747 |
| manual | 12 | 33.3% | 66.7% | 83.3% | 0.476 | 75.0% | 100.0% | 100.0% | 0.833 |
| cross-language | 65 | 23.6% | 53.3% | 70.0% | 0.412 | 55.4% | 92.3% | 95.4% | 0.701 |
| same-language | 202 | 33.9% | 65.8% | 74.7% | 0.500 | 65.3% | 91.6% | 93.1% | 0.767 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5359, m014 0.5081, m015 0.4582)


## 2026-10-01T15:26:57+00:00 — benchmark method-comparison: merge-1200-bm25

store: `data/benchmark_stores/merge-1200.json` — 4,488 chunks, bge-m3 (1024d), built 2026-10-01T15:14:47+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 30.0% | 52.4% | 59.3% | 0.416 | 52.4% | 74.9% | 79.0% | 0.624 |
| en | 169 | 32.2% | 53.3% | 59.5% | 0.431 | 54.4% | 71.6% | 75.7% | 0.623 |
| es | 98 | 26.0% | 51.0% | 59.0% | 0.390 | 49.0% | 80.6% | 84.7% | 0.626 |
| synthetic | 255 | 30.6% | 53.7% | 60.5% | 0.426 | 51.4% | 74.1% | 78.4% | 0.616 |
| manual | 12 | 16.7% | 25.0% | 33.3% | 0.215 | 75.0% | 91.7% | 91.7% | 0.806 |
| cross-language | 65 | 3.1% | 10.8% | 15.4% | 0.069 | 9.2% | 26.2% | 30.8% | 0.161 |
| same-language | 202 | 38.6% | 65.8% | 73.4% | 0.528 | 66.3% | 90.6% | 94.6% | 0.773 |

Unanswerable: 3 rows — false-retrieval not measured (the ranking method's top-1 score is not cosine-calibrated)
note: false-retrieval is cosine-specific — retrieval 'bm25' scores on a different scale, so comparison cells read —


## 2026-10-01T15:26:59+00:00 — benchmark method-comparison: merge-1200-rrf

store: `data/benchmark_stores/merge-1200.json` — 4,488 chunks, bge-m3 (1024d), built 2026-10-01T15:14:47+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 32.0% | 59.9% | 72.1% | 0.475 | 58.8% | 86.9% | 95.5% | 0.718 |
| en | 169 | 35.2% | 61.5% | 71.9% | 0.494 | 61.5% | 84.6% | 95.9% | 0.725 |
| es | 98 | 26.5% | 57.1% | 72.4% | 0.441 | 54.1% | 90.8% | 94.9% | 0.706 |
| synthetic | 255 | 33.1% | 60.8% | 71.6% | 0.483 | 58.4% | 86.3% | 95.3% | 0.714 |
| manual | 12 | 8.3% | 41.7% | 83.3% | 0.291 | 66.7% | 100.0% | 100.0% | 0.806 |
| cross-language | 65 | 10.8% | 21.5% | 35.6% | 0.195 | 23.1% | 63.1% | 87.7% | 0.410 |
| same-language | 202 | 38.9% | 72.3% | 83.8% | 0.565 | 70.3% | 94.6% | 98.0% | 0.817 |

Unanswerable: 3 rows — false-retrieval not measured (the ranking method's top-1 score is not cosine-calibrated)
note: false-retrieval is cosine-specific — retrieval 'rrf' scores on a different scale, so comparison cells read —


## 2026-10-01T15:27:03+00:00 — benchmark method-comparison: noheader-embedding

store: `data/benchmark_stores/merge-1800-noheader.json` — 2,850 chunks, bge-m3 (1024d), built 2026-10-01T15:16:03+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header OFF

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.1% | 64.8% | 74.3% | 0.488 | 61.8% | 91.0% | 92.9% | 0.739 |
| en | 169 | 31.7% | 66.9% | 75.7% | 0.489 | 65.7% | 91.1% | 92.9% | 0.756 |
| es | 98 | 30.1% | 61.2% | 71.9% | 0.487 | 55.1% | 90.8% | 92.9% | 0.708 |
| synthetic | 255 | 31.6% | 64.9% | 74.3% | 0.492 | 61.2% | 91.0% | 92.5% | 0.734 |
| manual | 12 | 20.8% | 62.5% | 75.0% | 0.403 | 75.0% | 91.7% | 100.0% | 0.828 |
| cross-language | 65 | 23.1% | 57.7% | 70.8% | 0.417 | 55.4% | 92.3% | 96.9% | 0.693 |
| same-language | 202 | 33.7% | 67.1% | 75.5% | 0.511 | 63.9% | 90.6% | 91.6% | 0.753 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4983, m014 0.5066, m015 0.4675)


## 2026-10-01T15:27:06+00:00 — benchmark method-comparison: noheader-bm25

store: `data/benchmark_stores/merge-1800-noheader.json` — 2,850 chunks, bge-m3 (1024d), built 2026-10-01T15:16:03+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header OFF

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 30.5% | 54.7% | 60.1% | 0.445 | 53.6% | 74.9% | 78.3% | 0.631 |
| en | 169 | 28.4% | 54.4% | 60.4% | 0.428 | 52.1% | 72.8% | 76.3% | 0.616 |
| es | 98 | 34.2% | 55.1% | 59.7% | 0.474 | 56.1% | 78.6% | 81.6% | 0.658 |
| synthetic | 255 | 31.2% | 56.1% | 61.8% | 0.456 | 52.9% | 74.5% | 77.6% | 0.626 |
| manual | 12 | 16.7% | 25.0% | 25.0% | 0.205 | 66.7% | 83.3% | 91.7% | 0.747 |
| cross-language | 65 | 3.1% | 9.2% | 10.8% | 0.064 | 10.8% | 21.5% | 21.5% | 0.146 |
| same-language | 202 | 39.4% | 69.3% | 76.0% | 0.568 | 67.3% | 92.1% | 96.5% | 0.788 |

Unanswerable: 3 rows — false-retrieval not measured (the ranking method's top-1 score is not cosine-calibrated)
note: false-retrieval is cosine-specific — retrieval 'bm25' scores on a different scale, so comparison cells read —


## 2026-10-01T15:27:07+00:00 — benchmark method-comparison: noheader-rrf

store: `data/benchmark_stores/merge-1800-noheader.json` — 2,850 chunks, bge-m3 (1024d), built 2026-10-01T15:16:03+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header OFF

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 34.5% | 61.2% | 70.0% | 0.494 | 59.2% | 82.8% | 93.6% | 0.702 |
| en | 169 | 34.0% | 63.3% | 69.8% | 0.491 | 60.4% | 81.1% | 94.1% | 0.704 |
| es | 98 | 35.2% | 57.7% | 70.4% | 0.499 | 57.1% | 85.7% | 92.9% | 0.700 |
| synthetic | 255 | 35.7% | 62.5% | 70.8% | 0.506 | 58.8% | 82.0% | 93.3% | 0.698 |
| manual | 12 | 8.3% | 33.3% | 54.2% | 0.246 | 66.7% | 100.0% | 100.0% | 0.799 |
| cross-language | 65 | 10.8% | 21.5% | 25.4% | 0.181 | 18.5% | 43.1% | 83.1% | 0.335 |
| same-language | 202 | 42.1% | 74.0% | 84.4% | 0.595 | 72.3% | 95.5% | 97.0% | 0.821 |

Unanswerable: 3 rows — false-retrieval not measured (the ranking method's top-1 score is not cosine-calibrated)
note: false-retrieval is cosine-specific — retrieval 'rrf' scores on a different scale, so comparison cells read —


## 2026-10-01T15:27:10+00:00 — benchmark method-comparison: qwen3-06b-embedding

store: `data/benchmark_stores/qwen3-06b.json` — 2,850 chunks, qwen3-embedding:0.6b (1024d), built 2026-10-01T15:17:16+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 29.8% | 62.2% | 74.2% | 0.483 | 59.9% | 88.8% | 93.6% | 0.722 |
| en | 169 | 29.6% | 61.2% | 73.1% | 0.469 | 59.8% | 87.0% | 92.9% | 0.716 |
| es | 98 | 30.1% | 63.8% | 76.0% | 0.506 | 60.2% | 91.8% | 94.9% | 0.733 |
| synthetic | 255 | 30.6% | 62.4% | 74.5% | 0.489 | 59.6% | 88.2% | 93.3% | 0.718 |
| manual | 12 | 12.5% | 58.3% | 66.7% | 0.343 | 66.7% | 100.0% | 100.0% | 0.819 |
| cross-language | 65 | 32.3% | 63.8% | 73.1% | 0.502 | 58.5% | 92.3% | 96.9% | 0.720 |
| same-language | 202 | 29.0% | 61.6% | 74.5% | 0.477 | 60.4% | 87.6% | 92.6% | 0.723 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4671, m014 0.4360, m015 0.3119)


## 2026-10-01T15:27:14+00:00 — benchmark method-comparison: qwen3-06b-bm25

store: `data/benchmark_stores/qwen3-06b.json` — 2,850 chunks, qwen3-embedding:0.6b (1024d), built 2026-10-01T15:17:16+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.6% | 55.2% | 62.2% | 0.451 | 54.7% | 75.3% | 79.4% | 0.640 |
| en | 169 | 30.2% | 54.7% | 61.2% | 0.437 | 53.8% | 71.6% | 75.7% | 0.623 |
| es | 98 | 34.2% | 56.1% | 63.8% | 0.476 | 56.1% | 81.6% | 85.7% | 0.671 |
| synthetic | 255 | 32.4% | 56.7% | 63.1% | 0.461 | 53.7% | 74.9% | 78.8% | 0.634 |
| manual | 12 | 16.7% | 25.0% | 41.7% | 0.231 | 75.0% | 83.3% | 91.7% | 0.781 |
| cross-language | 65 | 4.6% | 12.3% | 14.6% | 0.085 | 10.8% | 26.2% | 29.2% | 0.173 |
| same-language | 202 | 40.3% | 69.1% | 77.5% | 0.569 | 68.8% | 91.1% | 95.5% | 0.791 |

Unanswerable: 3 rows — false-retrieval not measured (the ranking method's top-1 score is not cosine-calibrated)
note: false-retrieval is cosine-specific — retrieval 'bm25' scores on a different scale, so comparison cells read —


## 2026-10-01T15:27:15+00:00 — benchmark method-comparison: qwen3-06b-rrf

store: `data/benchmark_stores/qwen3-06b.json` — 2,850 chunks, qwen3-embedding:0.6b (1024d), built 2026-10-01T15:17:16+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 30.7% | 58.8% | 72.3% | 0.479 | 58.4% | 86.9% | 95.5% | 0.707 |
| en | 169 | 28.4% | 58.3% | 69.8% | 0.455 | 57.4% | 82.2% | 93.5% | 0.686 |
| es | 98 | 34.7% | 59.7% | 76.5% | 0.519 | 60.2% | 94.9% | 99.0% | 0.744 |
| synthetic | 255 | 31.4% | 60.0% | 72.7% | 0.487 | 57.3% | 86.3% | 95.3% | 0.698 |
| manual | 12 | 16.7% | 33.3% | 62.5% | 0.294 | 83.3% | 100.0% | 100.0% | 0.896 |
| cross-language | 65 | 10.8% | 24.6% | 36.2% | 0.211 | 23.1% | 63.1% | 90.8% | 0.394 |
| same-language | 202 | 37.1% | 69.8% | 83.9% | 0.565 | 69.8% | 94.6% | 97.0% | 0.808 |

Unanswerable: 3 rows — false-retrieval not measured (the ranking method's top-1 score is not cosine-calibrated)
note: false-retrieval is cosine-specific — retrieval 'rrf' scores on a different scale, so comparison cells read —


## 2026-10-01T15:27:19+00:00 — benchmark method-comparison: nomic-v2-moe-embedding

store: `data/benchmark_stores/nomic-v2-moe.json` — 2,850 chunks, nomic-embed-text-v2-moe (768d), built 2026-10-01T15:18:43+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 33.0% | 65.7% | 78.3% | 0.508 | 63.3% | 88.4% | 95.1% | 0.745 |
| en | 169 | 35.2% | 67.8% | 79.3% | 0.523 | 66.3% | 88.2% | 94.1% | 0.755 |
| es | 98 | 29.1% | 62.2% | 76.5% | 0.483 | 58.2% | 88.8% | 96.9% | 0.728 |
| synthetic | 255 | 33.9% | 65.9% | 78.4% | 0.515 | 62.7% | 88.2% | 95.3% | 0.741 |
| manual | 12 | 12.5% | 62.5% | 75.0% | 0.354 | 75.0% | 91.7% | 91.7% | 0.833 |
| cross-language | 65 | 30.0% | 62.3% | 76.9% | 0.475 | 60.0% | 89.2% | 96.9% | 0.714 |
| same-language | 202 | 33.9% | 66.8% | 78.7% | 0.519 | 64.4% | 88.1% | 94.6% | 0.755 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5017, m014 0.4497, m015 0.4142)


## 2026-10-01T15:27:22+00:00 — benchmark method-comparison: nomic-v2-moe-bm25

store: `data/benchmark_stores/nomic-v2-moe.json` — 2,850 chunks, nomic-embed-text-v2-moe (768d), built 2026-10-01T15:18:43+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.6% | 55.2% | 62.2% | 0.451 | 54.7% | 75.3% | 79.4% | 0.640 |
| en | 169 | 30.2% | 54.7% | 61.2% | 0.437 | 53.8% | 71.6% | 75.7% | 0.623 |
| es | 98 | 34.2% | 56.1% | 63.8% | 0.476 | 56.1% | 81.6% | 85.7% | 0.671 |
| synthetic | 255 | 32.4% | 56.7% | 63.1% | 0.461 | 53.7% | 74.9% | 78.8% | 0.634 |
| manual | 12 | 16.7% | 25.0% | 41.7% | 0.231 | 75.0% | 83.3% | 91.7% | 0.781 |
| cross-language | 65 | 4.6% | 12.3% | 14.6% | 0.085 | 10.8% | 26.2% | 29.2% | 0.173 |
| same-language | 202 | 40.3% | 69.1% | 77.5% | 0.569 | 68.8% | 91.1% | 95.5% | 0.791 |

Unanswerable: 3 rows — false-retrieval not measured (the ranking method's top-1 score is not cosine-calibrated)
note: false-retrieval is cosine-specific — retrieval 'bm25' scores on a different scale, so comparison cells read —


## 2026-10-01T15:27:23+00:00 — benchmark method-comparison: nomic-v2-moe-rrf

store: `data/benchmark_stores/nomic-v2-moe.json` — 2,850 chunks, nomic-embed-text-v2-moe (768d), built 2026-10-01T15:18:43+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 34.1% | 61.0% | 69.3% | 0.497 | 58.1% | 85.0% | 95.1% | 0.706 |
| en | 169 | 32.5% | 62.7% | 70.1% | 0.485 | 58.0% | 81.1% | 93.5% | 0.692 |
| es | 98 | 36.7% | 58.2% | 67.9% | 0.518 | 58.2% | 91.8% | 98.0% | 0.730 |
| synthetic | 255 | 35.3% | 62.0% | 70.0% | 0.509 | 56.9% | 84.7% | 95.3% | 0.698 |
| manual | 12 | 8.3% | 41.7% | 54.2% | 0.241 | 83.3% | 91.7% | 91.7% | 0.861 |
| cross-language | 65 | 10.8% | 23.8% | 35.4% | 0.204 | 23.1% | 55.4% | 86.2% | 0.385 |
| same-language | 202 | 41.6% | 73.0% | 80.2% | 0.592 | 69.3% | 94.6% | 98.0% | 0.809 |

Unanswerable: 3 rows — false-retrieval not measured (the ranking method's top-1 score is not cosine-calibrated)
note: false-retrieval is cosine-specific — retrieval 'rrf' scores on a different scale, so comparison cells read —


## 2026-10-01T15:27:26+00:00 — benchmark method-comparison — comparison (18 experiments)

| experiment | model | chunk cfg | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline-embedding | bge-m3 | 1800/0.15/on | 267 | 30.0% | 65.9% | 75.7% | 0.490 | 62.5% | 89.5% | 92.5% | 0.746 | 0/3 | reuse / 4.5s |
| baseline-bm25 | bge-m3 | 1800/0.15/on | 267 | 31.6% | 55.2% | 62.2% | 0.451 | 54.7% | 75.3% | 79.4% | 0.640 | — | reuse / 1.0s |
| baseline-rrf | bge-m3 | 1800/0.15/on | 267 | 31.5% | 60.9% | 71.5% | 0.487 | 58.1% | 85.4% | 95.1% | 0.705 | — | reuse / 3.4s |
| merge-2400-embedding | bge-m3 | 2400/0.15/on | 267 | 29.6% | 63.5% | 71.2% | 0.465 | 59.6% | 89.1% | 93.3% | 0.722 | 0/3 | reuse / 2.3s |
| merge-2400-bm25 | bge-m3 | 2400/0.15/on | 267 | 26.8% | 56.6% | 64.8% | 0.416 | 49.8% | 76.0% | 79.8% | 0.612 | — | reuse / 0.8s |
| merge-2400-rrf | bge-m3 | 2400/0.15/on | 267 | 29.8% | 59.4% | 71.2% | 0.462 | 56.2% | 84.3% | 94.8% | 0.693 | — | reuse / 2.9s |
| merge-1200-embedding | bge-m3 | 1200/0.15/on | 267 | 31.4% | 62.8% | 73.5% | 0.479 | 62.9% | 91.8% | 93.6% | 0.751 | 0/3 | reuse / 3.6s |
| merge-1200-bm25 | bge-m3 | 1200/0.15/on | 267 | 30.0% | 52.4% | 59.3% | 0.416 | 52.4% | 74.9% | 79.0% | 0.624 | — | reuse / 1.3s |
| merge-1200-rrf | bge-m3 | 1200/0.15/on | 267 | 32.0% | 59.9% | 72.1% | 0.475 | 58.8% | 86.9% | 95.5% | 0.718 | — | reuse / 4.4s |
| noheader-embedding | bge-m3 | 1800/0.15/off | 267 | 31.1% | 64.8% | 74.3% | 0.488 | 61.8% | 91.0% | 92.9% | 0.739 | 0/3 | reuse / 2.6s |
| noheader-bm25 | bge-m3 | 1800/0.15/off | 267 | 30.5% | 54.7% | 60.1% | 0.445 | 53.6% | 74.9% | 78.3% | 0.631 | — | reuse / 0.9s |
| noheader-rrf | bge-m3 | 1800/0.15/off | 267 | 34.5% | 61.2% | 70.0% | 0.494 | 59.2% | 82.8% | 93.6% | 0.702 | — | reuse / 3.1s |
| qwen3-06b-embedding | qwen3-embedding:0.6b | 1800/0.15/on | 267 | 29.8% | 62.2% | 74.2% | 0.483 | 59.9% | 88.8% | 93.6% | 0.722 | 0/3 | reuse / 3.7s |
| qwen3-06b-bm25 | qwen3-embedding:0.6b | 1800/0.15/on | 267 | 31.6% | 55.2% | 62.2% | 0.451 | 54.7% | 75.3% | 79.4% | 0.640 | — | reuse / 1.0s |
| qwen3-06b-rrf | qwen3-embedding:0.6b | 1800/0.15/on | 267 | 30.7% | 58.8% | 72.3% | 0.479 | 58.4% | 86.9% | 95.5% | 0.707 | — | reuse / 3.7s |
| nomic-v2-moe-embedding | nomic-embed-text-v2-moe | 1800/0.15/on | 267 | 33.0% | 65.7% | 78.3% | 0.508 | 63.3% | 88.4% | 95.1% | 0.745 | 0/3 | reuse / 3.3s |
| nomic-v2-moe-bm25 | nomic-embed-text-v2-moe | 1800/0.15/on | 267 | 31.6% | 55.2% | 62.2% | 0.451 | 54.7% | 75.3% | 79.4% | 0.640 | — | reuse / 0.9s |
| nomic-v2-moe-rrf | nomic-embed-text-v2-moe | 1800/0.15/on | 267 | 34.1% | 61.0% | 69.3% | 0.497 | 58.1% | 85.0% | 95.1% | 0.706 | — | reuse / 3.0s |

## 2026-10-01T15:29:26+00:00 — VERDICT — Step 4 defaults (evidence: the sweep + method blocks above)

Chunk config: **keep the merge chunker at 1800 chars / 0.15 overlap / header ON** (Step 2 constants stand).

- 2400 is strictly worse everywhere that matters (doc R@1 59.6% vs 62.5%, chunk MRR 0.465 vs 0.490) — bigger chunks dilute the target passage.
- 1200 is a wash: doc R@5 91.8% (+2.3) but chunk R@5 62.8% (−3.1) and chunk R@10 down; within self-echo tolerance, not a win. No reason to move a settled pipeline.
- no-header helps chunk R@1 (+1.1 pt) but costs doc R@1 (−0.7 pt) and manual chunk R@1 badly (29.2% → 20.8%) — the header rows m001/m011/m012 retrieve through the title. Header stays on.

Embedding model: **nomic-embed-text-v2-moe (768d) becomes the Step 4 default; bge-m3 stays the standby (stores kept, not deleted).**

- nomic wins the aggregate at chunk level (R@1 33.0% vs 30.0%, R@10 78.3% vs 75.7%, MRR 0.508 vs 0.490) and the depths citations care about (doc R@10 95.1% vs 92.5%).
- Cross-language (65 rows): chunk R@1 30.0% vs 23.1% (+6.9), doc R@10 96.9% vs 98.5% (~par); es scope doc R@1 58.2% vs 53.1%. The long-term roadmap is a global multilingual repository, so the CL/es edge compounds.
- Manual rows (12 hand-written): doc level is a tie (R@1 75.0% both, MRR 0.833 vs 0.826 — nomic slightly ahead); nomic loses chunk R@1 (12.5% vs 29.2%) while chunk R@5 (62.5% vs 66.7%) and R@10 (75.0% vs 75.0%) are near-level. The losing rows are the header/number probes — the exact queries the lexical arm fixes (see BM25 below). 12 rows is small; doc-level tie + chunk-level R@5/R@10 tie reads as acceptable.
- qwen3-embedding:0.6b drops (doc R@1 59.9% trails; only its es doc R@1 60.2% leads, and nomic already improved es).
- Unanswerable margins survive the model switch at the 0.55 threshold: nomic top-1 max 0.5017 (m013) vs bge 0.5081 — both cleanly separated from answerable top-1s. FALSE_RETRIEVAL_THRESHOLD stays 0.55; re-derive from data if future models join.

Retrieval method: **embedding-only for Step 4. BM25/RRF stay benchmarked, not shipped.**

- Pure BM25 does exactly what vectors can't — m002 (number probe) chunk rank 3 → 1, m001 (header-driven) 98 → 15, m011 24 → 3 — but it cannot cross languages (cross-language chunk R@5 12.3% vs embedding 62.3%; doc R@10 29.2% vs 96.9%) and it ejects paraphrase rows from the ranking (m004, m006 → rank 0). It is a repair arm, never the only arm, in a multilingual repository.
- RRF (unweighted, k=60) improves same-language retrieval meaningfully (chunk R@1 38.1% vs 32.2%, doc R@1 69.8% vs 63.9%, MRR 0.580 vs 0.508) but lets BM25's junk cross-language rankings poison good embedding rankings (cross-language chunk R@10 34.6% vs 71.5%, doc R@10 89.2% vs 98.5%). Fusion needs language-awareness before it ships: detect the query language or fuse the lexical arm only for same-language rows / at reduced weight. That is Step 5 work, where hybrid lands in the retrieval path properly; m002/m003's before/after (3→1, 1→1 at chunk rank) is the acceptance evidence recorded above.

Open chunker knobs (NOT implemented — awaiting explicit OK, evidence gathered):

- drop_footnotes: 2,696 footnote paragraphs, ~660k chars (~15% of corpus volume) — cheap to build, data invites it — but it changes the keepable-paragraph drop rule, and **36 of 267 answerable golden rows (13.5%) anchor footnote paragraphs**: those rows degrade to ungradable (or force golden re-anchoring decisions later). Needs a deliberate decision, not a knob flip.
- section-based chunking: 1,117 typed Section header paragraphs; 76/267 rows anchor at least one section-header paragraph, but a section chunker only re-grouping keepable paragraphs (drop rule unchanged) leaves every row gradeable via the paragraph_ids contract — safe to try later as a new pure strategy in the stores spec (`chunker = "section"`), once a real need shows up.

Corpus locality caveat: everything here is 77 IACHR-style reports from one instance with self-echo-biased questions (255 synthetic). Scores are relative (A vs B), never absolute; absolute recall will read lower on the full collection and, after Step 4's scale-up, chunking conclusions must be re-checked first (chunk geometry interacts with corpus mix). An external legal-RAG dataset (user-supplied, preferred over generic MIRACL) can still be added as a second opinion on the MODEL ranking only — never on chunking — and only if two models tie here (they do not: nomic leads on the shared corpus, bge leads on manual chunk R@1; the doc-level tie + CL edge broke it for nomic).

Step 4 inherits: chunker merge / 1800 / 0.15 / header on; model nomic-embed-text-v2-moe (EMBEDDING_DIMENSIONS → 768, .env); retrieval embedding-only; false-retrieval threshold 0.55 unchanged.
## 2026-10-02T12:33:59+00:00 — benchmark sweep2_models — resolved plan

plan    : sweep2_models — 3 experiment(s) over 3 store cell(s)
captures: data/raw/bdd5a7c445847b35 — 77 capture(s)
golden  : data/eval/golden.jsonl — 270 row(s)
stores  :
  baseline               merge 1800/0.15/on     × bge-m3                       → data/benchmark_stores/0ac7665e253e3e842a94cf8985283a95.json
  qwen3-06b              merge 1800/0.15/on     × qwen3-embedding:0.6b         → data/benchmark_stores/c5a3f43dfdc0418eb400325f3a2ace51.json
  nomic-v2-moe           merge 1800/0.15/on     × nomic-embed-text-v2-moe      → data/benchmark_stores/3b54e62444bbbe62672c466a4226a4e6.json
experiments:
  1. baseline-embedding           → baseline               retrieval embedding
  2. qwen3-06b-embedding          → qwen3-06b              retrieval embedding
  3. nomic-v2-moe-embedding       → nomic-v2-moe           retrieval embedding


## 2026-10-02T12:33:59+00:00 — benchmark sweep2_models: baseline-embedding

store: `data/benchmark_stores/0ac7665e253e3e842a94cf8985283a95.json` — 2,850 chunks, bge-m3 (1024d), built 2026-10-02T12:34:01+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 30.0% | 65.9% | 75.7% | 0.490 | 62.5% | 89.5% | 92.5% | 0.746 |
| en | 169 | 32.5% | 70.4% | 76.3% | 0.506 | 68.0% | 90.5% | 93.5% | 0.777 |
| es | 98 | 25.5% | 58.2% | 74.5% | 0.462 | 53.1% | 87.8% | 90.8% | 0.691 |
| synthetic | 255 | 30.0% | 65.9% | 75.7% | 0.492 | 62.0% | 89.4% | 92.5% | 0.742 |
| manual | 12 | 29.2% | 66.7% | 75.0% | 0.445 | 75.0% | 91.7% | 91.7% | 0.826 |
| cross-language | 65 | 23.1% | 62.3% | 71.5% | 0.436 | 58.5% | 93.8% | 98.5% | 0.729 |
| same-language | 202 | 32.2% | 67.1% | 77.0% | 0.508 | 63.9% | 88.1% | 90.6% | 0.751 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5081, m014 0.5040, m015 0.4606)
retrieval: embedding


## 2026-10-02T12:34:35+00:00 — benchmark sweep2_models: qwen3-06b-embedding

store: `data/benchmark_stores/c5a3f43dfdc0418eb400325f3a2ace51.json` — 2,850 chunks, qwen3-embedding:0.6b (1024d), built 2026-10-02T12:34:36+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 29.8% | 62.5% | 74.2% | 0.481 | 59.9% | 88.8% | 93.6% | 0.722 |
| en | 169 | 29.6% | 61.2% | 73.1% | 0.468 | 59.8% | 87.0% | 92.9% | 0.716 |
| es | 98 | 30.1% | 64.8% | 76.0% | 0.503 | 60.2% | 91.8% | 94.9% | 0.734 |
| synthetic | 255 | 30.6% | 62.7% | 74.5% | 0.487 | 59.6% | 88.2% | 93.3% | 0.718 |
| manual | 12 | 12.5% | 58.3% | 66.7% | 0.343 | 66.7% | 100.0% | 100.0% | 0.819 |
| cross-language | 65 | 32.3% | 63.8% | 73.1% | 0.496 | 58.5% | 92.3% | 96.9% | 0.720 |
| same-language | 202 | 29.0% | 62.1% | 74.5% | 0.476 | 60.4% | 87.6% | 92.6% | 0.723 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4671, m014 0.4364, m015 0.3122)
retrieval: embedding


## 2026-10-02T12:35:50+00:00 — benchmark sweep2_models: nomic-v2-moe-embedding

store: `data/benchmark_stores/3b54e62444bbbe62672c466a4226a4e6.json` — 2,850 chunks, nomic-embed-text-v2-moe (768d), built 2026-10-02T12:35:53+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 33.0% | 65.7% | 78.3% | 0.508 | 63.3% | 88.4% | 95.1% | 0.745 |
| en | 169 | 35.2% | 67.8% | 79.3% | 0.523 | 66.3% | 88.2% | 94.1% | 0.755 |
| es | 98 | 29.1% | 62.2% | 76.5% | 0.483 | 58.2% | 88.8% | 96.9% | 0.728 |
| synthetic | 255 | 33.9% | 65.9% | 78.4% | 0.515 | 62.7% | 88.2% | 95.3% | 0.741 |
| manual | 12 | 12.5% | 62.5% | 75.0% | 0.354 | 75.0% | 91.7% | 91.7% | 0.833 |
| cross-language | 65 | 30.0% | 62.3% | 76.9% | 0.475 | 60.0% | 89.2% | 96.9% | 0.714 |
| same-language | 202 | 33.9% | 66.8% | 78.7% | 0.519 | 64.4% | 88.1% | 94.6% | 0.755 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5017, m014 0.4497, m015 0.4142)
retrieval: embedding


## 2026-10-02T12:36:17+00:00 — benchmark sweep2_models — comparison (3 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline-embedding | bge-m3 | 1800/0.15/on | embedding | 267 | 30.0% | 65.9% | 75.7% | 0.490 | 62.5% | 89.5% | 92.5% | 0.746 | 0/3 | 31s / 2.8s |
| qwen3-06b-embedding | qwen3-embedding:0.6b | 1800/0.15/on | embedding | 267 | 29.8% | 62.5% | 74.2% | 0.481 | 59.9% | 88.8% | 93.6% | 0.722 | 0/3 | 71s / 2.9s |
| nomic-v2-moe-embedding | nomic-embed-text-v2-moe | 1800/0.15/on | embedding | 267 | 33.0% | 65.7% | 78.3% | 0.508 | 63.3% | 88.4% | 95.1% | 0.745 | 0/3 | 22s / 2.2s |


## 2026-10-02T12:36:49+00:00 — benchmark sweep2_models — resolved plan

plan    : sweep2_models — 1 experiment(s) over 1 store cell(s)
captures: data/raw/bdd5a7c445847b35 — 77 capture(s)
golden  : data/eval/golden.jsonl — 270 row(s)
stores  :
  qwen3-06b              merge 1800/0.15/on     × qwen3-embedding:0.6b         → data/benchmark_stores/c5a3f43dfdc0418eb400325f3a2ace51.json
experiments:
  1. qwen3-06b-embedding          → qwen3-06b              retrieval embedding


## 2026-10-02T12:36:49+00:00 — benchmark sweep2_models: qwen3-06b-embedding

store: `data/benchmark_stores/c5a3f43dfdc0418eb400325f3a2ace51.json` — 2,850 chunks, qwen3-embedding:0.6b (1024d), built 2026-10-02T12:36:49+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 29.8% | 62.2% | 74.2% | 0.482 | 59.9% | 89.1% | 94.0% | 0.722 |
| en | 169 | 29.6% | 61.2% | 73.1% | 0.469 | 59.8% | 87.6% | 92.9% | 0.716 |
| es | 98 | 30.1% | 63.8% | 76.0% | 0.505 | 60.2% | 91.8% | 95.9% | 0.733 |
| synthetic | 255 | 30.6% | 62.4% | 74.5% | 0.489 | 59.6% | 88.6% | 93.7% | 0.718 |
| manual | 12 | 12.5% | 58.3% | 66.7% | 0.344 | 66.7% | 100.0% | 100.0% | 0.819 |
| cross-language | 65 | 32.3% | 63.8% | 73.1% | 0.500 | 58.5% | 92.3% | 96.9% | 0.721 |
| same-language | 202 | 29.0% | 61.6% | 74.5% | 0.477 | 60.4% | 88.1% | 93.1% | 0.723 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4671, m014 0.4364, m015 0.3119)
retrieval: embedding


## 2026-10-02T12:38:03+00:00 — benchmark sweep2_models — comparison (1 experiment)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen3-06b-embedding | qwen3-embedding:0.6b | 1800/0.15/on | embedding | 267 | 29.8% | 62.2% | 74.2% | 0.482 | 59.9% | 89.1% | 94.0% | 0.722 | 0/3 | 70s / 2.9s |


## 2026-10-02T12:38:03+00:00 — Step 3.5 migration parity: sweep 2 re-run through the rewritten config layer

Acceptance re-run for the benchmark redesign (TOML sweep specs → method packages + `use_cases/run_sweep.py`,
user-approved): `uwazi-rag benchmark --spec benchmarks/sweep2_models.py`. Grid = 3 store cells (MergeChunker
at the Step 2 geometry, one per model) × EmbeddingRetrieval; stores rebuilt under content-derived fingerprints
(`data/benchmark_stores/<sha256[:32]>.json`; the committed `data/naive_store.json` was not reused — the bge-m3
cell rebuilt it from the same corpus). The shared grading path is untouched
(`prepare_run` byte-verify + `rank_rows` + `score_rows`); per-experiment blocks above carry the resolved plan.

- bge-m3: EXACT — every scope cell and all unanswerable top-1s equal the recorded 2026-10-01 block, across a
  store built 2026-09-30 vs rebuilt 2026-10-02. The rewritten layer reproduces bit-stable pipelines exactly.
- nomic-embed-text-v2-moe: EXACT (all scopes + top-1s 0.5017/0.4497/0.4142).
- qwen3-embedding:0.6b: near-tie drift only — top-1 scores move ±0.0004 (e.g. m014 0.4360/0.4364), flipping
  1–2 rows near rank 5–10: chunk R@5 62.2%↔62.5%, chunk MRR 0.481–0.483, doc R@5/R@10 ±0.4pp; R@1, R@10-level
  all-scope structure and doc MRR stable. Two fresh builds through the NEW runner differ from each other the
  same way, so this is Ollama's qwen3 embeds not being bit-identical across store builds (bge-m3/nomic are) —
  not a migration artifact; the old runner's builds carried the same property.

Recorded sweep numbers remain final (append-only; nothing above rewritten). Recorded VERDICTS unchanged:
nomic-embed-text-v2-moe leads with ~3pp margins vs ~4e-4 rebuild noise; bge-m3 standby; embedding-only for
Step 4; FALSE_RETRIEVAL_THRESHOLD 0.55.

## 2026-10-02T15:56:07+00:00 — benchmark sweep2_models — resolved plan

plan    : sweep2_models — 5 experiment(s) over 5 store cell(s)
captures: data/raw/bdd5a7c445847b35 — 77 capture(s)
golden  : data/eval/golden.jsonl — 270 row(s)
stores  :
  baseline               merge 1800/0.15/on     × bge-m3                       → data/benchmark_stores/0ac7665e253e3e842a94cf8985283a95.json
  qwen3-06b              merge 1800/0.15/on     × qwen3-embedding:0.6b         → data/benchmark_stores/c5a3f43dfdc0418eb400325f3a2ace51.json
  nomic-v2-moe           merge 1800/0.15/on     × nomic-embed-text-v2-moe      → data/benchmark_stores/3b54e62444bbbe62672c466a4226a4e6.json
  qwen3-8b               merge 1800/0.15/on     × qwen3-embedding:8b           → data/benchmark_stores/ae9f2e8585ffd72012a4f800fa0fc08f.json
  embeddinggemma         merge 1800/0.15/on     × embeddinggemma               → data/benchmark_stores/e5f634b561e4684981ebbc88c4c5b173.json
experiments:
  1. baseline-embedding           → baseline               retrieval embedding
  2. qwen3-06b-embedding          → qwen3-06b              retrieval embedding
  3. nomic-v2-moe-embedding       → nomic-v2-moe           retrieval embedding
  4. qwen3-8b-embedding           → qwen3-8b               retrieval embedding
  5. embeddinggemma-embedding     → embeddinggemma         retrieval embedding


## 2026-10-02T15:56:07+00:00 — benchmark sweep2_models: baseline-embedding

store: `data/benchmark_stores/0ac7665e253e3e842a94cf8985283a95.json` — 2,850 chunks, bge-m3 (1024d), built 2026-10-02T12:34:01+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 30.0% | 65.9% | 75.7% | 0.490 | 62.5% | 89.5% | 92.5% | 0.746 |
| en | 169 | 32.5% | 70.4% | 76.3% | 0.506 | 68.0% | 90.5% | 93.5% | 0.777 |
| es | 98 | 25.5% | 58.2% | 74.5% | 0.462 | 53.1% | 87.8% | 90.8% | 0.691 |
| synthetic | 255 | 30.0% | 65.9% | 75.7% | 0.492 | 62.0% | 89.4% | 92.5% | 0.742 |
| manual | 12 | 29.2% | 66.7% | 75.0% | 0.445 | 75.0% | 91.7% | 91.7% | 0.826 |
| cross-language | 65 | 23.1% | 62.3% | 71.5% | 0.436 | 58.5% | 93.8% | 98.5% | 0.729 |
| same-language | 202 | 32.2% | 67.1% | 77.0% | 0.508 | 63.9% | 88.1% | 90.6% | 0.751 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5081, m014 0.5040, m015 0.4606)
retrieval: embedding


## 2026-10-02T15:56:12+00:00 — benchmark sweep2_models: qwen3-06b-embedding

store: `data/benchmark_stores/c5a3f43dfdc0418eb400325f3a2ace51.json` — 2,850 chunks, qwen3-embedding:0.6b (1024d), built 2026-10-02T12:36:49+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 29.8% | 62.2% | 74.2% | 0.482 | 59.9% | 89.1% | 94.0% | 0.722 |
| en | 169 | 29.6% | 61.2% | 73.1% | 0.469 | 59.8% | 87.6% | 92.9% | 0.716 |
| es | 98 | 30.1% | 63.8% | 76.0% | 0.505 | 60.2% | 91.8% | 95.9% | 0.733 |
| synthetic | 255 | 30.6% | 62.4% | 74.5% | 0.489 | 59.6% | 88.6% | 93.7% | 0.718 |
| manual | 12 | 12.5% | 58.3% | 66.7% | 0.344 | 66.7% | 100.0% | 100.0% | 0.819 |
| cross-language | 65 | 32.3% | 63.8% | 73.1% | 0.500 | 58.5% | 92.3% | 96.9% | 0.721 |
| same-language | 202 | 29.0% | 61.6% | 74.5% | 0.477 | 60.4% | 88.1% | 93.1% | 0.723 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4671, m014 0.4364, m015 0.3119)
retrieval: embedding


## 2026-10-02T15:56:15+00:00 — benchmark sweep2_models: nomic-v2-moe-embedding

store: `data/benchmark_stores/3b54e62444bbbe62672c466a4226a4e6.json` — 2,850 chunks, nomic-embed-text-v2-moe (768d), built 2026-10-02T12:35:53+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 33.0% | 65.7% | 78.3% | 0.508 | 63.3% | 88.4% | 95.1% | 0.745 |
| en | 169 | 35.2% | 67.8% | 79.3% | 0.523 | 66.3% | 88.2% | 94.1% | 0.755 |
| es | 98 | 29.1% | 62.2% | 76.5% | 0.483 | 58.2% | 88.8% | 96.9% | 0.728 |
| synthetic | 255 | 33.9% | 65.9% | 78.4% | 0.515 | 62.7% | 88.2% | 95.3% | 0.741 |
| manual | 12 | 12.5% | 62.5% | 75.0% | 0.354 | 75.0% | 91.7% | 91.7% | 0.833 |
| cross-language | 65 | 30.0% | 62.3% | 76.9% | 0.475 | 60.0% | 89.2% | 96.9% | 0.714 |
| same-language | 202 | 33.9% | 66.8% | 78.7% | 0.519 | 64.4% | 88.1% | 94.6% | 0.755 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5017, m014 0.4497, m015 0.4142)
retrieval: embedding


## 2026-10-02T15:56:19+00:00 — benchmark sweep2_models: qwen3-8b-embedding

store: `data/benchmark_stores/ae9f2e8585ffd72012a4f800fa0fc08f.json` — 2,850 chunks, qwen3-embedding:8b (4096d), built 2026-10-02T15:56:38+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 30.7% | 66.5% | 82.0% | 0.509 | 65.9% | 94.4% | 97.4% | 0.781 |
| en | 169 | 31.7% | 68.6% | 80.5% | 0.509 | 70.4% | 93.5% | 96.4% | 0.800 |
| es | 98 | 29.1% | 62.8% | 84.7% | 0.511 | 58.2% | 95.9% | 99.0% | 0.749 |
| synthetic | 255 | 31.2% | 67.3% | 82.4% | 0.515 | 65.9% | 94.1% | 97.3% | 0.780 |
| manual | 12 | 20.8% | 50.0% | 75.0% | 0.396 | 66.7% | 100.0% | 100.0% | 0.808 |
| cross-language | 65 | 24.6% | 66.9% | 78.5% | 0.463 | 56.9% | 96.9% | 98.5% | 0.732 |
| same-language | 202 | 32.7% | 66.3% | 83.2% | 0.524 | 68.8% | 93.6% | 97.0% | 0.797 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 1/3 (33.3%) (top-1: m013 0.5866, m014 0.5389, m015 0.4367)
retrieval: embedding


## 2026-10-02T16:00:59+00:00 — benchmark sweep2_models: embeddinggemma-embedding

store: `data/benchmark_stores/e5f634b561e4684981ebbc88c4c5b173.json` — 2,850 chunks, embeddinggemma (768d), built 2026-10-02T16:01:06+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |
|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 35.0% | 69.1% | 80.3% | 0.541 | 65.5% | 93.3% | 97.0% | 0.774 |
| en | 169 | 35.5% | 69.8% | 77.8% | 0.541 | 68.0% | 90.5% | 95.9% | 0.782 |
| es | 98 | 34.2% | 67.9% | 84.7% | 0.542 | 61.2% | 98.0% | 99.0% | 0.761 |
| synthetic | 255 | 35.3% | 69.8% | 80.2% | 0.544 | 64.7% | 92.9% | 96.9% | 0.767 |
| manual | 12 | 29.2% | 54.2% | 83.3% | 0.477 | 83.3% | 100.0% | 100.0% | 0.917 |
| cross-language | 65 | 23.8% | 63.8% | 80.0% | 0.450 | 53.8% | 92.3% | 98.5% | 0.699 |
| same-language | 202 | 38.6% | 70.8% | 80.4% | 0.570 | 69.3% | 93.6% | 96.5% | 0.798 |

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4635, m014 0.4292, m015 0.3883)
retrieval: embedding


p1 p2 p3

p1-p2 , p3


## 2026-10-02T16:01:34+00:00 — benchmark sweep2_models — comparison (5 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline-embedding | bge-m3 | 1800/0.15/on | embedding | 267 | 30.0% | 65.9% | 75.7% | 0.490 | 62.5% | 89.5% | 92.5% | 0.746 | 0/3 | reuse / 4.2s |
| qwen3-06b-embedding | qwen3-embedding:0.6b | 1800/0.15/on | embedding | 267 | 29.8% | 62.2% | 74.2% | 0.482 | 59.9% | 89.1% | 94.0% | 0.722 | 0/3 | reuse / 3.3s |
| nomic-v2-moe-embedding | nomic-embed-text-v2-moe | 1800/0.15/on | embedding | 267 | 33.0% | 65.7% | 78.3% | 0.508 | 63.3% | 88.4% | 95.1% | 0.745 | 0/3 | reuse / 3.0s |
| qwen3-8b-embedding | qwen3-embedding:8b | 1800/0.15/on | embedding | 267 | 30.7% | 66.5% | 82.0% | 0.509 | 65.9% | 94.4% | 97.4% | 0.781 | 1/3 | 247s / 12.5s |
| embeddinggemma-embedding | embeddinggemma | 1800/0.15/on | embedding | 267 | 35.0% | 69.1% | 80.3% | 0.541 | 65.5% | 93.3% | 97.0% | 0.774 | 0/3 | 25s / 3.1s |

1 / rank of the first golden chunk

## 2026-10-05T11:48:35+00:00 — benchmark sweep2_models — resolved plan

plan    : sweep2_models — 5 experiment(s) over 5 store cell(s)
captures: data/raw/bdd5a7c445847b35 — 77 capture(s)
golden  : data/eval/golden.jsonl — 270 row(s)
stores  :
  baseline               merge 1800/0.15/on     × bge-m3                       → data/benchmark_stores/merge-1800-0.15-on__bge-m3-4d284af0.json
  qwen3-06b              merge 1800/0.15/on     × qwen3-embedding:0.6b         → data/benchmark_stores/merge-1800-0.15-on__qwen3-embedding-0.6b-4d284af0.json
  nomic-v2-moe           merge 1800/0.15/on     × nomic-embed-text-v2-moe      → data/benchmark_stores/merge-1800-0.15-on__nomic-embed-text-v2-moe-4d284af0.json
  qwen3-8b               merge 1800/0.15/on     × qwen3-embedding:8b           → data/benchmark_stores/merge-1800-0.15-on__qwen3-embedding-8b-4d284af0.json
  embeddinggemma         merge 1800/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-1800-0.15-on__embeddinggemma-4d284af0.json
experiments:
  1. baseline-embedding           → baseline               retrieval embedding
  2. qwen3-06b-embedding          → qwen3-06b              retrieval embedding
  3. nomic-v2-moe-embedding       → nomic-v2-moe           retrieval embedding
  4. qwen3-8b-embedding           → qwen3-8b               retrieval embedding
  5. embeddinggemma-embedding     → embeddinggemma         retrieval embedding


## 2026-10-05T11:48:35+00:00 — benchmark sweep2_models: baseline-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__bge-m3-4d284af0.json` — 2,850 chunks, bge-m3 (1024d), built 2026-10-05T11:48:37+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 30.0% | 65.9% | 75.7% | 0.490 | 62.5% | 89.5% | 92.5% | 0.746 | 30.8% | 67.9% | 77.4% | 36.1% | 33.0% | 14.9% | 8.7% | 32.0% |
| en | 169 | 32.5% | 70.4% | 76.3% | 0.506 | 68.0% | 90.5% | 93.5% | 0.777 | 33.0% | 71.8% | 77.5% | 38.5% | 34.9% | 15.6% | 8.5% | 34.3% |
| es | 98 | 25.5% | 58.2% | 74.5% | 0.462 | 53.1% | 87.8% | 90.8% | 0.691 | 26.9% | 61.3% | 77.4% | 31.8% | 29.6% | 13.7% | 8.9% | 28.1% |
| synthetic | 255 | 30.0% | 65.9% | 75.7% | 0.492 | 62.0% | 89.4% | 92.5% | 0.742 | 30.9% | 68.0% | 77.6% | 36.4% | 32.9% | 14.9% | 8.7% | 32.2% |
| manual | 12 | 29.2% | 66.7% | 75.0% | 0.445 | 75.0% | 91.7% | 91.7% | 0.826 | 29.2% | 66.7% | 75.0% | 29.2% | 33.3% | 15.0% | 8.3% | 29.2% |
| cross-language | 65 | 23.1% | 62.3% | 71.5% | 0.436 | 58.5% | 93.8% | 98.5% | 0.729 | 24.7% | 65.6% | 74.1% | 27.9% | 26.2% | 14.2% | 8.3% | 24.6% |
| same-language | 202 | 32.2% | 67.1% | 77.0% | 0.508 | 63.9% | 88.1% | 90.6% | 0.751 | 32.7% | 68.7% | 78.5% | 38.7% | 35.1% | 15.1% | 8.8% | 34.4% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5081, m014 0.5040, m015 0.4606)
retrieval: embedding


## 2026-10-05T11:49:09+00:00 — benchmark sweep2_models: qwen3-06b-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__qwen3-embedding-0.6b-4d284af0.json` — 2,850 chunks, qwen3-embedding:0.6b (1024d), built 2026-10-05T11:49:10+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 29.8% | 62.5% | 74.2% | 0.482 | 60.3% | 88.8% | 93.6% | 0.725 | 30.9% | 64.3% | 76.0% | 35.2% | 33.3% | 14.3% | 8.5% | 31.6% |
| en | 169 | 29.6% | 61.2% | 73.1% | 0.470 | 60.4% | 87.0% | 92.9% | 0.720 | 30.5% | 62.5% | 74.2% | 36.3% | 32.0% | 13.6% | 8.1% | 30.8% |
| es | 98 | 30.1% | 64.8% | 76.0% | 0.504 | 60.2% | 91.8% | 94.9% | 0.734 | 31.6% | 67.3% | 78.9% | 33.4% | 35.7% | 15.5% | 9.1% | 33.2% |
| synthetic | 255 | 30.6% | 62.7% | 74.5% | 0.489 | 60.0% | 88.2% | 93.3% | 0.720 | 31.8% | 64.6% | 76.4% | 35.9% | 34.1% | 14.4% | 8.5% | 32.5% |
| manual | 12 | 12.5% | 58.3% | 66.7% | 0.351 | 66.7% | 100.0% | 100.0% | 0.819 | 12.5% | 58.3% | 66.7% | 20.8% | 16.7% | 13.3% | 7.5% | 12.5% |
| cross-language | 65 | 32.3% | 63.8% | 73.1% | 0.499 | 58.5% | 92.3% | 96.9% | 0.721 | 34.5% | 66.4% | 75.6% | 39.2% | 36.9% | 14.8% | 8.3% | 35.4% |
| same-language | 202 | 29.0% | 62.1% | 74.5% | 0.477 | 60.9% | 87.6% | 92.6% | 0.726 | 29.7% | 63.6% | 76.1% | 33.9% | 32.2% | 14.2% | 8.5% | 30.4% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4643, m014 0.4360, m015 0.3122)
retrieval: embedding


## 2026-10-05T11:50:23+00:00 — benchmark sweep2_models: nomic-v2-moe-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__nomic-embed-text-v2-moe-4d284af0.json` — 2,850 chunks, nomic-embed-text-v2-moe (768d), built 2026-10-05T11:50:25+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 33.0% | 65.7% | 78.3% | 0.508 | 63.3% | 88.4% | 95.1% | 0.745 | 33.7% | 67.4% | 79.6% | 38.9% | 36.3% | 15.0% | 9.0% | 34.6% |
| en | 169 | 35.2% | 67.8% | 79.3% | 0.523 | 66.3% | 88.2% | 94.1% | 0.755 | 36.0% | 69.1% | 80.3% | 41.1% | 37.9% | 14.9% | 8.9% | 37.0% |
| es | 98 | 29.1% | 62.2% | 76.5% | 0.483 | 58.2% | 88.8% | 96.9% | 0.728 | 29.8% | 64.6% | 78.6% | 34.9% | 33.7% | 15.1% | 9.3% | 30.6% |
| synthetic | 255 | 33.9% | 65.9% | 78.4% | 0.515 | 62.7% | 88.2% | 95.3% | 0.741 | 34.7% | 67.7% | 79.9% | 40.1% | 37.3% | 15.1% | 9.1% | 35.7% |
| manual | 12 | 12.5% | 62.5% | 75.0% | 0.354 | 75.0% | 91.7% | 91.7% | 0.833 | 12.5% | 62.5% | 75.0% | 12.5% | 16.7% | 13.3% | 8.3% | 12.5% |
| cross-language | 65 | 30.0% | 62.3% | 76.9% | 0.475 | 60.0% | 89.2% | 96.9% | 0.714 | 30.8% | 65.4% | 79.2% | 31.8% | 33.8% | 14.8% | 8.9% | 31.5% |
| same-language | 202 | 33.9% | 66.8% | 78.7% | 0.519 | 64.4% | 88.1% | 94.6% | 0.755 | 34.7% | 68.1% | 79.8% | 41.1% | 37.1% | 15.0% | 9.1% | 35.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5017, m014 0.4497, m015 0.4142)
retrieval: embedding


## 2026-10-05T11:50:49+00:00 — benchmark sweep2_models: qwen3-8b-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__qwen3-embedding-8b-4d284af0.json` — 2,850 chunks, qwen3-embedding:8b (4096d), built 2026-10-05T11:50:58+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.6% | 66.7% | 81.6% | 0.514 | 66.3% | 94.0% | 97.4% | 0.783 | 32.8% | 68.2% | 82.7% | 38.8% | 35.2% | 15.1% | 9.3% | 33.0% |
| en | 169 | 33.4% | 69.2% | 80.5% | 0.519 | 71.0% | 92.9% | 96.4% | 0.804 | 34.2% | 70.3% | 81.1% | 40.8% | 36.1% | 15.3% | 9.0% | 34.3% |
| es | 98 | 28.6% | 62.2% | 83.7% | 0.506 | 58.2% | 95.9% | 99.0% | 0.748 | 30.3% | 64.7% | 85.4% | 35.4% | 33.7% | 14.7% | 9.9% | 30.6% |
| synthetic | 255 | 32.2% | 67.5% | 82.0% | 0.520 | 66.3% | 93.7% | 97.3% | 0.782 | 33.3% | 69.1% | 83.0% | 39.7% | 35.7% | 15.2% | 9.4% | 33.5% |
| manual | 12 | 20.8% | 50.0% | 75.0% | 0.396 | 66.7% | 100.0% | 100.0% | 0.808 | 20.8% | 50.0% | 75.0% | 20.8% | 25.0% | 11.7% | 8.3% | 20.8% |
| cross-language | 65 | 26.2% | 66.9% | 78.5% | 0.471 | 56.9% | 96.9% | 98.5% | 0.731 | 27.8% | 69.5% | 80.3% | 33.5% | 29.2% | 15.7% | 9.1% | 27.7% |
| same-language | 202 | 33.4% | 66.6% | 82.7% | 0.528 | 69.3% | 93.1% | 97.0% | 0.800 | 34.4% | 67.8% | 83.4% | 40.6% | 37.1% | 14.9% | 9.4% | 34.7% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 1/3 (33.3%) (top-1: m013 0.5858, m014 0.5389, m015 0.4367)
retrieval: embedding


## 2026-10-05T11:55:43+00:00 — benchmark sweep2_models: embeddinggemma-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__embeddinggemma-4d284af0.json` — 2,850 chunks, embeddinggemma (768d), built 2026-10-05T11:55:44+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 35.0% | 69.1% | 80.3% | 0.541 | 65.5% | 93.3% | 97.0% | 0.774 | 36.1% | 70.7% | 81.9% | 40.7% | 39.0% | 15.4% | 9.1% | 36.7% |
| en | 169 | 35.5% | 69.8% | 77.8% | 0.541 | 68.0% | 90.5% | 95.9% | 0.782 | 36.5% | 71.1% | 78.8% | 42.5% | 39.1% | 15.3% | 8.6% | 36.7% |
| es | 98 | 34.2% | 67.9% | 84.7% | 0.542 | 61.2% | 98.0% | 99.0% | 0.761 | 35.4% | 70.0% | 87.3% | 37.7% | 38.8% | 15.7% | 9.9% | 36.7% |
| synthetic | 255 | 35.3% | 69.8% | 80.2% | 0.544 | 64.7% | 92.9% | 96.9% | 0.767 | 36.4% | 71.4% | 81.8% | 41.3% | 39.2% | 15.6% | 9.1% | 37.1% |
| manual | 12 | 29.2% | 54.2% | 83.3% | 0.477 | 83.3% | 100.0% | 100.0% | 0.917 | 29.2% | 54.2% | 83.3% | 29.2% | 33.3% | 11.7% | 9.2% | 29.2% |
| cross-language | 65 | 23.8% | 63.8% | 80.0% | 0.450 | 53.8% | 92.3% | 98.5% | 0.699 | 25.3% | 65.9% | 82.8% | 31.3% | 27.7% | 14.5% | 9.1% | 26.9% |
| same-language | 202 | 38.6% | 70.8% | 80.4% | 0.570 | 69.3% | 93.6% | 96.5% | 0.798 | 39.6% | 72.2% | 81.6% | 43.8% | 42.6% | 15.7% | 9.1% | 39.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4635, m014 0.4292, m015 0.3883)
retrieval: embedding


## 2026-10-05T11:56:15+00:00 — benchmark sweep2_models — comparison (5 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline-embedding | bge-m3 | 1800/0.15/on | embedding | 267 | 30.0% | 65.9% | 75.7% | 0.490 | 62.5% | 89.5% | 92.5% | 0.746 | 30.8% | 67.9% | 77.4% | 36.1% | 33.0% | 14.9% | 8.7% | 32.0% | 0/3 | 29s / 2.9s |
| qwen3-06b-embedding | qwen3-embedding:0.6b | 1800/0.15/on | embedding | 267 | 29.8% | 62.5% | 74.2% | 0.482 | 60.3% | 88.8% | 93.6% | 0.725 | 30.9% | 64.3% | 76.0% | 35.2% | 33.3% | 14.3% | 8.5% | 31.6% | 0/3 | 70s / 3.0s |
| nomic-v2-moe-embedding | nomic-embed-text-v2-moe | 1800/0.15/on | embedding | 267 | 33.0% | 65.7% | 78.3% | 0.508 | 63.3% | 88.4% | 95.1% | 0.745 | 33.7% | 67.4% | 79.6% | 38.9% | 36.3% | 15.0% | 9.0% | 34.6% | 0/3 | 22s / 2.0s |
| qwen3-8b-embedding | qwen3-embedding:8b | 1800/0.15/on | embedding | 267 | 31.6% | 66.7% | 81.6% | 0.514 | 66.3% | 94.0% | 97.4% | 0.783 | 32.8% | 68.2% | 82.7% | 38.8% | 35.2% | 15.1% | 9.3% | 33.0% | 1/3 | 273s / 10.1s |
| embeddinggemma-embedding | embeddinggemma | 1800/0.15/on | embedding | 267 | 35.0% | 69.1% | 80.3% | 0.541 | 65.5% | 93.3% | 97.0% | 0.774 | 36.1% | 70.7% | 81.9% | 40.7% | 39.0% | 15.4% | 9.1% | 36.7% | 0/3 | 28s / 2.2s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes

## 2026-10-05T11:56:15+00:00 — Step 3.6 scorecard-honesty parity: fresh sweep re-run through the new runner under readable store names

Acceptance re-run for the Step 3.6 upgrade (user-approved: cov@k / cov@3000 / P@k / RP added above; readable store names
`<method-slug(params)>__<model-slug>-<corpus-digest8>.json` replace the raw 32-hex fingerprint paths). All five stores
rebuilt under the new names (`merge-1800-0.15-on__<model>-4d284af0.json`; corpus digest unchanged). The graded path is
untouched (`prepare_run` byte-verify + `rank_rows` + `score_rows`); the upgrade only ADDED columns, so the OLD metric
columns in the comparison above must match the recorded 2026-10-02T16:01:34 comparison values.

OLD-column parity:

- bge-m3: EXACT — every old cell in every scope plus all unanswerable top-1s (0.5081/0.5040/0.4606) equal the recorded block.
- nomic-embed-text-v2-moe: EXACT (all scopes + top-1s 0.5017/0.4497/0.4142). embeddinggemma: EXACT (all scopes + top-1s
  0.4635/0.4292/0.3883). The store-naming change is layer-thin: bit-stable models reproduce bit-stable numbers.
- qwen3-embedding:0.6b: inside the already-recorded rebuild-drift family (qwen embeds are not bit-stable across builds):
  chunk R@1 29.8%, chunk R@10 74.2%, chunk MRR 0.482 all exact; chunk R@5 62.2%→62.5%; doc cells ±0.4pp (doc R@1
  59.9→60.3, doc R@5 89.1→88.8, doc R@10 94.0→93.6, doc MRR 0.722→0.725); top-1s move ≤ ±0.003, false-retrieval 0/3 kept.
- qwen3-embedding:8b: same fresh-build flip family, a little wider at the very top (single fresh build, one recorded
  predecessor): chunk R@1 30.7%→31.6% (a few rows flipping across the rank-1/2 boundary of 267), chunk R@5 66.5→66.7,
  chunk R@10 82.0→81.6, chunk MRR 0.509→0.514, doc cells ±0.4pp (doc R@10 exact 97.4%); top-1s 0.5858/0.5389/0.4367 and
  false-retrieval still 1/3 (m013 0.5858 ≥ 0.55 — the noted threshold item stands UNCHANGED, separate step).
- Verdict order unchanged in both currencies: embeddinggemma leads chunk-level, qwen3-8b leads doc-level, nomic-v2-moe
  keeps its margins; decisions untouched (nomic standby verdict per recorded blocks, embedding-only, threshold 0.55).

Recorded numbers remain final (append-only; nothing above rewritten). The new currency columns (cov@k, cov@3000, P@k, RP)
first appear recorded in this run's blocks; their interpretation is the next analysis step, not part of this parity note.


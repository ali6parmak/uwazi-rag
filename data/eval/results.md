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


# Retrieval eval results — `uwazi-rag eval` (Step 3.5)

Append-only scorecard log: every run appends one dated, labeled block below. The golden set is the committed `data/eval/golden.jsonl`; scores are *relative* (config A vs config B, shared self-echo bias), never absolute (see `data/eval/about.md`).

## 2026-10-06T12:08:05+00:00 — benchmark sweep_legalbenchrag_privacyqa — resolved plan

plan    : sweep_legalbenchrag_privacyqa — 1 experiment(s) over 1 store cell(s)
dataset : legalbenchrag-privacyqa
captures: data/raw/8a3f38ffd23a75e2 — 7 capture(s)
golden  : data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl — 199 row(s)
stores  :
  baseline               merge 1800/0.15/on     × bge-m3                       → data/benchmark_stores/merge-1800-0.15-on__bge-m3-260a60f1.json
experiments:
  1. baseline-embedding           → baseline               retrieval embedding


## 2026-10-06T12:08:05+00:00 — benchmark sweep_legalbenchrag_privacyqa: baseline-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__bge-m3-260a60f1.json` — 106 chunks, bge-m3 (1024d), built 2026-10-06T12:08:07+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 32.5% | 72.6% | 89.8% | 0.696 | 100.0% | 100.0% | 100.0% | 1.000 | 34.4% | 75.0% | 91.4% | 34.4% | 53.6% | 27.2% | 18.1% | 46.2% |
| en | 194 | 32.5% | 72.6% | 89.8% | 0.696 | 100.0% | 100.0% | 100.0% | 1.000 | 34.4% | 75.0% | 91.4% | 34.4% | 53.6% | 27.2% | 18.1% | 46.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 32.5% | 72.6% | 89.8% | 0.696 | 100.0% | 100.0% | 100.0% | 1.000 | 34.4% | 75.0% | 91.4% | 34.4% | 53.6% | 27.2% | 18.1% | 46.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 1/5 (20.0%) (top-1: m001 0.4383, m002 0.5036, m003 0.4775, m004 0.5023, m005 0.5518)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-06T12:08:10+00:00 — benchmark sweep_legalbenchrag_privacyqa — dataset legalbenchrag-privacyqa — comparison (1 experiment)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline-embedding | bge-m3 | 1800/0.15/on | embedding | 194 | 32.5% | 72.6% | 89.8% | 0.696 | 100.0% | 100.0% | 100.0% | 1.000 | 34.4% | 75.0% | 91.4% | 34.4% | 53.6% | 27.2% | 18.1% | 46.2% | 1/5 | 2s / 1.1s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes


## 2026-10-06T12:08:16+00:00 — benchmark sweep_legalbenchrag_privacyqa — resolved plan

plan    : sweep_legalbenchrag_privacyqa — 4 experiment(s) over 4 store cell(s)
dataset : legalbenchrag-privacyqa
captures: data/raw/8a3f38ffd23a75e2 — 7 capture(s)
golden  : data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl — 199 row(s)
stores  :
  baseline               merge 1800/0.15/on     × bge-m3                       → data/benchmark_stores/merge-1800-0.15-on__bge-m3-260a60f1.json
  merge-1200             merge 1200/0.15/on     × bge-m3                       → data/benchmark_stores/merge-1200-0.15-on__bge-m3-260a60f1.json
  merge-2400             merge 2400/0.15/on     × bge-m3                       → data/benchmark_stores/merge-2400-0.15-on__bge-m3-260a60f1.json
  noheader               merge 1800/0.15/off    × bge-m3                       → data/benchmark_stores/merge-1800-0.15-off__bge-m3-260a60f1.json
experiments:
  1. baseline-embedding           → baseline               retrieval embedding
  2. merge-1200-embedding         → merge-1200             retrieval embedding
  3. merge-2400-embedding         → merge-2400             retrieval embedding
  4. noheader-embedding           → noheader               retrieval embedding


## 2026-10-06T12:08:16+00:00 — benchmark sweep_legalbenchrag_privacyqa: baseline-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__bge-m3-260a60f1.json` — 106 chunks, bge-m3 (1024d), built 2026-10-06T12:08:07+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 32.5% | 72.6% | 89.8% | 0.696 | 100.0% | 100.0% | 100.0% | 1.000 | 34.4% | 75.0% | 91.4% | 34.4% | 53.6% | 27.2% | 18.1% | 46.2% |
| en | 194 | 32.5% | 72.6% | 89.8% | 0.696 | 100.0% | 100.0% | 100.0% | 1.000 | 34.4% | 75.0% | 91.4% | 34.4% | 53.6% | 27.2% | 18.1% | 46.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 32.5% | 72.6% | 89.8% | 0.696 | 100.0% | 100.0% | 100.0% | 1.000 | 34.4% | 75.0% | 91.4% | 34.4% | 53.6% | 27.2% | 18.1% | 46.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 1/5 (20.0%) (top-1: m001 0.4383, m002 0.5036, m003 0.4775, m004 0.5023, m005 0.5518)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-06T12:08:17+00:00 — benchmark sweep_legalbenchrag_privacyqa: merge-1200-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__bge-m3-260a60f1.json` — 163 chunks, bge-m3 (1024d), built 2026-10-06T12:08:17+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 29.5% | 66.8% | 82.4% | 0.676 | 100.0% | 100.0% | 100.0% | 1.000 | 31.0% | 67.2% | 83.0% | 47.7% | 51.0% | 28.2% | 18.2% | 47.4% |
| en | 194 | 29.5% | 66.8% | 82.4% | 0.676 | 100.0% | 100.0% | 100.0% | 1.000 | 31.0% | 67.2% | 83.0% | 47.7% | 51.0% | 28.2% | 18.2% | 47.4% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 29.5% | 66.8% | 82.4% | 0.676 | 100.0% | 100.0% | 100.0% | 1.000 | 31.0% | 67.2% | 83.0% | 47.7% | 51.0% | 28.2% | 18.2% | 47.4% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.4373, m002 0.4836, m003 0.4628, m004 0.5121, m005 0.5491)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-06T12:08:20+00:00 — benchmark sweep_legalbenchrag_privacyqa: merge-2400-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__bge-m3-260a60f1.json` — 79 chunks, bge-m3 (1024d), built 2026-10-06T12:08:20+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 36.2% | 82.5% | 95.5% | 0.752 | 100.0% | 100.0% | 100.0% | 1.000 | 38.4% | 81.6% | 95.5% | 38.4% | 59.8% | 30.2% | 18.2% | 53.0% |
| en | 194 | 36.2% | 82.5% | 95.5% | 0.752 | 100.0% | 100.0% | 100.0% | 1.000 | 38.4% | 81.6% | 95.5% | 38.4% | 59.8% | 30.2% | 18.2% | 53.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 36.2% | 82.5% | 95.5% | 0.752 | 100.0% | 100.0% | 100.0% | 1.000 | 38.4% | 81.6% | 95.5% | 38.4% | 59.8% | 30.2% | 18.2% | 53.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 1/5 (20.0%) (top-1: m001 0.4335, m002 0.5098, m003 0.4798, m004 0.5167, m005 0.5676)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-06T12:08:22+00:00 — benchmark sweep_legalbenchrag_privacyqa: noheader-embedding

store: `data/benchmark_stores/merge-1800-0.15-off__bge-m3-260a60f1.json` — 106 chunks, bge-m3 (1024d), built 2026-10-06T12:08:22+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header OFF

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 29.9% | 68.4% | 82.8% | 0.649 | 92.3% | 99.5% | 100.0% | 0.952 | 31.2% | 70.4% | 84.8% | 32.2% | 48.5% | 25.2% | 16.0% | 42.5% |
| en | 194 | 29.9% | 68.4% | 82.8% | 0.649 | 92.3% | 99.5% | 100.0% | 0.952 | 31.2% | 70.4% | 84.8% | 32.2% | 48.5% | 25.2% | 16.0% | 42.5% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 29.9% | 68.4% | 82.8% | 0.649 | 92.3% | 99.5% | 100.0% | 0.952 | 31.2% | 70.4% | 84.8% | 32.2% | 48.5% | 25.2% | 16.0% | 42.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.4496, m002 0.4966, m003 0.4544, m004 0.5128, m005 0.5027)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-06T12:08:24+00:00 — benchmark sweep_legalbenchrag_privacyqa — dataset legalbenchrag-privacyqa — comparison (4 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline-embedding | bge-m3 | 1800/0.15/on | embedding | 194 | 32.5% | 72.6% | 89.8% | 0.696 | 100.0% | 100.0% | 100.0% | 1.000 | 34.4% | 75.0% | 91.4% | 34.4% | 53.6% | 27.2% | 18.1% | 46.2% | 1/5 | reuse / 1.1s |
| merge-1200-embedding | bge-m3 | 1200/0.15/on | embedding | 194 | 29.5% | 66.8% | 82.4% | 0.676 | 100.0% | 100.0% | 100.0% | 1.000 | 31.0% | 67.2% | 83.0% | 47.7% | 51.0% | 28.2% | 18.2% | 47.4% | 0/5 | 1s / 1.1s |
| merge-2400-embedding | bge-m3 | 2400/0.15/on | embedding | 194 | 36.2% | 82.5% | 95.5% | 0.752 | 100.0% | 100.0% | 100.0% | 1.000 | 38.4% | 81.6% | 95.5% | 38.4% | 59.8% | 30.2% | 18.2% | 53.0% | 1/5 | 1s / 1.0s |
| noheader-embedding | bge-m3 | 1800/0.15/off | embedding | 194 | 29.9% | 68.4% | 82.8% | 0.649 | 92.3% | 99.5% | 100.0% | 0.952 | 31.2% | 70.4% | 84.8% | 32.2% | 48.5% | 25.2% | 16.0% | 42.5% | 0/5 | 1s / 1.0s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes


## 2026-10-06T12:08:28+00:00 — benchmark sweep_legalbenchrag_contractnli — resolved plan

plan    : sweep_legalbenchrag_contractnli — 3 experiment(s) over 3 store cell(s)
dataset : legalbenchrag-contractnli
captures: data/raw/d7f14657e7264534 — 95 capture(s)
golden  : data/eval/datasets/legalbenchrag-contractnli/golden.jsonl — 982 row(s)
stores  :
  baseline               merge 1800/0.15/on     × bge-m3                       → data/benchmark_stores/merge-1800-0.15-on__bge-m3-826d4d38.json
  merge-1200             merge 1200/0.15/on     × bge-m3                       → data/benchmark_stores/merge-1200-0.15-on__bge-m3-826d4d38.json
  noheader               merge 1800/0.15/off    × bge-m3                       → data/benchmark_stores/merge-1800-0.15-off__bge-m3-826d4d38.json
experiments:
  1. baseline-embedding           → baseline               retrieval embedding
  2. merge-1200-embedding         → merge-1200             retrieval embedding
  3. noheader-embedding           → noheader               retrieval embedding


## 2026-10-06T12:08:28+00:00 — benchmark sweep_legalbenchrag_contractnli: baseline-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__bge-m3-826d4d38.json` — 703 chunks, bge-m3 (1024d), built 2026-10-06T12:08:28+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 35.7% | 77.5% | 87.3% | 0.591 | 84.0% | 94.9% | 96.9% | 0.887 | 36.7% | 78.5% | 88.0% | 41.0% | 41.7% | 19.1% | 11.0% | 39.8% |
| en | 977 | 35.7% | 77.5% | 87.3% | 0.591 | 84.0% | 94.9% | 96.9% | 0.887 | 36.7% | 78.5% | 88.0% | 41.0% | 41.7% | 19.1% | 11.0% | 39.8% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 35.7% | 77.5% | 87.3% | 0.591 | 84.0% | 94.9% | 96.9% | 0.887 | 36.7% | 78.5% | 88.0% | 41.0% | 41.7% | 19.1% | 11.0% | 39.8% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 3/5 (60.0%) (top-1: m001 0.6020, m002 0.5827, m003 0.5052, m004 0.5955, m005 0.5354)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-06T12:08:42+00:00 — benchmark sweep_legalbenchrag_contractnli: merge-1200-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__bge-m3-826d4d38.json` — 1,091 chunks, bge-m3 (1024d), built 2026-10-06T12:08:42+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 34.4% | 71.7% | 82.2% | 0.601 | 84.7% | 94.9% | 97.4% | 0.891 | 38.6% | 75.7% | 84.7% | 57.8% | 44.8% | 19.8% | 11.6% | 40.5% |
| en | 977 | 34.4% | 71.7% | 82.2% | 0.601 | 84.7% | 94.9% | 97.4% | 0.891 | 38.6% | 75.7% | 84.7% | 57.8% | 44.8% | 19.8% | 11.6% | 40.5% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 34.4% | 71.7% | 82.2% | 0.601 | 84.7% | 94.9% | 97.4% | 0.891 | 38.6% | 75.7% | 84.7% | 57.8% | 44.8% | 19.8% | 11.6% | 40.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 3/5 (60.0%) (top-1: m001 0.5987, m002 0.5915, m003 0.5079, m004 0.5906, m005 0.5354)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-06T12:08:59+00:00 — benchmark sweep_legalbenchrag_contractnli: noheader-embedding

store: `data/benchmark_stores/merge-1800-0.15-off__bge-m3-826d4d38.json` — 703 chunks, bge-m3 (1024d), built 2026-10-06T12:08:59+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header OFF

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 14.7% | 28.5% | 34.2% | 0.251 | 54.8% | 67.2% | 73.8% | 0.612 | 14.7% | 28.6% | 34.3% | 16.9% | 17.5% | 6.9% | 4.1% | 16.1% |
| en | 977 | 14.7% | 28.5% | 34.2% | 0.251 | 54.8% | 67.2% | 73.8% | 0.612 | 14.7% | 28.6% | 34.3% | 16.9% | 17.5% | 6.9% | 4.1% | 16.1% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 14.7% | 28.5% | 34.2% | 0.251 | 54.8% | 67.2% | 73.8% | 0.612 | 14.7% | 28.6% | 34.3% | 16.9% | 17.5% | 6.9% | 4.1% | 16.1% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 4/5 (80.0%) (top-1: m001 0.6092, m002 0.6008, m003 0.4966, m004 0.6185, m005 0.5512)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-06T12:09:14+00:00 — benchmark sweep_legalbenchrag_contractnli — dataset legalbenchrag-contractnli — comparison (3 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline-embedding | bge-m3 | 1800/0.15/on | embedding | 977 | 35.7% | 77.5% | 87.3% | 0.591 | 84.0% | 94.9% | 96.9% | 0.887 | 36.7% | 78.5% | 88.0% | 41.0% | 41.7% | 19.1% | 11.0% | 39.8% | 3/5 | 7s / 6.9s |
| merge-1200-embedding | bge-m3 | 1200/0.15/on | embedding | 977 | 34.4% | 71.7% | 82.2% | 0.601 | 84.7% | 94.9% | 97.4% | 0.891 | 38.6% | 75.7% | 84.7% | 57.8% | 44.8% | 19.8% | 11.6% | 40.5% | 3/5 | 9s / 7.5s |
| noheader-embedding | bge-m3 | 1800/0.15/off | embedding | 977 | 14.7% | 28.5% | 34.2% | 0.251 | 54.8% | 67.2% | 73.8% | 0.612 | 14.7% | 28.6% | 34.3% | 16.9% | 17.5% | 6.9% | 4.1% | 16.1% | 4/5 | 8s / 7.0s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes


## 2026-10-06T12:09:18+00:00 — benchmark sweep_vic_chargebook — resolved plan

plan    : sweep_vic_chargebook — 2 experiment(s) over 2 store cell(s)
dataset : vic-chargebook
captures: data/raw/c49c2465f4afa801 — 4876 capture(s)
golden  : data/eval/datasets/vic-chargebook/golden.jsonl — 104 row(s)
stores  :
  baseline               passthrough 4096/on    × bge-m3                       → data/benchmark_stores/passthrough-4096-on__bge-m3-6adfbee8.json
  noheader               passthrough 4096/off   × bge-m3                       → data/benchmark_stores/passthrough-4096-off__bge-m3-6adfbee8.json
experiments:
  1. baseline-embedding           → baseline               retrieval embedding
  2. noheader-embedding           → noheader               retrieval embedding


## 2026-10-06T12:09:18+00:00 — benchmark sweep_vic_chargebook: baseline-embedding

store: `data/benchmark_stores/passthrough-4096-on__bge-m3-6adfbee8.json` — 4,876 chunks, bge-m3 (1024d), built 2026-10-06T12:09:18+00:00
golden: `data/eval/datasets/vic-chargebook/golden.jsonl` — 104 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 4096, overlap 0, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 100 | 16.0% | 35.0% | 42.0% | 0.248 | 16.0% | 35.0% | 42.0% | 0.248 | 16.0% | 35.0% | 42.0% | 18.0% | 16.0% | 7.0% | 4.2% | 16.0% |
| en | 100 | 16.0% | 35.0% | 42.0% | 0.248 | 16.0% | 35.0% | 42.0% | 0.248 | 16.0% | 35.0% | 42.0% | 18.0% | 16.0% | 7.0% | 4.2% | 16.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 100 | 16.0% | 35.0% | 42.0% | 0.248 | 16.0% | 35.0% | 42.0% | 0.248 | 16.0% | 35.0% | 42.0% | 18.0% | 16.0% | 7.0% | 4.2% | 16.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 3/4 (75.0%) (top-1: m001 0.5837, m002 0.5563, m003 0.5499, m004 0.5571)
retrieval: embedding
dataset: vic-chargebook


## 2026-10-06T12:10:08+00:00 — benchmark sweep_vic_chargebook: noheader-embedding

store: `data/benchmark_stores/passthrough-4096-off__bge-m3-6adfbee8.json` — 4,876 chunks, bge-m3 (1024d), built 2026-10-06T12:10:08+00:00
golden: `data/eval/datasets/vic-chargebook/golden.jsonl` — 104 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 4096, overlap 0, header OFF

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 100 | 13.0% | 34.0% | 41.0% | 0.229 | 13.0% | 34.0% | 41.0% | 0.229 | 13.0% | 34.0% | 41.0% | 15.0% | 13.0% | 6.8% | 4.1% | 13.0% |
| en | 100 | 13.0% | 34.0% | 41.0% | 0.229 | 13.0% | 34.0% | 41.0% | 0.229 | 13.0% | 34.0% | 41.0% | 15.0% | 13.0% | 6.8% | 4.1% | 13.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 100 | 13.0% | 34.0% | 41.0% | 0.229 | 13.0% | 34.0% | 41.0% | 0.229 | 13.0% | 34.0% | 41.0% | 15.0% | 13.0% | 6.8% | 4.1% | 13.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 3/4 (75.0%) (top-1: m001 0.5696, m002 0.5526, m003 0.5351, m004 0.5504)
retrieval: embedding
dataset: vic-chargebook


## 2026-10-06T12:10:56+00:00 — benchmark sweep_vic_chargebook — dataset vic-chargebook — comparison (2 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline-embedding | bge-m3 | 4096/0/on | embedding | 100 | 16.0% | 35.0% | 42.0% | 0.248 | 16.0% | 35.0% | 42.0% | 0.248 | 16.0% | 35.0% | 42.0% | 18.0% | 16.0% | 7.0% | 4.2% | 16.0% | 3/4 | 47s / 1.9s |
| noheader-embedding | bge-m3 | 4096/0/off | embedding | 100 | 13.0% | 34.0% | 41.0% | 0.229 | 13.0% | 34.0% | 41.0% | 0.229 | 13.0% | 34.0% | 41.0% | 15.0% | 13.0% | 6.8% | 4.1% | 13.0% | 3/4 | 46s / 1.8s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes


## 2026-10-06T12:17:31+00:00 — benchmark sweep_legalbenchrag_cuad — resolved plan

plan    : sweep_legalbenchrag_cuad — 1 experiment(s) over 1 store cell(s)
dataset : legalbenchrag-cuad
captures: data/raw/c88547bc806ea086 — 462 capture(s)
golden  : data/eval/datasets/legalbenchrag-cuad/golden.jsonl — 4046 row(s)
stores  :
  baseline               merge 1800/0.15/on     × bge-m3                       → data/benchmark_stores/merge-1800-0.15-on__bge-m3-47d5d5a2.json
experiments:
  1. baseline-embedding           → baseline               retrieval embedding


## 2026-10-06T12:17:31+00:00 — benchmark sweep_legalbenchrag_cuad: baseline-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__bge-m3-47d5d5a2.json` — 18,024 chunks, bge-m3 (1024d), built 2026-10-06T12:11:02+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 7.7% | 37.2% | 54.8% | 0.297 | 98.7% | 100.0% | 100.0% | 0.993 | 10.6% | 45.8% | 64.4% | 13.6% | 12.7% | 12.7% | 9.9% | 13.2% |
| en | 4042 | 7.7% | 37.2% | 54.8% | 0.297 | 98.7% | 100.0% | 100.0% | 0.993 | 10.6% | 45.8% | 64.4% | 13.6% | 12.7% | 12.7% | 9.9% | 13.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 7.7% | 37.2% | 54.8% | 0.297 | 98.7% | 100.0% | 100.0% | 0.993 | 10.6% | 45.8% | 64.4% | 13.6% | 12.7% | 12.7% | 9.9% | 13.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6007, m002 0.5775, m003 0.6123, m004 0.5847)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-06T12:19:11+00:00 — benchmark sweep_legalbenchrag_cuad — dataset legalbenchrag-cuad — comparison (1 experiment)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline-embedding | bge-m3 | 1800/0.15/on | embedding | 4042 | 7.7% | 37.2% | 54.8% | 0.297 | 98.7% | 100.0% | 100.0% | 0.993 | 10.6% | 45.8% | 64.4% | 13.6% | 12.7% | 12.7% | 9.9% | 13.2% | 4/4 | reuse / 97.6s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes


## 2026-10-07T11:43:21+00:00 — benchmark sweep2_models — resolved plan

plan    : sweep2_models — 21 experiment(s) over 21 store cell(s)
captures: data/raw/bdd5a7c445847b35 — 77 capture(s)
golden  : data/eval/golden.jsonl — 270 row(s)
stores  :
  merge-1800-bge-m3      merge 1800/0.15/on     × bge-m3                       → data/benchmark_stores/merge-1800-0.15-on__bge-m3-4d284af0.json
  merge-1200-bge-m3      merge 1200/0.15/on     × bge-m3                       → data/benchmark_stores/merge-1200-0.15-on__bge-m3-4d284af0.json
  merge-2400-bge-m3      merge 2400/0.15/on     × bge-m3                       → data/benchmark_stores/merge-2400-0.15-on__bge-m3-4d284af0.json
  merge-1800-nomic-embed-text-v2-moe merge 1800/0.15/on     × nomic-embed-text-v2-moe      → data/benchmark_stores/merge-1800-0.15-on__nomic-embed-text-v2-moe-4d284af0.json
  merge-1200-nomic-embed-text-v2-moe merge 1200/0.15/on     × nomic-embed-text-v2-moe      → data/benchmark_stores/merge-1200-0.15-on__nomic-embed-text-v2-moe-4d284af0.json
  merge-2400-nomic-embed-text-v2-moe merge 2400/0.15/on     × nomic-embed-text-v2-moe      → data/benchmark_stores/merge-2400-0.15-on__nomic-embed-text-v2-moe-4d284af0.json
  merge-1800-qwen3-embedding-8b merge 1800/0.15/on     × qwen3-embedding:8b           → data/benchmark_stores/merge-1800-0.15-on__qwen3-embedding-8b-4d284af0.json
  merge-1200-qwen3-embedding-8b merge 1200/0.15/on     × qwen3-embedding:8b           → data/benchmark_stores/merge-1200-0.15-on__qwen3-embedding-8b-4d284af0.json
  merge-2400-qwen3-embedding-8b merge 2400/0.15/on     × qwen3-embedding:8b           → data/benchmark_stores/merge-2400-0.15-on__qwen3-embedding-8b-4d284af0.json
  merge-1800-embeddinggemma merge 1800/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-1800-0.15-on__embeddinggemma-4d284af0.json
  merge-1200-embeddinggemma merge 1200/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-1200-0.15-on__embeddinggemma-4d284af0.json
  merge-2400-embeddinggemma merge 2400/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-2400-0.15-on__embeddinggemma-4d284af0.json
  merge-1800-granite-embedding merge 1800/0.15/on     × granite-embedding            → data/benchmark_stores/merge-1800-0.15-on__granite-embedding-4d284af0.json
  merge-1200-granite-embedding merge 1200/0.15/on     × granite-embedding            → data/benchmark_stores/merge-1200-0.15-on__granite-embedding-4d284af0.json
  merge-2400-granite-embedding merge 2400/0.15/on     × granite-embedding            → data/benchmark_stores/merge-2400-0.15-on__granite-embedding-4d284af0.json
  merge-1800-snowflake-arctic-embed2 merge 1800/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-1800-0.15-on__snowflake-arctic-embed2-4d284af0.json
  merge-1200-snowflake-arctic-embed2 merge 1200/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-1200-0.15-on__snowflake-arctic-embed2-4d284af0.json
  merge-2400-snowflake-arctic-embed2 merge 2400/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-2400-0.15-on__snowflake-arctic-embed2-4d284af0.json
  merge-1800-mxbai-embed-large merge 1800/0.15/on     × mxbai-embed-large            → data/benchmark_stores/merge-1800-0.15-on__mxbai-embed-large-4d284af0.json
  merge-1200-mxbai-embed-large merge 1200/0.15/on     × mxbai-embed-large            → data/benchmark_stores/merge-1200-0.15-on__mxbai-embed-large-4d284af0.json
  merge-2400-mxbai-embed-large merge 2400/0.15/on     × mxbai-embed-large            → data/benchmark_stores/merge-2400-0.15-on__mxbai-embed-large-4d284af0.json
experiments:
  1. merge-1800-bge-m3-embedding  → merge-1800-bge-m3      retrieval embedding
  2. merge-1200-bge-m3-embedding  → merge-1200-bge-m3      retrieval embedding
  3. merge-2400-bge-m3-embedding  → merge-2400-bge-m3      retrieval embedding
  4. merge-1800-nomic-embed-text-v2-moe-embedding → merge-1800-nomic-embed-text-v2-moe retrieval embedding
  5. merge-1200-nomic-embed-text-v2-moe-embedding → merge-1200-nomic-embed-text-v2-moe retrieval embedding
  6. merge-2400-nomic-embed-text-v2-moe-embedding → merge-2400-nomic-embed-text-v2-moe retrieval embedding
  7. merge-1800-qwen3-embedding-8b-embedding → merge-1800-qwen3-embedding-8b retrieval embedding
  8. merge-1200-qwen3-embedding-8b-embedding → merge-1200-qwen3-embedding-8b retrieval embedding
  9. merge-2400-qwen3-embedding-8b-embedding → merge-2400-qwen3-embedding-8b retrieval embedding
  10. merge-1800-embeddinggemma-embedding → merge-1800-embeddinggemma retrieval embedding
  11. merge-1200-embeddinggemma-embedding → merge-1200-embeddinggemma retrieval embedding
  12. merge-2400-embeddinggemma-embedding → merge-2400-embeddinggemma retrieval embedding
  13. merge-1800-granite-embedding-embedding → merge-1800-granite-embedding retrieval embedding
  14. merge-1200-granite-embedding-embedding → merge-1200-granite-embedding retrieval embedding
  15. merge-2400-granite-embedding-embedding → merge-2400-granite-embedding retrieval embedding
  16. merge-1800-snowflake-arctic-embed2-embedding → merge-1800-snowflake-arctic-embed2 retrieval embedding
  17. merge-1200-snowflake-arctic-embed2-embedding → merge-1200-snowflake-arctic-embed2 retrieval embedding
  18. merge-2400-snowflake-arctic-embed2-embedding → merge-2400-snowflake-arctic-embed2 retrieval embedding
  19. merge-1800-mxbai-embed-large-embedding → merge-1800-mxbai-embed-large retrieval embedding
  20. merge-1200-mxbai-embed-large-embedding → merge-1200-mxbai-embed-large retrieval embedding
  21. merge-2400-mxbai-embed-large-embedding → merge-2400-mxbai-embed-large retrieval embedding


## 2026-10-07T11:43:21+00:00 — benchmark sweep2_models: merge-1800-bge-m3-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__bge-m3-4d284af0.json` — 2,850 chunks, bge-m3 (1024d), built 2026-10-07T11:43:21+00:00
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


## 2026-10-07T11:43:51+00:00 — benchmark sweep2_models: merge-1200-bge-m3-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__bge-m3-4d284af0.json` — 4,488 chunks, bge-m3 (1024d), built 2026-10-07T11:43:51+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.4% | 62.8% | 73.5% | 0.479 | 62.9% | 91.8% | 93.6% | 0.751 | 32.7% | 64.9% | 75.7% | 49.3% | 33.0% | 13.4% | 7.9% | 32.8% |
| en | 169 | 32.8% | 64.2% | 73.4% | 0.484 | 68.0% | 92.9% | 93.5% | 0.782 | 33.3% | 66.3% | 75.0% | 50.5% | 33.7% | 13.6% | 7.8% | 34.3% |
| es | 98 | 28.9% | 60.4% | 73.8% | 0.470 | 54.1% | 89.8% | 93.9% | 0.698 | 31.6% | 62.6% | 76.9% | 47.3% | 31.6% | 13.1% | 8.1% | 30.3% |
| synthetic | 255 | 31.3% | 62.6% | 73.1% | 0.479 | 62.4% | 91.4% | 93.3% | 0.747 | 32.7% | 64.8% | 75.4% | 49.7% | 32.9% | 13.4% | 7.9% | 32.8% |
| manual | 12 | 33.3% | 66.7% | 83.3% | 0.476 | 75.0% | 100.0% | 100.0% | 0.833 | 33.3% | 66.7% | 83.3% | 41.7% | 33.3% | 13.3% | 8.3% | 33.3% |
| cross-language | 65 | 23.6% | 53.3% | 70.0% | 0.412 | 55.4% | 92.3% | 95.4% | 0.701 | 25.1% | 56.9% | 72.1% | 37.4% | 26.2% | 11.7% | 7.8% | 24.1% |
| same-language | 202 | 33.9% | 65.8% | 74.7% | 0.500 | 65.3% | 91.6% | 93.1% | 0.767 | 35.1% | 67.5% | 76.9% | 53.1% | 35.1% | 14.0% | 7.9% | 35.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5359, m014 0.5081, m015 0.4582)
retrieval: embedding


## 2026-10-07T11:44:31+00:00 — benchmark sweep2_models: merge-2400-bge-m3-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__bge-m3-4d284af0.json` — 2,069 chunks, bge-m3 (1024d), built 2026-10-07T11:44:31+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 29.6% | 63.5% | 71.2% | 0.465 | 59.6% | 89.1% | 93.3% | 0.722 | 29.7% | 64.0% | 71.7% | 29.7% | 31.5% | 13.6% | 7.8% | 30.3% |
| en | 169 | 29.6% | 66.9% | 74.9% | 0.472 | 62.7% | 89.9% | 94.1% | 0.744 | 29.5% | 66.9% | 74.9% | 30.1% | 32.0% | 14.3% | 8.1% | 30.2% |
| es | 98 | 29.6% | 57.7% | 64.8% | 0.453 | 54.1% | 87.8% | 91.8% | 0.683 | 30.1% | 59.1% | 66.3% | 29.1% | 30.6% | 12.4% | 7.2% | 30.6% |
| synthetic | 255 | 29.8% | 64.1% | 72.2% | 0.469 | 58.8% | 89.0% | 92.9% | 0.717 | 29.9% | 64.7% | 72.7% | 29.9% | 31.8% | 13.8% | 7.9% | 30.6% |
| manual | 12 | 25.0% | 50.0% | 50.0% | 0.373 | 75.0% | 91.7% | 100.0% | 0.831 | 25.0% | 50.0% | 50.0% | 25.0% | 25.0% | 10.0% | 5.0% | 25.0% |
| cross-language | 65 | 25.4% | 66.2% | 73.8% | 0.448 | 53.8% | 93.8% | 98.5% | 0.694 | 26.2% | 68.3% | 75.6% | 24.6% | 27.7% | 15.1% | 8.5% | 26.2% |
| same-language | 202 | 30.9% | 62.6% | 70.3% | 0.470 | 61.4% | 87.6% | 91.6% | 0.731 | 30.9% | 62.6% | 70.5% | 31.4% | 32.7% | 13.2% | 7.6% | 31.7% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5167, m014 0.5154, m015 0.4686)
retrieval: embedding


## 2026-10-07T11:44:59+00:00 — benchmark sweep2_models: merge-1800-nomic-embed-text-v2-moe-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__nomic-embed-text-v2-moe-4d284af0.json` — 2,850 chunks, nomic-embed-text-v2-moe (768d), built 2026-10-07T11:45:00+00:00
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


## 2026-10-07T11:45:25+00:00 — benchmark sweep2_models: merge-1200-nomic-embed-text-v2-moe-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__nomic-embed-text-v2-moe-4d284af0.json` — 4,488 chunks, nomic-embed-text-v2-moe (768d), built 2026-10-07T11:45:25+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 34.3% | 63.6% | 78.0% | 0.498 | 65.9% | 91.4% | 94.8% | 0.763 | 36.5% | 65.7% | 80.0% | 49.6% | 36.7% | 13.7% | 8.4% | 35.3% |
| en | 169 | 37.3% | 62.1% | 79.0% | 0.507 | 71.6% | 90.5% | 92.9% | 0.788 | 38.7% | 63.5% | 80.2% | 49.3% | 39.1% | 13.3% | 8.4% | 37.9% |
| es | 98 | 29.3% | 66.2% | 76.4% | 0.483 | 56.1% | 92.9% | 98.0% | 0.719 | 32.7% | 69.4% | 79.6% | 50.0% | 32.7% | 14.5% | 8.3% | 31.0% |
| synthetic | 255 | 35.2% | 64.2% | 78.2% | 0.506 | 65.5% | 91.4% | 94.9% | 0.760 | 37.4% | 66.4% | 80.2% | 50.3% | 37.6% | 13.9% | 8.4% | 36.2% |
| manual | 12 | 16.7% | 50.0% | 75.0% | 0.338 | 75.0% | 91.7% | 91.7% | 0.833 | 16.7% | 50.0% | 75.0% | 33.3% | 16.7% | 10.0% | 7.5% | 16.7% |
| cross-language | 65 | 25.6% | 56.9% | 81.5% | 0.435 | 58.5% | 90.8% | 95.4% | 0.699 | 28.2% | 59.0% | 83.8% | 37.4% | 29.2% | 12.9% | 9.1% | 26.2% |
| same-language | 202 | 37.1% | 65.8% | 76.9% | 0.518 | 68.3% | 91.6% | 94.6% | 0.783 | 39.1% | 67.8% | 78.7% | 53.5% | 39.1% | 14.0% | 8.1% | 38.3% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4652, m014 0.4479, m015 0.4398)
retrieval: embedding


## 2026-10-07T11:45:56+00:00 — benchmark sweep2_models: merge-2400-nomic-embed-text-v2-moe-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__nomic-embed-text-v2-moe-4d284af0.json` — 2,069 chunks, nomic-embed-text-v2-moe (768d), built 2026-10-07T11:45:56+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 30.3% | 66.5% | 74.2% | 0.476 | 58.8% | 89.1% | 92.9% | 0.717 | 30.5% | 66.8% | 74.6% | 31.0% | 32.2% | 14.4% | 8.1% | 31.5% |
| en | 169 | 31.7% | 68.9% | 76.0% | 0.484 | 63.3% | 89.3% | 92.3% | 0.735 | 31.6% | 68.8% | 76.0% | 32.1% | 33.7% | 14.9% | 8.2% | 32.5% |
| es | 98 | 28.1% | 62.2% | 70.9% | 0.462 | 51.0% | 88.8% | 93.9% | 0.686 | 28.6% | 63.3% | 72.2% | 29.1% | 29.6% | 13.5% | 7.8% | 29.6% |
| synthetic | 255 | 31.0% | 67.3% | 74.5% | 0.482 | 58.4% | 89.0% | 92.9% | 0.713 | 31.1% | 67.6% | 75.0% | 31.7% | 32.9% | 14.6% | 8.1% | 32.2% |
| manual | 12 | 16.7% | 50.0% | 66.7% | 0.336 | 66.7% | 91.7% | 91.7% | 0.792 | 16.7% | 50.0% | 66.7% | 16.7% | 16.7% | 10.0% | 6.7% | 16.7% |
| cross-language | 65 | 26.9% | 69.2% | 74.6% | 0.461 | 50.8% | 86.2% | 93.8% | 0.661 | 27.7% | 70.3% | 76.0% | 26.2% | 29.2% | 15.7% | 8.5% | 30.0% |
| same-language | 202 | 31.4% | 65.6% | 74.0% | 0.481 | 61.4% | 90.1% | 92.6% | 0.735 | 31.4% | 65.7% | 74.2% | 32.6% | 33.2% | 14.0% | 7.9% | 31.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4440, m014 0.4536, m015 0.3906)
retrieval: embedding


## 2026-10-07T11:46:16+00:00 — benchmark sweep2_models: merge-1800-qwen3-embedding-8b-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__qwen3-embedding-8b-4d284af0.json` — 2,850 chunks, qwen3-embedding:8b (4096d), built 2026-10-07T11:46:28+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.6% | 66.5% | 82.4% | 0.514 | 66.3% | 94.0% | 97.4% | 0.784 | 32.8% | 68.0% | 83.4% | 38.3% | 35.2% | 15.1% | 9.4% | 33.0% |
| en | 169 | 33.4% | 68.9% | 81.1% | 0.518 | 71.0% | 92.9% | 96.4% | 0.805 | 34.2% | 70.0% | 81.7% | 39.9% | 36.1% | 15.3% | 9.1% | 34.3% |
| es | 98 | 28.6% | 62.2% | 84.7% | 0.506 | 58.2% | 95.9% | 99.0% | 0.749 | 30.3% | 64.7% | 86.4% | 35.4% | 33.7% | 14.7% | 10.0% | 30.6% |
| synthetic | 255 | 32.2% | 67.3% | 82.7% | 0.519 | 66.3% | 93.7% | 97.3% | 0.783 | 33.3% | 68.9% | 83.8% | 39.1% | 35.7% | 15.2% | 9.5% | 33.5% |
| manual | 12 | 20.8% | 50.0% | 75.0% | 0.400 | 66.7% | 100.0% | 100.0% | 0.808 | 20.8% | 50.0% | 75.0% | 20.8% | 25.0% | 11.7% | 8.3% | 20.8% |
| cross-language | 65 | 26.2% | 66.9% | 78.5% | 0.471 | 56.9% | 96.9% | 98.5% | 0.733 | 27.8% | 69.5% | 80.3% | 33.5% | 29.2% | 15.7% | 9.1% | 27.7% |
| same-language | 202 | 33.4% | 66.3% | 83.7% | 0.527 | 69.3% | 93.1% | 97.0% | 0.801 | 34.4% | 67.6% | 84.4% | 39.8% | 37.1% | 14.9% | 9.5% | 34.7% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 1/3 (33.3%) (top-1: m013 0.5877, m014 0.5389, m015 0.4382)
retrieval: embedding


## 2026-10-07T11:51:23+00:00 — benchmark sweep2_models: merge-1200-qwen3-embedding-8b-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__qwen3-embedding-8b-4d284af0.json` — 4,488 chunks, qwen3-embedding:8b (4096d), built 2026-10-07T11:51:23+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 39.7% | 70.7% | 83.3% | 0.558 | 67.4% | 95.1% | 97.8% | 0.794 | 41.4% | 73.6% | 85.7% | 57.2% | 41.6% | 15.2% | 9.0% | 41.1% |
| en | 169 | 40.8% | 70.1% | 83.7% | 0.553 | 72.2% | 92.9% | 97.0% | 0.813 | 41.7% | 72.3% | 84.9% | 57.3% | 42.0% | 14.9% | 8.9% | 42.0% |
| es | 98 | 37.8% | 71.8% | 82.5% | 0.566 | 59.2% | 99.0% | 99.0% | 0.759 | 40.8% | 75.9% | 87.1% | 57.1% | 40.8% | 15.7% | 9.0% | 39.6% |
| synthetic | 255 | 40.0% | 70.9% | 83.7% | 0.561 | 66.7% | 94.9% | 97.6% | 0.788 | 41.8% | 73.9% | 86.2% | 58.0% | 42.0% | 15.3% | 9.0% | 41.5% |
| manual | 12 | 33.3% | 66.7% | 75.0% | 0.488 | 83.3% | 100.0% | 100.0% | 0.917 | 33.3% | 66.7% | 75.0% | 41.7% | 33.3% | 13.3% | 7.5% | 33.3% |
| cross-language | 65 | 29.5% | 66.2% | 84.6% | 0.503 | 60.0% | 96.9% | 100.0% | 0.750 | 31.5% | 69.5% | 86.9% | 49.0% | 32.3% | 14.8% | 9.4% | 31.5% |
| same-language | 202 | 43.0% | 72.2% | 82.8% | 0.576 | 69.8% | 94.6% | 97.0% | 0.808 | 44.6% | 74.9% | 85.3% | 59.9% | 44.6% | 15.3% | 8.8% | 44.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 2/3 (66.7%) (top-1: m013 0.6159, m014 0.5734, m015 0.4390)
retrieval: embedding


## 2026-10-07T11:57:07+00:00 — benchmark sweep2_models: merge-2400-qwen3-embedding-8b-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__qwen3-embedding-8b-4d284af0.json` — 2,069 chunks, qwen3-embedding:8b (4096d), built 2026-10-07T11:57:07+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 35.8% | 67.6% | 76.6% | 0.533 | 64.4% | 91.8% | 95.1% | 0.764 | 36.0% | 68.0% | 77.0% | 36.6% | 39.0% | 15.0% | 8.5% | 37.8% |
| en | 169 | 32.5% | 70.4% | 79.6% | 0.517 | 65.1% | 89.9% | 94.1% | 0.762 | 32.5% | 70.4% | 79.6% | 33.1% | 35.5% | 15.3% | 8.6% | 34.3% |
| es | 98 | 41.3% | 62.8% | 71.4% | 0.560 | 63.3% | 94.9% | 96.9% | 0.768 | 42.0% | 63.9% | 72.5% | 42.5% | 44.9% | 14.5% | 8.3% | 43.9% |
| synthetic | 255 | 36.7% | 68.8% | 76.7% | 0.544 | 64.7% | 91.8% | 95.3% | 0.765 | 36.9% | 69.2% | 77.1% | 37.5% | 40.0% | 15.3% | 8.5% | 38.8% |
| manual | 12 | 16.7% | 41.7% | 75.0% | 0.301 | 58.3% | 91.7% | 91.7% | 0.744 | 16.7% | 41.7% | 75.0% | 16.7% | 16.7% | 8.3% | 7.5% | 16.7% |
| cross-language | 65 | 44.6% | 75.4% | 78.5% | 0.604 | 66.2% | 93.8% | 95.4% | 0.775 | 46.2% | 76.5% | 79.6% | 44.6% | 49.2% | 17.5% | 9.1% | 48.5% |
| same-language | 202 | 32.9% | 65.1% | 76.0% | 0.510 | 63.9% | 91.1% | 95.0% | 0.761 | 32.8% | 65.3% | 76.2% | 34.0% | 35.6% | 14.2% | 8.3% | 34.4% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 1/3 (33.3%) (top-1: m013 0.6156, m014 0.5305, m015 0.4343)
retrieval: embedding


## 2026-10-07T12:01:34+00:00 — benchmark sweep2_models: merge-1800-embeddinggemma-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__embeddinggemma-4d284af0.json` — 2,850 chunks, embeddinggemma (768d), built 2026-10-07T12:01:35+00:00
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


## 2026-10-07T12:02:02+00:00 — benchmark sweep2_models: merge-1200-embeddinggemma-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__embeddinggemma-4d284af0.json` — 4,488 chunks, embeddinggemma (768d), built 2026-10-07T12:02:02+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 37.2% | 65.2% | 79.5% | 0.528 | 67.8% | 92.9% | 97.8% | 0.787 | 38.8% | 67.4% | 81.6% | 54.3% | 39.3% | 13.9% | 8.5% | 37.7% |
| en | 169 | 38.5% | 66.3% | 79.6% | 0.535 | 70.4% | 91.1% | 97.0% | 0.796 | 39.4% | 67.8% | 81.4% | 54.2% | 40.2% | 14.1% | 8.5% | 38.8% |
| es | 98 | 35.0% | 63.4% | 79.3% | 0.516 | 63.3% | 95.9% | 99.0% | 0.773 | 37.8% | 66.7% | 82.0% | 54.4% | 37.8% | 13.7% | 8.6% | 35.9% |
| synthetic | 255 | 37.8% | 65.6% | 78.9% | 0.533 | 67.1% | 92.5% | 97.6% | 0.781 | 39.5% | 67.8% | 81.1% | 54.5% | 40.0% | 14.0% | 8.5% | 38.3% |
| manual | 12 | 25.0% | 58.3% | 91.7% | 0.423 | 83.3% | 100.0% | 100.0% | 0.917 | 25.0% | 58.3% | 91.7% | 50.0% | 25.0% | 11.7% | 9.2% | 25.0% |
| cross-language | 65 | 35.1% | 59.7% | 77.4% | 0.501 | 56.9% | 89.2% | 98.5% | 0.707 | 36.4% | 62.3% | 79.2% | 45.6% | 38.5% | 13.2% | 8.5% | 35.1% |
| same-language | 202 | 37.9% | 67.0% | 80.1% | 0.537 | 71.3% | 94.1% | 97.5% | 0.813 | 39.6% | 69.0% | 82.3% | 57.1% | 39.6% | 14.2% | 8.5% | 38.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4994, m014 0.4174, m015 0.3793)
retrieval: embedding


## 2026-10-07T12:02:34+00:00 — benchmark sweep2_models: merge-2400-embeddinggemma-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__embeddinggemma-4d284af0.json` — 2,069 chunks, embeddinggemma (768d), built 2026-10-07T12:02:34+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.6% | 65.4% | 77.5% | 0.491 | 64.4% | 89.1% | 95.5% | 0.757 | 31.7% | 65.8% | 78.0% | 32.3% | 34.1% | 14.2% | 8.5% | 33.0% |
| en | 169 | 31.4% | 68.9% | 76.6% | 0.492 | 66.9% | 88.2% | 95.3% | 0.765 | 31.3% | 68.9% | 76.5% | 31.9% | 33.7% | 14.8% | 8.3% | 32.5% |
| es | 98 | 32.1% | 59.2% | 79.1% | 0.489 | 60.2% | 90.8% | 95.9% | 0.742 | 32.5% | 60.5% | 80.6% | 33.0% | 34.7% | 13.1% | 8.9% | 33.7% |
| synthetic | 255 | 32.0% | 66.1% | 77.6% | 0.497 | 63.1% | 88.6% | 95.3% | 0.748 | 32.0% | 66.6% | 78.2% | 32.6% | 34.5% | 14.4% | 8.5% | 33.3% |
| manual | 12 | 25.0% | 50.0% | 75.0% | 0.354 | 91.7% | 100.0% | 100.0% | 0.944 | 25.0% | 50.0% | 75.0% | 25.0% | 25.0% | 10.0% | 7.5% | 25.0% |
| cross-language | 65 | 23.8% | 63.8% | 79.2% | 0.454 | 55.4% | 87.7% | 95.4% | 0.693 | 24.6% | 65.3% | 81.0% | 24.6% | 26.2% | 14.5% | 9.1% | 26.9% |
| same-language | 202 | 34.2% | 65.8% | 77.0% | 0.503 | 67.3% | 89.6% | 95.5% | 0.777 | 34.0% | 66.0% | 77.1% | 34.7% | 36.6% | 14.1% | 8.3% | 34.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4520, m014 0.4148, m015 0.4028)
retrieval: embedding


## 2026-10-07T12:02:57+00:00 — benchmark sweep2_models: merge-1800-granite-embedding-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__granite-embedding-4d284af0.json` — 2,850 chunks, granite-embedding (384d), built 2026-10-07T12:02:57+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 18.9% | 45.3% | 57.3% | 0.323 | 50.2% | 74.2% | 79.8% | 0.603 | 18.9% | 46.4% | 58.3% | 21.7% | 20.6% | 10.2% | 6.5% | 19.9% |
| en | 169 | 21.6% | 51.5% | 62.1% | 0.357 | 55.6% | 73.4% | 78.1% | 0.635 | 21.9% | 52.3% | 63.1% | 24.6% | 23.1% | 11.1% | 6.9% | 22.2% |
| es | 98 | 14.3% | 34.7% | 49.0% | 0.266 | 40.8% | 75.5% | 82.7% | 0.547 | 13.9% | 36.1% | 50.1% | 16.7% | 16.3% | 8.6% | 5.8% | 15.8% |
| synthetic | 255 | 18.8% | 45.3% | 56.5% | 0.321 | 49.0% | 72.9% | 78.8% | 0.592 | 18.9% | 46.4% | 57.5% | 21.7% | 20.4% | 10.2% | 6.4% | 19.8% |
| manual | 12 | 20.8% | 45.8% | 75.0% | 0.365 | 75.0% | 100.0% | 100.0% | 0.840 | 20.8% | 45.8% | 75.0% | 20.8% | 25.0% | 10.0% | 8.3% | 20.8% |
| cross-language | 65 | 6.9% | 20.0% | 30.8% | 0.137 | 26.2% | 47.7% | 52.3% | 0.356 | 6.5% | 20.0% | 30.8% | 7.7% | 7.7% | 4.6% | 3.4% | 6.9% |
| same-language | 202 | 22.8% | 53.5% | 65.8% | 0.383 | 57.9% | 82.7% | 88.6% | 0.682 | 22.9% | 54.9% | 67.2% | 26.2% | 24.8% | 12.0% | 7.5% | 24.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 3/3 (100.0%) (top-1: m013 0.7594, m014 0.6993, m015 0.7733)
retrieval: embedding


## 2026-10-07T12:03:08+00:00 — benchmark sweep2_models: merge-1200-granite-embedding-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__granite-embedding-4d284af0.json` — 4,488 chunks, granite-embedding (384d), built 2026-10-07T12:03:08+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 20.6% | 41.5% | 52.9% | 0.313 | 49.4% | 76.4% | 79.8% | 0.603 | 21.3% | 42.7% | 54.1% | 30.0% | 21.3% | 8.6% | 5.5% | 21.1% |
| en | 169 | 22.5% | 48.2% | 57.7% | 0.345 | 54.4% | 74.6% | 78.7% | 0.634 | 23.1% | 49.1% | 58.6% | 35.5% | 23.1% | 9.9% | 6.0% | 23.1% |
| es | 98 | 17.3% | 29.9% | 44.7% | 0.259 | 40.8% | 79.6% | 81.6% | 0.550 | 18.4% | 31.6% | 46.3% | 20.4% | 18.4% | 6.3% | 4.7% | 17.7% |
| synthetic | 255 | 20.4% | 41.1% | 51.9% | 0.309 | 48.2% | 75.7% | 78.8% | 0.592 | 21.2% | 42.4% | 53.1% | 29.8% | 21.2% | 8.5% | 5.4% | 20.9% |
| manual | 12 | 25.0% | 50.0% | 75.0% | 0.394 | 75.0% | 91.7% | 100.0% | 0.847 | 25.0% | 50.0% | 75.0% | 33.3% | 25.0% | 10.0% | 7.5% | 25.0% |
| cross-language | 65 | 4.6% | 16.9% | 32.3% | 0.111 | 26.2% | 50.8% | 55.4% | 0.372 | 4.6% | 16.9% | 32.3% | 6.2% | 4.6% | 3.4% | 3.2% | 4.6% |
| same-language | 202 | 25.7% | 49.4% | 59.6% | 0.378 | 56.9% | 84.7% | 87.6% | 0.678 | 26.7% | 51.0% | 61.1% | 37.6% | 26.7% | 10.3% | 6.2% | 26.4% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 3/3 (100.0%) (top-1: m013 0.7276, m014 0.6911, m015 0.7733)
retrieval: embedding


## 2026-10-07T12:03:22+00:00 — benchmark sweep2_models: merge-2400-granite-embedding-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__granite-embedding-4d284af0.json` — 2,069 chunks, granite-embedding (384d), built 2026-10-07T12:03:22+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 19.7% | 42.7% | 54.1% | 0.319 | 48.7% | 73.4% | 80.1% | 0.598 | 19.9% | 42.8% | 54.2% | 20.5% | 21.0% | 9.2% | 5.8% | 20.8% |
| en | 169 | 19.2% | 44.4% | 58.3% | 0.327 | 52.1% | 72.8% | 78.1% | 0.614 | 19.3% | 44.3% | 58.3% | 19.9% | 20.7% | 9.6% | 6.3% | 20.4% |
| es | 98 | 20.4% | 39.8% | 46.9% | 0.307 | 42.9% | 74.5% | 83.7% | 0.570 | 20.9% | 40.3% | 47.3% | 21.4% | 21.4% | 8.6% | 5.1% | 21.4% |
| synthetic | 255 | 20.2% | 41.6% | 53.5% | 0.320 | 48.2% | 72.5% | 79.2% | 0.592 | 20.5% | 41.7% | 53.7% | 21.0% | 21.6% | 9.0% | 5.8% | 21.4% |
| manual | 12 | 8.3% | 66.7% | 66.7% | 0.299 | 58.3% | 91.7% | 100.0% | 0.726 | 8.3% | 66.7% | 66.7% | 8.3% | 8.3% | 13.3% | 6.7% | 8.3% |
| cross-language | 65 | 13.1% | 29.2% | 32.3% | 0.202 | 26.2% | 47.7% | 52.3% | 0.359 | 13.6% | 29.5% | 32.6% | 13.6% | 13.8% | 6.5% | 3.5% | 13.8% |
| same-language | 202 | 21.8% | 47.0% | 61.1% | 0.357 | 55.9% | 81.7% | 89.1% | 0.675 | 21.9% | 47.1% | 61.2% | 22.7% | 23.3% | 10.1% | 6.6% | 23.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 3/3 (100.0%) (top-1: m013 0.7300, m014 0.6902, m015 0.7733)
retrieval: embedding


## 2026-10-07T12:03:31+00:00 — benchmark sweep2_models: merge-1800-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__snowflake-arctic-embed2-4d284af0.json` — 2,850 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-07T12:03:32+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.8% | 68.7% | 77.7% | 0.512 | 62.9% | 92.5% | 95.5% | 0.757 | 32.6% | 70.7% | 79.4% | 39.1% | 35.2% | 15.7% | 8.9% | 33.9% |
| en | 169 | 32.5% | 71.0% | 81.4% | 0.522 | 64.5% | 92.3% | 95.3% | 0.766 | 33.1% | 72.5% | 82.5% | 40.8% | 34.9% | 15.7% | 9.1% | 34.3% |
| es | 98 | 30.6% | 64.8% | 71.4% | 0.495 | 60.2% | 92.9% | 95.9% | 0.741 | 31.7% | 67.6% | 74.0% | 36.0% | 35.7% | 15.5% | 8.6% | 33.2% |
| synthetic | 255 | 32.4% | 68.6% | 77.5% | 0.514 | 62.0% | 92.2% | 95.3% | 0.749 | 33.1% | 70.7% | 79.2% | 39.1% | 35.7% | 15.7% | 8.9% | 34.5% |
| manual | 12 | 20.8% | 70.8% | 83.3% | 0.476 | 83.3% | 100.0% | 100.0% | 0.917 | 20.8% | 70.8% | 83.3% | 37.5% | 25.0% | 15.0% | 9.2% | 20.8% |
| cross-language | 65 | 23.1% | 62.3% | 76.9% | 0.464 | 52.3% | 95.4% | 98.5% | 0.707 | 24.7% | 65.4% | 79.7% | 32.8% | 27.7% | 14.8% | 8.9% | 25.4% |
| same-language | 202 | 34.7% | 70.8% | 78.0% | 0.528 | 66.3% | 91.6% | 94.6% | 0.773 | 35.1% | 72.4% | 79.3% | 41.1% | 37.6% | 15.9% | 8.9% | 36.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.3947, m014 0.3921, m015 0.3506)
retrieval: embedding


## 2026-10-07T12:04:02+00:00 — benchmark sweep2_models: merge-1200-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__snowflake-arctic-embed2-4d284af0.json` — 4,488 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-07T12:04:02+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 37.3% | 63.8% | 75.0% | 0.515 | 64.8% | 89.9% | 94.8% | 0.754 | 38.8% | 66.0% | 77.1% | 50.7% | 39.3% | 13.7% | 8.1% | 38.6% |
| en | 169 | 37.3% | 63.6% | 76.9% | 0.509 | 67.5% | 89.3% | 94.1% | 0.765 | 38.1% | 65.1% | 78.4% | 49.7% | 38.5% | 13.5% | 8.2% | 38.8% |
| es | 98 | 37.4% | 64.1% | 71.8% | 0.525 | 60.2% | 90.8% | 95.9% | 0.736 | 40.1% | 67.7% | 74.8% | 52.4% | 40.8% | 14.1% | 7.9% | 38.3% |
| synthetic | 255 | 37.5% | 64.1% | 74.6% | 0.517 | 63.9% | 89.4% | 94.5% | 0.747 | 39.1% | 66.4% | 76.8% | 50.7% | 39.6% | 13.8% | 8.1% | 38.8% |
| manual | 12 | 33.3% | 58.3% | 83.3% | 0.476 | 83.3% | 100.0% | 100.0% | 0.903 | 33.3% | 58.3% | 83.3% | 50.0% | 33.3% | 11.7% | 8.3% | 33.3% |
| cross-language | 65 | 30.3% | 60.8% | 73.1% | 0.468 | 53.8% | 89.2% | 93.8% | 0.681 | 32.8% | 63.1% | 76.2% | 41.5% | 33.8% | 13.5% | 8.2% | 31.5% |
| same-language | 202 | 39.6% | 64.8% | 75.7% | 0.530 | 68.3% | 90.1% | 95.0% | 0.778 | 40.8% | 67.0% | 77.4% | 53.6% | 41.1% | 13.8% | 8.1% | 40.8% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4227, m014 0.4076, m015 0.3614)
retrieval: embedding


## 2026-10-07T12:04:40+00:00 — benchmark sweep2_models: merge-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__snowflake-arctic-embed2-4d284af0.json` — 2,069 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-07T12:04:40+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 32.2% | 65.9% | 74.5% | 0.499 | 62.9% | 91.8% | 94.8% | 0.752 | 32.9% | 66.4% | 75.0% | 33.8% | 35.2% | 14.5% | 8.2% | 33.9% |
| en | 169 | 30.5% | 67.2% | 77.8% | 0.494 | 64.5% | 91.7% | 95.3% | 0.759 | 31.0% | 67.1% | 77.7% | 31.0% | 33.7% | 14.7% | 8.4% | 31.7% |
| es | 98 | 35.2% | 63.8% | 68.9% | 0.508 | 60.2% | 91.8% | 93.9% | 0.740 | 36.2% | 65.3% | 70.4% | 38.8% | 37.8% | 14.3% | 7.8% | 37.8% |
| synthetic | 255 | 32.5% | 66.7% | 74.5% | 0.504 | 62.0% | 91.4% | 94.5% | 0.744 | 33.3% | 67.2% | 75.0% | 34.2% | 35.7% | 14.7% | 8.2% | 34.3% |
| manual | 12 | 25.0% | 50.0% | 75.0% | 0.406 | 83.3% | 100.0% | 100.0% | 0.917 | 25.0% | 50.0% | 75.0% | 25.0% | 25.0% | 10.0% | 7.5% | 25.0% |
| cross-language | 65 | 23.1% | 72.3% | 78.5% | 0.464 | 53.8% | 93.8% | 98.5% | 0.703 | 26.2% | 74.1% | 80.3% | 24.6% | 27.7% | 16.6% | 8.9% | 25.4% |
| same-language | 202 | 35.1% | 63.9% | 73.3% | 0.511 | 65.8% | 91.1% | 93.6% | 0.768 | 35.1% | 63.9% | 73.3% | 36.8% | 37.6% | 13.9% | 7.9% | 36.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4549, m014 0.3758, m015 0.3697)
retrieval: embedding


## 2026-10-07T12:05:06+00:00 — benchmark sweep2_models: merge-1800-mxbai-embed-large-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__mxbai-embed-large-4d284af0.json` — 2,850 chunks, mxbai-embed-large (1024d), built 2026-10-07T12:05:11+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 23.8% | 50.7% | 62.5% | 0.392 | 52.1% | 76.8% | 82.8% | 0.633 | 24.1% | 51.8% | 63.4% | 29.7% | 26.6% | 11.8% | 7.2% | 24.5% |
| en | 169 | 28.4% | 56.8% | 66.6% | 0.440 | 55.6% | 76.3% | 80.5% | 0.657 | 28.8% | 57.9% | 67.4% | 33.8% | 30.8% | 12.8% | 7.5% | 29.3% |
| es | 98 | 15.8% | 40.3% | 55.6% | 0.308 | 45.9% | 77.6% | 86.7% | 0.592 | 16.1% | 41.3% | 56.5% | 22.4% | 19.4% | 10.0% | 6.7% | 16.3% |
| synthetic | 255 | 23.9% | 51.4% | 62.0% | 0.392 | 51.4% | 75.7% | 82.0% | 0.625 | 24.3% | 52.5% | 62.9% | 29.3% | 26.7% | 11.9% | 7.1% | 24.7% |
| manual | 12 | 20.8% | 37.5% | 75.0% | 0.383 | 66.7% | 100.0% | 100.0% | 0.799 | 20.8% | 37.5% | 75.0% | 37.5% | 25.0% | 8.3% | 8.3% | 20.8% |
| cross-language | 65 | 9.2% | 23.1% | 33.8% | 0.187 | 27.7% | 49.2% | 55.4% | 0.381 | 9.1% | 24.1% | 34.9% | 12.6% | 10.8% | 5.5% | 3.8% | 10.0% |
| same-language | 202 | 28.5% | 59.7% | 71.8% | 0.458 | 59.9% | 85.6% | 91.6% | 0.714 | 29.0% | 60.7% | 72.6% | 35.1% | 31.7% | 13.8% | 8.3% | 29.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 3/3 (100.0%) (top-1: m013 0.6295, m014 0.5605, m015 0.6120)
retrieval: embedding


## 2026-10-07T12:05:39+00:00 — benchmark sweep2_models: merge-1200-mxbai-embed-large-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__mxbai-embed-large-4d284af0.json` — 4,488 chunks, mxbai-embed-large (1024d), built 2026-10-07T12:05:39+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 22.1% | 48.6% | 60.7% | 0.366 | 52.8% | 76.8% | 83.9% | 0.636 | 23.3% | 50.3% | 62.7% | 37.6% | 23.6% | 10.3% | 6.4% | 22.3% |
| en | 169 | 27.5% | 54.7% | 64.5% | 0.416 | 57.4% | 76.9% | 81.1% | 0.662 | 28.4% | 55.6% | 65.7% | 43.8% | 28.4% | 11.4% | 6.7% | 27.5% |
| es | 98 | 12.8% | 37.9% | 54.3% | 0.278 | 44.9% | 76.5% | 88.8% | 0.591 | 14.6% | 41.2% | 57.5% | 26.9% | 15.3% | 8.4% | 5.8% | 13.4% |
| synthetic | 255 | 22.4% | 49.7% | 60.8% | 0.370 | 52.2% | 76.1% | 83.1% | 0.631 | 23.7% | 51.5% | 62.9% | 38.2% | 23.9% | 10.5% | 6.4% | 22.6% |
| manual | 12 | 16.7% | 25.0% | 58.3% | 0.271 | 66.7% | 91.7% | 100.0% | 0.750 | 16.7% | 25.0% | 58.3% | 25.0% | 16.7% | 5.0% | 5.8% | 16.7% |
| cross-language | 65 | 6.2% | 22.1% | 34.4% | 0.155 | 24.6% | 50.8% | 56.9% | 0.358 | 6.2% | 23.1% | 35.4% | 15.4% | 6.2% | 4.6% | 3.5% | 6.7% |
| same-language | 202 | 27.2% | 57.1% | 69.2% | 0.433 | 61.9% | 85.1% | 92.6% | 0.725 | 28.9% | 59.1% | 71.5% | 44.7% | 29.2% | 12.1% | 7.3% | 27.4% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 3/3 (100.0%) (top-1: m013 0.6527, m014 0.5549, m015 0.6179)
retrieval: embedding


## 2026-10-07T12:06:17+00:00 — benchmark sweep2_models: merge-2400-mxbai-embed-large-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__mxbai-embed-large-4d284af0.json` — 2,069 chunks, mxbai-embed-large (1024d), built 2026-10-07T12:06:17+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 21.7% | 49.4% | 57.9% | 0.364 | 52.8% | 75.7% | 81.6% | 0.629 | 21.5% | 49.8% | 58.2% | 22.5% | 23.2% | 10.7% | 6.3% | 23.4% |
| en | 169 | 24.3% | 54.4% | 61.2% | 0.397 | 55.6% | 75.1% | 78.7% | 0.643 | 24.0% | 54.3% | 61.2% | 24.6% | 26.0% | 11.7% | 6.6% | 25.4% |
| es | 98 | 17.3% | 40.8% | 52.0% | 0.306 | 48.0% | 76.5% | 86.7% | 0.605 | 17.3% | 41.8% | 53.1% | 18.9% | 18.4% | 9.0% | 5.7% | 19.9% |
| synthetic | 255 | 22.0% | 49.0% | 57.5% | 0.364 | 51.8% | 74.5% | 80.8% | 0.619 | 21.8% | 49.3% | 57.8% | 22.7% | 23.5% | 10.7% | 6.2% | 23.7% |
| manual | 12 | 16.7% | 58.3% | 66.7% | 0.346 | 75.0% | 100.0% | 100.0% | 0.840 | 16.7% | 58.3% | 66.7% | 16.7% | 16.7% | 11.7% | 6.7% | 16.7% |
| cross-language | 65 | 8.5% | 27.7% | 32.3% | 0.188 | 27.7% | 49.2% | 55.4% | 0.382 | 7.9% | 28.7% | 33.3% | 7.9% | 9.2% | 6.2% | 3.5% | 10.0% |
| same-language | 202 | 26.0% | 56.4% | 66.1% | 0.420 | 60.9% | 84.2% | 90.1% | 0.708 | 25.9% | 56.5% | 66.3% | 27.1% | 27.7% | 12.2% | 7.1% | 27.7% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 2/3 (66.7%) (top-1: m013 0.6161, m014 0.5491, m015 0.6120)
retrieval: embedding


## 2026-10-07T12:06:39+00:00 — benchmark sweep2_models — comparison (21 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| merge-1800-bge-m3-embedding | bge-m3 | 1800/0.15/on | embedding | 267 | 30.0% | 65.9% | 75.7% | 0.490 | 62.5% | 89.5% | 92.5% | 0.746 | 30.8% | 67.9% | 77.4% | 36.1% | 33.0% | 14.9% | 8.7% | 32.0% | 0/3 | 27s / 2.5s |
| merge-1200-bge-m3-embedding | bge-m3 | 1200/0.15/on | embedding | 267 | 31.4% | 62.8% | 73.5% | 0.479 | 62.9% | 91.8% | 93.6% | 0.751 | 32.7% | 64.9% | 75.7% | 49.3% | 33.0% | 13.4% | 7.9% | 32.8% | 0/3 | 36s / 2.9s |
| merge-2400-bge-m3-embedding | bge-m3 | 2400/0.15/on | embedding | 267 | 29.6% | 63.5% | 71.2% | 0.465 | 59.6% | 89.1% | 93.3% | 0.722 | 29.7% | 64.0% | 71.7% | 29.7% | 31.5% | 13.6% | 7.8% | 30.3% | 0/3 | 25s / 2.1s |
| merge-1800-nomic-embed-text-v2-moe-embedding | nomic-embed-text-v2-moe | 1800/0.15/on | embedding | 267 | 33.0% | 65.7% | 78.3% | 0.508 | 63.3% | 88.4% | 95.1% | 0.745 | 33.7% | 67.4% | 79.6% | 38.9% | 36.3% | 15.0% | 9.0% | 34.6% | 0/3 | 22s / 2.4s |
| merge-1200-nomic-embed-text-v2-moe-embedding | nomic-embed-text-v2-moe | 1200/0.15/on | embedding | 267 | 34.3% | 63.6% | 78.0% | 0.498 | 65.9% | 91.4% | 94.8% | 0.763 | 36.5% | 65.7% | 80.0% | 49.6% | 36.7% | 13.7% | 8.4% | 35.3% | 0/3 | 28s / 2.6s |
| merge-2400-nomic-embed-text-v2-moe-embedding | nomic-embed-text-v2-moe | 2400/0.15/on | embedding | 267 | 30.3% | 66.5% | 74.2% | 0.476 | 58.8% | 89.1% | 92.9% | 0.717 | 30.5% | 66.8% | 74.6% | 31.0% | 32.2% | 14.4% | 8.1% | 31.5% | 0/3 | 18s / 2.2s |
| merge-1800-qwen3-embedding-8b-embedding | qwen3-embedding:8b | 1800/0.15/on | embedding | 267 | 31.6% | 66.5% | 82.4% | 0.514 | 66.3% | 94.0% | 97.4% | 0.784 | 32.8% | 68.0% | 83.4% | 38.3% | 35.2% | 15.1% | 9.4% | 33.0% | 1/3 | 280s / 12.3s |
| merge-1200-qwen3-embedding-8b-embedding | qwen3-embedding:8b | 1200/0.15/on | embedding | 267 | 39.7% | 70.7% | 83.3% | 0.558 | 67.4% | 95.1% | 97.8% | 0.794 | 41.4% | 73.6% | 85.7% | 57.2% | 41.6% | 15.2% | 9.0% | 41.1% | 2/3 | 329s / 12.1s |
| merge-2400-qwen3-embedding-8b-embedding | qwen3-embedding:8b | 2400/0.15/on | embedding | 267 | 35.8% | 67.6% | 76.6% | 0.533 | 64.4% | 91.8% | 95.1% | 0.764 | 36.0% | 68.0% | 77.0% | 36.6% | 39.0% | 15.0% | 8.5% | 37.8% | 1/3 | 258s / 7.4s |
| merge-1800-embeddinggemma-embedding | embeddinggemma | 1800/0.15/on | embedding | 267 | 35.0% | 69.1% | 80.3% | 0.541 | 65.5% | 93.3% | 97.0% | 0.774 | 36.1% | 70.7% | 81.9% | 40.7% | 39.0% | 15.4% | 9.1% | 36.7% | 0/3 | 25s / 2.0s |
| merge-1200-embeddinggemma-embedding | embeddinggemma | 1200/0.15/on | embedding | 267 | 37.2% | 65.2% | 79.5% | 0.528 | 67.8% | 92.9% | 97.8% | 0.787 | 38.8% | 67.4% | 81.6% | 54.3% | 39.3% | 13.9% | 8.5% | 37.7% | 0/3 | 29s / 2.4s |
| merge-2400-embeddinggemma-embedding | embeddinggemma | 2400/0.15/on | embedding | 267 | 31.6% | 65.4% | 77.5% | 0.491 | 64.4% | 89.1% | 95.5% | 0.757 | 31.7% | 65.8% | 78.0% | 32.3% | 34.1% | 14.2% | 8.5% | 33.0% | 0/3 | 21s / 2.0s |
| merge-1800-granite-embedding-embedding | granite-embedding | 1800/0.15/on | embedding | 267 | 18.9% | 45.3% | 57.3% | 0.323 | 50.2% | 74.2% | 79.8% | 0.603 | 18.9% | 46.4% | 58.3% | 21.7% | 20.6% | 10.2% | 6.5% | 19.9% | 3/3 | 9s / 1.6s |
| merge-1200-granite-embedding-embedding | granite-embedding | 1200/0.15/on | embedding | 267 | 20.6% | 41.5% | 52.9% | 0.313 | 49.4% | 76.4% | 79.8% | 0.603 | 21.3% | 42.7% | 54.1% | 30.0% | 21.3% | 8.6% | 5.5% | 21.1% | 3/3 | 12s / 1.8s |
| merge-2400-granite-embedding-embedding | granite-embedding | 2400/0.15/on | embedding | 267 | 19.7% | 42.7% | 54.1% | 0.319 | 48.7% | 73.4% | 80.1% | 0.598 | 19.9% | 42.8% | 54.2% | 20.5% | 21.0% | 9.2% | 5.8% | 20.8% | 3/3 | 7s / 1.6s |
| merge-1800-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1800/0.15/on | embedding | 267 | 31.8% | 68.7% | 77.7% | 0.512 | 62.9% | 92.5% | 95.5% | 0.757 | 32.6% | 70.7% | 79.4% | 39.1% | 35.2% | 15.7% | 8.9% | 33.9% | 0/3 | 27s / 2.4s |
| merge-1200-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1200/0.15/on | embedding | 267 | 37.3% | 63.8% | 75.0% | 0.515 | 64.8% | 89.9% | 94.8% | 0.754 | 38.8% | 66.0% | 77.1% | 50.7% | 39.3% | 13.7% | 8.1% | 38.6% | 0/3 | 34s / 3.0s |
| merge-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0.15/on | embedding | 267 | 32.2% | 65.9% | 74.5% | 0.499 | 62.9% | 91.8% | 94.8% | 0.752 | 32.9% | 66.4% | 75.0% | 33.8% | 35.2% | 14.5% | 8.2% | 33.9% | 0/3 | 23s / 2.3s |
| merge-1800-mxbai-embed-large-embedding | mxbai-embed-large | 1800/0.15/on | embedding | 267 | 23.8% | 50.7% | 62.5% | 0.392 | 52.1% | 76.8% | 82.8% | 0.633 | 24.1% | 51.8% | 63.4% | 29.7% | 26.6% | 11.8% | 7.2% | 24.5% | 3/3 | 25s / 2.4s |
| merge-1200-mxbai-embed-large-embedding | mxbai-embed-large | 1200/0.15/on | embedding | 267 | 22.1% | 48.6% | 60.7% | 0.366 | 52.8% | 76.8% | 83.9% | 0.636 | 23.3% | 50.3% | 62.7% | 37.6% | 23.6% | 10.3% | 6.4% | 22.3% | 3/3 | 33s / 3.0s |
| merge-2400-mxbai-embed-large-embedding | mxbai-embed-large | 2400/0.15/on | embedding | 267 | 21.7% | 49.4% | 57.9% | 0.364 | 52.8% | 75.7% | 81.6% | 0.629 | 21.5% | 49.8% | 58.2% | 22.5% | 23.2% | 10.7% | 6.3% | 23.4% | 2/3 | 20s / 2.1s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes


## 2026-10-08T12:44:28+00:00 — benchmark sweep_legalbenchrag_privacyqa — resolved plan

plan    : sweep_legalbenchrag_privacyqa — 14 experiment(s) over 14 store cell(s)
dataset : legalbenchrag-privacyqa
captures: data/raw/8a3f38ffd23a75e2 — 7 capture(s)
golden  : data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl — 199 row(s)
stores  :
  baseline-bge-m3        merge 1800/0.15/on     × bge-m3                       → data/benchmark_stores/merge-1800-0.15-on__bge-m3-260a60f1.json
  merge-2400-bge-m3      merge 2400/0.15/on     × bge-m3                       → data/benchmark_stores/merge-2400-0.15-on__bge-m3-260a60f1.json
  baseline-qwen3-embedding-8b merge 1800/0.15/on     × qwen3-embedding:8b           → data/benchmark_stores/merge-1800-0.15-on__qwen3-embedding-8b-260a60f1.json
  merge-2400-qwen3-embedding-8b merge 2400/0.15/on     × qwen3-embedding:8b           → data/benchmark_stores/merge-2400-0.15-on__qwen3-embedding-8b-260a60f1.json
  baseline-nomic-embed-text-v2-moe merge 1800/0.15/on     × nomic-embed-text-v2-moe      → data/benchmark_stores/merge-1800-0.15-on__nomic-embed-text-v2-moe-260a60f1.json
  merge-2400-nomic-embed-text-v2-moe merge 2400/0.15/on     × nomic-embed-text-v2-moe      → data/benchmark_stores/merge-2400-0.15-on__nomic-embed-text-v2-moe-260a60f1.json
  baseline-embeddinggemma merge 1800/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-1800-0.15-on__embeddinggemma-260a60f1.json
  merge-2400-embeddinggemma merge 2400/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-2400-0.15-on__embeddinggemma-260a60f1.json
  baseline-granite-embedding merge 1800/0.15/on     × granite-embedding            → data/benchmark_stores/merge-1800-0.15-on__granite-embedding-260a60f1.json
  merge-2400-granite-embedding merge 2400/0.15/on     × granite-embedding            → data/benchmark_stores/merge-2400-0.15-on__granite-embedding-260a60f1.json
  baseline-snowflake-arctic-embed2 merge 1800/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-1800-0.15-on__snowflake-arctic-embed2-260a60f1.json
  merge-2400-snowflake-arctic-embed2 merge 2400/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-2400-0.15-on__snowflake-arctic-embed2-260a60f1.json
  baseline-mxbai-embed-large merge 1800/0.15/on     × mxbai-embed-large            → data/benchmark_stores/merge-1800-0.15-on__mxbai-embed-large-260a60f1.json
  merge-2400-mxbai-embed-large merge 2400/0.15/on     × mxbai-embed-large            → data/benchmark_stores/merge-2400-0.15-on__mxbai-embed-large-260a60f1.json
experiments:
  1. baseline-bge-m3-embedding    → baseline-bge-m3        retrieval embedding
  2. merge-2400-bge-m3-embedding  → merge-2400-bge-m3      retrieval embedding
  3. baseline-qwen3-embedding-8b-embedding → baseline-qwen3-embedding-8b retrieval embedding
  4. merge-2400-qwen3-embedding-8b-embedding → merge-2400-qwen3-embedding-8b retrieval embedding
  5. baseline-nomic-embed-text-v2-moe-embedding → baseline-nomic-embed-text-v2-moe retrieval embedding
  6. merge-2400-nomic-embed-text-v2-moe-embedding → merge-2400-nomic-embed-text-v2-moe retrieval embedding
  7. baseline-embeddinggemma-embedding → baseline-embeddinggemma retrieval embedding
  8. merge-2400-embeddinggemma-embedding → merge-2400-embeddinggemma retrieval embedding
  9. baseline-granite-embedding-embedding → baseline-granite-embedding retrieval embedding
  10. merge-2400-granite-embedding-embedding → merge-2400-granite-embedding retrieval embedding
  11. baseline-snowflake-arctic-embed2-embedding → baseline-snowflake-arctic-embed2 retrieval embedding
  12. merge-2400-snowflake-arctic-embed2-embedding → merge-2400-snowflake-arctic-embed2 retrieval embedding
  13. baseline-mxbai-embed-large-embedding → baseline-mxbai-embed-large retrieval embedding
  14. merge-2400-mxbai-embed-large-embedding → merge-2400-mxbai-embed-large retrieval embedding


## 2026-10-08T12:44:28+00:00 — benchmark sweep_legalbenchrag_privacyqa: baseline-bge-m3-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__bge-m3-260a60f1.json` — 106 chunks, bge-m3 (1024d), built 2026-10-08T12:44:30+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 32.5% | 72.6% | 89.8% | 0.696 | 100.0% | 100.0% | 100.0% | 1.000 | 34.4% | 75.0% | 91.4% | 34.4% | 53.6% | 27.2% | 18.1% | 46.2% |
| en | 194 | 32.5% | 72.6% | 89.8% | 0.696 | 100.0% | 100.0% | 100.0% | 1.000 | 34.4% | 75.0% | 91.4% | 34.4% | 53.6% | 27.2% | 18.1% | 46.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 32.5% | 72.6% | 89.8% | 0.696 | 100.0% | 100.0% | 100.0% | 1.000 | 34.4% | 75.0% | 91.4% | 34.4% | 53.6% | 27.2% | 18.1% | 46.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 1/5 (20.0%) (top-1: m001 0.4383, m002 0.5036, m003 0.4775, m004 0.5023, m005 0.5518)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-08T12:44:33+00:00 — benchmark sweep_legalbenchrag_privacyqa: merge-2400-bge-m3-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__bge-m3-260a60f1.json` — 79 chunks, bge-m3 (1024d), built 2026-10-08T12:44:33+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 36.2% | 82.5% | 95.5% | 0.752 | 100.0% | 100.0% | 100.0% | 1.000 | 38.4% | 81.6% | 95.5% | 38.4% | 59.8% | 30.2% | 18.2% | 53.0% |
| en | 194 | 36.2% | 82.5% | 95.5% | 0.752 | 100.0% | 100.0% | 100.0% | 1.000 | 38.4% | 81.6% | 95.5% | 38.4% | 59.8% | 30.2% | 18.2% | 53.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 36.2% | 82.5% | 95.5% | 0.752 | 100.0% | 100.0% | 100.0% | 1.000 | 38.4% | 81.6% | 95.5% | 38.4% | 59.8% | 30.2% | 18.2% | 53.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 1/5 (20.0%) (top-1: m001 0.4335, m002 0.5098, m003 0.4798, m004 0.5167, m005 0.5676)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-08T12:44:35+00:00 — benchmark sweep_legalbenchrag_privacyqa: baseline-qwen3-embedding-8b-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__qwen3-embedding-8b-260a60f1.json` — 106 chunks, qwen3-embedding:8b (4096d), built 2026-10-08T12:44:37+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 36.1% | 74.3% | 90.4% | 0.724 | 100.0% | 100.0% | 100.0% | 1.000 | 38.5% | 76.8% | 90.9% | 39.8% | 58.8% | 27.8% | 18.2% | 51.7% |
| en | 194 | 36.1% | 74.3% | 90.4% | 0.724 | 100.0% | 100.0% | 100.0% | 1.000 | 38.5% | 76.8% | 90.9% | 39.8% | 58.8% | 27.8% | 18.2% | 51.7% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 36.1% | 74.3% | 90.4% | 0.724 | 100.0% | 100.0% | 100.0% | 1.000 | 38.5% | 76.8% | 90.9% | 39.8% | 58.8% | 27.8% | 18.2% | 51.7% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 3/5 (60.0%) (top-1: m001 0.5828, m002 0.5757, m003 0.4824, m004 0.5736, m005 0.5471)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-08T12:44:49+00:00 — benchmark sweep_legalbenchrag_privacyqa: merge-2400-qwen3-embedding-8b-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__qwen3-embedding-8b-260a60f1.json` — 79 chunks, qwen3-embedding:8b (4096d), built 2026-10-08T12:44:49+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 34.6% | 81.4% | 94.1% | 0.715 | 100.0% | 100.0% | 100.0% | 1.000 | 35.9% | 83.8% | 93.4% | 35.9% | 52.6% | 29.6% | 18.0% | 54.3% |
| en | 194 | 34.6% | 81.4% | 94.1% | 0.715 | 100.0% | 100.0% | 100.0% | 1.000 | 35.9% | 83.8% | 93.4% | 35.9% | 52.6% | 29.6% | 18.0% | 54.3% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 34.6% | 81.4% | 94.1% | 0.715 | 100.0% | 100.0% | 100.0% | 1.000 | 35.9% | 83.8% | 93.4% | 35.9% | 52.6% | 29.6% | 18.0% | 54.3% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 3/5 (60.0%) (top-1: m001 0.5812, m002 0.6133, m003 0.5007, m004 0.5862, m005 0.5480)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-08T12:45:01+00:00 — benchmark sweep_legalbenchrag_privacyqa: baseline-nomic-embed-text-v2-moe-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__nomic-embed-text-v2-moe-260a60f1.json` — 106 chunks, nomic-embed-text-v2-moe (768d), built 2026-10-08T12:45:03+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 21.7% | 64.3% | 86.0% | 0.587 | 100.0% | 100.0% | 100.0% | 1.000 | 23.5% | 66.5% | 87.1% | 25.3% | 39.7% | 23.9% | 17.0% | 33.1% |
| en | 194 | 21.7% | 64.3% | 86.0% | 0.587 | 100.0% | 100.0% | 100.0% | 1.000 | 23.5% | 66.5% | 87.1% | 25.3% | 39.7% | 23.9% | 17.0% | 33.1% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 21.7% | 64.3% | 86.0% | 0.587 | 100.0% | 100.0% | 100.0% | 1.000 | 23.5% | 66.5% | 87.1% | 25.3% | 39.7% | 23.9% | 17.0% | 33.1% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.3323, m002 0.4110, m003 0.3599, m004 0.4410, m005 0.4471)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-08T12:45:05+00:00 — benchmark sweep_legalbenchrag_privacyqa: merge-2400-nomic-embed-text-v2-moe-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__nomic-embed-text-v2-moe-260a60f1.json` — 79 chunks, nomic-embed-text-v2-moe (768d), built 2026-10-08T12:45:05+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 19.3% | 71.0% | 93.5% | 0.570 | 100.0% | 100.0% | 100.0% | 1.000 | 20.6% | 71.5% | 93.7% | 20.6% | 36.1% | 25.2% | 17.8% | 31.8% |
| en | 194 | 19.3% | 71.0% | 93.5% | 0.570 | 100.0% | 100.0% | 100.0% | 1.000 | 20.6% | 71.5% | 93.7% | 20.6% | 36.1% | 25.2% | 17.8% | 31.8% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 19.3% | 71.0% | 93.5% | 0.570 | 100.0% | 100.0% | 100.0% | 1.000 | 20.6% | 71.5% | 93.7% | 20.6% | 36.1% | 25.2% | 17.8% | 31.8% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.3209, m002 0.4246, m003 0.3536, m004 0.4332, m005 0.4414)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-08T12:45:07+00:00 — benchmark sweep_legalbenchrag_privacyqa: baseline-embeddinggemma-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__embeddinggemma-260a60f1.json` — 106 chunks, embeddinggemma (768d), built 2026-10-08T12:45:08+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 34.8% | 69.5% | 86.8% | 0.694 | 100.0% | 100.0% | 100.0% | 1.000 | 36.4% | 71.8% | 88.5% | 38.5% | 55.7% | 25.9% | 17.1% | 48.0% |
| en | 194 | 34.8% | 69.5% | 86.8% | 0.694 | 100.0% | 100.0% | 100.0% | 1.000 | 36.4% | 71.8% | 88.5% | 38.5% | 55.7% | 25.9% | 17.1% | 48.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 34.8% | 69.5% | 86.8% | 0.694 | 100.0% | 100.0% | 100.0% | 1.000 | 36.4% | 71.8% | 88.5% | 38.5% | 55.7% | 25.9% | 17.1% | 48.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.4503, m002 0.5150, m003 0.3851, m004 0.4273, m005 0.4114)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-08T12:45:10+00:00 — benchmark sweep_legalbenchrag_privacyqa: merge-2400-embeddinggemma-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__embeddinggemma-260a60f1.json` — 79 chunks, embeddinggemma (768d), built 2026-10-08T12:45:11+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 27.1% | 75.3% | 93.9% | 0.665 | 100.0% | 100.0% | 100.0% | 1.000 | 27.6% | 76.6% | 94.8% | 28.4% | 47.4% | 26.5% | 17.8% | 41.2% |
| en | 194 | 27.1% | 75.3% | 93.9% | 0.665 | 100.0% | 100.0% | 100.0% | 1.000 | 27.6% | 76.6% | 94.8% | 28.4% | 47.4% | 26.5% | 17.8% | 41.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 27.1% | 75.3% | 93.9% | 0.665 | 100.0% | 100.0% | 100.0% | 1.000 | 27.6% | 76.6% | 94.8% | 28.4% | 47.4% | 26.5% | 17.8% | 41.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.4271, m002 0.4689, m003 0.3906, m004 0.4205, m005 0.3975)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-08T12:45:13+00:00 — benchmark sweep_legalbenchrag_privacyqa: baseline-granite-embedding-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__granite-embedding-260a60f1.json` — 106 chunks, granite-embedding (384d), built 2026-10-08T12:45:18+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 27.8% | 66.8% | 88.3% | 0.629 | 99.5% | 100.0% | 100.0% | 0.997 | 29.4% | 68.8% | 89.0% | 30.3% | 45.4% | 24.5% | 17.3% | 39.9% |
| en | 194 | 27.8% | 66.8% | 88.3% | 0.629 | 99.5% | 100.0% | 100.0% | 0.997 | 29.4% | 68.8% | 89.0% | 30.3% | 45.4% | 24.5% | 17.3% | 39.9% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 27.8% | 66.8% | 88.3% | 0.629 | 99.5% | 100.0% | 100.0% | 0.997 | 29.4% | 68.8% | 89.0% | 30.3% | 45.4% | 24.5% | 17.3% | 39.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 5/5 (100.0%) (top-1: m001 0.6963, m002 0.6993, m003 0.6866, m004 0.6907, m005 0.7083)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-08T12:45:19+00:00 — benchmark sweep_legalbenchrag_privacyqa: merge-2400-granite-embedding-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__granite-embedding-260a60f1.json` — 79 chunks, granite-embedding (384d), built 2026-10-08T12:45:19+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 27.0% | 65.4% | 90.8% | 0.587 | 99.5% | 100.0% | 100.0% | 0.997 | 28.3% | 67.5% | 91.4% | 28.8% | 39.7% | 23.0% | 17.2% | 38.7% |
| en | 194 | 27.0% | 65.4% | 90.8% | 0.587 | 99.5% | 100.0% | 100.0% | 0.997 | 28.3% | 67.5% | 91.4% | 28.8% | 39.7% | 23.0% | 17.2% | 38.7% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 27.0% | 65.4% | 90.8% | 0.587 | 99.5% | 100.0% | 100.0% | 0.997 | 28.3% | 67.5% | 91.4% | 28.8% | 39.7% | 23.0% | 17.2% | 38.7% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 5/5 (100.0%) (top-1: m001 0.6708, m002 0.7106, m003 0.7175, m004 0.6733, m005 0.7042)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-08T12:45:20+00:00 — benchmark sweep_legalbenchrag_privacyqa: baseline-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__snowflake-arctic-embed2-260a60f1.json` — 106 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-08T12:45:26+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 27.9% | 67.6% | 89.0% | 0.632 | 100.0% | 100.0% | 100.0% | 1.000 | 30.3% | 69.0% | 90.2% | 30.5% | 45.9% | 25.1% | 18.0% | 41.6% |
| en | 194 | 27.9% | 67.6% | 89.0% | 0.632 | 100.0% | 100.0% | 100.0% | 1.000 | 30.3% | 69.0% | 90.2% | 30.5% | 45.9% | 25.1% | 18.0% | 41.6% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 27.9% | 67.6% | 89.0% | 0.632 | 100.0% | 100.0% | 100.0% | 1.000 | 30.3% | 69.0% | 90.2% | 30.5% | 45.9% | 25.1% | 18.0% | 41.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.3593, m002 0.4413, m003 0.3619, m004 0.4118, m005 0.5186)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-08T12:45:29+00:00 — benchmark sweep_legalbenchrag_privacyqa: merge-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__snowflake-arctic-embed2-260a60f1.json` — 79 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-08T12:45:29+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 33.8% | 80.9% | 96.0% | 0.717 | 100.0% | 100.0% | 100.0% | 1.000 | 34.5% | 83.3% | 97.1% | 34.5% | 55.2% | 29.6% | 18.4% | 49.1% |
| en | 194 | 33.8% | 80.9% | 96.0% | 0.717 | 100.0% | 100.0% | 100.0% | 1.000 | 34.5% | 83.3% | 97.1% | 34.5% | 55.2% | 29.6% | 18.4% | 49.1% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 33.8% | 80.9% | 96.0% | 0.717 | 100.0% | 100.0% | 100.0% | 1.000 | 34.5% | 83.3% | 97.1% | 34.5% | 55.2% | 29.6% | 18.4% | 49.1% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.3286, m002 0.4456, m003 0.3651, m004 0.4128, m005 0.5280)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-08T12:45:31+00:00 — benchmark sweep_legalbenchrag_privacyqa: baseline-mxbai-embed-large-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__mxbai-embed-large-260a60f1.json` — 106 chunks, mxbai-embed-large (1024d), built 2026-10-08T12:45:37+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 29.4% | 69.8% | 86.7% | 0.635 | 100.0% | 100.0% | 100.0% | 1.000 | 31.4% | 72.8% | 87.0% | 33.0% | 44.8% | 25.8% | 17.1% | 41.5% |
| en | 194 | 29.4% | 69.8% | 86.7% | 0.635 | 100.0% | 100.0% | 100.0% | 1.000 | 31.4% | 72.8% | 87.0% | 33.0% | 44.8% | 25.8% | 17.1% | 41.5% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 29.4% | 69.8% | 86.7% | 0.635 | 100.0% | 100.0% | 100.0% | 1.000 | 31.4% | 72.8% | 87.0% | 33.0% | 44.8% | 25.8% | 17.1% | 41.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 5/5 (100.0%) (top-1: m001 0.6095, m002 0.6728, m003 0.5686, m004 0.6441, m005 0.6650)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-08T12:45:39+00:00 — benchmark sweep_legalbenchrag_privacyqa: merge-2400-mxbai-embed-large-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__mxbai-embed-large-260a60f1.json` — 79 chunks, mxbai-embed-large (1024d), built 2026-10-08T12:45:39+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 29.2% | 75.4% | 92.9% | 0.630 | 100.0% | 100.0% | 100.0% | 1.000 | 30.4% | 76.0% | 92.1% | 30.4% | 45.9% | 26.9% | 17.6% | 38.4% |
| en | 194 | 29.2% | 75.4% | 92.9% | 0.630 | 100.0% | 100.0% | 100.0% | 1.000 | 30.4% | 76.0% | 92.1% | 30.4% | 45.9% | 26.9% | 17.6% | 38.4% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 29.2% | 75.4% | 92.9% | 0.630 | 100.0% | 100.0% | 100.0% | 1.000 | 30.4% | 76.0% | 92.1% | 30.4% | 45.9% | 26.9% | 17.6% | 38.4% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 5/5 (100.0%) (top-1: m001 0.6129, m002 0.6609, m003 0.5675, m004 0.6150, m005 0.6825)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-08T12:45:41+00:00 — benchmark sweep_legalbenchrag_privacyqa — dataset legalbenchrag-privacyqa — comparison (14 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline-bge-m3-embedding | bge-m3 | 1800/0.15/on | embedding | 194 | 32.5% | 72.6% | 89.8% | 0.696 | 100.0% | 100.0% | 100.0% | 1.000 | 34.4% | 75.0% | 91.4% | 34.4% | 53.6% | 27.2% | 18.1% | 46.2% | 1/5 | 1s / 1.1s |
| merge-2400-bge-m3-embedding | bge-m3 | 2400/0.15/on | embedding | 194 | 36.2% | 82.5% | 95.5% | 0.752 | 100.0% | 100.0% | 100.0% | 1.000 | 38.4% | 81.6% | 95.5% | 38.4% | 59.8% | 30.2% | 18.2% | 53.0% | 1/5 | 1s / 1.0s |
| baseline-qwen3-embedding-8b-embedding | qwen3-embedding:8b | 1800/0.15/on | embedding | 194 | 36.1% | 74.3% | 90.4% | 0.724 | 100.0% | 100.0% | 100.0% | 1.000 | 38.5% | 76.8% | 90.9% | 39.8% | 58.8% | 27.8% | 18.2% | 51.7% | 3/5 | 8s / 3.8s |
| merge-2400-qwen3-embedding-8b-embedding | qwen3-embedding:8b | 2400/0.15/on | embedding | 194 | 34.6% | 81.4% | 94.1% | 0.715 | 100.0% | 100.0% | 100.0% | 1.000 | 35.9% | 83.8% | 93.4% | 35.9% | 52.6% | 29.6% | 18.0% | 54.3% | 3/5 | 8s / 3.8s |
| baseline-nomic-embed-text-v2-moe-embedding | nomic-embed-text-v2-moe | 1800/0.15/on | embedding | 194 | 21.7% | 64.3% | 86.0% | 0.587 | 100.0% | 100.0% | 100.0% | 1.000 | 23.5% | 66.5% | 87.1% | 25.3% | 39.7% | 23.9% | 17.0% | 33.1% | 0/5 | 1s / 0.7s |
| merge-2400-nomic-embed-text-v2-moe-embedding | nomic-embed-text-v2-moe | 2400/0.15/on | embedding | 194 | 19.3% | 71.0% | 93.5% | 0.570 | 100.0% | 100.0% | 100.0% | 1.000 | 20.6% | 71.5% | 93.7% | 20.6% | 36.1% | 25.2% | 17.8% | 31.8% | 0/5 | 1s / 0.7s |
| baseline-embeddinggemma-embedding | embeddinggemma | 1800/0.15/on | embedding | 194 | 34.8% | 69.5% | 86.8% | 0.694 | 100.0% | 100.0% | 100.0% | 1.000 | 36.4% | 71.8% | 88.5% | 38.5% | 55.7% | 25.9% | 17.1% | 48.0% | 0/5 | 1s / 0.9s |
| merge-2400-embeddinggemma-embedding | embeddinggemma | 2400/0.15/on | embedding | 194 | 27.1% | 75.3% | 93.9% | 0.665 | 100.0% | 100.0% | 100.0% | 1.000 | 27.6% | 76.6% | 94.8% | 28.4% | 47.4% | 26.5% | 17.8% | 41.2% | 0/5 | 2s / 0.8s |
| baseline-granite-embedding-embedding | granite-embedding | 1800/0.15/on | embedding | 194 | 27.8% | 66.8% | 88.3% | 0.629 | 99.5% | 100.0% | 100.0% | 0.997 | 29.4% | 68.8% | 89.0% | 30.3% | 45.4% | 24.5% | 17.3% | 39.9% | 5/5 | 1s / 0.4s |
| merge-2400-granite-embedding-embedding | granite-embedding | 2400/0.15/on | embedding | 194 | 27.0% | 65.4% | 90.8% | 0.587 | 99.5% | 100.0% | 100.0% | 0.997 | 28.3% | 67.5% | 91.4% | 28.8% | 39.7% | 23.0% | 17.2% | 38.7% | 5/5 | 0s / 0.3s |
| baseline-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1800/0.15/on | embedding | 194 | 27.9% | 67.6% | 89.0% | 0.632 | 100.0% | 100.0% | 100.0% | 1.000 | 30.3% | 69.0% | 90.2% | 30.5% | 45.9% | 25.1% | 18.0% | 41.6% | 0/5 | 1s / 1.1s |
| merge-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0.15/on | embedding | 194 | 33.8% | 80.9% | 96.0% | 0.717 | 100.0% | 100.0% | 100.0% | 1.000 | 34.5% | 83.3% | 97.1% | 34.5% | 55.2% | 29.6% | 18.4% | 49.1% | 0/5 | 1s / 1.1s |
| baseline-mxbai-embed-large-embedding | mxbai-embed-large | 1800/0.15/on | embedding | 194 | 29.4% | 69.8% | 86.7% | 0.635 | 100.0% | 100.0% | 100.0% | 1.000 | 31.4% | 72.8% | 87.0% | 33.0% | 44.8% | 25.8% | 17.1% | 41.5% | 5/5 | 1s / 1.1s |
| merge-2400-mxbai-embed-large-embedding | mxbai-embed-large | 2400/0.15/on | embedding | 194 | 29.2% | 75.4% | 92.9% | 0.630 | 100.0% | 100.0% | 100.0% | 1.000 | 30.4% | 76.0% | 92.1% | 30.4% | 45.9% | 26.9% | 17.6% | 38.4% | 5/5 | 1s / 1.1s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes


## 2026-10-08T12:48:41+00:00 — benchmark sweep_legalbenchrag_contractnli — resolved plan

plan    : sweep_legalbenchrag_contractnli — 14 experiment(s) over 14 store cell(s)
dataset : legalbenchrag-contractnli
captures: data/raw/d7f14657e7264534 — 95 capture(s)
golden  : data/eval/datasets/legalbenchrag-contractnli/golden.jsonl — 982 row(s)
stores  :
  baseline-bge-m3        merge 1800/0.15/on     × bge-m3                       → data/benchmark_stores/merge-1800-0.15-on__bge-m3-826d4d38.json
  merge-1200-bge-m3      merge 1200/0.15/on     × bge-m3                       → data/benchmark_stores/merge-1200-0.15-on__bge-m3-826d4d38.json
  baseline-qwen3-embedding-8b merge 1800/0.15/on     × qwen3-embedding:8b           → data/benchmark_stores/merge-1800-0.15-on__qwen3-embedding-8b-826d4d38.json
  merge-1200-qwen3-embedding-8b merge 1200/0.15/on     × qwen3-embedding:8b           → data/benchmark_stores/merge-1200-0.15-on__qwen3-embedding-8b-826d4d38.json
  baseline-nomic-embed-text-v2-moe merge 1800/0.15/on     × nomic-embed-text-v2-moe      → data/benchmark_stores/merge-1800-0.15-on__nomic-embed-text-v2-moe-826d4d38.json
  merge-1200-nomic-embed-text-v2-moe merge 1200/0.15/on     × nomic-embed-text-v2-moe      → data/benchmark_stores/merge-1200-0.15-on__nomic-embed-text-v2-moe-826d4d38.json
  baseline-embeddinggemma merge 1800/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-1800-0.15-on__embeddinggemma-826d4d38.json
  merge-1200-embeddinggemma merge 1200/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-1200-0.15-on__embeddinggemma-826d4d38.json
  baseline-granite-embedding merge 1800/0.15/on     × granite-embedding            → data/benchmark_stores/merge-1800-0.15-on__granite-embedding-826d4d38.json
  merge-1200-granite-embedding merge 1200/0.15/on     × granite-embedding            → data/benchmark_stores/merge-1200-0.15-on__granite-embedding-826d4d38.json
  baseline-snowflake-arctic-embed2 merge 1800/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-1800-0.15-on__snowflake-arctic-embed2-826d4d38.json
  merge-1200-snowflake-arctic-embed2 merge 1200/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-1200-0.15-on__snowflake-arctic-embed2-826d4d38.json
  baseline-mxbai-embed-large merge 1800/0.15/on     × mxbai-embed-large            → data/benchmark_stores/merge-1800-0.15-on__mxbai-embed-large-826d4d38.json
  merge-1200-mxbai-embed-large merge 1200/0.15/on     × mxbai-embed-large            → data/benchmark_stores/merge-1200-0.15-on__mxbai-embed-large-826d4d38.json
experiments:
  1. baseline-bge-m3-embedding    → baseline-bge-m3        retrieval embedding
  2. merge-1200-bge-m3-embedding  → merge-1200-bge-m3      retrieval embedding
  3. baseline-qwen3-embedding-8b-embedding → baseline-qwen3-embedding-8b retrieval embedding
  4. merge-1200-qwen3-embedding-8b-embedding → merge-1200-qwen3-embedding-8b retrieval embedding
  5. baseline-nomic-embed-text-v2-moe-embedding → baseline-nomic-embed-text-v2-moe retrieval embedding
  6. merge-1200-nomic-embed-text-v2-moe-embedding → merge-1200-nomic-embed-text-v2-moe retrieval embedding
  7. baseline-embeddinggemma-embedding → baseline-embeddinggemma retrieval embedding
  8. merge-1200-embeddinggemma-embedding → merge-1200-embeddinggemma retrieval embedding
  9. baseline-granite-embedding-embedding → baseline-granite-embedding retrieval embedding
  10. merge-1200-granite-embedding-embedding → merge-1200-granite-embedding retrieval embedding
  11. baseline-snowflake-arctic-embed2-embedding → baseline-snowflake-arctic-embed2 retrieval embedding
  12. merge-1200-snowflake-arctic-embed2-embedding → merge-1200-snowflake-arctic-embed2 retrieval embedding
  13. baseline-mxbai-embed-large-embedding → baseline-mxbai-embed-large retrieval embedding
  14. merge-1200-mxbai-embed-large-embedding → merge-1200-mxbai-embed-large retrieval embedding


## 2026-10-08T12:48:41+00:00 — benchmark sweep_legalbenchrag_contractnli: baseline-bge-m3-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__bge-m3-826d4d38.json` — 703 chunks, bge-m3 (1024d), built 2026-10-08T12:48:41+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 35.7% | 77.5% | 87.3% | 0.591 | 84.0% | 94.9% | 96.9% | 0.887 | 36.7% | 78.5% | 88.0% | 41.0% | 41.7% | 19.1% | 11.0% | 39.8% |
| en | 977 | 35.7% | 77.5% | 87.3% | 0.591 | 84.0% | 94.9% | 96.9% | 0.887 | 36.7% | 78.5% | 88.0% | 41.0% | 41.7% | 19.1% | 11.0% | 39.8% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 35.7% | 77.5% | 87.3% | 0.591 | 84.0% | 94.9% | 96.9% | 0.887 | 36.7% | 78.5% | 88.0% | 41.0% | 41.7% | 19.1% | 11.0% | 39.8% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 3/5 (60.0%) (top-1: m001 0.6020, m002 0.5827, m003 0.5052, m004 0.5955, m005 0.5354)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-08T12:48:54+00:00 — benchmark sweep_legalbenchrag_contractnli: merge-1200-bge-m3-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__bge-m3-826d4d38.json` — 1,091 chunks, bge-m3 (1024d), built 2026-10-08T12:48:54+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 34.4% | 71.7% | 82.2% | 0.601 | 84.7% | 94.9% | 97.4% | 0.891 | 38.6% | 75.7% | 84.7% | 57.8% | 44.8% | 19.8% | 11.6% | 40.5% |
| en | 977 | 34.4% | 71.7% | 82.2% | 0.601 | 84.7% | 94.9% | 97.4% | 0.891 | 38.6% | 75.7% | 84.7% | 57.8% | 44.8% | 19.8% | 11.6% | 40.5% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 34.4% | 71.7% | 82.2% | 0.601 | 84.7% | 94.9% | 97.4% | 0.891 | 38.6% | 75.7% | 84.7% | 57.8% | 44.8% | 19.8% | 11.6% | 40.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 3/5 (60.0%) (top-1: m001 0.5987, m002 0.5915, m003 0.5079, m004 0.5906, m005 0.5354)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-08T12:49:09+00:00 — benchmark sweep_legalbenchrag_contractnli: baseline-qwen3-embedding-8b-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__qwen3-embedding-8b-826d4d38.json` — 703 chunks, qwen3-embedding:8b (4096d), built 2026-10-08T12:49:15+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 27.8% | 60.3% | 71.2% | 0.481 | 64.5% | 83.1% | 89.3% | 0.733 | 28.3% | 61.1% | 72.0% | 34.6% | 32.9% | 14.8% | 8.8% | 31.8% |
| en | 977 | 27.8% | 60.3% | 71.2% | 0.481 | 64.5% | 83.1% | 89.3% | 0.733 | 28.3% | 61.1% | 72.0% | 34.6% | 32.9% | 14.8% | 8.8% | 31.8% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 27.8% | 60.3% | 71.2% | 0.481 | 64.5% | 83.1% | 89.3% | 0.733 | 28.3% | 61.1% | 72.0% | 34.6% | 32.9% | 14.8% | 8.8% | 31.8% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 3/5 (60.0%) (top-1: m001 0.6028, m002 0.6481, m003 0.4156, m004 0.5788, m005 0.4870)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-08T12:50:34+00:00 — benchmark sweep_legalbenchrag_contractnli: merge-1200-qwen3-embedding-8b-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__qwen3-embedding-8b-826d4d38.json` — 1,091 chunks, qwen3-embedding:8b (4096d), built 2026-10-08T12:50:34+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 25.4% | 57.6% | 68.3% | 0.474 | 68.3% | 87.4% | 92.0% | 0.763 | 28.7% | 61.9% | 71.6% | 44.3% | 32.8% | 15.9% | 9.6% | 29.7% |
| en | 977 | 25.4% | 57.6% | 68.3% | 0.474 | 68.3% | 87.4% | 92.0% | 0.763 | 28.7% | 61.9% | 71.6% | 44.3% | 32.8% | 15.9% | 9.6% | 29.7% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 25.4% | 57.6% | 68.3% | 0.474 | 68.3% | 87.4% | 92.0% | 0.763 | 28.7% | 61.9% | 71.6% | 44.3% | 32.8% | 15.9% | 9.6% | 29.7% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 3/5 (60.0%) (top-1: m001 0.6233, m002 0.6459, m003 0.3944, m004 0.5696, m005 0.4862)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-08T12:51:55+00:00 — benchmark sweep_legalbenchrag_contractnli: baseline-nomic-embed-text-v2-moe-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__nomic-embed-text-v2-moe-826d4d38.json` — 703 chunks, nomic-embed-text-v2-moe (768d), built 2026-10-08T12:51:56+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 29.2% | 63.2% | 73.3% | 0.490 | 75.3% | 88.6% | 92.8% | 0.812 | 30.0% | 64.0% | 74.0% | 34.6% | 34.5% | 15.7% | 9.2% | 32.7% |
| en | 977 | 29.2% | 63.2% | 73.3% | 0.490 | 75.3% | 88.6% | 92.8% | 0.812 | 30.0% | 64.0% | 74.0% | 34.6% | 34.5% | 15.7% | 9.2% | 32.7% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 29.2% | 63.2% | 73.3% | 0.490 | 75.3% | 88.6% | 92.8% | 0.812 | 30.0% | 64.0% | 74.0% | 34.6% | 34.5% | 15.7% | 9.2% | 32.7% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.5331, m002 0.4726, m003 0.3791, m004 0.5035, m005 0.3523)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-08T12:52:08+00:00 — benchmark sweep_legalbenchrag_contractnli: merge-1200-nomic-embed-text-v2-moe-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__nomic-embed-text-v2-moe-826d4d38.json` — 1,091 chunks, nomic-embed-text-v2-moe (768d), built 2026-10-08T12:52:08+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 28.1% | 58.4% | 70.8% | 0.498 | 76.5% | 88.6% | 93.3% | 0.822 | 31.9% | 62.2% | 73.4% | 45.8% | 36.3% | 16.4% | 10.1% | 33.2% |
| en | 977 | 28.1% | 58.4% | 70.8% | 0.498 | 76.5% | 88.6% | 93.3% | 0.822 | 31.9% | 62.2% | 73.4% | 45.8% | 36.3% | 16.4% | 10.1% | 33.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 28.1% | 58.4% | 70.8% | 0.498 | 76.5% | 88.6% | 93.3% | 0.822 | 31.9% | 62.2% | 73.4% | 45.8% | 36.3% | 16.4% | 10.1% | 33.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.5199, m002 0.4807, m003 0.3781, m004 0.5169, m005 0.3620)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-08T12:52:21+00:00 — benchmark sweep_legalbenchrag_contractnli: baseline-embeddinggemma-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__embeddinggemma-826d4d38.json` — 703 chunks, embeddinggemma (768d), built 2026-10-08T12:52:26+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 41.7% | 79.3% | 87.5% | 0.641 | 90.6% | 96.3% | 98.3% | 0.933 | 42.7% | 80.0% | 88.1% | 47.5% | 48.8% | 19.5% | 11.0% | 46.1% |
| en | 977 | 41.7% | 79.3% | 87.5% | 0.641 | 90.6% | 96.3% | 98.3% | 0.933 | 42.7% | 80.0% | 88.1% | 47.5% | 48.8% | 19.5% | 11.0% | 46.1% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 41.7% | 79.3% | 87.5% | 0.641 | 90.6% | 96.3% | 98.3% | 0.933 | 42.7% | 80.0% | 88.1% | 47.5% | 48.8% | 19.5% | 11.0% | 46.1% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 1/5 (20.0%) (top-1: m001 0.6199, m002 0.5497, m003 0.4080, m004 0.5377, m005 0.4682)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-08T12:52:39+00:00 — benchmark sweep_legalbenchrag_contractnli: merge-1200-embeddinggemma-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__embeddinggemma-826d4d38.json` — 1,091 chunks, embeddinggemma (768d), built 2026-10-08T12:52:39+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 39.4% | 76.1% | 86.9% | 0.651 | 91.2% | 97.6% | 99.1% | 0.938 | 44.4% | 79.3% | 89.0% | 61.7% | 51.1% | 21.0% | 12.3% | 45.6% |
| en | 977 | 39.4% | 76.1% | 86.9% | 0.651 | 91.2% | 97.6% | 99.1% | 0.938 | 44.4% | 79.3% | 89.0% | 61.7% | 51.1% | 21.0% | 12.3% | 45.6% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 39.4% | 76.1% | 86.9% | 0.651 | 91.2% | 97.6% | 99.1% | 0.938 | 44.4% | 79.3% | 89.0% | 61.7% | 51.1% | 21.0% | 12.3% | 45.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 2/5 (40.0%) (top-1: m001 0.6348, m002 0.5382, m003 0.4253, m004 0.5654, m005 0.4834)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-08T12:52:53+00:00 — benchmark sweep_legalbenchrag_contractnli: baseline-granite-embedding-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__granite-embedding-826d4d38.json` — 703 chunks, granite-embedding (384d), built 2026-10-08T12:52:59+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 28.2% | 64.2% | 74.2% | 0.489 | 71.9% | 86.1% | 91.1% | 0.784 | 29.1% | 64.5% | 74.5% | 32.6% | 33.7% | 15.9% | 9.3% | 31.8% |
| en | 977 | 28.2% | 64.2% | 74.2% | 0.489 | 71.9% | 86.1% | 91.1% | 0.784 | 29.1% | 64.5% | 74.5% | 32.6% | 33.7% | 15.9% | 9.3% | 31.8% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 28.2% | 64.2% | 74.2% | 0.489 | 71.9% | 86.1% | 91.1% | 0.784 | 29.1% | 64.5% | 74.5% | 32.6% | 33.7% | 15.9% | 9.3% | 31.8% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 5/5 (100.0%) (top-1: m001 0.8060, m002 0.8025, m003 0.6782, m004 0.8022, m005 0.7098)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-08T12:53:03+00:00 — benchmark sweep_legalbenchrag_contractnli: merge-1200-granite-embedding-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__granite-embedding-826d4d38.json` — 1,091 chunks, granite-embedding (384d), built 2026-10-08T12:53:03+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 22.5% | 54.6% | 66.4% | 0.447 | 68.7% | 83.5% | 88.5% | 0.757 | 26.2% | 57.1% | 68.3% | 41.5% | 30.6% | 15.4% | 9.5% | 28.2% |
| en | 977 | 22.5% | 54.6% | 66.4% | 0.447 | 68.7% | 83.5% | 88.5% | 0.757 | 26.2% | 57.1% | 68.3% | 41.5% | 30.6% | 15.4% | 9.5% | 28.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 22.5% | 54.6% | 66.4% | 0.447 | 68.7% | 83.5% | 88.5% | 0.757 | 26.2% | 57.1% | 68.3% | 41.5% | 30.6% | 15.4% | 9.5% | 28.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 5/5 (100.0%) (top-1: m001 0.8105, m002 0.8193, m003 0.6906, m004 0.7924, m005 0.7216)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-08T12:53:08+00:00 — benchmark sweep_legalbenchrag_contractnli: baseline-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__snowflake-arctic-embed2-826d4d38.json` — 703 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-08T12:53:14+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 35.7% | 75.1% | 83.1% | 0.589 | 85.7% | 93.6% | 96.5% | 0.893 | 37.0% | 76.0% | 83.7% | 41.5% | 42.6% | 18.5% | 10.4% | 39.6% |
| en | 977 | 35.7% | 75.1% | 83.1% | 0.589 | 85.7% | 93.6% | 96.5% | 0.893 | 37.0% | 76.0% | 83.7% | 41.5% | 42.6% | 18.5% | 10.4% | 39.6% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 35.7% | 75.1% | 83.1% | 0.589 | 85.7% | 93.6% | 96.5% | 0.893 | 37.0% | 76.0% | 83.7% | 41.5% | 42.6% | 18.5% | 10.4% | 39.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.5284, m002 0.5016, m003 0.3151, m004 0.4771, m005 0.3917)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-08T12:53:27+00:00 — benchmark sweep_legalbenchrag_contractnli: merge-1200-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__snowflake-arctic-embed2-826d4d38.json` — 1,091 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-08T12:53:27+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 30.7% | 66.5% | 76.8% | 0.563 | 82.0% | 95.0% | 97.2% | 0.877 | 35.0% | 70.3% | 79.1% | 53.9% | 40.4% | 18.5% | 11.0% | 37.5% |
| en | 977 | 30.7% | 66.5% | 76.8% | 0.563 | 82.0% | 95.0% | 97.2% | 0.877 | 35.0% | 70.3% | 79.1% | 53.9% | 40.4% | 18.5% | 11.0% | 37.5% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 30.7% | 66.5% | 76.8% | 0.563 | 82.0% | 95.0% | 97.2% | 0.877 | 35.0% | 70.3% | 79.1% | 53.9% | 40.4% | 18.5% | 11.0% | 37.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.5421, m002 0.5065, m003 0.3097, m004 0.4755, m005 0.4074)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-08T12:53:42+00:00 — benchmark sweep_legalbenchrag_contractnli: baseline-mxbai-embed-large-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__mxbai-embed-large-826d4d38.json` — 703 chunks, mxbai-embed-large (1024d), built 2026-10-08T12:53:48+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 33.5% | 70.4% | 79.8% | 0.552 | 85.0% | 92.5% | 95.5% | 0.883 | 34.8% | 71.0% | 80.2% | 38.1% | 39.6% | 17.4% | 10.0% | 37.4% |
| en | 977 | 33.5% | 70.4% | 79.8% | 0.552 | 85.0% | 92.5% | 95.5% | 0.883 | 34.8% | 71.0% | 80.2% | 38.1% | 39.6% | 17.4% | 10.0% | 37.4% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 33.5% | 70.4% | 79.8% | 0.552 | 85.0% | 92.5% | 95.5% | 0.883 | 34.8% | 71.0% | 80.2% | 38.1% | 39.6% | 17.4% | 10.0% | 37.4% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 5/5 (100.0%) (top-1: m001 0.6712, m002 0.7015, m003 0.5690, m004 0.6491, m005 0.6194)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-08T12:54:01+00:00 — benchmark sweep_legalbenchrag_contractnli: merge-1200-mxbai-embed-large-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__mxbai-embed-large-826d4d38.json` — 1,091 chunks, mxbai-embed-large (1024d), built 2026-10-08T12:54:01+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 29.9% | 64.4% | 77.4% | 0.539 | 85.4% | 93.0% | 95.8% | 0.889 | 34.0% | 67.5% | 79.8% | 52.1% | 39.0% | 17.9% | 11.1% | 35.1% |
| en | 977 | 29.9% | 64.4% | 77.4% | 0.539 | 85.4% | 93.0% | 95.8% | 0.889 | 34.0% | 67.5% | 79.8% | 52.1% | 39.0% | 17.9% | 11.1% | 35.1% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 29.9% | 64.4% | 77.4% | 0.539 | 85.4% | 93.0% | 95.8% | 0.889 | 34.0% | 67.5% | 79.8% | 52.1% | 39.0% | 17.9% | 11.1% | 35.1% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 5/5 (100.0%) (top-1: m001 0.6699, m002 0.7091, m003 0.5704, m004 0.6486, m005 0.6173)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-08T12:54:16+00:00 — benchmark sweep_legalbenchrag_contractnli — dataset legalbenchrag-contractnli — comparison (14 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline-bge-m3-embedding | bge-m3 | 1800/0.15/on | embedding | 977 | 35.7% | 77.5% | 87.3% | 0.591 | 84.0% | 94.9% | 96.9% | 0.887 | 36.7% | 78.5% | 88.0% | 41.0% | 41.7% | 19.1% | 11.0% | 39.8% | 3/5 | 6s / 6.4s |
| merge-1200-bge-m3-embedding | bge-m3 | 1200/0.15/on | embedding | 977 | 34.4% | 71.7% | 82.2% | 0.601 | 84.7% | 94.9% | 97.4% | 0.891 | 38.6% | 75.7% | 84.7% | 57.8% | 44.8% | 19.8% | 11.6% | 40.5% | 3/5 | 8s / 6.8s |
| baseline-qwen3-embedding-8b-embedding | qwen3-embedding:8b | 1800/0.15/on | embedding | 977 | 27.8% | 60.3% | 71.2% | 0.481 | 64.5% | 83.1% | 89.3% | 0.733 | 28.3% | 61.1% | 72.0% | 34.6% | 32.9% | 14.8% | 8.8% | 31.8% | 3/5 | 54s / 24.0s |
| merge-1200-qwen3-embedding-8b-embedding | qwen3-embedding:8b | 1200/0.15/on | embedding | 977 | 25.4% | 57.6% | 68.3% | 0.474 | 68.3% | 87.4% | 92.0% | 0.763 | 28.7% | 61.9% | 71.6% | 44.3% | 32.8% | 15.9% | 9.6% | 29.7% | 3/5 | 55s / 25.9s |
| baseline-nomic-embed-text-v2-moe-embedding | nomic-embed-text-v2-moe | 1800/0.15/on | embedding | 977 | 29.2% | 63.2% | 73.3% | 0.490 | 75.3% | 88.6% | 92.8% | 0.812 | 30.0% | 64.0% | 74.0% | 34.6% | 34.5% | 15.7% | 9.2% | 32.7% | 0/5 | 5s / 6.6s |
| merge-1200-nomic-embed-text-v2-moe-embedding | nomic-embed-text-v2-moe | 1200/0.15/on | embedding | 977 | 28.1% | 58.4% | 70.8% | 0.498 | 76.5% | 88.6% | 93.3% | 0.822 | 31.9% | 62.2% | 73.4% | 45.8% | 36.3% | 16.4% | 10.1% | 33.2% | 0/5 | 6s / 5.8s |
| baseline-embeddinggemma-embedding | embeddinggemma | 1800/0.15/on | embedding | 977 | 41.7% | 79.3% | 87.5% | 0.641 | 90.6% | 96.3% | 98.3% | 0.933 | 42.7% | 80.0% | 88.1% | 47.5% | 48.8% | 19.5% | 11.0% | 46.1% | 1/5 | 6s / 6.7s |
| merge-1200-embeddinggemma-embedding | embeddinggemma | 1200/0.15/on | embedding | 977 | 39.4% | 76.1% | 86.9% | 0.651 | 91.2% | 97.6% | 99.1% | 0.938 | 44.4% | 79.3% | 89.0% | 61.7% | 51.1% | 21.0% | 12.3% | 45.6% | 2/5 | 7s / 7.5s |
| baseline-granite-embedding-embedding | granite-embedding | 1800/0.15/on | embedding | 977 | 28.2% | 64.2% | 74.2% | 0.489 | 71.9% | 86.1% | 91.1% | 0.784 | 29.1% | 64.5% | 74.5% | 32.6% | 33.7% | 15.9% | 9.3% | 31.8% | 5/5 | 2s / 1.9s |
| merge-1200-granite-embedding-embedding | granite-embedding | 1200/0.15/on | embedding | 977 | 22.5% | 54.6% | 66.4% | 0.447 | 68.7% | 83.5% | 88.5% | 0.757 | 26.2% | 57.1% | 68.3% | 41.5% | 30.6% | 15.4% | 9.5% | 28.2% | 5/5 | 3s / 2.0s |
| baseline-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1800/0.15/on | embedding | 977 | 35.7% | 75.1% | 83.1% | 0.589 | 85.7% | 93.6% | 96.5% | 0.893 | 37.0% | 76.0% | 83.7% | 41.5% | 42.6% | 18.5% | 10.4% | 39.6% | 0/5 | 6s / 6.5s |
| merge-1200-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1200/0.15/on | embedding | 977 | 30.7% | 66.5% | 76.8% | 0.563 | 82.0% | 95.0% | 97.2% | 0.877 | 35.0% | 70.3% | 79.1% | 53.9% | 40.4% | 18.5% | 11.0% | 37.5% | 0/5 | 8s / 7.3s |
| baseline-mxbai-embed-large-embedding | mxbai-embed-large | 1800/0.15/on | embedding | 977 | 33.5% | 70.4% | 79.8% | 0.552 | 85.0% | 92.5% | 95.5% | 0.883 | 34.8% | 71.0% | 80.2% | 38.1% | 39.6% | 17.4% | 10.0% | 37.4% | 5/5 | 6s / 6.8s |
| merge-1200-mxbai-embed-large-embedding | mxbai-embed-large | 1200/0.15/on | embedding | 977 | 29.9% | 64.4% | 77.4% | 0.539 | 85.4% | 93.0% | 95.8% | 0.889 | 34.0% | 67.5% | 79.8% | 52.1% | 39.0% | 17.9% | 11.1% | 35.1% | 5/5 | 8s / 7.7s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes


## 2026-10-08T12:59:11+00:00 — benchmark sweep_legalbenchrag_cuad — resolved plan

plan    : sweep_legalbenchrag_cuad — 14 experiment(s) over 14 store cell(s)
dataset : legalbenchrag-cuad
captures: data/raw/c88547bc806ea086 — 462 capture(s)
golden  : data/eval/datasets/legalbenchrag-cuad/golden.jsonl — 4046 row(s)
stores  :
  baseline-bge-m3        merge 1800/0.15/on     × bge-m3                       → data/benchmark_stores/merge-1800-0.15-on__bge-m3-47d5d5a2.json
  merge-2400-bge-m3      merge 2400/0.15/on     × bge-m3                       → data/benchmark_stores/merge-2400-0.15-on__bge-m3-47d5d5a2.json
  baseline-qwen3-embedding-8b merge 1800/0.15/on     × qwen3-embedding:8b           → data/benchmark_stores/merge-1800-0.15-on__qwen3-embedding-8b-47d5d5a2.json
  merge-2400-qwen3-embedding-8b merge 2400/0.15/on     × qwen3-embedding:8b           → data/benchmark_stores/merge-2400-0.15-on__qwen3-embedding-8b-47d5d5a2.json
  baseline-nomic-embed-text-v2-moe merge 1800/0.15/on     × nomic-embed-text-v2-moe      → data/benchmark_stores/merge-1800-0.15-on__nomic-embed-text-v2-moe-47d5d5a2.json
  merge-2400-nomic-embed-text-v2-moe merge 2400/0.15/on     × nomic-embed-text-v2-moe      → data/benchmark_stores/merge-2400-0.15-on__nomic-embed-text-v2-moe-47d5d5a2.json
  baseline-embeddinggemma merge 1800/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-1800-0.15-on__embeddinggemma-47d5d5a2.json
  merge-2400-embeddinggemma merge 2400/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-2400-0.15-on__embeddinggemma-47d5d5a2.json
  baseline-granite-embedding merge 1800/0.15/on     × granite-embedding            → data/benchmark_stores/merge-1800-0.15-on__granite-embedding-47d5d5a2.json
  merge-2400-granite-embedding merge 2400/0.15/on     × granite-embedding            → data/benchmark_stores/merge-2400-0.15-on__granite-embedding-47d5d5a2.json
  baseline-snowflake-arctic-embed2 merge 1800/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-1800-0.15-on__snowflake-arctic-embed2-47d5d5a2.json
  merge-2400-snowflake-arctic-embed2 merge 2400/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-2400-0.15-on__snowflake-arctic-embed2-47d5d5a2.json
  baseline-mxbai-embed-large merge 1800/0.15/on     × mxbai-embed-large            → data/benchmark_stores/merge-1800-0.15-on__mxbai-embed-large-47d5d5a2.json
  merge-2400-mxbai-embed-large merge 2400/0.15/on     × mxbai-embed-large            → data/benchmark_stores/merge-2400-0.15-on__mxbai-embed-large-47d5d5a2.json
experiments:
  1. baseline-bge-m3-embedding    → baseline-bge-m3        retrieval embedding
  2. merge-2400-bge-m3-embedding  → merge-2400-bge-m3      retrieval embedding
  3. baseline-qwen3-embedding-8b-embedding → baseline-qwen3-embedding-8b retrieval embedding
  4. merge-2400-qwen3-embedding-8b-embedding → merge-2400-qwen3-embedding-8b retrieval embedding
  5. baseline-nomic-embed-text-v2-moe-embedding → baseline-nomic-embed-text-v2-moe retrieval embedding
  6. merge-2400-nomic-embed-text-v2-moe-embedding → merge-2400-nomic-embed-text-v2-moe retrieval embedding
  7. baseline-embeddinggemma-embedding → baseline-embeddinggemma retrieval embedding
  8. merge-2400-embeddinggemma-embedding → merge-2400-embeddinggemma retrieval embedding
  9. baseline-granite-embedding-embedding → baseline-granite-embedding retrieval embedding
  10. merge-2400-granite-embedding-embedding → merge-2400-granite-embedding retrieval embedding
  11. baseline-snowflake-arctic-embed2-embedding → baseline-snowflake-arctic-embed2 retrieval embedding
  12. merge-2400-snowflake-arctic-embed2-embedding → merge-2400-snowflake-arctic-embed2 retrieval embedding
  13. baseline-mxbai-embed-large-embedding → baseline-mxbai-embed-large retrieval embedding
  14. merge-2400-mxbai-embed-large-embedding → merge-2400-mxbai-embed-large retrieval embedding


## 2026-10-08T12:59:11+00:00 — benchmark sweep_legalbenchrag_cuad: baseline-bge-m3-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__bge-m3-47d5d5a2.json` — 18,024 chunks, bge-m3 (1024d), built 2026-10-08T12:59:12+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 7.7% | 37.2% | 54.8% | 0.297 | 98.7% | 100.0% | 100.0% | 0.993 | 10.6% | 45.8% | 64.4% | 13.6% | 12.7% | 12.7% | 9.9% | 13.2% |
| en | 4042 | 7.7% | 37.2% | 54.8% | 0.297 | 98.7% | 100.0% | 100.0% | 0.993 | 10.6% | 45.8% | 64.4% | 13.6% | 12.7% | 12.7% | 9.9% | 13.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 7.7% | 37.2% | 54.8% | 0.297 | 98.7% | 100.0% | 100.0% | 0.993 | 10.6% | 45.8% | 64.4% | 13.6% | 12.7% | 12.7% | 9.9% | 13.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6007, m002 0.5775, m003 0.6123, m004 0.5847)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-08T13:03:49+00:00 — benchmark sweep_legalbenchrag_cuad: merge-2400-bge-m3-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__bge-m3-47d5d5a2.json` — 13,459 chunks, bge-m3 (1024d), built 2026-10-08T13:03:49+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 9.8% | 42.4% | 60.5% | 0.318 | 98.6% | 100.0% | 100.0% | 0.993 | 11.9% | 49.0% | 67.3% | 12.5% | 14.2% | 13.1% | 9.9% | 14.5% |
| en | 4042 | 9.8% | 42.4% | 60.5% | 0.318 | 98.6% | 100.0% | 100.0% | 0.993 | 11.9% | 49.0% | 67.3% | 12.5% | 14.2% | 13.1% | 9.9% | 14.5% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 9.8% | 42.4% | 60.5% | 0.318 | 98.6% | 100.0% | 100.0% | 0.993 | 11.9% | 49.0% | 67.3% | 12.5% | 14.2% | 13.1% | 9.9% | 14.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6057, m002 0.5807, m003 0.6199, m004 0.5856)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-08T13:07:56+00:00 — benchmark sweep_legalbenchrag_cuad: baseline-qwen3-embedding-8b-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__qwen3-embedding-8b-47d5d5a2.json` — 18,024 chunks, qwen3-embedding:8b (4096d), built 2026-10-08T13:07:57+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 12.6% | 42.7% | 57.1% | 0.367 | 93.3% | 99.1% | 99.6% | 0.960 | 16.6% | 52.2% | 66.9% | 22.4% | 19.6% | 14.6% | 10.3% | 19.3% |
| en | 4042 | 12.6% | 42.7% | 57.1% | 0.367 | 93.3% | 99.1% | 99.6% | 0.960 | 16.6% | 52.2% | 66.9% | 22.4% | 19.6% | 14.6% | 10.3% | 19.3% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 12.6% | 42.7% | 57.1% | 0.367 | 93.3% | 99.1% | 99.6% | 0.960 | 16.6% | 52.2% | 66.9% | 22.4% | 19.6% | 14.6% | 10.3% | 19.3% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6440, m002 0.5700, m003 0.6797, m004 0.5524)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-08T13:39:17+00:00 — benchmark sweep_legalbenchrag_cuad: merge-2400-qwen3-embedding-8b-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__qwen3-embedding-8b-47d5d5a2.json` — 13,459 chunks, qwen3-embedding:8b (4096d), built 2026-10-08T13:39:17+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 14.7% | 48.2% | 62.7% | 0.387 | 92.3% | 99.1% | 99.5% | 0.953 | 18.0% | 55.5% | 69.3% | 19.6% | 21.0% | 15.0% | 10.2% | 20.7% |
| en | 4042 | 14.7% | 48.2% | 62.7% | 0.387 | 92.3% | 99.1% | 99.5% | 0.953 | 18.0% | 55.5% | 69.3% | 19.6% | 21.0% | 15.0% | 10.2% | 20.7% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 14.7% | 48.2% | 62.7% | 0.387 | 92.3% | 99.1% | 99.5% | 0.953 | 18.0% | 55.5% | 69.3% | 19.6% | 21.0% | 15.0% | 10.2% | 20.7% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 3/4 (75.0%) (top-1: m001 0.6169, m002 0.5469, m003 0.6856, m004 0.5594)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-08T14:08:29+00:00 — benchmark sweep_legalbenchrag_cuad: baseline-nomic-embed-text-v2-moe-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__nomic-embed-text-v2-moe-47d5d5a2.json` — 18,024 chunks, nomic-embed-text-v2-moe (768d), built 2026-10-08T14:08:29+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 12.3% | 40.4% | 55.9% | 0.353 | 97.2% | 99.8% | 99.9% | 0.984 | 16.5% | 49.4% | 65.2% | 19.4% | 19.6% | 14.1% | 10.2% | 18.4% |
| en | 4042 | 12.3% | 40.4% | 55.9% | 0.353 | 97.2% | 99.8% | 99.9% | 0.984 | 16.5% | 49.4% | 65.2% | 19.4% | 19.6% | 14.1% | 10.2% | 18.4% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 12.3% | 40.4% | 55.9% | 0.353 | 97.2% | 99.8% | 99.9% | 0.984 | 16.5% | 49.4% | 65.2% | 19.4% | 19.6% | 14.1% | 10.2% | 18.4% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5111, m002 0.5116, m003 0.5734, m004 0.4970)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-08T14:11:39+00:00 — benchmark sweep_legalbenchrag_cuad: merge-2400-nomic-embed-text-v2-moe-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__nomic-embed-text-v2-moe-47d5d5a2.json` — 13,459 chunks, nomic-embed-text-v2-moe (768d), built 2026-10-08T14:11:39+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 13.8% | 44.3% | 60.9% | 0.369 | 97.3% | 99.8% | 99.9% | 0.985 | 17.0% | 51.3% | 68.2% | 17.6% | 20.2% | 14.0% | 10.0% | 19.2% |
| en | 4042 | 13.8% | 44.3% | 60.9% | 0.369 | 97.3% | 99.8% | 99.9% | 0.985 | 17.0% | 51.3% | 68.2% | 17.6% | 20.2% | 14.0% | 10.0% | 19.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 13.8% | 44.3% | 60.9% | 0.369 | 97.3% | 99.8% | 99.9% | 0.985 | 17.0% | 51.3% | 68.2% | 17.6% | 20.2% | 14.0% | 10.0% | 19.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.4999, m002 0.5166, m003 0.5622, m004 0.4961)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-08T14:14:19+00:00 — benchmark sweep_legalbenchrag_cuad: baseline-embeddinggemma-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__embeddinggemma-47d5d5a2.json` — 18,024 chunks, embeddinggemma (768d), built 2026-10-08T14:14:20+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 14.9% | 45.8% | 62.1% | 0.402 | 97.3% | 100.0% | 100.0% | 0.985 | 19.2% | 55.5% | 71.8% | 22.8% | 22.9% | 15.8% | 11.2% | 22.2% |
| en | 4042 | 14.9% | 45.8% | 62.1% | 0.402 | 97.3% | 100.0% | 100.0% | 0.985 | 19.2% | 55.5% | 71.8% | 22.8% | 22.9% | 15.8% | 11.2% | 22.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 14.9% | 45.8% | 62.1% | 0.402 | 97.3% | 100.0% | 100.0% | 0.985 | 19.2% | 55.5% | 71.8% | 22.8% | 22.9% | 15.8% | 11.2% | 22.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5434, m002 0.5342, m003 0.6000, m004 0.5095)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-08T14:18:01+00:00 — benchmark sweep_legalbenchrag_cuad: merge-2400-embeddinggemma-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__embeddinggemma-47d5d5a2.json` — 13,459 chunks, embeddinggemma (768d), built 2026-10-08T14:18:01+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 16.8% | 51.8% | 68.0% | 0.421 | 97.9% | 100.0% | 100.0% | 0.989 | 20.2% | 58.9% | 75.0% | 21.1% | 24.2% | 16.0% | 11.0% | 22.9% |
| en | 4042 | 16.8% | 51.8% | 68.0% | 0.421 | 97.9% | 100.0% | 100.0% | 0.989 | 20.2% | 58.9% | 75.0% | 21.1% | 24.2% | 16.0% | 11.0% | 22.9% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 16.8% | 51.8% | 68.0% | 0.421 | 97.9% | 100.0% | 100.0% | 0.989 | 20.2% | 58.9% | 75.0% | 21.1% | 24.2% | 16.0% | 11.0% | 22.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5256, m002 0.5389, m003 0.5898, m004 0.5026)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-08T14:21:13+00:00 — benchmark sweep_legalbenchrag_cuad: baseline-granite-embedding-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__granite-embedding-47d5d5a2.json` — 18,024 chunks, granite-embedding (384d), built 2026-10-08T14:21:14+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 10.0% | 33.8% | 48.4% | 0.306 | 94.9% | 99.5% | 99.7% | 0.970 | 13.4% | 41.9% | 57.0% | 16.4% | 16.0% | 11.7% | 8.9% | 15.5% |
| en | 4042 | 10.0% | 33.8% | 48.4% | 0.306 | 94.9% | 99.5% | 99.7% | 0.970 | 13.4% | 41.9% | 57.0% | 16.4% | 16.0% | 11.7% | 8.9% | 15.5% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 10.0% | 33.8% | 48.4% | 0.306 | 94.9% | 99.5% | 99.7% | 0.970 | 13.4% | 41.9% | 57.0% | 16.4% | 16.0% | 11.7% | 8.9% | 15.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.7743, m002 0.7748, m003 0.7912, m004 0.7668)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-08T14:23:07+00:00 — benchmark sweep_legalbenchrag_cuad: merge-2400-granite-embedding-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__granite-embedding-47d5d5a2.json` — 13,459 chunks, granite-embedding (384d), built 2026-10-08T14:23:07+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 12.2% | 38.6% | 54.9% | 0.328 | 95.5% | 99.5% | 99.8% | 0.973 | 14.9% | 45.0% | 61.6% | 15.4% | 17.8% | 12.2% | 9.0% | 16.9% |
| en | 4042 | 12.2% | 38.6% | 54.9% | 0.328 | 95.5% | 99.5% | 99.8% | 0.973 | 14.9% | 45.0% | 61.6% | 15.4% | 17.8% | 12.2% | 9.0% | 16.9% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 12.2% | 38.6% | 54.9% | 0.328 | 95.5% | 99.5% | 99.8% | 0.973 | 14.9% | 45.0% | 61.6% | 15.4% | 17.8% | 12.2% | 9.0% | 16.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.7802, m002 0.7706, m003 0.7912, m004 0.7735)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-08T14:24:41+00:00 — benchmark sweep_legalbenchrag_cuad: baseline-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__snowflake-arctic-embed2-47d5d5a2.json` — 18,024 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-08T14:24:43+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 8.0% | 37.0% | 54.1% | 0.298 | 98.8% | 100.0% | 100.0% | 0.994 | 11.0% | 45.1% | 63.0% | 13.9% | 12.9% | 12.7% | 9.8% | 13.6% |
| en | 4042 | 8.0% | 37.0% | 54.1% | 0.298 | 98.8% | 100.0% | 100.0% | 0.994 | 11.0% | 45.1% | 63.0% | 13.9% | 12.9% | 12.7% | 9.8% | 13.6% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 8.0% | 37.0% | 54.1% | 0.298 | 98.8% | 100.0% | 100.0% | 0.994 | 11.0% | 45.1% | 63.0% | 13.9% | 12.9% | 12.7% | 9.8% | 13.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5023, m002 0.4842, m003 0.5711, m004 0.5117)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-08T14:29:14+00:00 — benchmark sweep_legalbenchrag_cuad: merge-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__snowflake-arctic-embed2-47d5d5a2.json` — 13,459 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-08T14:29:14+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 10.2% | 41.8% | 61.0% | 0.318 | 98.5% | 100.0% | 100.0% | 0.992 | 12.5% | 47.6% | 67.2% | 13.2% | 14.5% | 12.8% | 9.9% | 14.9% |
| en | 4042 | 10.2% | 41.8% | 61.0% | 0.318 | 98.5% | 100.0% | 100.0% | 0.992 | 12.5% | 47.6% | 67.2% | 13.2% | 14.5% | 12.8% | 9.9% | 14.9% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 10.2% | 41.8% | 61.0% | 0.318 | 98.5% | 100.0% | 100.0% | 0.992 | 12.5% | 47.6% | 67.2% | 13.2% | 14.5% | 12.8% | 9.9% | 14.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.4727, m002 0.4814, m003 0.5743, m004 0.4756)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-08T14:33:08+00:00 — benchmark sweep_legalbenchrag_cuad: baseline-mxbai-embed-large-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__mxbai-embed-large-47d5d5a2.json` — 18,024 chunks, mxbai-embed-large (1024d), built 2026-10-08T14:33:08+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 12.9% | 41.4% | 58.3% | 0.369 | 98.0% | 100.0% | 100.0% | 0.989 | 17.2% | 51.1% | 68.1% | 19.9% | 20.1% | 14.3% | 10.6% | 19.6% |
| en | 4042 | 12.9% | 41.4% | 58.3% | 0.369 | 98.0% | 100.0% | 100.0% | 0.989 | 17.2% | 51.1% | 68.1% | 19.9% | 20.1% | 14.3% | 10.6% | 19.6% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 12.9% | 41.4% | 58.3% | 0.369 | 98.0% | 100.0% | 100.0% | 0.989 | 17.2% | 51.1% | 68.1% | 19.9% | 20.1% | 14.3% | 10.6% | 19.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.7129, m002 0.6612, m003 0.7501, m004 0.6679)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-08T14:37:31+00:00 — benchmark sweep_legalbenchrag_cuad: merge-2400-mxbai-embed-large-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__mxbai-embed-large-47d5d5a2.json` — 13,459 chunks, mxbai-embed-large (1024d), built 2026-10-08T14:37:31+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 14.7% | 46.4% | 64.4% | 0.383 | 98.0% | 100.0% | 100.0% | 0.990 | 17.9% | 53.9% | 71.9% | 18.1% | 20.8% | 14.4% | 10.4% | 20.3% |
| en | 4042 | 14.7% | 46.4% | 64.4% | 0.383 | 98.0% | 100.0% | 100.0% | 0.990 | 17.9% | 53.9% | 71.9% | 18.1% | 20.8% | 14.4% | 10.4% | 20.3% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 14.7% | 46.4% | 64.4% | 0.383 | 98.0% | 100.0% | 100.0% | 0.990 | 17.9% | 53.9% | 71.9% | 18.1% | 20.8% | 14.4% | 10.4% | 20.3% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.7092, m002 0.6612, m003 0.7525, m004 0.6515)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-08T14:41:05+00:00 — benchmark sweep_legalbenchrag_cuad — dataset legalbenchrag-cuad — comparison (14 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline-bge-m3-embedding | bge-m3 | 1800/0.15/on | embedding | 4042 | 7.7% | 37.2% | 54.8% | 0.297 | 98.7% | 100.0% | 100.0% | 0.993 | 10.6% | 45.8% | 64.4% | 13.6% | 12.7% | 12.7% | 9.9% | 13.2% | 4/4 | 169s / 105.0s |
| merge-2400-bge-m3-embedding | bge-m3 | 2400/0.15/on | embedding | 4042 | 9.8% | 42.4% | 60.5% | 0.318 | 98.6% | 100.0% | 100.0% | 0.993 | 11.9% | 49.0% | 67.3% | 12.5% | 14.2% | 13.1% | 9.9% | 14.5% | 4/4 | 156s / 88.5s |
| baseline-qwen3-embedding-8b-embedding | qwen3-embedding:8b | 1800/0.15/on | embedding | 4042 | 12.6% | 42.7% | 57.1% | 0.367 | 93.3% | 99.1% | 99.6% | 0.960 | 16.6% | 52.2% | 66.9% | 22.4% | 19.6% | 14.6% | 10.3% | 19.3% | 4/4 | 1455s / 412.6s |
| merge-2400-qwen3-embedding-8b-embedding | qwen3-embedding:8b | 2400/0.15/on | embedding | 4042 | 14.7% | 48.2% | 62.7% | 0.387 | 92.3% | 99.1% | 99.5% | 0.953 | 18.0% | 55.5% | 69.3% | 19.6% | 21.0% | 15.0% | 10.2% | 20.7% | 3/4 | 1418s / 323.6s |
| baseline-nomic-embed-text-v2-moe-embedding | nomic-embed-text-v2-moe | 1800/0.15/on | embedding | 4042 | 12.3% | 40.4% | 55.9% | 0.353 | 97.2% | 99.8% | 99.9% | 0.984 | 16.5% | 49.4% | 65.2% | 19.4% | 19.6% | 14.1% | 10.2% | 18.4% | 1/4 | 122s / 65.9s |
| merge-2400-nomic-embed-text-v2-moe-embedding | nomic-embed-text-v2-moe | 2400/0.15/on | embedding | 4042 | 13.8% | 44.3% | 60.9% | 0.369 | 97.3% | 99.8% | 99.9% | 0.985 | 17.0% | 51.3% | 68.2% | 17.6% | 20.2% | 14.0% | 10.0% | 19.2% | 1/4 | 103s / 54.4s |
| baseline-embeddinggemma-embedding | embeddinggemma | 1800/0.15/on | embedding | 4042 | 14.9% | 45.8% | 62.1% | 0.402 | 97.3% | 100.0% | 100.0% | 0.985 | 19.2% | 55.5% | 71.8% | 22.8% | 22.9% | 15.8% | 11.2% | 22.2% | 1/4 | 149s / 69.6s |
| merge-2400-embeddinggemma-embedding | embeddinggemma | 2400/0.15/on | embedding | 4042 | 16.8% | 51.8% | 68.0% | 0.421 | 97.9% | 100.0% | 100.0% | 0.989 | 20.2% | 58.9% | 75.0% | 21.1% | 24.2% | 16.0% | 11.0% | 22.9% | 1/4 | 128s / 63.2s |
| baseline-granite-embedding-embedding | granite-embedding | 1800/0.15/on | embedding | 4042 | 10.0% | 33.8% | 48.4% | 0.306 | 94.9% | 99.5% | 99.7% | 0.970 | 13.4% | 41.9% | 57.0% | 16.4% | 16.0% | 11.7% | 8.9% | 15.5% | 4/4 | 63s / 49.4s |
| merge-2400-granite-embedding-embedding | granite-embedding | 2400/0.15/on | embedding | 4042 | 12.2% | 38.6% | 54.9% | 0.328 | 95.5% | 99.5% | 99.8% | 0.973 | 14.9% | 45.0% | 61.6% | 15.4% | 17.8% | 12.2% | 9.0% | 16.9% | 4/4 | 50s / 43.6s |
| baseline-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1800/0.15/on | embedding | 4042 | 8.0% | 37.0% | 54.1% | 0.298 | 98.8% | 100.0% | 100.0% | 0.994 | 11.0% | 45.1% | 63.0% | 13.9% | 12.9% | 12.7% | 9.8% | 13.6% | 1/4 | 174s / 94.1s |
| merge-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0.15/on | embedding | 4042 | 10.2% | 41.8% | 61.0% | 0.318 | 98.5% | 100.0% | 100.0% | 0.992 | 12.5% | 47.6% | 67.2% | 13.2% | 14.5% | 12.8% | 9.9% | 14.9% | 1/4 | 155s / 75.7s |
| baseline-mxbai-embed-large-embedding | mxbai-embed-large | 1800/0.15/on | embedding | 4042 | 12.9% | 41.4% | 58.3% | 0.369 | 98.0% | 100.0% | 100.0% | 0.989 | 17.2% | 51.1% | 68.1% | 19.9% | 20.1% | 14.3% | 10.6% | 19.6% | 4/4 | 164s / 96.1s |
| merge-2400-mxbai-embed-large-embedding | mxbai-embed-large | 2400/0.15/on | embedding | 4042 | 14.7% | 46.4% | 64.4% | 0.383 | 98.0% | 100.0% | 100.0% | 0.990 | 17.9% | 53.9% | 71.9% | 18.1% | 20.8% | 14.4% | 10.4% | 20.3% | 4/4 | 137s / 73.9s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes


## 2026-10-09T08:58:06+00:00 — benchmark sweep_legalbenchrag_maud — resolved plan

plan    : sweep_legalbenchrag_maud — 14 experiment(s) over 14 store cell(s)
dataset : legalbenchrag-maud
captures: data/raw/4961ebee611362f6 — 150 capture(s)
golden  : data/eval/datasets/legalbenchrag-maud/golden.jsonl — 1680 row(s)
stores  :
  baseline-bge-m3        merge 1800/0.15/on     × bge-m3                       → data/benchmark_stores/merge-1800-0.15-on__bge-m3-68231218.json
  merge-2400-bge-m3      merge 2400/0.15/on     × bge-m3                       → data/benchmark_stores/merge-2400-0.15-on__bge-m3-68231218.json
  baseline-qwen3-embedding-8b merge 1800/0.15/on     × qwen3-embedding:8b           → data/benchmark_stores/merge-1800-0.15-on__qwen3-embedding-8b-68231218.json
  merge-2400-qwen3-embedding-8b merge 2400/0.15/on     × qwen3-embedding:8b           → data/benchmark_stores/merge-2400-0.15-on__qwen3-embedding-8b-68231218.json
  baseline-nomic-embed-text-v2-moe merge 1800/0.15/on     × nomic-embed-text-v2-moe      → data/benchmark_stores/merge-1800-0.15-on__nomic-embed-text-v2-moe-68231218.json
  merge-2400-nomic-embed-text-v2-moe merge 2400/0.15/on     × nomic-embed-text-v2-moe      → data/benchmark_stores/merge-2400-0.15-on__nomic-embed-text-v2-moe-68231218.json
  baseline-embeddinggemma merge 1800/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-1800-0.15-on__embeddinggemma-68231218.json
  merge-2400-embeddinggemma merge 2400/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-2400-0.15-on__embeddinggemma-68231218.json
  baseline-granite-embedding merge 1800/0.15/on     × granite-embedding            → data/benchmark_stores/merge-1800-0.15-on__granite-embedding-68231218.json
  merge-2400-granite-embedding merge 2400/0.15/on     × granite-embedding            → data/benchmark_stores/merge-2400-0.15-on__granite-embedding-68231218.json
  baseline-snowflake-arctic-embed2 merge 1800/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-1800-0.15-on__snowflake-arctic-embed2-68231218.json
  merge-2400-snowflake-arctic-embed2 merge 2400/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-2400-0.15-on__snowflake-arctic-embed2-68231218.json
  baseline-mxbai-embed-large merge 1800/0.15/on     × mxbai-embed-large            → data/benchmark_stores/merge-1800-0.15-on__mxbai-embed-large-68231218.json
  merge-2400-mxbai-embed-large merge 2400/0.15/on     × mxbai-embed-large            → data/benchmark_stores/merge-2400-0.15-on__mxbai-embed-large-68231218.json
experiments:
  1. baseline-bge-m3-embedding    → baseline-bge-m3        retrieval embedding
  2. merge-2400-bge-m3-embedding  → merge-2400-bge-m3      retrieval embedding
  3. baseline-qwen3-embedding-8b-embedding → baseline-qwen3-embedding-8b retrieval embedding
  4. merge-2400-qwen3-embedding-8b-embedding → merge-2400-qwen3-embedding-8b retrieval embedding
  5. baseline-nomic-embed-text-v2-moe-embedding → baseline-nomic-embed-text-v2-moe retrieval embedding
  6. merge-2400-nomic-embed-text-v2-moe-embedding → merge-2400-nomic-embed-text-v2-moe retrieval embedding
  7. baseline-embeddinggemma-embedding → baseline-embeddinggemma retrieval embedding
  8. merge-2400-embeddinggemma-embedding → merge-2400-embeddinggemma retrieval embedding
  9. baseline-granite-embedding-embedding → baseline-granite-embedding retrieval embedding
  10. merge-2400-granite-embedding-embedding → merge-2400-granite-embedding retrieval embedding
  11. baseline-snowflake-arctic-embed2-embedding → baseline-snowflake-arctic-embed2 retrieval embedding
  12. merge-2400-snowflake-arctic-embed2-embedding → merge-2400-snowflake-arctic-embed2 retrieval embedding
  13. baseline-mxbai-embed-large-embedding → baseline-mxbai-embed-large retrieval embedding
  14. merge-2400-mxbai-embed-large-embedding → merge-2400-mxbai-embed-large retrieval embedding


## 2026-10-09T08:58:06+00:00 — benchmark sweep_legalbenchrag_maud: baseline-bge-m3-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__bge-m3-68231218.json` — 38,692 chunks, bge-m3 (1024d), built 2026-10-09T08:58:08+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 11.3% | 23.1% | 30.7% | 0.327 | 94.6% | 97.6% | 98.4% | 0.960 | 17.6% | 35.2% | 45.0% | 19.2% | 22.0% | 10.8% | 7.6% | 16.9% |
| en | 1676 | 11.3% | 23.1% | 30.7% | 0.327 | 94.6% | 97.6% | 98.4% | 0.960 | 17.6% | 35.2% | 45.0% | 19.2% | 22.0% | 10.8% | 7.6% | 16.9% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 11.3% | 23.1% | 30.7% | 0.327 | 94.6% | 97.6% | 98.4% | 0.960 | 17.6% | 35.2% | 45.0% | 19.2% | 22.0% | 10.8% | 7.6% | 16.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6137, m002 0.5811, m003 0.5691, m004 0.5770)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-09T09:06:18+00:00 — benchmark sweep_legalbenchrag_maud: merge-2400-bge-m3-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__bge-m3-68231218.json` — 28,860 chunks, bge-m3 (1024d), built 2026-10-09T09:06:18+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 11.0% | 26.0% | 35.3% | 0.312 | 93.4% | 98.0% | 99.0% | 0.955 | 15.6% | 35.1% | 46.6% | 15.9% | 19.6% | 10.8% | 7.6% | 16.6% |
| en | 1676 | 11.0% | 26.0% | 35.3% | 0.312 | 93.4% | 98.0% | 99.0% | 0.955 | 15.6% | 35.1% | 46.6% | 15.9% | 19.6% | 10.8% | 7.6% | 16.6% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 11.0% | 26.0% | 35.3% | 0.312 | 93.4% | 98.0% | 99.0% | 0.955 | 15.6% | 35.1% | 46.6% | 15.9% | 19.6% | 10.8% | 7.6% | 16.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6228, m002 0.5728, m003 0.5710, m004 0.5636)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-09T09:13:28+00:00 — benchmark sweep_legalbenchrag_maud: baseline-qwen3-embedding-8b-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__qwen3-embedding-8b-68231218.json` — 38,692 chunks, qwen3-embedding:8b (4096d), built 2026-10-09T09:13:30+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 8.4% | 23.6% | 31.9% | 0.317 | 77.7% | 92.0% | 95.6% | 0.840 | 14.9% | 37.2% | 47.9% | 17.5% | 18.7% | 12.0% | 8.6% | 15.2% |
| en | 1676 | 8.4% | 23.6% | 31.9% | 0.317 | 77.7% | 92.0% | 95.6% | 0.840 | 14.9% | 37.2% | 47.9% | 17.5% | 18.7% | 12.0% | 8.6% | 15.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 8.4% | 23.6% | 31.9% | 0.317 | 77.7% | 92.0% | 95.6% | 0.840 | 14.9% | 37.2% | 47.9% | 17.5% | 18.7% | 12.0% | 8.6% | 15.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6012, m002 0.5646, m003 0.6574, m004 0.5589)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-09T10:07:31+00:00 — benchmark sweep_legalbenchrag_maud: merge-2400-qwen3-embedding-8b-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__qwen3-embedding-8b-68231218.json` — 28,860 chunks, qwen3-embedding:8b (4096d), built 2026-10-09T10:07:31+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 9.5% | 24.9% | 34.4% | 0.314 | 78.8% | 90.8% | 94.7% | 0.842 | 15.5% | 35.5% | 46.5% | 15.7% | 20.0% | 10.9% | 7.7% | 15.0% |
| en | 1676 | 9.5% | 24.9% | 34.4% | 0.314 | 78.8% | 90.8% | 94.7% | 0.842 | 15.5% | 35.5% | 46.5% | 15.7% | 20.0% | 10.9% | 7.7% | 15.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 9.5% | 24.9% | 34.4% | 0.314 | 78.8% | 90.8% | 94.7% | 0.842 | 15.5% | 35.5% | 46.5% | 15.7% | 20.0% | 10.9% | 7.7% | 15.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 3/4 (75.0%) (top-1: m001 0.5958, m002 0.5619, m003 0.6345, m004 0.5430)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-09T10:57:49+00:00 — benchmark sweep_legalbenchrag_maud: baseline-nomic-embed-text-v2-moe-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__nomic-embed-text-v2-moe-68231218.json` — 38,692 chunks, nomic-embed-text-v2-moe (768d), built 2026-10-09T10:57:51+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 9.2% | 19.7% | 26.8% | 0.273 | 82.8% | 90.1% | 92.8% | 0.863 | 14.0% | 29.7% | 39.5% | 15.8% | 17.5% | 9.2% | 6.6% | 13.5% |
| en | 1676 | 9.2% | 19.7% | 26.8% | 0.273 | 82.8% | 90.1% | 92.8% | 0.863 | 14.0% | 29.7% | 39.5% | 15.8% | 17.5% | 9.2% | 6.6% | 13.5% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 9.2% | 19.7% | 26.8% | 0.273 | 82.8% | 90.1% | 92.8% | 0.863 | 14.0% | 29.7% | 39.5% | 15.8% | 17.5% | 9.2% | 6.6% | 13.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 0/4 (0.0%) (top-1: m001 0.4820, m002 0.4998, m003 0.5020, m004 0.5157)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-09T11:03:52+00:00 — benchmark sweep_legalbenchrag_maud: merge-2400-nomic-embed-text-v2-moe-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__nomic-embed-text-v2-moe-68231218.json` — 28,860 chunks, nomic-embed-text-v2-moe (768d), built 2026-10-09T11:03:52+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 9.2% | 21.0% | 29.5% | 0.270 | 82.3% | 89.6% | 92.8% | 0.859 | 12.8% | 29.0% | 39.5% | 13.5% | 16.5% | 8.9% | 6.4% | 13.4% |
| en | 1676 | 9.2% | 21.0% | 29.5% | 0.270 | 82.3% | 89.6% | 92.8% | 0.859 | 12.8% | 29.0% | 39.5% | 13.5% | 16.5% | 8.9% | 6.4% | 13.4% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 9.2% | 21.0% | 29.5% | 0.270 | 82.3% | 89.6% | 92.8% | 0.859 | 12.8% | 29.0% | 39.5% | 13.5% | 16.5% | 8.9% | 6.4% | 13.4% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 0/4 (0.0%) (top-1: m001 0.4786, m002 0.4998, m003 0.4945, m004 0.5210)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-09T11:08:35+00:00 — benchmark sweep_legalbenchrag_maud: baseline-embeddinggemma-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__embeddinggemma-68231218.json` — 38,692 chunks, embeddinggemma (768d), built 2026-10-09T11:08:36+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 9.3% | 21.7% | 29.6% | 0.294 | 92.5% | 97.6% | 99.2% | 0.949 | 15.1% | 32.1% | 42.7% | 17.1% | 18.8% | 10.0% | 7.3% | 14.2% |
| en | 1676 | 9.3% | 21.7% | 29.6% | 0.294 | 92.5% | 97.6% | 99.2% | 0.949 | 15.1% | 32.1% | 42.7% | 17.1% | 18.8% | 10.0% | 7.3% | 14.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 9.3% | 21.7% | 29.6% | 0.294 | 92.5% | 97.6% | 99.2% | 0.949 | 15.1% | 32.1% | 42.7% | 17.1% | 18.8% | 10.0% | 7.3% | 14.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5465, m002 0.5377, m003 0.5161, m004 0.5518)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-09T11:15:00+00:00 — benchmark sweep_legalbenchrag_maud: merge-2400-embeddinggemma-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__embeddinggemma-68231218.json` — 28,860 chunks, embeddinggemma (768d), built 2026-10-09T11:15:00+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 9.4% | 24.0% | 33.6% | 0.284 | 90.8% | 97.8% | 98.7% | 0.938 | 13.1% | 32.3% | 43.3% | 14.0% | 16.9% | 9.6% | 7.0% | 14.0% |
| en | 1676 | 9.4% | 24.0% | 33.6% | 0.284 | 90.8% | 97.8% | 98.7% | 0.938 | 13.1% | 32.3% | 43.3% | 14.0% | 16.9% | 9.6% | 7.0% | 14.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 9.4% | 24.0% | 33.6% | 0.284 | 90.8% | 97.8% | 98.7% | 0.938 | 13.1% | 32.3% | 43.3% | 14.0% | 16.9% | 9.6% | 7.0% | 14.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5299, m002 0.5417, m003 0.5307, m004 0.5751)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-09T11:20:37+00:00 — benchmark sweep_legalbenchrag_maud: baseline-granite-embedding-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__granite-embedding-68231218.json` — 38,692 chunks, granite-embedding (384d), built 2026-10-09T11:20:37+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 8.2% | 17.7% | 24.9% | 0.261 | 88.4% | 95.6% | 97.5% | 0.916 | 13.1% | 27.4% | 37.0% | 14.8% | 16.7% | 8.7% | 6.5% | 12.9% |
| en | 1676 | 8.2% | 17.7% | 24.9% | 0.261 | 88.4% | 95.6% | 97.5% | 0.916 | 13.1% | 27.4% | 37.0% | 14.8% | 16.7% | 8.7% | 6.5% | 12.9% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 8.2% | 17.7% | 24.9% | 0.261 | 88.4% | 95.6% | 97.5% | 0.916 | 13.1% | 27.4% | 37.0% | 14.8% | 16.7% | 8.7% | 6.5% | 12.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.7579, m002 0.7689, m003 0.7306, m004 0.7498)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-09T11:23:30+00:00 — benchmark sweep_legalbenchrag_maud: merge-2400-granite-embedding-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__granite-embedding-68231218.json` — 28,860 chunks, granite-embedding (384d), built 2026-10-09T11:23:30+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 8.2% | 19.5% | 28.0% | 0.254 | 85.9% | 94.9% | 97.6% | 0.900 | 11.5% | 27.4% | 37.6% | 11.8% | 15.3% | 8.5% | 6.3% | 12.4% |
| en | 1676 | 8.2% | 19.5% | 28.0% | 0.254 | 85.9% | 94.9% | 97.6% | 0.900 | 11.5% | 27.4% | 37.6% | 11.8% | 15.3% | 8.5% | 6.3% | 12.4% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 8.2% | 19.5% | 28.0% | 0.254 | 85.9% | 94.9% | 97.6% | 0.900 | 11.5% | 27.4% | 37.6% | 11.8% | 15.3% | 8.5% | 6.3% | 12.4% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.7663, m002 0.7673, m003 0.7186, m004 0.7454)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-09T11:25:54+00:00 — benchmark sweep_legalbenchrag_maud: baseline-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__snowflake-arctic-embed2-68231218.json` — 38,692 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-09T11:25:56+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 7.2% | 18.3% | 26.2% | 0.255 | 93.7% | 97.7% | 98.7% | 0.954 | 12.2% | 28.4% | 39.0% | 13.9% | 14.9% | 8.9% | 6.7% | 12.4% |
| en | 1676 | 7.2% | 18.3% | 26.2% | 0.255 | 93.7% | 97.7% | 98.7% | 0.954 | 12.2% | 28.4% | 39.0% | 13.9% | 14.9% | 8.9% | 6.7% | 12.4% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 7.2% | 18.3% | 26.2% | 0.255 | 93.7% | 97.7% | 98.7% | 0.954 | 12.2% | 28.4% | 39.0% | 13.9% | 14.9% | 8.9% | 6.7% | 12.4% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 0/4 (0.0%) (top-1: m001 0.4927, m002 0.5014, m003 0.5280, m004 0.5287)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-09T11:33:06+00:00 — benchmark sweep_legalbenchrag_maud: merge-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__snowflake-arctic-embed2-68231218.json` — 28,860 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-09T11:33:06+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 6.7% | 18.9% | 29.3% | 0.231 | 93.2% | 97.6% | 98.4% | 0.952 | 9.7% | 25.4% | 38.0% | 10.2% | 12.7% | 7.8% | 6.4% | 10.2% |
| en | 1676 | 6.7% | 18.9% | 29.3% | 0.231 | 93.2% | 97.6% | 98.4% | 0.952 | 9.7% | 25.4% | 38.0% | 10.2% | 12.7% | 7.8% | 6.4% | 10.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 6.7% | 18.9% | 29.3% | 0.231 | 93.2% | 97.6% | 98.4% | 0.952 | 9.7% | 25.4% | 38.0% | 10.2% | 12.7% | 7.8% | 6.4% | 10.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 0/4 (0.0%) (top-1: m001 0.5088, m002 0.4913, m003 0.4963, m004 0.5138)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-09T11:39:55+00:00 — benchmark sweep_legalbenchrag_maud: baseline-mxbai-embed-large-embedding

store: `data/benchmark_stores/merge-1800-0.15-on__mxbai-embed-large-68231218.json` — 38,692 chunks, mxbai-embed-large (1024d), built 2026-10-09T11:39:56+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 1800, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 8.9% | 19.6% | 27.2% | 0.288 | 88.9% | 96.3% | 98.2% | 0.922 | 14.3% | 30.6% | 40.9% | 16.0% | 17.9% | 9.4% | 6.9% | 13.8% |
| en | 1676 | 8.9% | 19.6% | 27.2% | 0.288 | 88.9% | 96.3% | 98.2% | 0.922 | 14.3% | 30.6% | 40.9% | 16.0% | 17.9% | 9.4% | 6.9% | 13.8% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 8.9% | 19.6% | 27.2% | 0.288 | 88.9% | 96.3% | 98.2% | 0.922 | 14.3% | 30.6% | 40.9% | 16.0% | 17.9% | 9.4% | 6.9% | 13.8% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6919, m002 0.6385, m003 0.6795, m004 0.6710)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-09T11:47:01+00:00 — benchmark sweep_legalbenchrag_maud: merge-2400-mxbai-embed-large-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__mxbai-embed-large-68231218.json` — 28,860 chunks, mxbai-embed-large (1024d), built 2026-10-09T11:47:01+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 9.1% | 20.8% | 30.0% | 0.277 | 90.0% | 97.3% | 98.6% | 0.933 | 13.3% | 29.3% | 41.0% | 13.5% | 16.8% | 9.0% | 6.7% | 13.7% |
| en | 1676 | 9.1% | 20.8% | 30.0% | 0.277 | 90.0% | 97.3% | 98.6% | 0.933 | 13.3% | 29.3% | 41.0% | 13.5% | 16.8% | 9.0% | 6.7% | 13.7% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 9.1% | 20.8% | 30.0% | 0.277 | 90.0% | 97.3% | 98.6% | 0.933 | 13.3% | 29.3% | 41.0% | 13.5% | 16.8% | 9.0% | 6.7% | 13.7% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6774, m002 0.6421, m003 0.6880, m004 0.6678)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-09T11:52:29+00:00 — benchmark sweep_legalbenchrag_maud — dataset legalbenchrag-maud — comparison (14 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline-bge-m3-embedding | bge-m3 | 1800/0.15/on | embedding | 1676 | 11.3% | 23.1% | 30.7% | 0.327 | 94.6% | 97.6% | 98.4% | 0.960 | 17.6% | 35.2% | 45.0% | 19.2% | 22.0% | 10.8% | 7.6% | 16.9% | 4/4 | 388s / 94.1s |
| merge-2400-bge-m3-embedding | bge-m3 | 2400/0.15/on | embedding | 1676 | 11.0% | 26.0% | 35.3% | 0.312 | 93.4% | 98.0% | 99.0% | 0.955 | 15.6% | 35.1% | 46.6% | 15.9% | 19.6% | 10.8% | 7.6% | 16.6% | 4/4 | 347s / 78.3s |
| baseline-qwen3-embedding-8b-embedding | qwen3-embedding:8b | 1800/0.15/on | embedding | 1676 | 8.4% | 23.6% | 31.9% | 0.317 | 77.7% | 92.0% | 95.6% | 0.840 | 14.9% | 37.2% | 47.9% | 17.5% | 18.7% | 12.0% | 8.6% | 15.2% | 4/4 | 2902s / 311.0s |
| merge-2400-qwen3-embedding-8b-embedding | qwen3-embedding:8b | 2400/0.15/on | embedding | 1676 | 9.5% | 24.9% | 34.4% | 0.314 | 78.8% | 90.8% | 94.7% | 0.842 | 15.5% | 35.5% | 46.5% | 15.7% | 20.0% | 10.9% | 7.7% | 15.0% | 3/4 | 2736s / 261.1s |
| baseline-nomic-embed-text-v2-moe-embedding | nomic-embed-text-v2-moe | 1800/0.15/on | embedding | 1676 | 9.2% | 19.7% | 26.8% | 0.273 | 82.8% | 90.1% | 92.8% | 0.863 | 14.0% | 29.7% | 39.5% | 15.8% | 17.5% | 9.2% | 6.6% | 13.5% | 0/4 | 294s / 62.0s |
| merge-2400-nomic-embed-text-v2-moe-embedding | nomic-embed-text-v2-moe | 2400/0.15/on | embedding | 1676 | 9.2% | 21.0% | 29.5% | 0.270 | 82.3% | 89.6% | 92.8% | 0.859 | 12.8% | 29.0% | 39.5% | 13.5% | 16.5% | 8.9% | 6.4% | 13.4% | 0/4 | 231s / 48.1s |
| baseline-embeddinggemma-embedding | embeddinggemma | 1800/0.15/on | embedding | 1676 | 9.3% | 21.7% | 29.6% | 0.294 | 92.5% | 97.6% | 99.2% | 0.949 | 15.1% | 32.1% | 42.7% | 17.1% | 18.8% | 10.0% | 7.3% | 14.2% | 1/4 | 315s / 62.9s |
| merge-2400-embeddinggemma-embedding | embeddinggemma | 2400/0.15/on | embedding | 1676 | 9.4% | 24.0% | 33.6% | 0.284 | 90.8% | 97.8% | 98.7% | 0.938 | 13.1% | 32.3% | 43.3% | 14.0% | 16.9% | 9.6% | 7.0% | 14.0% | 1/4 | 279s / 53.8s |
| baseline-granite-embedding-embedding | granite-embedding | 1800/0.15/on | embedding | 1676 | 8.2% | 17.7% | 24.9% | 0.261 | 88.4% | 95.6% | 97.5% | 0.916 | 13.1% | 27.4% | 37.0% | 14.8% | 16.7% | 8.7% | 6.5% | 12.9% | 4/4 | 133s / 36.9s |
| merge-2400-granite-embedding-embedding | granite-embedding | 2400/0.15/on | embedding | 1676 | 8.2% | 19.5% | 28.0% | 0.254 | 85.9% | 94.9% | 97.6% | 0.900 | 11.5% | 27.4% | 37.6% | 11.8% | 15.3% | 8.5% | 6.3% | 12.4% | 4/4 | 115s / 26.9s |
| baseline-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1800/0.15/on | embedding | 1676 | 7.2% | 18.3% | 26.2% | 0.255 | 93.7% | 97.7% | 98.7% | 0.954 | 12.2% | 28.4% | 39.0% | 13.9% | 14.9% | 8.9% | 6.7% | 12.4% | 0/4 | 354s / 69.5s |
| merge-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0.15/on | embedding | 1676 | 6.7% | 18.9% | 29.3% | 0.231 | 93.2% | 97.6% | 98.4% | 0.952 | 9.7% | 25.4% | 38.0% | 10.2% | 12.7% | 7.8% | 6.4% | 10.2% | 0/4 | 339s / 64.4s |
| baseline-mxbai-embed-large-embedding | mxbai-embed-large | 1800/0.15/on | embedding | 1676 | 8.9% | 19.6% | 27.2% | 0.288 | 88.9% | 96.3% | 98.2% | 0.922 | 14.3% | 30.6% | 40.9% | 16.0% | 17.9% | 9.4% | 6.9% | 13.8% | 4/4 | 348s / 69.2s |
| merge-2400-mxbai-embed-large-embedding | mxbai-embed-large | 2400/0.15/on | embedding | 1676 | 9.1% | 20.8% | 30.0% | 0.277 | 90.0% | 97.3% | 98.6% | 0.933 | 13.3% | 29.3% | 41.0% | 13.5% | 16.8% | 9.0% | 6.7% | 13.7% | 4/4 | 268s / 54.9s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes


## 2026-10-09T12:07:05+00:00 — benchmark sweep_vic_chargebook — resolved plan

plan    : sweep_vic_chargebook — 14 experiment(s) over 14 store cell(s)
dataset : vic-chargebook
captures: data/raw/c49c2465f4afa801 — 4876 capture(s)
golden  : data/eval/datasets/vic-chargebook/golden.jsonl — 104 row(s)
stores  :
  baseline-bge-m3        passthrough 4096/on    × bge-m3                       → data/benchmark_stores/passthrough-4096-on__bge-m3-6adfbee8.json
  noheader-bge-m3        passthrough 4096/off   × bge-m3                       → data/benchmark_stores/passthrough-4096-off__bge-m3-6adfbee8.json
  baseline-qwen3-embedding-8b passthrough 4096/on    × qwen3-embedding:8b           → data/benchmark_stores/passthrough-4096-on__qwen3-embedding-8b-6adfbee8.json
  noheader-qwen3-embedding-8b passthrough 4096/off   × qwen3-embedding:8b           → data/benchmark_stores/passthrough-4096-off__qwen3-embedding-8b-6adfbee8.json
  baseline-nomic-embed-text-v2-moe passthrough 4096/on    × nomic-embed-text-v2-moe      → data/benchmark_stores/passthrough-4096-on__nomic-embed-text-v2-moe-6adfbee8.json
  noheader-nomic-embed-text-v2-moe passthrough 4096/off   × nomic-embed-text-v2-moe      → data/benchmark_stores/passthrough-4096-off__nomic-embed-text-v2-moe-6adfbee8.json
  baseline-embeddinggemma passthrough 4096/on    × embeddinggemma               → data/benchmark_stores/passthrough-4096-on__embeddinggemma-6adfbee8.json
  noheader-embeddinggemma passthrough 4096/off   × embeddinggemma               → data/benchmark_stores/passthrough-4096-off__embeddinggemma-6adfbee8.json
  baseline-granite-embedding passthrough 4096/on    × granite-embedding            → data/benchmark_stores/passthrough-4096-on__granite-embedding-6adfbee8.json
  noheader-granite-embedding passthrough 4096/off   × granite-embedding            → data/benchmark_stores/passthrough-4096-off__granite-embedding-6adfbee8.json
  baseline-snowflake-arctic-embed2 passthrough 4096/on    × snowflake-arctic-embed2      → data/benchmark_stores/passthrough-4096-on__snowflake-arctic-embed2-6adfbee8.json
  noheader-snowflake-arctic-embed2 passthrough 4096/off   × snowflake-arctic-embed2      → data/benchmark_stores/passthrough-4096-off__snowflake-arctic-embed2-6adfbee8.json
  baseline-mxbai-embed-large passthrough 4096/on    × mxbai-embed-large            → data/benchmark_stores/passthrough-4096-on__mxbai-embed-large-6adfbee8.json
  noheader-mxbai-embed-large passthrough 4096/off   × mxbai-embed-large            → data/benchmark_stores/passthrough-4096-off__mxbai-embed-large-6adfbee8.json
experiments:
  1. baseline-bge-m3-embedding    → baseline-bge-m3        retrieval embedding
  2. noheader-bge-m3-embedding    → noheader-bge-m3        retrieval embedding
  3. baseline-qwen3-embedding-8b-embedding → baseline-qwen3-embedding-8b retrieval embedding
  4. noheader-qwen3-embedding-8b-embedding → noheader-qwen3-embedding-8b retrieval embedding
  5. baseline-nomic-embed-text-v2-moe-embedding → baseline-nomic-embed-text-v2-moe retrieval embedding
  6. noheader-nomic-embed-text-v2-moe-embedding → noheader-nomic-embed-text-v2-moe retrieval embedding
  7. baseline-embeddinggemma-embedding → baseline-embeddinggemma retrieval embedding
  8. noheader-embeddinggemma-embedding → noheader-embeddinggemma retrieval embedding
  9. baseline-granite-embedding-embedding → baseline-granite-embedding retrieval embedding
  10. noheader-granite-embedding-embedding → noheader-granite-embedding retrieval embedding
  11. baseline-snowflake-arctic-embed2-embedding → baseline-snowflake-arctic-embed2 retrieval embedding
  12. noheader-snowflake-arctic-embed2-embedding → noheader-snowflake-arctic-embed2 retrieval embedding
  13. baseline-mxbai-embed-large-embedding → baseline-mxbai-embed-large retrieval embedding
  14. noheader-mxbai-embed-large-embedding → noheader-mxbai-embed-large retrieval embedding


## 2026-10-09T12:07:05+00:00 — benchmark sweep_vic_chargebook: baseline-bge-m3-embedding

store: `data/benchmark_stores/passthrough-4096-on__bge-m3-6adfbee8.json` — 4,876 chunks, bge-m3 (1024d), built 2026-10-09T12:07:07+00:00
golden: `data/eval/datasets/vic-chargebook/golden.jsonl` — 104 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 4096, overlap 0, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 100 | 16.0% | 35.0% | 42.0% | 0.248 | 16.0% | 35.0% | 42.0% | 0.248 | 16.0% | 35.0% | 42.0% | 18.0% | 16.0% | 7.0% | 4.2% | 16.0% |
| en | 100 | 16.0% | 35.0% | 42.0% | 0.248 | 16.0% | 35.0% | 42.0% | 0.248 | 16.0% | 35.0% | 42.0% | 18.0% | 16.0% | 7.0% | 4.2% | 16.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 100 | 16.0% | 35.0% | 42.0% | 0.248 | 16.0% | 35.0% | 42.0% | 0.248 | 16.0% | 35.0% | 42.0% | 18.0% | 16.0% | 7.0% | 4.2% | 16.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 3/4 (75.0%) (top-1: m001 0.5837, m002 0.5563, m003 0.5499, m004 0.5571)
retrieval: embedding
dataset: vic-chargebook


## 2026-10-09T12:07:58+00:00 — benchmark sweep_vic_chargebook: noheader-bge-m3-embedding

store: `data/benchmark_stores/passthrough-4096-off__bge-m3-6adfbee8.json` — 4,876 chunks, bge-m3 (1024d), built 2026-10-09T12:07:58+00:00
golden: `data/eval/datasets/vic-chargebook/golden.jsonl` — 104 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 4096, overlap 0, header OFF

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 100 | 13.0% | 34.0% | 41.0% | 0.229 | 13.0% | 34.0% | 41.0% | 0.229 | 13.0% | 34.0% | 41.0% | 15.0% | 13.0% | 6.8% | 4.1% | 13.0% |
| en | 100 | 13.0% | 34.0% | 41.0% | 0.229 | 13.0% | 34.0% | 41.0% | 0.229 | 13.0% | 34.0% | 41.0% | 15.0% | 13.0% | 6.8% | 4.1% | 13.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 100 | 13.0% | 34.0% | 41.0% | 0.229 | 13.0% | 34.0% | 41.0% | 0.229 | 13.0% | 34.0% | 41.0% | 15.0% | 13.0% | 6.8% | 4.1% | 13.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 3/4 (75.0%) (top-1: m001 0.5696, m002 0.5526, m003 0.5351, m004 0.5504)
retrieval: embedding
dataset: vic-chargebook


## 2026-10-09T12:08:46+00:00 — benchmark sweep_vic_chargebook: baseline-qwen3-embedding-8b-embedding

store: `data/benchmark_stores/passthrough-4096-on__qwen3-embedding-8b-6adfbee8.json` — 4,876 chunks, qwen3-embedding:8b (4096d), built 2026-10-09T12:08:47+00:00
golden: `data/eval/datasets/vic-chargebook/golden.jsonl` — 104 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 4096, overlap 0, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 100 | 19.0% | 54.0% | 70.0% | 0.356 | 19.0% | 54.0% | 70.0% | 0.356 | 19.0% | 54.0% | 70.0% | 28.0% | 19.0% | 10.8% | 7.0% | 19.0% |
| en | 100 | 19.0% | 54.0% | 70.0% | 0.356 | 19.0% | 54.0% | 70.0% | 0.356 | 19.0% | 54.0% | 70.0% | 28.0% | 19.0% | 10.8% | 7.0% | 19.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 100 | 19.0% | 54.0% | 70.0% | 0.356 | 19.0% | 54.0% | 70.0% | 0.356 | 19.0% | 54.0% | 70.0% | 28.0% | 19.0% | 10.8% | 7.0% | 19.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 2/4 (50.0%) (top-1: m001 0.6060, m002 0.5410, m003 0.6149, m004 0.5348)
retrieval: embedding
dataset: vic-chargebook


## 2026-10-09T12:15:01+00:00 — benchmark sweep_vic_chargebook: noheader-qwen3-embedding-8b-embedding

store: `data/benchmark_stores/passthrough-4096-off__qwen3-embedding-8b-6adfbee8.json` — 4,876 chunks, qwen3-embedding:8b (4096d), built 2026-10-09T12:15:01+00:00
golden: `data/eval/datasets/vic-chargebook/golden.jsonl` — 104 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 4096, overlap 0, header OFF

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 100 | 17.0% | 50.0% | 69.0% | 0.322 | 17.0% | 50.0% | 69.0% | 0.322 | 17.0% | 50.0% | 69.0% | 22.0% | 17.0% | 10.0% | 6.9% | 17.0% |
| en | 100 | 17.0% | 50.0% | 69.0% | 0.322 | 17.0% | 50.0% | 69.0% | 0.322 | 17.0% | 50.0% | 69.0% | 22.0% | 17.0% | 10.0% | 6.9% | 17.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 100 | 17.0% | 50.0% | 69.0% | 0.322 | 17.0% | 50.0% | 69.0% | 0.322 | 17.0% | 50.0% | 69.0% | 22.0% | 17.0% | 10.0% | 6.9% | 17.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 2/4 (50.0%) (top-1: m001 0.6043, m002 0.5277, m003 0.5970, m004 0.5249)
retrieval: embedding
dataset: vic-chargebook


## 2026-10-09T12:21:10+00:00 — benchmark sweep_vic_chargebook: baseline-nomic-embed-text-v2-moe-embedding

store: `data/benchmark_stores/passthrough-4096-on__nomic-embed-text-v2-moe-6adfbee8.json` — 4,876 chunks, nomic-embed-text-v2-moe (768d), built 2026-10-09T12:21:11+00:00
golden: `data/eval/datasets/vic-chargebook/golden.jsonl` — 104 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 4096, overlap 0, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 100 | 10.0% | 40.0% | 50.0% | 0.241 | 10.0% | 40.0% | 50.0% | 0.241 | 10.0% | 40.0% | 50.0% | 18.0% | 10.0% | 8.0% | 5.0% | 10.0% |
| en | 100 | 10.0% | 40.0% | 50.0% | 0.241 | 10.0% | 40.0% | 50.0% | 0.241 | 10.0% | 40.0% | 50.0% | 18.0% | 10.0% | 8.0% | 5.0% | 10.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 100 | 10.0% | 40.0% | 50.0% | 0.241 | 10.0% | 40.0% | 50.0% | 0.241 | 10.0% | 40.0% | 50.0% | 18.0% | 10.0% | 8.0% | 5.0% | 10.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 0/4 (0.0%) (top-1: m001 0.5488, m002 0.5372, m003 0.5080, m004 0.4864)
retrieval: embedding
dataset: vic-chargebook


## 2026-10-09T12:21:46+00:00 — benchmark sweep_vic_chargebook: noheader-nomic-embed-text-v2-moe-embedding

store: `data/benchmark_stores/passthrough-4096-off__nomic-embed-text-v2-moe-6adfbee8.json` — 4,876 chunks, nomic-embed-text-v2-moe (768d), built 2026-10-09T12:21:46+00:00
golden: `data/eval/datasets/vic-chargebook/golden.jsonl` — 104 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 4096, overlap 0, header OFF

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 100 | 17.0% | 38.0% | 48.0% | 0.272 | 17.0% | 38.0% | 48.0% | 0.272 | 17.0% | 38.0% | 48.0% | 20.0% | 17.0% | 7.6% | 4.8% | 17.0% |
| en | 100 | 17.0% | 38.0% | 48.0% | 0.272 | 17.0% | 38.0% | 48.0% | 0.272 | 17.0% | 38.0% | 48.0% | 20.0% | 17.0% | 7.6% | 4.8% | 17.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 100 | 17.0% | 38.0% | 48.0% | 0.272 | 17.0% | 38.0% | 48.0% | 0.272 | 17.0% | 38.0% | 48.0% | 20.0% | 17.0% | 7.6% | 4.8% | 17.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5580, m002 0.5368, m003 0.5073, m004 0.4746)
retrieval: embedding
dataset: vic-chargebook


## 2026-10-09T12:22:20+00:00 — benchmark sweep_vic_chargebook: baseline-embeddinggemma-embedding

store: `data/benchmark_stores/passthrough-4096-on__embeddinggemma-6adfbee8.json` — 4,876 chunks, embeddinggemma (768d), built 2026-10-09T12:22:21+00:00
golden: `data/eval/datasets/vic-chargebook/golden.jsonl` — 104 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 4096, overlap 0, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 100 | 18.0% | 34.0% | 44.0% | 0.274 | 18.0% | 34.0% | 44.0% | 0.274 | 18.0% | 34.0% | 44.0% | 22.0% | 18.0% | 6.8% | 4.4% | 18.0% |
| en | 100 | 18.0% | 34.0% | 44.0% | 0.274 | 18.0% | 34.0% | 44.0% | 0.274 | 18.0% | 34.0% | 44.0% | 22.0% | 18.0% | 6.8% | 4.4% | 18.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 100 | 18.0% | 34.0% | 44.0% | 0.274 | 18.0% | 34.0% | 44.0% | 0.274 | 18.0% | 34.0% | 44.0% | 22.0% | 18.0% | 6.8% | 4.4% | 18.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 0/4 (0.0%) (top-1: m001 0.4915, m002 0.5093, m003 0.5028, m004 0.5120)
retrieval: embedding
dataset: vic-chargebook


## 2026-10-09T12:23:03+00:00 — benchmark sweep_vic_chargebook: noheader-embeddinggemma-embedding

store: `data/benchmark_stores/passthrough-4096-off__embeddinggemma-6adfbee8.json` — 4,876 chunks, embeddinggemma (768d), built 2026-10-09T12:23:03+00:00
golden: `data/eval/datasets/vic-chargebook/golden.jsonl` — 104 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 4096, overlap 0, header OFF

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 100 | 21.0% | 36.0% | 48.0% | 0.289 | 21.0% | 36.0% | 48.0% | 0.289 | 21.0% | 36.0% | 48.0% | 23.0% | 21.0% | 7.2% | 4.8% | 21.0% |
| en | 100 | 21.0% | 36.0% | 48.0% | 0.289 | 21.0% | 36.0% | 48.0% | 0.289 | 21.0% | 36.0% | 48.0% | 23.0% | 21.0% | 7.2% | 4.8% | 21.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 100 | 21.0% | 36.0% | 48.0% | 0.289 | 21.0% | 36.0% | 48.0% | 0.289 | 21.0% | 36.0% | 48.0% | 23.0% | 21.0% | 7.2% | 4.8% | 21.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 0/4 (0.0%) (top-1: m001 0.5179, m002 0.4776, m003 0.5307, m004 0.4987)
retrieval: embedding
dataset: vic-chargebook


## 2026-10-09T12:23:42+00:00 — benchmark sweep_vic_chargebook: baseline-granite-embedding-embedding

store: `data/benchmark_stores/passthrough-4096-on__granite-embedding-6adfbee8.json` — 4,876 chunks, granite-embedding (384d), built 2026-10-09T12:23:43+00:00
golden: `data/eval/datasets/vic-chargebook/golden.jsonl` — 104 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 4096, overlap 0, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 100 | 14.0% | 27.0% | 40.0% | 0.212 | 14.0% | 27.0% | 40.0% | 0.212 | 14.0% | 27.0% | 40.0% | 14.0% | 14.0% | 5.4% | 4.0% | 14.0% |
| en | 100 | 14.0% | 27.0% | 40.0% | 0.212 | 14.0% | 27.0% | 40.0% | 0.212 | 14.0% | 27.0% | 40.0% | 14.0% | 14.0% | 5.4% | 4.0% | 14.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 100 | 14.0% | 27.0% | 40.0% | 0.212 | 14.0% | 27.0% | 40.0% | 0.212 | 14.0% | 27.0% | 40.0% | 14.0% | 14.0% | 5.4% | 4.0% | 14.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.7812, m002 0.7583, m003 0.7613, m004 0.7308)
retrieval: embedding
dataset: vic-chargebook


## 2026-10-09T12:23:59+00:00 — benchmark sweep_vic_chargebook: noheader-granite-embedding-embedding

store: `data/benchmark_stores/passthrough-4096-off__granite-embedding-6adfbee8.json` — 4,876 chunks, granite-embedding (384d), built 2026-10-09T12:23:59+00:00
golden: `data/eval/datasets/vic-chargebook/golden.jsonl` — 104 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 4096, overlap 0, header OFF

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 100 | 11.0% | 27.0% | 39.0% | 0.197 | 11.0% | 27.0% | 39.0% | 0.197 | 11.0% | 27.0% | 39.0% | 16.0% | 11.0% | 5.4% | 3.9% | 11.0% |
| en | 100 | 11.0% | 27.0% | 39.0% | 0.197 | 11.0% | 27.0% | 39.0% | 0.197 | 11.0% | 27.0% | 39.0% | 16.0% | 11.0% | 5.4% | 3.9% | 11.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 100 | 11.0% | 27.0% | 39.0% | 0.197 | 11.0% | 27.0% | 39.0% | 0.197 | 11.0% | 27.0% | 39.0% | 16.0% | 11.0% | 5.4% | 3.9% | 11.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.7662, m002 0.7534, m003 0.7483, m004 0.7209)
retrieval: embedding
dataset: vic-chargebook


## 2026-10-09T12:24:16+00:00 — benchmark sweep_vic_chargebook: baseline-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/passthrough-4096-on__snowflake-arctic-embed2-6adfbee8.json` — 4,876 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-09T12:24:22+00:00
golden: `data/eval/datasets/vic-chargebook/golden.jsonl` — 104 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 4096, overlap 0, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 100 | 26.0% | 43.0% | 56.0% | 0.352 | 26.0% | 43.0% | 56.0% | 0.352 | 26.0% | 43.0% | 56.0% | 32.0% | 26.0% | 8.6% | 5.6% | 26.0% |
| en | 100 | 26.0% | 43.0% | 56.0% | 0.352 | 26.0% | 43.0% | 56.0% | 0.352 | 26.0% | 43.0% | 56.0% | 32.0% | 26.0% | 8.6% | 5.6% | 26.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 100 | 26.0% | 43.0% | 56.0% | 0.352 | 26.0% | 43.0% | 56.0% | 0.352 | 26.0% | 43.0% | 56.0% | 32.0% | 26.0% | 8.6% | 5.6% | 26.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 0/4 (0.0%) (top-1: m001 0.4907, m002 0.5085, m003 0.5152, m004 0.5275)
retrieval: embedding
dataset: vic-chargebook


## 2026-10-09T12:25:13+00:00 — benchmark sweep_vic_chargebook: noheader-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/passthrough-4096-off__snowflake-arctic-embed2-6adfbee8.json` — 4,876 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-09T12:25:13+00:00
golden: `data/eval/datasets/vic-chargebook/golden.jsonl` — 104 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 4096, overlap 0, header OFF

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 100 | 21.0% | 40.0% | 49.0% | 0.308 | 21.0% | 40.0% | 49.0% | 0.308 | 21.0% | 40.0% | 49.0% | 27.0% | 21.0% | 8.0% | 4.9% | 21.0% |
| en | 100 | 21.0% | 40.0% | 49.0% | 0.308 | 21.0% | 40.0% | 49.0% | 0.308 | 21.0% | 40.0% | 49.0% | 27.0% | 21.0% | 8.0% | 4.9% | 21.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 100 | 21.0% | 40.0% | 49.0% | 0.308 | 21.0% | 40.0% | 49.0% | 0.308 | 21.0% | 40.0% | 49.0% | 27.0% | 21.0% | 8.0% | 4.9% | 21.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 0/4 (0.0%) (top-1: m001 0.4876, m002 0.4987, m003 0.4976, m004 0.5168)
retrieval: embedding
dataset: vic-chargebook


## 2026-10-09T12:25:59+00:00 — benchmark sweep_vic_chargebook: baseline-mxbai-embed-large-embedding

store: `data/benchmark_stores/passthrough-4096-on__mxbai-embed-large-6adfbee8.json` — 4,876 chunks, mxbai-embed-large (1024d), built 2026-10-09T12:26:05+00:00
golden: `data/eval/datasets/vic-chargebook/golden.jsonl` — 104 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 4096, overlap 0, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 100 | 8.0% | 31.0% | 37.0% | 0.194 | 8.0% | 31.0% | 37.0% | 0.194 | 8.0% | 31.0% | 37.0% | 12.0% | 8.0% | 6.2% | 3.7% | 8.0% |
| en | 100 | 8.0% | 31.0% | 37.0% | 0.194 | 8.0% | 31.0% | 37.0% | 0.194 | 8.0% | 31.0% | 37.0% | 12.0% | 8.0% | 6.2% | 3.7% | 8.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 100 | 8.0% | 31.0% | 37.0% | 0.194 | 8.0% | 31.0% | 37.0% | 0.194 | 8.0% | 31.0% | 37.0% | 12.0% | 8.0% | 6.2% | 3.7% | 8.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6301, m002 0.6977, m003 0.6261, m004 0.6352)
retrieval: embedding
dataset: vic-chargebook


## 2026-10-09T12:26:46+00:00 — benchmark sweep_vic_chargebook: noheader-mxbai-embed-large-embedding

store: `data/benchmark_stores/passthrough-4096-off__mxbai-embed-large-6adfbee8.json` — 4,876 chunks, mxbai-embed-large (1024d), built 2026-10-09T12:26:46+00:00
golden: `data/eval/datasets/vic-chargebook/golden.jsonl` — 104 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 4096, overlap 0, header OFF

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 100 | 10.0% | 29.0% | 38.0% | 0.188 | 10.0% | 29.0% | 38.0% | 0.188 | 10.0% | 29.0% | 38.0% | 13.0% | 10.0% | 5.8% | 3.8% | 10.0% |
| en | 100 | 10.0% | 29.0% | 38.0% | 0.188 | 10.0% | 29.0% | 38.0% | 0.188 | 10.0% | 29.0% | 38.0% | 13.0% | 10.0% | 5.8% | 3.8% | 10.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 100 | 10.0% | 29.0% | 38.0% | 0.188 | 10.0% | 29.0% | 38.0% | 0.188 | 10.0% | 29.0% | 38.0% | 13.0% | 10.0% | 5.8% | 3.8% | 10.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6477, m002 0.7060, m003 0.6300, m004 0.6530)
retrieval: embedding
dataset: vic-chargebook


## 2026-10-09T12:27:27+00:00 — benchmark sweep_vic_chargebook — dataset vic-chargebook — comparison (14 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline-bge-m3-embedding | bge-m3 | 4096/0/on | embedding | 100 | 16.0% | 35.0% | 42.0% | 0.248 | 16.0% | 35.0% | 42.0% | 0.248 | 16.0% | 35.0% | 42.0% | 18.0% | 16.0% | 7.0% | 4.2% | 16.0% | 3/4 | 48s / 1.8s |
| noheader-bge-m3-embedding | bge-m3 | 4096/0/off | embedding | 100 | 13.0% | 34.0% | 41.0% | 0.229 | 13.0% | 34.0% | 41.0% | 0.229 | 13.0% | 34.0% | 41.0% | 15.0% | 13.0% | 6.8% | 4.1% | 13.0% | 3/4 | 45s / 2.3s |
| baseline-qwen3-embedding-8b-embedding | qwen3-embedding:8b | 4096/0/on | embedding | 100 | 19.0% | 54.0% | 70.0% | 0.356 | 19.0% | 54.0% | 70.0% | 0.356 | 19.0% | 54.0% | 70.0% | 28.0% | 19.0% | 10.8% | 7.0% | 19.0% | 2/4 | 364s / 6.9s |
| noheader-qwen3-embedding-8b-embedding | qwen3-embedding:8b | 4096/0/off | embedding | 100 | 17.0% | 50.0% | 69.0% | 0.322 | 17.0% | 50.0% | 69.0% | 0.322 | 17.0% | 50.0% | 69.0% | 22.0% | 17.0% | 10.0% | 6.9% | 17.0% | 2/4 | 357s / 7.7s |
| baseline-nomic-embed-text-v2-moe-embedding | nomic-embed-text-v2-moe | 4096/0/on | embedding | 100 | 10.0% | 40.0% | 50.0% | 0.241 | 10.0% | 40.0% | 50.0% | 0.241 | 10.0% | 40.0% | 50.0% | 18.0% | 10.0% | 8.0% | 5.0% | 10.0% | 0/4 | 33s / 1.4s |
| noheader-nomic-embed-text-v2-moe-embedding | nomic-embed-text-v2-moe | 4096/0/off | embedding | 100 | 17.0% | 38.0% | 48.0% | 0.272 | 17.0% | 38.0% | 48.0% | 0.272 | 17.0% | 38.0% | 48.0% | 20.0% | 17.0% | 7.6% | 4.8% | 17.0% | 1/4 | 32s / 1.4s |
| baseline-embeddinggemma-embedding | embeddinggemma | 4096/0/on | embedding | 100 | 18.0% | 34.0% | 44.0% | 0.274 | 18.0% | 34.0% | 44.0% | 0.274 | 18.0% | 34.0% | 44.0% | 22.0% | 18.0% | 6.8% | 4.4% | 18.0% | 0/4 | 40s / 1.5s |
| noheader-embeddinggemma-embedding | embeddinggemma | 4096/0/off | embedding | 100 | 21.0% | 36.0% | 48.0% | 0.289 | 21.0% | 36.0% | 48.0% | 0.289 | 21.0% | 36.0% | 48.0% | 23.0% | 21.0% | 7.2% | 4.8% | 21.0% | 0/4 | 37s / 1.8s |
| baseline-granite-embedding-embedding | granite-embedding | 4096/0/on | embedding | 100 | 14.0% | 27.0% | 40.0% | 0.212 | 14.0% | 27.0% | 40.0% | 0.212 | 14.0% | 27.0% | 40.0% | 14.0% | 14.0% | 5.4% | 4.0% | 14.0% | 4/4 | 15s / 1.1s |
| noheader-granite-embedding-embedding | granite-embedding | 4096/0/off | embedding | 100 | 11.0% | 27.0% | 39.0% | 0.197 | 11.0% | 27.0% | 39.0% | 0.197 | 11.0% | 27.0% | 39.0% | 16.0% | 11.0% | 5.4% | 3.9% | 11.0% | 4/4 | 15s / 0.9s |
| baseline-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 4096/0/on | embedding | 100 | 26.0% | 43.0% | 56.0% | 0.352 | 26.0% | 43.0% | 56.0% | 0.352 | 26.0% | 43.0% | 56.0% | 32.0% | 26.0% | 8.6% | 5.6% | 26.0% | 0/4 | 48s / 2.0s |
| noheader-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 4096/0/off | embedding | 100 | 21.0% | 40.0% | 49.0% | 0.308 | 21.0% | 40.0% | 49.0% | 0.308 | 21.0% | 40.0% | 49.0% | 27.0% | 21.0% | 8.0% | 4.9% | 21.0% | 0/4 | 43s / 2.2s |
| baseline-mxbai-embed-large-embedding | mxbai-embed-large | 4096/0/on | embedding | 100 | 8.0% | 31.0% | 37.0% | 0.194 | 8.0% | 31.0% | 37.0% | 0.194 | 8.0% | 31.0% | 37.0% | 12.0% | 8.0% | 6.2% | 3.7% | 8.0% | 4/4 | 39s / 1.6s |
| noheader-mxbai-embed-large-embedding | mxbai-embed-large | 4096/0/off | embedding | 100 | 10.0% | 29.0% | 38.0% | 0.188 | 10.0% | 29.0% | 38.0% | 0.188 | 10.0% | 29.0% | 38.0% | 13.0% | 10.0% | 5.8% | 3.8% | 10.0% | 4/4 | 38s / 1.8s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage it quotes); compare configs, never absolutes


## 2026-10-09 — Stage 2 verdict (hand-recorded: read of the race comparisons above — no new runs, no new numbers)

Scope: sweep2_models (uwazi golden, 21 cells) + the five dataset races (14 cells each; qwen3-embedding:0.6b was excluded from the dataset specs before the run — commit 08822d0 — while the uwazi race itself already ran 7 models). Lenses per the agreed methodology: doc R@10 = decider, chunk R@1 + chunk MRR on under-saturated instruments, false-retr at the single global 0.55 = GATE, cov@3000 = cross-geometry lens. Comparisons within a dataset only; verdicts are snapshots, not permanent picks.

| instrument | decider lens (doc) | chunk lens leader | false-retr gate (0.55) |
|---|---|---|---|
| uwazi | LIVE: gemma@1200 97.8% = qwen3-8b@1200 97.8% > nomic@1800 95.1% > bge-m3 max 93.6% | qwen3-8b 39.7 / gemma 37.2 / snowflake 37.3 @1 (all @1200) | qwen3-8b trips (1/3, 2/3, 1/3); gemma 0/3 = clean leader |
| privacyqa | saturated (7 docs, 100% except granite 99.5%) | bge-m3@2400: 36.2% @1 / 0.752 MRR (incumbent lead confirmed) | granite + mxbai 5/5; qwen3-8b 3/5 — killed |
| contractnli | gemma: doc@1 90.6–91.2% vs bge 84.0%; doc@10 98.3–99.1% | gemma 41.7% @1 / 0.641 MRR (+6 pts over bge); snowflake 35.7 @1 with 0/5 = clean runner-up | gemma 1–2/5; qwen3-8b 3/5; granite + mxbai 5/5 |
| cuad | compressed: doc@10 99.5–100% for all, doc@1 92.3–98.8% | gemma@2400: 16.8% @1 / 0.421 MRR; incumbent bge chunk-weak (9.8%) | bge trips 4/4; gemma/nomic/snowflake 1/4 |
| maud | bge-m3: doc@1 94.6% / doc@10 99.0% (leader); qwen3-8b collapses (77.7% doc@1) | bge-m3: 11.3% @1 / 0.327 MRR (next best ~9.3%) | snowflake + nomic 0/4; bge trips 4/4 |
| vic | = chunk (hit-rate currency; doc=chunk by construction) | snowflake: 26% @1 / 56% @10, 0/4 (clean leader); qwen3-8b raw-best @10 (70%) yet 2/4 | bge 3/4; header on/off flips direction per model |

Findings (in-dataset comparisons only):

1. **No model leads everywhere.** embeddinggemma — uwazi / contractnli / cuad; bge-m3 — privacyqa@2400 + maud; snowflake-arctic-embed2 — vic. The split is what the Stage-4 re-race (at the locked geometry) exists to settle.
2. **The false-retr gate tracks the model, not the geometry.** Each model's trip count is ~constant across a dataset's two geometries (bge-m3 3/5→3/5 contractnli, 4/4→4/4 cuad+maud; qwen3-8b 4/4→3/4 cuad) while it varies enormously across models: granite + mxbai trip everywhere (and collapse multilingually), nomic/gemma/snowflake stay at 0–1 trips per dataset → per-model FALSE_RETRIEVAL_THRESHOLD re-derivation (deferred at Step 3.6) is now justified and pre-declared as its own wave before Step 5.
3. **Multilingual scope (uwazi only).** Cross-language doc@10 near-saturated for the good models (98.5–100%); cross-language chunk R@1: gemma@1200 35.1% leads, nomic@1800 30.0%, qwen3-8b@1200 29.5% (its 44.6% @2400 rides a 65-row scope — small n), bge-m3 23–24%. granite (6.9%) and mxbai (9.2%) are effectively monolingual.
4. **Model × geometry interaction is real.** gemma prefers 1800 on privacyqa (34.8 → 27.1 at 2400) while snowflake prefers 2400 there (27.9 → 33.8) and bge prefers 2400 (32.5 → 36.2) — geometry is re-decided inside each Stage-3 method, never as a global knob.
5. **cov@3000 does its cross-geometry job.** 1200-char geometry packs ~1.5–2× more anchor text into the budget (uwazi bge 36.1 → 49.3; gemma 40.7 → 54.3) — pack lens and ranking lens move in opposite directions, so both stay in every future verdict table.
6. **Cost lens (Step 5 planning).** qwen3-8b: 4096 dims, 24–48 min per maud store (2,902s baseline / 1,418s cuad merge-2400) vs ~2–6 min for the mid field; embeddinggemma's 768 dims = smallest stores. qwen3-embedding:0.6b dropped from the roster after the Step 3.5 records; not reintroduced. nomic-embed-text:v1.5 stayed out by design (English-centric).

Decision recorded (user, 2026-10-09): Stage 3 method race runs at fixed reference model **bge-m3** (incumbent; maud — the flagship long-doc instrument — is its best dataset; Stage 4 re-races all models at the locked geometry, so nothing is frozen out). Pre-stated contingency: embeddinggemma joins the small-instrument method race if the arm ranking looks unstable. Step 5 shortlist (snapshot): bge-m3 / embeddinggemma / snowflake-arctic-embed2; qwen3-8b re-checked at Stage 4. vic-chargebook: config unchanged by both stages (pre-chunked corpus; out of scope for chunking methods).


## 2026-10-12T11:32:06+00:00 — benchmark sweep31_methods_uwazi — resolved plan

plan    : sweep31_methods_uwazi — 12 experiment(s) over 12 store cell(s)
captures: data/raw/bdd5a7c445847b35 — 77 capture(s)
golden  : data/eval/golden.jsonl — 270 row(s)
stores  :
  merge-1200-bge-m3      merge 1200/0.15/on     × bge-m3                       → data/benchmark_stores/merge-1200-0.15-on__bge-m3-4d284af0.json
  segment-2400-bge-m3    segment 2400/on        × bge-m3                       → data/benchmark_stores/segment-2400-on__bge-m3-4d284af0.json
  section-1200-bge-m3    section 1200/on        × bge-m3                       → data/benchmark_stores/section-1200-on__bge-m3-4d284af0.json
  section-split-1200-bge-m3 section-split 1200/on  × bge-m3                       → data/benchmark_stores/section-split-1200-on__bge-m3-4d284af0.json
  merge-1200-embeddinggemma merge 1200/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-1200-0.15-on__embeddinggemma-4d284af0.json
  segment-2400-embeddinggemma segment 2400/on        × embeddinggemma               → data/benchmark_stores/segment-2400-on__embeddinggemma-4d284af0.json
  section-1200-embeddinggemma section 1200/on        × embeddinggemma               → data/benchmark_stores/section-1200-on__embeddinggemma-4d284af0.json
  section-split-1200-embeddinggemma section-split 1200/on  × embeddinggemma               → data/benchmark_stores/section-split-1200-on__embeddinggemma-4d284af0.json
  merge-1200-snowflake-arctic-embed2 merge 1200/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-1200-0.15-on__snowflake-arctic-embed2-4d284af0.json
  segment-2400-snowflake-arctic-embed2 segment 2400/on        × snowflake-arctic-embed2      → data/benchmark_stores/segment-2400-on__snowflake-arctic-embed2-4d284af0.json
  section-1200-snowflake-arctic-embed2 section 1200/on        × snowflake-arctic-embed2      → data/benchmark_stores/section-1200-on__snowflake-arctic-embed2-4d284af0.json
  section-split-1200-snowflake-arctic-embed2 section-split 1200/on  × snowflake-arctic-embed2      → data/benchmark_stores/section-split-1200-on__snowflake-arctic-embed2-4d284af0.json
experiments:
  1. merge-1200-bge-m3-embedding  → merge-1200-bge-m3      retrieval embedding
  2. segment-2400-bge-m3-embedding → segment-2400-bge-m3    retrieval embedding
  3. section-1200-bge-m3-embedding → section-1200-bge-m3    retrieval embedding
  4. section-split-1200-bge-m3-embedding → section-split-1200-bge-m3 retrieval embedding
  5. merge-1200-embeddinggemma-embedding → merge-1200-embeddinggemma retrieval embedding
  6. segment-2400-embeddinggemma-embedding → segment-2400-embeddinggemma retrieval embedding
  7. section-1200-embeddinggemma-embedding → section-1200-embeddinggemma retrieval embedding
  8. section-split-1200-embeddinggemma-embedding → section-split-1200-embeddinggemma retrieval embedding
  9. merge-1200-snowflake-arctic-embed2-embedding → merge-1200-snowflake-arctic-embed2 retrieval embedding
  10. segment-2400-snowflake-arctic-embed2-embedding → segment-2400-snowflake-arctic-embed2 retrieval embedding
  11. section-1200-snowflake-arctic-embed2-embedding → section-1200-snowflake-arctic-embed2 retrieval embedding
  12. section-split-1200-snowflake-arctic-embed2-embedding → section-split-1200-snowflake-arctic-embed2 retrieval embedding


## 2026-10-12T11:32:06+00:00 — benchmark sweep31_methods_uwazi: merge-1200-bge-m3-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__bge-m3-4d284af0.json` — 4,488 chunks, bge-m3 (1024d), built 2026-10-07T11:43:51+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.4% | 62.8% | 73.5% | 0.479 | 62.9% | 91.8% | 93.6% | 0.751 | 32.7% | 64.9% | 75.7% | 49.3% | 33.0% | 13.4% | 7.9% | 32.8% |
| en | 169 | 32.8% | 64.2% | 73.4% | 0.484 | 68.0% | 92.9% | 93.5% | 0.782 | 33.3% | 66.3% | 75.0% | 50.5% | 33.7% | 13.6% | 7.8% | 34.3% |
| es | 98 | 28.9% | 60.4% | 73.8% | 0.470 | 54.1% | 89.8% | 93.9% | 0.698 | 31.6% | 62.6% | 76.9% | 47.3% | 31.6% | 13.1% | 8.1% | 30.3% |
| synthetic | 255 | 31.3% | 62.6% | 73.1% | 0.479 | 62.4% | 91.4% | 93.3% | 0.747 | 32.7% | 64.8% | 75.4% | 49.7% | 32.9% | 13.4% | 7.9% | 32.8% |
| manual | 12 | 33.3% | 66.7% | 83.3% | 0.476 | 75.0% | 100.0% | 100.0% | 0.833 | 33.3% | 66.7% | 83.3% | 41.7% | 33.3% | 13.3% | 8.3% | 33.3% |
| cross-language | 65 | 23.6% | 53.3% | 70.0% | 0.412 | 55.4% | 92.3% | 95.4% | 0.701 | 25.1% | 56.9% | 72.1% | 37.4% | 26.2% | 11.7% | 7.8% | 24.1% |
| same-language | 202 | 33.9% | 65.8% | 74.7% | 0.500 | 65.3% | 91.6% | 93.1% | 0.767 | 35.1% | 67.5% | 76.9% | 53.1% | 35.1% | 14.0% | 7.9% | 35.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5359, m014 0.5081, m015 0.4582)
retrieval: embedding


## 2026-10-12T11:32:13+00:00 — benchmark sweep31_methods_uwazi: segment-2400-bge-m3-embedding

store: `data/benchmark_stores/segment-2400-on__bge-m3-4d284af0.json` — 11,649 chunks, bge-m3 (1024d), built 2026-10-12T11:32:13+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 20.5% | 34.5% | 42.9% | 0.505 | 60.7% | 89.1% | 94.0% | 0.734 | 20.7% | 34.9% | 43.2% | 32.8% | 37.5% | 14.6% | 9.7% | 27.1% |
| en | 169 | 22.3% | 34.6% | 43.2% | 0.518 | 63.3% | 88.8% | 92.9% | 0.746 | 22.3% | 34.6% | 43.2% | 34.1% | 40.2% | 14.1% | 9.6% | 28.9% |
| es | 98 | 17.4% | 34.4% | 42.3% | 0.483 | 56.1% | 89.8% | 95.9% | 0.714 | 17.9% | 35.4% | 43.3% | 30.6% | 32.7% | 15.5% | 9.8% | 24.1% |
| synthetic | 255 | 20.7% | 34.5% | 42.6% | 0.507 | 60.0% | 89.0% | 93.7% | 0.729 | 20.9% | 34.9% | 43.0% | 32.7% | 37.6% | 14.7% | 9.8% | 27.3% |
| manual | 12 | 17.4% | 34.7% | 47.2% | 0.466 | 75.0% | 91.7% | 100.0% | 0.833 | 17.4% | 34.7% | 47.2% | 34.7% | 33.3% | 13.3% | 8.3% | 22.2% |
| cross-language | 65 | 17.6% | 31.0% | 39.4% | 0.461 | 60.0% | 90.8% | 93.8% | 0.721 | 18.4% | 31.8% | 40.1% | 29.4% | 35.4% | 13.5% | 9.4% | 22.4% |
| same-language | 202 | 21.5% | 35.6% | 44.0% | 0.519 | 60.9% | 88.6% | 94.1% | 0.738 | 21.5% | 35.9% | 44.2% | 33.9% | 38.1% | 15.0% | 9.8% | 28.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5359, m014 0.5082, m015 0.4632)
retrieval: embedding


## 2026-10-12T11:33:35+00:00 — benchmark sweep31_methods_uwazi: section-1200-bge-m3-embedding

store: `data/benchmark_stores/section-1200-on__bge-m3-4d284af0.json` — 4,771 chunks, bge-m3 (1024d), built 2026-10-12T11:33:35+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 25.5% | 51.5% | 63.8% | 0.501 | 61.0% | 88.8% | 92.9% | 0.732 | 28.4% | 56.1% | 68.1% | 40.0% | 36.7% | 16.7% | 11.3% | 30.7% |
| en | 169 | 26.8% | 51.2% | 62.6% | 0.523 | 65.7% | 88.2% | 93.5% | 0.760 | 29.1% | 55.5% | 66.6% | 39.8% | 39.6% | 18.5% | 12.6% | 33.7% |
| es | 98 | 23.4% | 52.2% | 65.8% | 0.462 | 53.1% | 89.8% | 91.8% | 0.685 | 27.2% | 57.2% | 70.8% | 40.5% | 31.6% | 13.7% | 9.1% | 25.4% |
| synthetic | 255 | 25.6% | 52.0% | 64.2% | 0.503 | 60.4% | 88.2% | 92.5% | 0.728 | 28.7% | 56.5% | 68.4% | 40.5% | 36.9% | 16.8% | 11.4% | 30.8% |
| manual | 12 | 23.6% | 42.3% | 54.8% | 0.450 | 75.0% | 100.0% | 100.0% | 0.836 | 23.6% | 48.6% | 63.2% | 30.6% | 33.3% | 15.0% | 9.2% | 27.6% |
| cross-language | 65 | 18.3% | 40.7% | 59.3% | 0.431 | 55.4% | 90.8% | 90.8% | 0.696 | 22.0% | 46.1% | 63.3% | 26.6% | 30.8% | 16.3% | 12.2% | 25.7% |
| same-language | 202 | 27.9% | 55.0% | 65.2% | 0.523 | 62.9% | 88.1% | 93.6% | 0.744 | 30.5% | 59.4% | 69.7% | 44.3% | 38.6% | 16.8% | 11.0% | 32.3% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5387, m014 0.5213, m015 0.4712)
retrieval: embedding


## 2026-10-12T11:34:16+00:00 — benchmark sweep31_methods_uwazi: section-split-1200-bge-m3-embedding

store: `data/benchmark_stores/section-split-1200-on__bge-m3-4d284af0.json` — 5,203 chunks, bge-m3 (1024d), built 2026-10-12T11:34:16+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 23.8% | 49.7% | 61.9% | 0.501 | 61.4% | 89.5% | 93.3% | 0.735 | 28.2% | 56.9% | 68.9% | 40.8% | 36.7% | 17.1% | 11.6% | 29.9% |
| en | 169 | 26.1% | 49.7% | 61.3% | 0.524 | 66.3% | 88.8% | 93.5% | 0.762 | 29.3% | 56.1% | 67.2% | 39.8% | 40.2% | 18.8% | 13.0% | 33.5% |
| es | 98 | 19.9% | 49.5% | 62.8% | 0.460 | 53.1% | 90.8% | 92.9% | 0.687 | 26.2% | 58.3% | 71.8% | 42.5% | 30.6% | 14.1% | 9.4% | 23.6% |
| synthetic | 255 | 23.8% | 50.0% | 62.2% | 0.503 | 60.8% | 89.0% | 92.9% | 0.729 | 28.4% | 57.3% | 69.1% | 41.3% | 36.9% | 17.2% | 11.8% | 30.0% |
| manual | 12 | 23.6% | 42.2% | 54.7% | 0.447 | 75.0% | 100.0% | 100.0% | 0.850 | 23.6% | 48.6% | 63.2% | 30.6% | 33.3% | 15.0% | 9.2% | 27.5% |
| cross-language | 65 | 17.0% | 40.0% | 58.4% | 0.445 | 55.4% | 92.3% | 92.3% | 0.694 | 23.6% | 49.1% | 64.0% | 28.2% | 32.3% | 16.9% | 12.6% | 24.2% |
| same-language | 202 | 26.0% | 52.8% | 63.0% | 0.519 | 63.4% | 88.6% | 93.6% | 0.748 | 29.7% | 59.4% | 70.4% | 44.8% | 38.1% | 17.1% | 11.3% | 31.7% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5387, m014 0.5213, m015 0.4712)
retrieval: embedding


## 2026-10-12T11:34:59+00:00 — benchmark sweep31_methods_uwazi: merge-1200-embeddinggemma-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__embeddinggemma-4d284af0.json` — 4,488 chunks, embeddinggemma (768d), built 2026-10-07T12:02:02+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 37.2% | 65.2% | 79.5% | 0.528 | 67.8% | 92.9% | 97.8% | 0.787 | 38.8% | 67.4% | 81.6% | 54.3% | 39.3% | 13.9% | 8.5% | 37.7% |
| en | 169 | 38.5% | 66.3% | 79.6% | 0.535 | 70.4% | 91.1% | 97.0% | 0.796 | 39.4% | 67.8% | 81.4% | 54.2% | 40.2% | 14.1% | 8.5% | 38.8% |
| es | 98 | 35.0% | 63.4% | 79.3% | 0.516 | 63.3% | 95.9% | 99.0% | 0.773 | 37.8% | 66.7% | 82.0% | 54.4% | 37.8% | 13.7% | 8.6% | 35.9% |
| synthetic | 255 | 37.8% | 65.6% | 78.9% | 0.533 | 67.1% | 92.5% | 97.6% | 0.781 | 39.5% | 67.8% | 81.1% | 54.5% | 40.0% | 14.0% | 8.5% | 38.3% |
| manual | 12 | 25.0% | 58.3% | 91.7% | 0.423 | 83.3% | 100.0% | 100.0% | 0.917 | 25.0% | 58.3% | 91.7% | 50.0% | 25.0% | 11.7% | 9.2% | 25.0% |
| cross-language | 65 | 35.1% | 59.7% | 77.4% | 0.501 | 56.9% | 89.2% | 98.5% | 0.707 | 36.4% | 62.3% | 79.2% | 45.6% | 38.5% | 13.2% | 8.5% | 35.1% |
| same-language | 202 | 37.9% | 67.0% | 80.1% | 0.537 | 71.3% | 94.1% | 97.5% | 0.813 | 39.6% | 69.0% | 82.3% | 57.1% | 39.6% | 14.2% | 8.5% | 38.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4994, m014 0.4174, m015 0.3793)
retrieval: embedding


## 2026-10-12T11:35:03+00:00 — benchmark sweep31_methods_uwazi: segment-2400-embeddinggemma-embedding

store: `data/benchmark_stores/segment-2400-on__embeddinggemma-4d284af0.json` — 11,649 chunks, embeddinggemma (768d), built 2026-10-12T11:35:03+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 19.6% | 36.5% | 45.2% | 0.515 | 65.2% | 91.8% | 96.3% | 0.771 | 19.6% | 36.7% | 45.6% | 36.5% | 36.7% | 16.0% | 10.6% | 27.7% |
| en | 169 | 20.4% | 37.5% | 45.6% | 0.516 | 68.6% | 89.9% | 94.7% | 0.785 | 20.4% | 37.5% | 45.6% | 38.0% | 36.7% | 16.0% | 10.8% | 29.2% |
| es | 98 | 18.1% | 34.9% | 44.6% | 0.513 | 59.2% | 94.9% | 99.0% | 0.746 | 18.1% | 35.4% | 45.6% | 33.7% | 36.7% | 16.1% | 10.4% | 25.2% |
| synthetic | 255 | 19.9% | 36.9% | 45.3% | 0.520 | 64.7% | 91.4% | 96.1% | 0.766 | 19.9% | 37.1% | 45.6% | 36.7% | 37.3% | 16.2% | 10.7% | 28.1% |
| manual | 12 | 13.2% | 29.2% | 45.1% | 0.397 | 75.0% | 100.0% | 100.0% | 0.875 | 13.2% | 29.2% | 45.1% | 31.9% | 25.0% | 13.3% | 10.0% | 20.1% |
| cross-language | 65 | 15.2% | 33.2% | 40.5% | 0.418 | 55.4% | 90.8% | 92.3% | 0.691 | 15.2% | 33.9% | 41.3% | 31.5% | 27.7% | 14.8% | 9.8% | 21.4% |
| same-language | 202 | 20.9% | 37.6% | 46.8% | 0.546 | 68.3% | 92.1% | 97.5% | 0.797 | 20.9% | 37.6% | 47.0% | 38.1% | 39.6% | 16.4% | 10.9% | 29.8% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5442, m014 0.4622, m015 0.4028)
retrieval: embedding


## 2026-10-12T11:36:10+00:00 — benchmark sweep31_methods_uwazi: section-1200-embeddinggemma-embedding

store: `data/benchmark_stores/section-1200-on__embeddinggemma-4d284af0.json` — 4,771 chunks, embeddinggemma (768d), built 2026-10-12T11:36:10+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 26.3% | 54.4% | 68.6% | 0.537 | 62.5% | 92.9% | 95.5% | 0.753 | 29.7% | 58.1% | 73.7% | 45.8% | 39.0% | 17.7% | 12.2% | 32.4% |
| en | 169 | 25.2% | 54.6% | 67.5% | 0.547 | 66.3% | 91.1% | 94.1% | 0.770 | 28.0% | 58.3% | 73.4% | 46.0% | 39.1% | 19.3% | 13.7% | 32.6% |
| es | 98 | 28.3% | 53.9% | 70.5% | 0.519 | 56.1% | 95.9% | 98.0% | 0.724 | 32.6% | 57.9% | 74.3% | 45.3% | 38.8% | 14.9% | 9.8% | 32.1% |
| synthetic | 255 | 26.7% | 55.3% | 69.2% | 0.541 | 61.6% | 92.5% | 95.3% | 0.746 | 30.2% | 59.0% | 74.0% | 46.5% | 39.6% | 18.0% | 12.3% | 32.6% |
| manual | 12 | 19.4% | 35.3% | 56.0% | 0.433 | 83.3% | 100.0% | 100.0% | 0.917 | 19.4% | 38.9% | 67.4% | 30.6% | 25.0% | 11.7% | 10.8% | 28.8% |
| cross-language | 65 | 24.1% | 50.4% | 68.8% | 0.535 | 60.0% | 93.8% | 93.8% | 0.731 | 28.8% | 54.0% | 73.2% | 38.4% | 41.5% | 18.8% | 13.8% | 30.1% |
| same-language | 202 | 27.1% | 55.6% | 68.5% | 0.537 | 63.4% | 92.6% | 96.0% | 0.761 | 30.0% | 59.5% | 73.9% | 48.1% | 38.1% | 17.3% | 11.7% | 33.1% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4889, m014 0.4150, m015 0.3812)
retrieval: embedding


## 2026-10-12T11:36:45+00:00 — benchmark sweep31_methods_uwazi: section-split-1200-embeddinggemma-embedding

store: `data/benchmark_stores/section-split-1200-on__embeddinggemma-4d284af0.json` — 5,203 chunks, embeddinggemma (768d), built 2026-10-12T11:36:45+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 25.4% | 52.9% | 66.3% | 0.537 | 62.9% | 92.5% | 95.9% | 0.753 | 30.2% | 58.9% | 73.5% | 45.1% | 39.7% | 18.1% | 12.5% | 31.2% |
| en | 169 | 24.7% | 53.5% | 65.9% | 0.548 | 66.9% | 91.1% | 94.1% | 0.770 | 28.8% | 58.8% | 73.0% | 45.5% | 40.2% | 19.8% | 14.0% | 31.6% |
| es | 98 | 26.6% | 51.9% | 67.0% | 0.519 | 56.1% | 94.9% | 99.0% | 0.723 | 32.6% | 58.9% | 74.3% | 44.3% | 38.8% | 15.3% | 9.9% | 30.6% |
| synthetic | 255 | 25.7% | 53.8% | 66.9% | 0.543 | 62.0% | 92.2% | 95.7% | 0.746 | 30.7% | 59.8% | 74.0% | 45.7% | 40.4% | 18.4% | 12.6% | 31.4% |
| manual | 12 | 19.4% | 35.3% | 53.1% | 0.418 | 83.3% | 100.0% | 100.0% | 0.903 | 19.4% | 38.9% | 61.8% | 30.6% | 25.0% | 11.7% | 10.0% | 28.6% |
| cross-language | 65 | 24.3% | 49.1% | 67.1% | 0.551 | 61.5% | 93.8% | 93.8% | 0.738 | 31.9% | 55.5% | 73.2% | 38.4% | 44.6% | 19.1% | 14.3% | 29.6% |
| same-language | 202 | 25.7% | 54.2% | 66.0% | 0.533 | 63.4% | 92.1% | 96.5% | 0.758 | 29.7% | 60.0% | 73.5% | 47.2% | 38.1% | 17.8% | 11.9% | 31.8% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4889, m014 0.4150, m015 0.3776)
retrieval: embedding


## 2026-10-12T11:37:21+00:00 — benchmark sweep31_methods_uwazi: merge-1200-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__snowflake-arctic-embed2-4d284af0.json` — 4,488 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-07T12:04:02+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 37.3% | 63.8% | 75.0% | 0.515 | 64.8% | 89.9% | 94.8% | 0.754 | 38.8% | 66.0% | 77.1% | 50.7% | 39.3% | 13.7% | 8.1% | 38.6% |
| en | 169 | 37.3% | 63.6% | 76.9% | 0.509 | 67.5% | 89.3% | 94.1% | 0.765 | 38.1% | 65.1% | 78.4% | 49.7% | 38.5% | 13.5% | 8.2% | 38.8% |
| es | 98 | 37.4% | 64.1% | 71.8% | 0.525 | 60.2% | 90.8% | 95.9% | 0.736 | 40.1% | 67.7% | 74.8% | 52.4% | 40.8% | 14.1% | 7.9% | 38.3% |
| synthetic | 255 | 37.5% | 64.1% | 74.6% | 0.517 | 63.9% | 89.4% | 94.5% | 0.747 | 39.1% | 66.4% | 76.8% | 50.7% | 39.6% | 13.8% | 8.1% | 38.8% |
| manual | 12 | 33.3% | 58.3% | 83.3% | 0.476 | 83.3% | 100.0% | 100.0% | 0.903 | 33.3% | 58.3% | 83.3% | 50.0% | 33.3% | 11.7% | 8.3% | 33.3% |
| cross-language | 65 | 30.3% | 60.8% | 73.1% | 0.468 | 53.8% | 89.2% | 93.8% | 0.681 | 32.8% | 63.1% | 76.2% | 41.5% | 33.8% | 13.5% | 8.2% | 31.5% |
| same-language | 202 | 39.6% | 64.8% | 75.7% | 0.530 | 68.3% | 90.1% | 95.0% | 0.778 | 40.8% | 67.0% | 77.4% | 53.6% | 41.1% | 13.8% | 8.1% | 40.8% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4227, m014 0.4076, m015 0.3614)
retrieval: embedding


## 2026-10-12T11:37:27+00:00 — benchmark sweep31_methods_uwazi: segment-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/segment-2400-on__snowflake-arctic-embed2-4d284af0.json` — 11,649 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-12T11:37:27+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 22.8% | 35.7% | 42.6% | 0.527 | 64.8% | 90.6% | 94.0% | 0.763 | 22.9% | 36.1% | 42.9% | 37.9% | 40.8% | 15.8% | 10.4% | 29.9% |
| en | 169 | 24.5% | 36.9% | 42.8% | 0.557 | 72.2% | 89.9% | 94.1% | 0.803 | 24.5% | 36.9% | 42.8% | 37.9% | 45.6% | 16.1% | 10.4% | 31.1% |
| es | 98 | 19.7% | 33.8% | 42.1% | 0.474 | 52.0% | 91.8% | 93.9% | 0.695 | 20.2% | 34.8% | 43.1% | 37.8% | 32.7% | 15.3% | 10.5% | 27.8% |
| synthetic | 255 | 22.6% | 35.6% | 42.4% | 0.528 | 63.9% | 90.6% | 93.7% | 0.758 | 22.8% | 36.0% | 42.8% | 37.6% | 40.8% | 15.8% | 10.5% | 29.8% |
| manual | 12 | 25.7% | 38.2% | 45.1% | 0.497 | 83.3% | 91.7% | 100.0% | 0.887 | 25.7% | 38.2% | 45.1% | 43.8% | 41.7% | 15.0% | 10.0% | 31.9% |
| cross-language | 65 | 14.8% | 31.1% | 36.2% | 0.403 | 55.4% | 89.2% | 90.8% | 0.693 | 15.6% | 31.8% | 37.0% | 32.4% | 26.2% | 14.8% | 9.8% | 24.3% |
| same-language | 202 | 25.3% | 37.2% | 44.6% | 0.566 | 67.8% | 91.1% | 95.0% | 0.786 | 25.3% | 37.5% | 44.8% | 39.6% | 45.5% | 16.1% | 10.6% | 31.7% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5087, m014 0.4550, m015 0.4235)
retrieval: embedding


## 2026-10-12T11:38:46+00:00 — benchmark sweep31_methods_uwazi: section-1200-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/section-1200-on__snowflake-arctic-embed2-4d284af0.json` — 4,771 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-12T11:38:46+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 26.3% | 51.4% | 64.4% | 0.505 | 61.4% | 89.9% | 94.0% | 0.735 | 29.2% | 55.7% | 67.8% | 43.3% | 36.7% | 16.8% | 11.5% | 31.5% |
| en | 169 | 26.7% | 50.4% | 65.2% | 0.529 | 65.7% | 89.3% | 95.3% | 0.757 | 29.0% | 55.1% | 68.8% | 42.4% | 39.1% | 18.2% | 13.1% | 32.6% |
| es | 98 | 25.5% | 53.2% | 63.0% | 0.463 | 54.1% | 90.8% | 91.8% | 0.695 | 29.5% | 56.5% | 66.0% | 44.8% | 32.7% | 14.3% | 8.6% | 29.7% |
| synthetic | 255 | 26.0% | 52.2% | 65.1% | 0.505 | 60.0% | 89.4% | 93.7% | 0.724 | 29.0% | 56.4% | 68.3% | 43.6% | 36.5% | 17.0% | 11.6% | 31.4% |
| manual | 12 | 31.9% | 35.3% | 49.0% | 0.514 | 91.7% | 100.0% | 100.0% | 0.958 | 31.9% | 38.9% | 55.6% | 36.1% | 41.7% | 11.7% | 9.2% | 34.3% |
| cross-language | 65 | 21.6% | 47.8% | 64.8% | 0.499 | 56.9% | 90.8% | 95.4% | 0.719 | 25.9% | 54.6% | 69.2% | 39.3% | 35.4% | 18.2% | 13.5% | 28.7% |
| same-language | 202 | 27.8% | 52.6% | 64.2% | 0.507 | 62.9% | 89.6% | 93.6% | 0.740 | 30.2% | 56.0% | 67.3% | 44.6% | 37.1% | 16.3% | 10.8% | 32.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4687, m014 0.4076, m015 0.3813)
retrieval: embedding


## 2026-10-12T11:39:27+00:00 — benchmark sweep31_methods_uwazi: section-split-1200-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/section-split-1200-on__snowflake-arctic-embed2-4d284af0.json` — 5,203 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-12T11:39:27+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 24.8% | 50.0% | 61.9% | 0.509 | 61.4% | 89.5% | 94.0% | 0.733 | 29.7% | 56.4% | 67.3% | 44.8% | 37.5% | 17.5% | 11.7% | 30.6% |
| en | 169 | 25.9% | 49.5% | 63.2% | 0.536 | 65.1% | 89.9% | 95.9% | 0.755 | 29.9% | 56.0% | 68.7% | 44.3% | 40.2% | 19.1% | 13.4% | 32.3% |
| es | 98 | 23.0% | 51.1% | 59.6% | 0.462 | 55.1% | 88.8% | 90.8% | 0.694 | 29.5% | 57.0% | 65.0% | 45.8% | 32.7% | 14.9% | 8.7% | 27.6% |
| synthetic | 255 | 24.5% | 50.7% | 62.5% | 0.509 | 60.4% | 89.0% | 93.7% | 0.724 | 29.6% | 57.2% | 67.9% | 45.2% | 37.3% | 17.8% | 11.8% | 30.4% |
| manual | 12 | 31.9% | 35.3% | 48.9% | 0.497 | 83.3% | 100.0% | 100.0% | 0.917 | 31.9% | 38.9% | 55.6% | 36.1% | 41.7% | 11.7% | 9.2% | 34.2% |
| cross-language | 65 | 20.3% | 46.2% | 62.5% | 0.507 | 58.5% | 92.3% | 96.9% | 0.726 | 27.4% | 56.9% | 69.8% | 40.8% | 36.9% | 19.1% | 13.8% | 27.8% |
| same-language | 202 | 26.3% | 51.3% | 61.7% | 0.509 | 62.4% | 88.6% | 93.1% | 0.735 | 30.5% | 56.2% | 66.5% | 46.1% | 37.6% | 17.0% | 11.0% | 31.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4687, m014 0.4076, m015 0.3813)
retrieval: embedding


## 2026-10-12T11:40:10+00:00 — benchmark sweep31_methods_uwazi — comparison (12 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| merge-1200-bge-m3-embedding | bge-m3 | 1200/0.15/on | embedding | 267 | 31.4% | 62.8% | 73.5% | 0.479 | 62.9% | 91.8% | 93.6% | 0.751 | 32.7% | 64.9% | 75.7% | 49.3% | 33.0% | 13.4% | 7.9% | 32.8% | 0/3 | reuse / 6.3s |
| segment-2400-bge-m3-embedding | bge-m3 | 2400/0/on | embedding | 267 | 20.5% | 34.5% | 42.9% | 0.505 | 60.7% | 89.1% | 94.0% | 0.734 | 20.7% | 34.9% | 43.2% | 32.8% | 37.5% | 14.6% | 9.7% | 27.1% | 0/3 | 74s / 6.4s |
| section-1200-bge-m3-embedding | bge-m3 | 1200/0.15/on | embedding | 267 | 25.5% | 51.5% | 63.8% | 0.501 | 61.0% | 88.8% | 92.9% | 0.732 | 28.4% | 56.1% | 68.1% | 40.0% | 36.7% | 16.7% | 11.3% | 30.7% | 0/3 | 37s / 3.3s |
| section-split-1200-bge-m3-embedding | bge-m3 | 1200/0.15/on | embedding | 267 | 23.8% | 49.7% | 61.9% | 0.501 | 61.4% | 89.5% | 93.3% | 0.735 | 28.2% | 56.9% | 68.9% | 40.8% | 36.7% | 17.1% | 11.6% | 29.9% | 0/3 | 38s / 3.7s |
| merge-1200-embeddinggemma-embedding | embeddinggemma | 1200/0.15/on | embedding | 267 | 37.2% | 65.2% | 79.5% | 0.528 | 67.8% | 92.9% | 97.8% | 0.787 | 38.8% | 67.4% | 81.6% | 54.3% | 39.3% | 13.9% | 8.5% | 37.7% | 0/3 | reuse / 3.3s |
| segment-2400-embeddinggemma-embedding | embeddinggemma | 2400/0/on | embedding | 267 | 19.6% | 36.5% | 45.2% | 0.515 | 65.2% | 91.8% | 96.3% | 0.771 | 19.6% | 36.7% | 45.6% | 36.5% | 36.7% | 16.0% | 10.6% | 27.7% | 0/3 | 61s / 4.8s |
| section-1200-embeddinggemma-embedding | embeddinggemma | 1200/0.15/on | embedding | 267 | 26.3% | 54.4% | 68.6% | 0.537 | 62.5% | 92.9% | 95.5% | 0.753 | 29.7% | 58.1% | 73.7% | 45.8% | 39.0% | 17.7% | 12.2% | 32.4% | 0/3 | 32s / 2.4s |
| section-split-1200-embeddinggemma-embedding | embeddinggemma | 1200/0.15/on | embedding | 267 | 25.4% | 52.9% | 66.3% | 0.537 | 62.9% | 92.5% | 95.9% | 0.753 | 30.2% | 58.9% | 73.5% | 45.1% | 39.7% | 18.1% | 12.5% | 31.2% | 0/3 | 33s / 2.6s |
| merge-1200-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1200/0.15/on | embedding | 267 | 37.3% | 63.8% | 75.0% | 0.515 | 64.8% | 89.9% | 94.8% | 0.754 | 38.8% | 66.0% | 77.1% | 50.7% | 39.3% | 13.7% | 8.1% | 38.6% | 0/3 | reuse / 4.8s |
| segment-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0/on | embedding | 267 | 22.8% | 35.7% | 42.6% | 0.527 | 64.8% | 90.6% | 94.0% | 0.763 | 22.9% | 36.1% | 42.9% | 37.9% | 40.8% | 15.8% | 10.4% | 29.9% | 0/3 | 71s / 6.3s |
| section-1200-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1200/0.15/on | embedding | 267 | 26.3% | 51.4% | 64.4% | 0.505 | 61.4% | 89.9% | 94.0% | 0.735 | 29.2% | 55.7% | 67.8% | 43.3% | 36.7% | 16.8% | 11.5% | 31.5% | 0/3 | 37s / 3.2s |
| section-split-1200-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1200/0.15/on | embedding | 267 | 24.8% | 50.0% | 61.9% | 0.509 | 61.4% | 89.5% | 94.0% | 0.733 | 29.7% | 56.4% | 67.3% | 44.8% | 37.5% | 17.5% | 11.7% | 30.6% | 0/3 | 39s / 3.4s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes


## 2026-10-12T11:47:53+00:00 — benchmark sweep31_methods_privacyqa — resolved plan

plan    : sweep31_methods_privacyqa — 6 experiment(s) over 6 store cell(s)
dataset : legalbenchrag-privacyqa
captures: data/raw/8a3f38ffd23a75e2 — 7 capture(s)
golden  : data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl — 199 row(s)
stores  :
  merge-2400-bge-m3      merge 2400/0.15/on     × bge-m3                       → data/benchmark_stores/merge-2400-0.15-on__bge-m3-260a60f1.json
  section-2400-bge-m3    section 2400/on        × bge-m3                       → data/benchmark_stores/section-2400-on__bge-m3-260a60f1.json
  merge-2400-embeddinggemma merge 2400/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-2400-0.15-on__embeddinggemma-260a60f1.json
  section-2400-embeddinggemma section 2400/on        × embeddinggemma               → data/benchmark_stores/section-2400-on__embeddinggemma-260a60f1.json
  merge-2400-snowflake-arctic-embed2 merge 2400/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-2400-0.15-on__snowflake-arctic-embed2-260a60f1.json
  section-2400-snowflake-arctic-embed2 section 2400/on        × snowflake-arctic-embed2      → data/benchmark_stores/section-2400-on__snowflake-arctic-embed2-260a60f1.json
experiments:
  1. merge-2400-bge-m3-embedding  → merge-2400-bge-m3      retrieval embedding
  2. section-2400-bge-m3-embedding → section-2400-bge-m3    retrieval embedding
  3. merge-2400-embeddinggemma-embedding → merge-2400-embeddinggemma retrieval embedding
  4. section-2400-embeddinggemma-embedding → section-2400-embeddinggemma retrieval embedding
  5. merge-2400-snowflake-arctic-embed2-embedding → merge-2400-snowflake-arctic-embed2 retrieval embedding
  6. section-2400-snowflake-arctic-embed2-embedding → section-2400-snowflake-arctic-embed2 retrieval embedding


## 2026-10-12T11:47:53+00:00 — benchmark sweep31_methods_privacyqa: merge-2400-bge-m3-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__bge-m3-260a60f1.json` — 79 chunks, bge-m3 (1024d), built 2026-10-08T12:44:33+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 36.2% | 82.5% | 95.5% | 0.752 | 100.0% | 100.0% | 100.0% | 1.000 | 38.4% | 81.6% | 95.5% | 38.4% | 59.8% | 30.2% | 18.2% | 53.0% |
| en | 194 | 36.2% | 82.5% | 95.5% | 0.752 | 100.0% | 100.0% | 100.0% | 1.000 | 38.4% | 81.6% | 95.5% | 38.4% | 59.8% | 30.2% | 18.2% | 53.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 36.2% | 82.5% | 95.5% | 0.752 | 100.0% | 100.0% | 100.0% | 1.000 | 38.4% | 81.6% | 95.5% | 38.4% | 59.8% | 30.2% | 18.2% | 53.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 1/5 (20.0%) (top-1: m001 0.4335, m002 0.5098, m003 0.4798, m004 0.5167, m005 0.5676)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-12T11:47:56+00:00 — benchmark sweep31_methods_privacyqa: section-2400-bge-m3-embedding

store: `data/benchmark_stores/section-2400-on__bge-m3-260a60f1.json` — 90 chunks, bge-m3 (1024d), built 2026-10-12T11:47:56+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 36.2% | 79.2% | 93.1% | 0.738 | 100.0% | 100.0% | 100.0% | 1.000 | 40.2% | 79.7% | 94.5% | 40.7% | 58.2% | 28.7% | 18.1% | 51.3% |
| en | 194 | 36.2% | 79.2% | 93.1% | 0.738 | 100.0% | 100.0% | 100.0% | 1.000 | 40.2% | 79.7% | 94.5% | 40.7% | 58.2% | 28.7% | 18.1% | 51.3% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 36.2% | 79.2% | 93.1% | 0.738 | 100.0% | 100.0% | 100.0% | 1.000 | 40.2% | 79.7% | 94.5% | 40.7% | 58.2% | 28.7% | 18.1% | 51.3% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 1/5 (20.0%) (top-1: m001 0.4335, m002 0.5098, m003 0.4798, m004 0.5167, m005 0.5676)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-12T11:47:58+00:00 — benchmark sweep31_methods_privacyqa: merge-2400-embeddinggemma-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__embeddinggemma-260a60f1.json` — 79 chunks, embeddinggemma (768d), built 2026-10-08T12:45:11+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 27.1% | 75.3% | 93.9% | 0.665 | 100.0% | 100.0% | 100.0% | 1.000 | 27.6% | 76.6% | 94.8% | 28.4% | 47.4% | 26.5% | 17.8% | 41.2% |
| en | 194 | 27.1% | 75.3% | 93.9% | 0.665 | 100.0% | 100.0% | 100.0% | 1.000 | 27.6% | 76.6% | 94.8% | 28.4% | 47.4% | 26.5% | 17.8% | 41.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 27.1% | 75.3% | 93.9% | 0.665 | 100.0% | 100.0% | 100.0% | 1.000 | 27.6% | 76.6% | 94.8% | 28.4% | 47.4% | 26.5% | 17.8% | 41.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.4271, m002 0.4689, m003 0.3906, m004 0.4205, m005 0.3975)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-12T11:48:00+00:00 — benchmark sweep31_methods_privacyqa: section-2400-embeddinggemma-embedding

store: `data/benchmark_stores/section-2400-on__embeddinggemma-260a60f1.json` — 90 chunks, embeddinggemma (768d), built 2026-10-12T11:48:00+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 31.2% | 76.1% | 91.9% | 0.716 | 100.0% | 100.0% | 100.0% | 1.000 | 32.7% | 77.3% | 93.3% | 35.2% | 56.2% | 27.9% | 18.1% | 46.6% |
| en | 194 | 31.2% | 76.1% | 91.9% | 0.716 | 100.0% | 100.0% | 100.0% | 1.000 | 32.7% | 77.3% | 93.3% | 35.2% | 56.2% | 27.9% | 18.1% | 46.6% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 31.2% | 76.1% | 91.9% | 0.716 | 100.0% | 100.0% | 100.0% | 1.000 | 32.7% | 77.3% | 93.3% | 35.2% | 56.2% | 27.9% | 18.1% | 46.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.4271, m002 0.4689, m003 0.3906, m004 0.4306, m005 0.3975)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-12T11:48:02+00:00 — benchmark sweep31_methods_privacyqa: merge-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__snowflake-arctic-embed2-260a60f1.json` — 79 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-08T12:45:29+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 33.8% | 80.9% | 96.0% | 0.717 | 100.0% | 100.0% | 100.0% | 1.000 | 34.5% | 83.3% | 97.1% | 34.5% | 55.2% | 29.6% | 18.4% | 49.1% |
| en | 194 | 33.8% | 80.9% | 96.0% | 0.717 | 100.0% | 100.0% | 100.0% | 1.000 | 34.5% | 83.3% | 97.1% | 34.5% | 55.2% | 29.6% | 18.4% | 49.1% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 33.8% | 80.9% | 96.0% | 0.717 | 100.0% | 100.0% | 100.0% | 1.000 | 34.5% | 83.3% | 97.1% | 34.5% | 55.2% | 29.6% | 18.4% | 49.1% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.3286, m002 0.4456, m003 0.3651, m004 0.4128, m005 0.5280)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-12T11:48:05+00:00 — benchmark sweep31_methods_privacyqa: section-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/section-2400-on__snowflake-arctic-embed2-260a60f1.json` — 90 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-12T11:48:05+00:00
golden: `data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl` — 199 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 194 | 33.6% | 77.5% | 94.1% | 0.714 | 100.0% | 100.0% | 100.0% | 1.000 | 35.0% | 79.3% | 95.4% | 36.4% | 55.7% | 29.0% | 18.6% | 49.9% |
| en | 194 | 33.6% | 77.5% | 94.1% | 0.714 | 100.0% | 100.0% | 100.0% | 1.000 | 35.0% | 79.3% | 95.4% | 36.4% | 55.7% | 29.0% | 18.6% | 49.9% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 194 | 33.6% | 77.5% | 94.1% | 0.714 | 100.0% | 100.0% | 100.0% | 1.000 | 35.0% | 79.3% | 95.4% | 36.4% | 55.7% | 29.0% | 18.6% | 49.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.3286, m002 0.4456, m003 0.3651, m004 0.4128, m005 0.5280)
retrieval: embedding
dataset: legalbenchrag-privacyqa


## 2026-10-12T11:48:07+00:00 — benchmark sweep31_methods_privacyqa — dataset legalbenchrag-privacyqa — comparison (6 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| merge-2400-bge-m3-embedding | bge-m3 | 2400/0.15/on | embedding | 194 | 36.2% | 82.5% | 95.5% | 0.752 | 100.0% | 100.0% | 100.0% | 1.000 | 38.4% | 81.6% | 95.5% | 38.4% | 59.8% | 30.2% | 18.2% | 53.0% | 1/5 | reuse / 2.8s |
| section-2400-bge-m3-embedding | bge-m3 | 2400/0.15/on | embedding | 194 | 36.2% | 79.2% | 93.1% | 0.738 | 100.0% | 100.0% | 100.0% | 1.000 | 40.2% | 79.7% | 94.5% | 40.7% | 58.2% | 28.7% | 18.1% | 51.3% | 1/5 | 1s / 1.0s |
| merge-2400-embeddinggemma-embedding | embeddinggemma | 2400/0.15/on | embedding | 194 | 27.1% | 75.3% | 93.9% | 0.665 | 100.0% | 100.0% | 100.0% | 1.000 | 27.6% | 76.6% | 94.8% | 28.4% | 47.4% | 26.5% | 17.8% | 41.2% | 0/5 | reuse / 1.7s |
| section-2400-embeddinggemma-embedding | embeddinggemma | 2400/0.15/on | embedding | 194 | 31.2% | 76.1% | 91.9% | 0.716 | 100.0% | 100.0% | 100.0% | 1.000 | 32.7% | 77.3% | 93.3% | 35.2% | 56.2% | 27.9% | 18.1% | 46.6% | 0/5 | 1s / 0.9s |
| merge-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0.15/on | embedding | 194 | 33.8% | 80.9% | 96.0% | 0.717 | 100.0% | 100.0% | 100.0% | 1.000 | 34.5% | 83.3% | 97.1% | 34.5% | 55.2% | 29.6% | 18.4% | 49.1% | 0/5 | reuse / 2.3s |
| section-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0.15/on | embedding | 194 | 33.6% | 77.5% | 94.1% | 0.714 | 100.0% | 100.0% | 100.0% | 1.000 | 35.0% | 79.3% | 95.4% | 36.4% | 55.7% | 29.0% | 18.6% | 49.9% | 0/5 | 1s / 1.0s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes


## 2026-10-12T11:48:15+00:00 — benchmark sweep31_methods_contractnli — resolved plan

plan    : sweep31_methods_contractnli — 9 experiment(s) over 9 store cell(s)
dataset : legalbenchrag-contractnli
captures: data/raw/d7f14657e7264534 — 95 capture(s)
golden  : data/eval/datasets/legalbenchrag-contractnli/golden.jsonl — 982 row(s)
stores  :
  merge-1200-bge-m3      merge 1200/0.15/on     × bge-m3                       → data/benchmark_stores/merge-1200-0.15-on__bge-m3-826d4d38.json
  section-1200-bge-m3    section 1200/on        × bge-m3                       → data/benchmark_stores/section-1200-on__bge-m3-826d4d38.json
  section-split-1200-bge-m3 section-split 1200/on  × bge-m3                       → data/benchmark_stores/section-split-1200-on__bge-m3-826d4d38.json
  merge-1200-embeddinggemma merge 1200/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-1200-0.15-on__embeddinggemma-826d4d38.json
  section-1200-embeddinggemma section 1200/on        × embeddinggemma               → data/benchmark_stores/section-1200-on__embeddinggemma-826d4d38.json
  section-split-1200-embeddinggemma section-split 1200/on  × embeddinggemma               → data/benchmark_stores/section-split-1200-on__embeddinggemma-826d4d38.json
  merge-1200-snowflake-arctic-embed2 merge 1200/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-1200-0.15-on__snowflake-arctic-embed2-826d4d38.json
  section-1200-snowflake-arctic-embed2 section 1200/on        × snowflake-arctic-embed2      → data/benchmark_stores/section-1200-on__snowflake-arctic-embed2-826d4d38.json
  section-split-1200-snowflake-arctic-embed2 section-split 1200/on  × snowflake-arctic-embed2      → data/benchmark_stores/section-split-1200-on__snowflake-arctic-embed2-826d4d38.json
experiments:
  1. merge-1200-bge-m3-embedding  → merge-1200-bge-m3      retrieval embedding
  2. section-1200-bge-m3-embedding → section-1200-bge-m3    retrieval embedding
  3. section-split-1200-bge-m3-embedding → section-split-1200-bge-m3 retrieval embedding
  4. merge-1200-embeddinggemma-embedding → merge-1200-embeddinggemma retrieval embedding
  5. section-1200-embeddinggemma-embedding → section-1200-embeddinggemma retrieval embedding
  6. section-split-1200-embeddinggemma-embedding → section-split-1200-embeddinggemma retrieval embedding
  7. merge-1200-snowflake-arctic-embed2-embedding → merge-1200-snowflake-arctic-embed2 retrieval embedding
  8. section-1200-snowflake-arctic-embed2-embedding → section-1200-snowflake-arctic-embed2 retrieval embedding
  9. section-split-1200-snowflake-arctic-embed2-embedding → section-split-1200-snowflake-arctic-embed2 retrieval embedding


## 2026-10-12T11:48:15+00:00 — benchmark sweep31_methods_contractnli: merge-1200-bge-m3-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__bge-m3-826d4d38.json` — 1,091 chunks, bge-m3 (1024d), built 2026-10-08T12:48:54+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 34.4% | 71.7% | 82.2% | 0.601 | 84.7% | 94.9% | 97.4% | 0.891 | 38.6% | 75.7% | 84.7% | 57.8% | 44.8% | 19.8% | 11.6% | 40.5% |
| en | 977 | 34.4% | 71.7% | 82.2% | 0.601 | 84.7% | 94.9% | 97.4% | 0.891 | 38.6% | 75.7% | 84.7% | 57.8% | 44.8% | 19.8% | 11.6% | 40.5% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 34.4% | 71.7% | 82.2% | 0.601 | 84.7% | 94.9% | 97.4% | 0.891 | 38.6% | 75.7% | 84.7% | 57.8% | 44.8% | 19.8% | 11.6% | 40.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 3/5 (60.0%) (top-1: m001 0.5987, m002 0.5915, m003 0.5079, m004 0.5906, m005 0.5354)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-12T11:48:21+00:00 — benchmark sweep31_methods_contractnli: section-1200-bge-m3-embedding

store: `data/benchmark_stores/section-1200-on__bge-m3-826d4d38.json` — 2,170 chunks, bge-m3 (1024d), built 2026-10-12T11:48:21+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 34.0% | 68.3% | 79.2% | 0.548 | 78.8% | 94.4% | 96.6% | 0.855 | 34.9% | 69.6% | 79.8% | 59.4% | 39.5% | 17.1% | 10.2% | 38.2% |
| en | 977 | 34.0% | 68.3% | 79.2% | 0.548 | 78.8% | 94.4% | 96.6% | 0.855 | 34.9% | 69.6% | 79.8% | 59.4% | 39.5% | 17.1% | 10.2% | 38.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 34.0% | 68.3% | 79.2% | 0.548 | 78.8% | 94.4% | 96.6% | 0.855 | 34.9% | 69.6% | 79.8% | 59.4% | 39.5% | 17.1% | 10.2% | 38.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 3/5 (60.0%) (top-1: m001 0.5911, m002 0.6278, m003 0.5061, m004 0.5906, m005 0.5349)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-12T11:48:43+00:00 — benchmark sweep31_methods_contractnli: section-split-1200-bge-m3-embedding

store: `data/benchmark_stores/section-split-1200-on__bge-m3-826d4d38.json` — 2,255 chunks, bge-m3 (1024d), built 2026-10-12T11:48:43+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 30.8% | 64.6% | 76.0% | 0.552 | 78.8% | 94.3% | 96.6% | 0.856 | 35.3% | 70.0% | 79.8% | 61.7% | 39.7% | 18.0% | 11.0% | 37.1% |
| en | 977 | 30.8% | 64.6% | 76.0% | 0.552 | 78.8% | 94.3% | 96.6% | 0.856 | 35.3% | 70.0% | 79.8% | 61.7% | 39.7% | 18.0% | 11.0% | 37.1% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 30.8% | 64.6% | 76.0% | 0.552 | 78.8% | 94.3% | 96.6% | 0.856 | 35.3% | 70.0% | 79.8% | 61.7% | 39.7% | 18.0% | 11.0% | 37.1% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 3/5 (60.0%) (top-1: m001 0.5904, m002 0.6278, m003 0.5061, m004 0.5906, m005 0.5349)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-12T11:49:06+00:00 — benchmark sweep31_methods_contractnli: merge-1200-embeddinggemma-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__embeddinggemma-826d4d38.json` — 1,091 chunks, embeddinggemma (768d), built 2026-10-08T12:52:39+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 39.4% | 76.1% | 86.9% | 0.651 | 91.2% | 97.6% | 99.1% | 0.938 | 44.4% | 79.3% | 89.0% | 61.7% | 51.1% | 21.0% | 12.3% | 45.6% |
| en | 977 | 39.4% | 76.1% | 86.9% | 0.651 | 91.2% | 97.6% | 99.1% | 0.938 | 44.4% | 79.3% | 89.0% | 61.7% | 51.1% | 21.0% | 12.3% | 45.6% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 39.4% | 76.1% | 86.9% | 0.651 | 91.2% | 97.6% | 99.1% | 0.938 | 44.4% | 79.3% | 89.0% | 61.7% | 51.1% | 21.0% | 12.3% | 45.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 2/5 (40.0%) (top-1: m001 0.6348, m002 0.5382, m003 0.4253, m004 0.5654, m005 0.4834)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-12T11:49:13+00:00 — benchmark sweep31_methods_contractnli: section-1200-embeddinggemma-embedding

store: `data/benchmark_stores/section-1200-on__embeddinggemma-826d4d38.json` — 2,170 chunks, embeddinggemma (768d), built 2026-10-12T11:49:13+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 37.8% | 72.4% | 82.7% | 0.598 | 86.9% | 96.4% | 98.3% | 0.910 | 39.1% | 73.4% | 83.5% | 64.5% | 44.4% | 18.2% | 10.6% | 42.2% |
| en | 977 | 37.8% | 72.4% | 82.7% | 0.598 | 86.9% | 96.4% | 98.3% | 0.910 | 39.1% | 73.4% | 83.5% | 64.5% | 44.4% | 18.2% | 10.6% | 42.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 37.8% | 72.4% | 82.7% | 0.598 | 86.9% | 96.4% | 98.3% | 0.910 | 39.1% | 73.4% | 83.5% | 64.5% | 44.4% | 18.2% | 10.6% | 42.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 3/5 (60.0%) (top-1: m001 0.6385, m002 0.5628, m003 0.4515, m004 0.5654, m005 0.5292)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-12T11:49:30+00:00 — benchmark sweep31_methods_contractnli: section-split-1200-embeddinggemma-embedding

store: `data/benchmark_stores/section-split-1200-on__embeddinggemma-826d4d38.json` — 2,255 chunks, embeddinggemma (768d), built 2026-10-12T11:49:30+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 35.3% | 69.3% | 80.8% | 0.610 | 87.5% | 97.1% | 98.5% | 0.916 | 40.8% | 74.2% | 84.5% | 65.6% | 46.1% | 19.4% | 11.6% | 41.2% |
| en | 977 | 35.3% | 69.3% | 80.8% | 0.610 | 87.5% | 97.1% | 98.5% | 0.916 | 40.8% | 74.2% | 84.5% | 65.6% | 46.1% | 19.4% | 11.6% | 41.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 35.3% | 69.3% | 80.8% | 0.610 | 87.5% | 97.1% | 98.5% | 0.916 | 40.8% | 74.2% | 84.5% | 65.6% | 46.1% | 19.4% | 11.6% | 41.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 3/5 (60.0%) (top-1: m001 0.6385, m002 0.5685, m003 0.4515, m004 0.5654, m005 0.5292)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-12T11:49:51+00:00 — benchmark sweep31_methods_contractnli: merge-1200-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__snowflake-arctic-embed2-826d4d38.json` — 1,091 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-08T12:53:27+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 30.7% | 66.5% | 76.8% | 0.563 | 82.0% | 95.0% | 97.2% | 0.877 | 35.0% | 70.3% | 79.1% | 53.9% | 40.4% | 18.5% | 11.0% | 37.5% |
| en | 977 | 30.7% | 66.5% | 76.8% | 0.563 | 82.0% | 95.0% | 97.2% | 0.877 | 35.0% | 70.3% | 79.1% | 53.9% | 40.4% | 18.5% | 11.0% | 37.5% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 30.7% | 66.5% | 76.8% | 0.563 | 82.0% | 95.0% | 97.2% | 0.877 | 35.0% | 70.3% | 79.1% | 53.9% | 40.4% | 18.5% | 11.0% | 37.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.5421, m002 0.5065, m003 0.3097, m004 0.4755, m005 0.4074)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-12T11:49:59+00:00 — benchmark sweep31_methods_contractnli: section-1200-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/section-1200-on__snowflake-arctic-embed2-826d4d38.json` — 2,170 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-12T11:49:59+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 28.2% | 63.2% | 74.2% | 0.497 | 83.6% | 94.9% | 96.6% | 0.887 | 29.3% | 64.0% | 74.6% | 58.3% | 34.0% | 16.1% | 9.7% | 32.1% |
| en | 977 | 28.2% | 63.2% | 74.2% | 0.497 | 83.6% | 94.9% | 96.6% | 0.887 | 29.3% | 64.0% | 74.6% | 58.3% | 34.0% | 16.1% | 9.7% | 32.1% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 28.2% | 63.2% | 74.2% | 0.497 | 83.6% | 94.9% | 96.6% | 0.887 | 29.3% | 64.0% | 74.6% | 58.3% | 34.0% | 16.1% | 9.7% | 32.1% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.5290, m002 0.5211, m003 0.3628, m004 0.4787, m005 0.4543)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-12T11:50:19+00:00 — benchmark sweep31_methods_contractnli: section-split-1200-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/section-split-1200-on__snowflake-arctic-embed2-826d4d38.json` — 2,255 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-12T11:50:19+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 25.9% | 60.4% | 72.2% | 0.509 | 83.7% | 94.9% | 96.6% | 0.888 | 30.7% | 65.0% | 75.4% | 60.9% | 35.4% | 17.3% | 10.6% | 31.5% |
| en | 977 | 25.9% | 60.4% | 72.2% | 0.509 | 83.7% | 94.9% | 96.6% | 0.888 | 30.7% | 65.0% | 75.4% | 60.9% | 35.4% | 17.3% | 10.6% | 31.5% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 25.9% | 60.4% | 72.2% | 0.509 | 83.7% | 94.9% | 96.6% | 0.888 | 30.7% | 65.0% | 75.4% | 60.9% | 35.4% | 17.3% | 10.6% | 31.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.5342, m002 0.5245, m003 0.3628, m004 0.4798, m005 0.4543)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-12T11:50:40+00:00 — benchmark sweep31_methods_contractnli — dataset legalbenchrag-contractnli — comparison (9 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| merge-1200-bge-m3-embedding | bge-m3 | 1200/0.15/on | embedding | 977 | 34.4% | 71.7% | 82.2% | 0.601 | 84.7% | 94.9% | 97.4% | 0.891 | 38.6% | 75.7% | 84.7% | 57.8% | 44.8% | 19.8% | 11.6% | 40.5% | 3/5 | reuse / 6.0s |
| section-1200-bge-m3-embedding | bge-m3 | 1200/0.15/on | embedding | 977 | 34.0% | 68.3% | 79.2% | 0.548 | 78.8% | 94.4% | 96.6% | 0.855 | 34.9% | 69.6% | 79.8% | 59.4% | 39.5% | 17.1% | 10.2% | 38.2% | 3/5 | 14s / 8.3s |
| section-split-1200-bge-m3-embedding | bge-m3 | 1200/0.15/on | embedding | 977 | 30.8% | 64.6% | 76.0% | 0.552 | 78.8% | 94.3% | 96.6% | 0.856 | 35.3% | 70.0% | 79.8% | 61.7% | 39.7% | 18.0% | 11.0% | 37.1% | 3/5 | 14s / 7.6s |
| merge-1200-embeddinggemma-embedding | embeddinggemma | 1200/0.15/on | embedding | 977 | 39.4% | 76.1% | 86.9% | 0.651 | 91.2% | 97.6% | 99.1% | 0.938 | 44.4% | 79.3% | 89.0% | 61.7% | 51.1% | 21.0% | 12.3% | 45.6% | 2/5 | reuse / 6.9s |
| section-1200-embeddinggemma-embedding | embeddinggemma | 1200/0.15/on | embedding | 977 | 37.8% | 72.4% | 82.7% | 0.598 | 86.9% | 96.4% | 98.3% | 0.910 | 39.1% | 73.4% | 83.5% | 64.5% | 44.4% | 18.2% | 10.6% | 42.2% | 3/5 | 11s / 6.6s |
| section-split-1200-embeddinggemma-embedding | embeddinggemma | 1200/0.15/on | embedding | 977 | 35.3% | 69.3% | 80.8% | 0.610 | 87.5% | 97.1% | 98.5% | 0.916 | 40.8% | 74.2% | 84.5% | 65.6% | 46.1% | 19.4% | 11.6% | 41.2% | 3/5 | 11s / 9.2s |
| merge-1200-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1200/0.15/on | embedding | 977 | 30.7% | 66.5% | 76.8% | 0.563 | 82.0% | 95.0% | 97.2% | 0.877 | 35.0% | 70.3% | 79.1% | 53.9% | 40.4% | 18.5% | 11.0% | 37.5% | 0/5 | reuse / 7.9s |
| section-1200-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1200/0.15/on | embedding | 977 | 28.2% | 63.2% | 74.2% | 0.497 | 83.6% | 94.9% | 96.6% | 0.887 | 29.3% | 64.0% | 74.6% | 58.3% | 34.0% | 16.1% | 9.7% | 32.1% | 0/5 | 13s / 7.3s |
| section-split-1200-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1200/0.15/on | embedding | 977 | 25.9% | 60.4% | 72.2% | 0.509 | 83.7% | 94.9% | 96.6% | 0.888 | 30.7% | 65.0% | 75.4% | 60.9% | 35.4% | 17.3% | 10.6% | 31.5% | 0/5 | 13s / 7.6s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes


## 2026-10-12T12:04:54+00:00 — benchmark sweep32_methods_cuad — resolved plan

plan    : sweep32_methods_cuad — 9 experiment(s) over 9 store cell(s)
dataset : legalbenchrag-cuad
captures: data/raw/c88547bc806ea086 — 462 capture(s)
golden  : data/eval/datasets/legalbenchrag-cuad/golden.jsonl — 4046 row(s)
stores  :
  merge-2400-bge-m3      merge 2400/0.15/on     × bge-m3                       → data/benchmark_stores/merge-2400-0.15-on__bge-m3-47d5d5a2.json
  section-2400-bge-m3    section 2400/on        × bge-m3                       → data/benchmark_stores/section-2400-on__bge-m3-47d5d5a2.json
  section-split-2400-bge-m3 section-split 2400/on  × bge-m3                       → data/benchmark_stores/section-split-2400-on__bge-m3-47d5d5a2.json
  merge-2400-embeddinggemma merge 2400/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-2400-0.15-on__embeddinggemma-47d5d5a2.json
  section-2400-embeddinggemma section 2400/on        × embeddinggemma               → data/benchmark_stores/section-2400-on__embeddinggemma-47d5d5a2.json
  section-split-2400-embeddinggemma section-split 2400/on  × embeddinggemma               → data/benchmark_stores/section-split-2400-on__embeddinggemma-47d5d5a2.json
  merge-2400-snowflake-arctic-embed2 merge 2400/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-2400-0.15-on__snowflake-arctic-embed2-47d5d5a2.json
  section-2400-snowflake-arctic-embed2 section 2400/on        × snowflake-arctic-embed2      → data/benchmark_stores/section-2400-on__snowflake-arctic-embed2-47d5d5a2.json
  section-split-2400-snowflake-arctic-embed2 section-split 2400/on  × snowflake-arctic-embed2      → data/benchmark_stores/section-split-2400-on__snowflake-arctic-embed2-47d5d5a2.json
experiments:
  1. merge-2400-bge-m3-embedding  → merge-2400-bge-m3      retrieval embedding
  2. section-2400-bge-m3-embedding → section-2400-bge-m3    retrieval embedding
  3. section-split-2400-bge-m3-embedding → section-split-2400-bge-m3 retrieval embedding
  4. merge-2400-embeddinggemma-embedding → merge-2400-embeddinggemma retrieval embedding
  5. section-2400-embeddinggemma-embedding → section-2400-embeddinggemma retrieval embedding
  6. section-split-2400-embeddinggemma-embedding → section-split-2400-embeddinggemma retrieval embedding
  7. merge-2400-snowflake-arctic-embed2-embedding → merge-2400-snowflake-arctic-embed2 retrieval embedding
  8. section-2400-snowflake-arctic-embed2-embedding → section-2400-snowflake-arctic-embed2 retrieval embedding
  9. section-split-2400-snowflake-arctic-embed2-embedding → section-split-2400-snowflake-arctic-embed2 retrieval embedding


## 2026-10-12T12:04:54+00:00 — benchmark sweep32_methods_cuad: merge-2400-bge-m3-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__bge-m3-47d5d5a2.json` — 13,459 chunks, bge-m3 (1024d), built 2026-10-08T13:03:49+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 9.8% | 42.4% | 60.5% | 0.318 | 98.6% | 100.0% | 100.0% | 0.993 | 11.9% | 49.0% | 67.3% | 12.5% | 14.2% | 13.1% | 9.9% | 14.5% |
| en | 4042 | 9.8% | 42.4% | 60.5% | 0.318 | 98.6% | 100.0% | 100.0% | 0.993 | 11.9% | 49.0% | 67.3% | 12.5% | 14.2% | 13.1% | 9.9% | 14.5% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 9.8% | 42.4% | 60.5% | 0.318 | 98.6% | 100.0% | 100.0% | 0.993 | 11.9% | 49.0% | 67.3% | 12.5% | 14.2% | 13.1% | 9.9% | 14.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6057, m002 0.5807, m003 0.6199, m004 0.5856)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-12T12:06:32+00:00 — benchmark sweep32_methods_cuad: section-2400-bge-m3-embedding

store: `data/benchmark_stores/section-2400-on__bge-m3-47d5d5a2.json` — 32,691 chunks, bge-m3 (1024d), built 2026-10-12T12:06:32+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 7.6% | 38.1% | 56.6% | 0.260 | 98.6% | 100.0% | 100.0% | 0.993 | 8.3% | 39.9% | 57.9% | 12.6% | 9.8% | 10.8% | 8.4% | 11.3% |
| en | 4042 | 7.6% | 38.1% | 56.6% | 0.260 | 98.6% | 100.0% | 100.0% | 0.993 | 8.3% | 39.9% | 57.9% | 12.6% | 9.8% | 10.8% | 8.4% | 11.3% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 7.6% | 38.1% | 56.6% | 0.260 | 98.6% | 100.0% | 100.0% | 0.993 | 8.3% | 39.9% | 57.9% | 12.6% | 9.8% | 10.8% | 8.4% | 11.3% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.5970, m002 0.5812, m003 0.6043, m004 0.6151)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-12T12:14:03+00:00 — benchmark sweep32_methods_cuad: section-split-2400-bge-m3-embedding

store: `data/benchmark_stores/section-split-2400-on__bge-m3-47d5d5a2.json` — 34,816 chunks, bge-m3 (1024d), built 2026-10-12T12:14:03+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 6.3% | 32.8% | 49.9% | 0.263 | 98.6% | 100.0% | 100.0% | 0.992 | 8.6% | 39.6% | 57.2% | 15.0% | 10.3% | 11.4% | 9.4% | 11.9% |
| en | 4042 | 6.3% | 32.8% | 49.9% | 0.263 | 98.6% | 100.0% | 100.0% | 0.992 | 8.6% | 39.6% | 57.2% | 15.0% | 10.3% | 11.4% | 9.4% | 11.9% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 6.3% | 32.8% | 49.9% | 0.263 | 98.6% | 100.0% | 100.0% | 0.992 | 8.6% | 39.6% | 57.2% | 15.0% | 10.3% | 11.4% | 9.4% | 11.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.5889, m002 0.5807, m003 0.6113, m004 0.6151)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-12T12:21:51+00:00 — benchmark sweep32_methods_cuad: merge-2400-embeddinggemma-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__embeddinggemma-47d5d5a2.json` — 13,459 chunks, embeddinggemma (768d), built 2026-10-08T14:18:01+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 16.8% | 51.8% | 68.0% | 0.421 | 97.9% | 100.0% | 100.0% | 0.989 | 20.2% | 58.9% | 75.0% | 21.1% | 24.2% | 16.0% | 11.0% | 22.9% |
| en | 4042 | 16.8% | 51.8% | 68.0% | 0.421 | 97.9% | 100.0% | 100.0% | 0.989 | 20.2% | 58.9% | 75.0% | 21.1% | 24.2% | 16.0% | 11.0% | 22.9% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 16.8% | 51.8% | 68.0% | 0.421 | 97.9% | 100.0% | 100.0% | 0.989 | 20.2% | 58.9% | 75.0% | 21.1% | 24.2% | 16.0% | 11.0% | 22.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5256, m002 0.5389, m003 0.5898, m004 0.5026)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-12T12:23:00+00:00 — benchmark sweep32_methods_cuad: section-2400-embeddinggemma-embedding

store: `data/benchmark_stores/section-2400-on__embeddinggemma-47d5d5a2.json` — 32,691 chunks, embeddinggemma (768d), built 2026-10-12T12:23:01+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 16.4% | 49.6% | 65.2% | 0.375 | 96.4% | 99.8% | 99.9% | 0.979 | 17.6% | 51.5% | 66.6% | 23.0% | 21.1% | 14.1% | 9.7% | 21.1% |
| en | 4042 | 16.4% | 49.6% | 65.2% | 0.375 | 96.4% | 99.8% | 99.9% | 0.979 | 17.6% | 51.5% | 66.6% | 23.0% | 21.1% | 14.1% | 9.7% | 21.1% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 16.4% | 49.6% | 65.2% | 0.375 | 96.4% | 99.8% | 99.9% | 0.979 | 17.6% | 51.5% | 66.6% | 23.0% | 21.1% | 14.1% | 9.7% | 21.1% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 2/4 (50.0%) (top-1: m001 0.5426, m002 0.5661, m003 0.6110, m004 0.5147)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-12T12:29:06+00:00 — benchmark sweep32_methods_cuad: section-split-2400-embeddinggemma-embedding

store: `data/benchmark_stores/section-split-2400-on__embeddinggemma-47d5d5a2.json` — 34,816 chunks, embeddinggemma (768d), built 2026-10-12T12:29:06+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 14.4% | 44.3% | 59.2% | 0.383 | 96.7% | 99.8% | 99.9% | 0.981 | 18.4% | 51.8% | 66.3% | 27.1% | 22.1% | 15.3% | 10.9% | 21.5% |
| en | 4042 | 14.4% | 44.3% | 59.2% | 0.383 | 96.7% | 99.8% | 99.9% | 0.981 | 18.4% | 51.8% | 66.3% | 27.1% | 22.1% | 15.3% | 10.9% | 21.5% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 14.4% | 44.3% | 59.2% | 0.383 | 96.7% | 99.8% | 99.9% | 0.981 | 18.4% | 51.8% | 66.3% | 27.1% | 22.1% | 15.3% | 10.9% | 21.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 2/4 (50.0%) (top-1: m001 0.5426, m002 0.5661, m003 0.6318, m004 0.5147)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-12T12:36:01+00:00 — benchmark sweep32_methods_cuad: merge-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__snowflake-arctic-embed2-47d5d5a2.json` — 13,459 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-08T14:29:14+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 10.2% | 41.8% | 61.0% | 0.318 | 98.5% | 100.0% | 100.0% | 0.992 | 12.5% | 47.6% | 67.2% | 13.2% | 14.5% | 12.8% | 9.9% | 14.9% |
| en | 4042 | 10.2% | 41.8% | 61.0% | 0.318 | 98.5% | 100.0% | 100.0% | 0.992 | 12.5% | 47.6% | 67.2% | 13.2% | 14.5% | 12.8% | 9.9% | 14.9% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 10.2% | 41.8% | 61.0% | 0.318 | 98.5% | 100.0% | 100.0% | 0.992 | 12.5% | 47.6% | 67.2% | 13.2% | 14.5% | 12.8% | 9.9% | 14.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.4727, m002 0.4814, m003 0.5743, m004 0.4756)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-12T12:37:19+00:00 — benchmark sweep32_methods_cuad: section-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/section-2400-on__snowflake-arctic-embed2-47d5d5a2.json` — 32,691 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-12T12:37:19+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 8.0% | 32.9% | 48.5% | 0.238 | 98.0% | 100.0% | 100.0% | 0.989 | 8.7% | 34.1% | 49.5% | 13.5% | 10.3% | 9.3% | 7.1% | 10.9% |
| en | 4042 | 8.0% | 32.9% | 48.5% | 0.238 | 98.0% | 100.0% | 100.0% | 0.989 | 8.7% | 34.1% | 49.5% | 13.5% | 10.3% | 9.3% | 7.1% | 10.9% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 8.0% | 32.9% | 48.5% | 0.238 | 98.0% | 100.0% | 100.0% | 0.989 | 8.7% | 34.1% | 49.5% | 13.5% | 10.3% | 9.3% | 7.1% | 10.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5098, m002 0.5198, m003 0.5926, m004 0.5414)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-12T12:45:36+00:00 — benchmark sweep32_methods_cuad: section-split-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/section-split-2400-on__snowflake-arctic-embed2-47d5d5a2.json` — 34,816 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-12T12:45:36+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 7.0% | 29.0% | 44.1% | 0.247 | 98.0% | 100.0% | 100.0% | 0.990 | 9.6% | 34.6% | 50.2% | 16.3% | 11.4% | 10.1% | 8.1% | 11.6% |
| en | 4042 | 7.0% | 29.0% | 44.1% | 0.247 | 98.0% | 100.0% | 100.0% | 0.990 | 9.6% | 34.6% | 50.2% | 16.3% | 11.4% | 10.1% | 8.1% | 11.6% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 7.0% | 29.0% | 44.1% | 0.247 | 98.0% | 100.0% | 100.0% | 0.990 | 9.6% | 34.6% | 50.2% | 16.3% | 11.4% | 10.1% | 8.1% | 11.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5098, m002 0.5198, m003 0.5926, m004 0.5414)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-12T12:54:08+00:00 — benchmark sweep32_methods_cuad — dataset legalbenchrag-cuad — comparison (9 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| merge-2400-bge-m3-embedding | bge-m3 | 2400/0.15/on | embedding | 4042 | 9.8% | 42.4% | 60.5% | 0.318 | 98.6% | 100.0% | 100.0% | 0.993 | 11.9% | 49.0% | 67.3% | 12.5% | 14.2% | 13.1% | 9.9% | 14.5% | 4/4 | reuse / 95.9s |
| section-2400-bge-m3-embedding | bge-m3 | 2400/0.15/on | embedding | 4042 | 7.6% | 38.1% | 56.6% | 0.260 | 98.6% | 100.0% | 100.0% | 0.993 | 8.3% | 39.9% | 57.9% | 12.6% | 9.8% | 10.8% | 8.4% | 11.3% | 4/4 | 272s / 173.6s |
| section-split-2400-bge-m3-embedding | bge-m3 | 2400/0.15/on | embedding | 4042 | 6.3% | 32.8% | 49.9% | 0.263 | 98.6% | 100.0% | 100.0% | 0.992 | 8.6% | 39.6% | 57.2% | 15.0% | 10.3% | 11.4% | 9.4% | 11.9% | 4/4 | 278s / 184.2s |
| merge-2400-embeddinggemma-embedding | embeddinggemma | 2400/0.15/on | embedding | 4042 | 16.8% | 51.8% | 68.0% | 0.421 | 97.9% | 100.0% | 100.0% | 0.989 | 20.2% | 58.9% | 75.0% | 21.1% | 24.2% | 16.0% | 11.0% | 22.9% | 1/4 | reuse / 68.5s |
| section-2400-embeddinggemma-embedding | embeddinggemma | 2400/0.15/on | embedding | 4042 | 16.4% | 49.6% | 65.2% | 0.375 | 96.4% | 99.8% | 99.9% | 0.979 | 17.6% | 51.5% | 66.6% | 23.0% | 21.1% | 14.1% | 9.7% | 21.1% | 2/4 | 223s / 138.0s |
| section-split-2400-embeddinggemma-embedding | embeddinggemma | 2400/0.15/on | embedding | 4042 | 14.4% | 44.3% | 59.2% | 0.383 | 96.7% | 99.8% | 99.9% | 0.981 | 18.4% | 51.8% | 66.3% | 27.1% | 22.1% | 15.3% | 10.9% | 21.5% | 2/4 | 255s / 155.6s |
| merge-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0.15/on | embedding | 4042 | 10.2% | 41.8% | 61.0% | 0.318 | 98.5% | 100.0% | 100.0% | 0.992 | 12.5% | 47.6% | 67.2% | 13.2% | 14.5% | 12.8% | 9.9% | 14.9% | 1/4 | reuse / 76.8s |
| section-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0.15/on | embedding | 4042 | 8.0% | 32.9% | 48.5% | 0.238 | 98.0% | 100.0% | 100.0% | 0.989 | 8.7% | 34.1% | 49.5% | 13.5% | 10.3% | 9.3% | 7.1% | 10.9% | 1/4 | 294s / 196.9s |
| section-split-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0.15/on | embedding | 4042 | 7.0% | 29.0% | 44.1% | 0.247 | 98.0% | 100.0% | 100.0% | 0.990 | 9.6% | 34.6% | 50.2% | 16.3% | 11.4% | 10.1% | 8.1% | 11.6% | 1/4 | 305s / 200.5s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes


## 2026-10-12T13:14:37+00:00 — benchmark sweep32_methods_maud — resolved plan

plan    : sweep32_methods_maud — 9 experiment(s) over 9 store cell(s)
dataset : legalbenchrag-maud
captures: data/raw/4961ebee611362f6 — 150 capture(s)
golden  : data/eval/datasets/legalbenchrag-maud/golden.jsonl — 1680 row(s)
stores  :
  merge-2400-bge-m3      merge 2400/0.15/on     × bge-m3                       → data/benchmark_stores/merge-2400-0.15-on__bge-m3-68231218.json
  section-2400-bge-m3    section 2400/on        × bge-m3                       → data/benchmark_stores/section-2400-on__bge-m3-68231218.json
  section-split-2400-bge-m3 section-split 2400/on  × bge-m3                       → data/benchmark_stores/section-split-2400-on__bge-m3-68231218.json
  merge-2400-embeddinggemma merge 2400/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-2400-0.15-on__embeddinggemma-68231218.json
  section-2400-embeddinggemma section 2400/on        × embeddinggemma               → data/benchmark_stores/section-2400-on__embeddinggemma-68231218.json
  section-split-2400-embeddinggemma section-split 2400/on  × embeddinggemma               → data/benchmark_stores/section-split-2400-on__embeddinggemma-68231218.json
  merge-2400-snowflake-arctic-embed2 merge 2400/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-2400-0.15-on__snowflake-arctic-embed2-68231218.json
  section-2400-snowflake-arctic-embed2 section 2400/on        × snowflake-arctic-embed2      → data/benchmark_stores/section-2400-on__snowflake-arctic-embed2-68231218.json
  section-split-2400-snowflake-arctic-embed2 section-split 2400/on  × snowflake-arctic-embed2      → data/benchmark_stores/section-split-2400-on__snowflake-arctic-embed2-68231218.json
experiments:
  1. merge-2400-bge-m3-embedding  → merge-2400-bge-m3      retrieval embedding
  2. section-2400-bge-m3-embedding → section-2400-bge-m3    retrieval embedding
  3. section-split-2400-bge-m3-embedding → section-split-2400-bge-m3 retrieval embedding
  4. merge-2400-embeddinggemma-embedding → merge-2400-embeddinggemma retrieval embedding
  5. section-2400-embeddinggemma-embedding → section-2400-embeddinggemma retrieval embedding
  6. section-split-2400-embeddinggemma-embedding → section-split-2400-embeddinggemma retrieval embedding
  7. merge-2400-snowflake-arctic-embed2-embedding → merge-2400-snowflake-arctic-embed2 retrieval embedding
  8. section-2400-snowflake-arctic-embed2-embedding → section-2400-snowflake-arctic-embed2 retrieval embedding
  9. section-split-2400-snowflake-arctic-embed2-embedding → section-split-2400-snowflake-arctic-embed2 retrieval embedding


## 2026-10-12T13:14:37+00:00 — benchmark sweep32_methods_maud: merge-2400-bge-m3-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__bge-m3-68231218.json` — 28,860 chunks, bge-m3 (1024d), built 2026-10-09T09:06:18+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 11.0% | 26.0% | 35.3% | 0.312 | 93.4% | 98.0% | 99.0% | 0.955 | 15.6% | 35.1% | 46.6% | 15.9% | 19.6% | 10.8% | 7.6% | 16.6% |
| en | 1676 | 11.0% | 26.0% | 35.3% | 0.312 | 93.4% | 98.0% | 99.0% | 0.955 | 15.6% | 35.1% | 46.6% | 15.9% | 19.6% | 10.8% | 7.6% | 16.6% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 11.0% | 26.0% | 35.3% | 0.312 | 93.4% | 98.0% | 99.0% | 0.955 | 15.6% | 35.1% | 46.6% | 15.9% | 19.6% | 10.8% | 7.6% | 16.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6228, m002 0.5728, m003 0.5710, m004 0.5636)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-12T13:15:52+00:00 — benchmark sweep32_methods_maud: section-2400-bge-m3-embedding

store: `data/benchmark_stores/section-2400-on__bge-m3-68231218.json` — 31,868 chunks, bge-m3 (1024d), built 2026-10-12T13:15:52+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 13.4% | 30.6% | 39.8% | 0.292 | 91.8% | 96.8% | 98.2% | 0.940 | 14.8% | 32.5% | 42.1% | 10.5% | 18.7% | 10.5% | 7.6% | 18.0% |
| en | 1676 | 13.4% | 30.6% | 39.8% | 0.292 | 91.8% | 96.8% | 98.2% | 0.940 | 14.8% | 32.5% | 42.1% | 10.5% | 18.7% | 10.5% | 7.6% | 18.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 13.4% | 30.6% | 39.8% | 0.292 | 91.8% | 96.8% | 98.2% | 0.940 | 14.8% | 32.5% | 42.1% | 10.5% | 18.7% | 10.5% | 7.6% | 18.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6224, m002 0.5805, m003 0.5662, m004 0.5763)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-12T13:24:02+00:00 — benchmark sweep32_methods_maud: section-split-2400-bge-m3-embedding

store: `data/benchmark_stores/section-split-2400-on__bge-m3-68231218.json` — 40,538 chunks, bge-m3 (1024d), built 2026-10-12T13:24:02+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 10.7% | 24.3% | 32.5% | 0.301 | 92.9% | 97.3% | 98.8% | 0.948 | 15.6% | 33.3% | 43.5% | 15.6% | 19.8% | 11.5% | 8.6% | 17.4% |
| en | 1676 | 10.7% | 24.3% | 32.5% | 0.301 | 92.9% | 97.3% | 98.8% | 0.948 | 15.6% | 33.3% | 43.5% | 15.6% | 19.8% | 11.5% | 8.6% | 17.4% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 10.7% | 24.3% | 32.5% | 0.301 | 92.9% | 97.3% | 98.8% | 0.948 | 15.6% | 33.3% | 43.5% | 15.6% | 19.8% | 11.5% | 8.6% | 17.4% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6199, m002 0.5812, m003 0.5710, m004 0.5739)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-12T13:33:41+00:00 — benchmark sweep32_methods_maud: merge-2400-embeddinggemma-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__embeddinggemma-68231218.json` — 28,860 chunks, embeddinggemma (768d), built 2026-10-09T11:15:00+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 9.4% | 24.0% | 33.6% | 0.284 | 90.8% | 97.8% | 98.7% | 0.938 | 13.1% | 32.3% | 43.3% | 14.0% | 16.9% | 9.6% | 7.0% | 14.0% |
| en | 1676 | 9.4% | 24.0% | 33.6% | 0.284 | 90.8% | 97.8% | 98.7% | 0.938 | 13.1% | 32.3% | 43.3% | 14.0% | 16.9% | 9.6% | 7.0% | 14.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 9.4% | 24.0% | 33.6% | 0.284 | 90.8% | 97.8% | 98.7% | 0.938 | 13.1% | 32.3% | 43.3% | 14.0% | 16.9% | 9.6% | 7.0% | 14.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5299, m002 0.5417, m003 0.5307, m004 0.5751)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-12T13:34:42+00:00 — benchmark sweep32_methods_maud: section-2400-embeddinggemma-embedding

store: `data/benchmark_stores/section-2400-on__embeddinggemma-68231218.json` — 31,868 chunks, embeddinggemma (768d), built 2026-10-12T13:34:42+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 8.6% | 22.3% | 32.1% | 0.211 | 87.3% | 94.6% | 97.2% | 0.907 | 9.4% | 24.2% | 34.6% | 8.9% | 11.5% | 7.3% | 6.0% | 11.7% |
| en | 1676 | 8.6% | 22.3% | 32.1% | 0.211 | 87.3% | 94.6% | 97.2% | 0.907 | 9.4% | 24.2% | 34.6% | 8.9% | 11.5% | 7.3% | 6.0% | 11.7% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 8.6% | 22.3% | 32.1% | 0.211 | 87.3% | 94.6% | 97.2% | 0.907 | 9.4% | 24.2% | 34.6% | 8.9% | 11.5% | 7.3% | 6.0% | 11.7% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5481, m002 0.5428, m003 0.5377, m004 0.5640)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-12T13:41:07+00:00 — benchmark sweep32_methods_maud: section-split-2400-embeddinggemma-embedding

store: `data/benchmark_stores/section-split-2400-on__embeddinggemma-68231218.json` — 40,538 chunks, embeddinggemma (768d), built 2026-10-12T13:41:07+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 8.1% | 19.8% | 28.0% | 0.249 | 89.9% | 96.1% | 98.2% | 0.928 | 11.9% | 27.9% | 38.3% | 14.4% | 14.9% | 9.0% | 7.1% | 13.2% |
| en | 1676 | 8.1% | 19.8% | 28.0% | 0.249 | 89.9% | 96.1% | 98.2% | 0.928 | 11.9% | 27.9% | 38.3% | 14.4% | 14.9% | 9.0% | 7.1% | 13.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 8.1% | 19.8% | 28.0% | 0.249 | 89.9% | 96.1% | 98.2% | 0.928 | 11.9% | 27.9% | 38.3% | 14.4% | 14.9% | 9.0% | 7.1% | 13.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5481, m002 0.5428, m003 0.5191, m004 0.5640)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-12T13:48:42+00:00 — benchmark sweep32_methods_maud: merge-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__snowflake-arctic-embed2-68231218.json` — 28,860 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-09T11:33:06+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 6.7% | 18.9% | 29.3% | 0.231 | 93.2% | 97.6% | 98.4% | 0.952 | 9.7% | 25.4% | 38.0% | 10.2% | 12.7% | 7.8% | 6.4% | 10.2% |
| en | 1676 | 6.7% | 18.9% | 29.3% | 0.231 | 93.2% | 97.6% | 98.4% | 0.952 | 9.7% | 25.4% | 38.0% | 10.2% | 12.7% | 7.8% | 6.4% | 10.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 6.7% | 18.9% | 29.3% | 0.231 | 93.2% | 97.6% | 98.4% | 0.952 | 9.7% | 25.4% | 38.0% | 10.2% | 12.7% | 7.8% | 6.4% | 10.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 0/4 (0.0%) (top-1: m001 0.5088, m002 0.4913, m003 0.4963, m004 0.5138)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-12T13:49:55+00:00 — benchmark sweep32_methods_maud: section-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/section-2400-on__snowflake-arctic-embed2-68231218.json` — 31,868 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-12T13:49:55+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 7.3% | 18.5% | 26.9% | 0.188 | 90.8% | 95.7% | 97.8% | 0.932 | 8.0% | 20.2% | 29.1% | 7.2% | 10.3% | 6.4% | 5.2% | 10.3% |
| en | 1676 | 7.3% | 18.5% | 26.9% | 0.188 | 90.8% | 95.7% | 97.8% | 0.932 | 8.0% | 20.2% | 29.1% | 7.2% | 10.3% | 6.4% | 5.2% | 10.3% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 7.3% | 18.5% | 26.9% | 0.188 | 90.8% | 95.7% | 97.8% | 0.932 | 8.0% | 20.2% | 29.1% | 7.2% | 10.3% | 6.4% | 5.2% | 10.3% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 0/4 (0.0%) (top-1: m001 0.4860, m002 0.4955, m003 0.4793, m004 0.5127)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-12T13:58:25+00:00 — benchmark sweep32_methods_maud: section-split-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/section-split-2400-on__snowflake-arctic-embed2-68231218.json` — 40,538 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-12T13:58:25+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 6.1% | 15.6% | 23.4% | 0.206 | 92.0% | 96.7% | 98.2% | 0.942 | 8.9% | 21.8% | 32.1% | 10.5% | 11.5% | 7.4% | 6.2% | 10.6% |
| en | 1676 | 6.1% | 15.6% | 23.4% | 0.206 | 92.0% | 96.7% | 98.2% | 0.942 | 8.9% | 21.8% | 32.1% | 10.5% | 11.5% | 7.4% | 6.2% | 10.6% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 6.1% | 15.6% | 23.4% | 0.206 | 92.0% | 96.7% | 98.2% | 0.942 | 8.9% | 21.8% | 32.1% | 10.5% | 11.5% | 7.4% | 6.2% | 10.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 0/4 (0.0%) (top-1: m001 0.5170, m002 0.4955, m003 0.4793, m004 0.5127)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-12T14:08:03+00:00 — benchmark sweep32_methods_maud — dataset legalbenchrag-maud — comparison (9 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| merge-2400-bge-m3-embedding | bge-m3 | 2400/0.15/on | embedding | 1676 | 11.0% | 26.0% | 35.3% | 0.312 | 93.4% | 98.0% | 99.0% | 0.955 | 15.6% | 35.1% | 46.6% | 15.9% | 19.6% | 10.8% | 7.6% | 16.6% | 4/4 | reuse / 71.5s |
| section-2400-bge-m3-embedding | bge-m3 | 2400/0.15/on | embedding | 1676 | 13.4% | 30.6% | 39.8% | 0.292 | 91.8% | 96.8% | 98.2% | 0.940 | 14.8% | 32.5% | 42.1% | 10.5% | 18.7% | 10.5% | 7.6% | 18.0% | 4/4 | 407s / 76.5s |
| section-split-2400-bge-m3-embedding | bge-m3 | 2400/0.15/on | embedding | 1676 | 10.7% | 24.3% | 32.5% | 0.301 | 92.9% | 97.3% | 98.8% | 0.948 | 15.6% | 33.3% | 43.5% | 15.6% | 19.8% | 11.5% | 8.6% | 17.4% | 4/4 | 479s / 93.5s |
| merge-2400-embeddinggemma-embedding | embeddinggemma | 2400/0.15/on | embedding | 1676 | 9.4% | 24.0% | 33.6% | 0.284 | 90.8% | 97.8% | 98.7% | 0.938 | 13.1% | 32.3% | 43.3% | 14.0% | 16.9% | 9.6% | 7.0% | 14.0% | 1/4 | reuse / 58.7s |
| section-2400-embeddinggemma-embedding | embeddinggemma | 2400/0.15/on | embedding | 1676 | 8.6% | 22.3% | 32.1% | 0.211 | 87.3% | 94.6% | 97.2% | 0.907 | 9.4% | 24.2% | 34.6% | 8.9% | 11.5% | 7.3% | 6.0% | 11.7% | 1/4 | 317s / 63.7s |
| section-split-2400-embeddinggemma-embedding | embeddinggemma | 2400/0.15/on | embedding | 1676 | 8.1% | 19.8% | 28.0% | 0.249 | 89.9% | 96.1% | 98.2% | 0.928 | 11.9% | 27.9% | 38.3% | 14.4% | 14.9% | 9.0% | 7.1% | 13.2% | 1/4 | 375s / 74.3s |
| merge-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0.15/on | embedding | 1676 | 6.7% | 18.9% | 29.3% | 0.231 | 93.2% | 97.6% | 98.4% | 0.952 | 9.7% | 25.4% | 38.0% | 10.2% | 12.7% | 7.8% | 6.4% | 10.2% | 0/4 | reuse / 69.3s |
| section-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0.15/on | embedding | 1676 | 7.3% | 18.5% | 26.9% | 0.188 | 90.8% | 95.7% | 97.8% | 0.932 | 8.0% | 20.2% | 29.1% | 7.2% | 10.3% | 6.4% | 5.2% | 10.3% | 0/4 | 426s / 79.1s |
| section-split-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0.15/on | embedding | 1676 | 6.1% | 15.6% | 23.4% | 0.206 | 92.0% | 96.7% | 98.2% | 0.942 | 8.9% | 21.8% | 32.1% | 10.5% | 11.5% | 7.4% | 6.2% | 10.6% | 0/4 | 478s / 92.0s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes


---

## 2026-10-13 — Stage 3 chunking-methods verdict (waves 3.0–3.2 combined — hand-recorded read of the sweep31/sweep32 comparison tables above; no new runs, no new numbers)

Scope: 45 cells — sweep31_methods_uwazi (4 arms × 3 models), sweep31_methods_privacyqa (2 × 3), sweep31_methods_contractnli (3 × 3), sweep32_methods_cuad (3 × 3), sweep32_methods_maud (3 × 3); three shortlist models (bge-m3 / embeddinggemma / snowflake-arctic-embed2); every arm raced at its home's recorded leader geometry; 15 of 45 rows reuse existing merge stores (30 new builds: 18 wave-3.1, 12 wave-3.2). No separate 3.1 verdict was recorded (user call 2026-10-12) — this is the one combined 3.x block. Lenses as in Stage 2: doc@10 = decider, chunk R@1/MRR = ranking lens, P@1, cov@3000 = cross-geometry pack lens, false-retr = GATE (directional at the single global 0.55), plus the new-for-4c chunk-count column (Step-5 cost proxy). Per-model triples below are bge / gemma / snowflake. m = merge, s = section, ss = section-split, seg = segment (uwazi-only).

| home (n) | chunks m / s / ss | decider doc@10 | chunk R@1 | chunk MRR | P@1 | cov@3000 | gate (0.55) |
|---|---|---|---|---|---|---|---|
| uwazi@1200 (267) | 4,488 / 4,771 / 5,203 (seg 11,649) | m 93.6/97.8/94.8; s −0.7/−2.3/−0.8; ss −0.3/−1.9/−0.8 → m all models | m 31.4/37.2/37.3; s −5.9…−11.0; ss −7.6…−12.5 → m | s +0.02/+0.01/−0.01; ss ≈ s → tie, bge-only s edge | s +3.7/−0.3/−2.6; ss +3.7/+0.4/−1.8 → m 2 of 3 | m 49.3/54.3/50.7; s −9.3/−8.5/−7.4; ss −8.5/−9.2/−5.9 → m | 0/3 on every arm, every model |
| privacyqa@2400 (194) | 79 / 90 / — (ss skipped: max paragraph 1,064 < 2400) | saturated: doc@10 100% every arm | bge tie 36.2=36.2; gemma s +4.1 (27.1→31.2); snowflake m +0.2 → m/tie on 2, s gemma | s −0.01/−0.00/+0.05 → tie | s +8.8 gemma (same single-doc effect) | s +2.3/+6.8/+1.9 | bge 1/5 both arms; gemma 0/5 both; snowflake 0/5 both |
| contractnli@1200 (977) | 1,091 / 2,170 / 2,255 | m 97.4/99.1/97.2; s −0.8/−0.8/−0.6; ss −0.8/−0.6/−0.6 → m all models | m 34.4/39.4/30.7; s −0.4…−2.5; ss −3.6…−4.8 → m | m 0.601/0.651/0.563; s −0.05…−0.07; ss −0.04…−0.05 → m | m 44.8/51.1/40.4; s −5.3…−6.7; ss −5.0…−5.1 → m | ss 61.7/65.6/60.9 (m −3.9/−3.9/−7.0) → ss | bge 3/5 all arms; gemma 2/5 m → 3/5 s,ss; snowflake 0/5 all arms |
| cuad@2400 (4,042) | 13,459 / 32,691 / 34,816 | saturated: doc@10 99.9–100 every arm (gemma doc@1 m 97.9 vs s 96.4 / ss 96.7) | m 9.8/16.8/10.2; s −0.4…−2.2; ss −2.4…−3.5 → m | m 0.318/0.421/0.318; s −0.05…−0.08; ss −0.04…−0.07 → m | m 14.2/24.2/14.5; s −3.1…−4.4; ss −2.1…−3.9 → m | ss 15.0/27.1/16.3 (m −2.5/−6.0/−3.1) → ss | bge 4/4 all arms; gemma 1/4 m → 2/4 s,ss; snowflake 1/4 all arms |
| maud@2400 (1,676) | 28,860 / 31,868 / 40,538 | m 99.0/98.7/98.4; s −0.8/−1.5/−0.6; ss −0.2/−0.5/−0.2 → m all models | m 11.0/9.4/6.7; s +2.4/−0.8/+0.6; ss 10.7/8.1/6.1 → m gemma, s edges bge+snowflake | m 0.312/0.284/0.231; s −0.02/−0.07/−0.04; ss −0.01/−0.04/−0.03 → m | m 19.6/16.9/12.7; s −0.9/−5.4/−2.4; ss −0.2(tie)/+2.0/+1.2 → m | m 15.9/14.0/10.2; s −5.4/−5.1/−3.0 (collapse); ss −0.3/+0.4/+0.3 (≈m) | bge 4/4 all arms; gemma 1/4 all arms; snowflake 0/4 all arms |

Findings (in-dataset comparisons only):

1. **merge holds the decider on all five homes; no arm ever wins doc@10.** Decisive on uwazi (all 3 models), contractnli (+0.6–0.8 merge margin on all 3), maud (all 3); saturated on privacyqa (7 docs) and cuad — where gemma's doc@1 (merge 97.9 vs s 96.4 / ss 96.7) is the only live doc-level residue, and it favors merge.
2. **Chunk-ranking lens: merge leads chunk R@1 outright on uwazi, contractnli, cuad (all models).** privacyqa ties (bge 36.2=36.2) or splits per model (snowflake merge; gemma's +4.1 section edge comes from the ONE headed doc — 6/7 stores byte-equal fallback, 79 vs 90 chunks); maud splits per model (gemma merge; s edges bge +2.4 and snowflake +0.6). A per-model split, not an arm split. R@5/R@10/RP follow the same tilt (the one section chunk-recall win: maud bge R@5 +4.6 / R@10 +4.5, inside that same pattern).
3. **cov@3000 is the only lens non-merge wins, and it buys nothing that matters.** ss leads contractnli (+3.9/+3.9/+7.0) and cuad (+2.5/+6.0/+3.1) while giving back chunk R@1 (−3.6…−4.8 / −2.4…−3.5) and MRR (−0.04…−0.07) — and the decider never moves to ss. On uwazi both section arms LOSE cov@3000 (−5.9…−9.3). Pack lens and ranking lens move in opposite directions again, exactly as Stage-2 finding 5 predicted.
4. **The maud monster readout validates the pre-stated mechanism — as repair, not as a win.** With 52.1% of text mass in over-budget sections, s's cov@3000 collapses (−5.4/−5.1/−3.0); ss's word-split monster pieces (overlap 0.15 inside the paragraph) repair it to merge parity (−0.3/+0.4/+0.3). But repair ≠ victory: ss multiplies maud's store 1.40× (40,538 vs 28,860) while R@1/MRR/P@1/doc@10 all stay merge (only bge P@1 ties, 19.8 vs 19.6).
5. **The false-retr gate tracks the model, not the geometry — Stage-2 finding reconfirmed on all five homes.** bge trips 3/5 (contractnli) and 4/4 (cuad, maud) on EVERY arm; snowflake is the cleanest (0 trips on uwazi/privacyqa/contractnli/maud, cuad 1/4); gemma middle. Only geometry deviations are one-row threshold crossings (gemma: contractnli 2/5→3/5, cuad 1/4→2/4 on section arms). Per-model threshold re-derivation (lock wave) stands as pre-declared.
6. **Cost column (Step 5).** s/ss stores: 2.43×/2.59× merge on cuad, ~2× on contractnli, 1.10×/1.40× on maud, 1.06–1.16× on uwazi, 1.14× on privacyqa; finalist builds 200–500s/model vs reused merge stores. Embedding + pgvector cost scales with this column — at zero decider gain. seg confirmed its pre-statement: line-per-chunk on the LBR captures (11,649 chunks vs merge 4,488 on uwazi), disqualified as pre-stated.

Decision (user, 2026-10-13): **merge wins Stage 3.** Lock chunker = merge at each home's recorded leader geometry — uwazi@1200, privacyqa@2400, contractnli@1200, cuad@2400, maud@2400; vic passthrough-4096 unchanged (out of scope, pre-chunked); header on; overlap 0.15 on merge's monster cuts. section, section-split and segment arms are rejected for the lock (their code stays as race arms; unused at the lock). Wave 3.3 rung 2 runs ON merge, ONE change at a time: (a) monster cuts prefer sentence ends (new pure cut code; tests + PLAN pre-statement first); (b) every-chunk breadcrumb "title — section". Small instruments first, finalists confirm.


## 2026-10-13T12:52:51+00:00 — benchmark sweep33_methods_uwazi — resolved plan

plan    : sweep33_methods_uwazi — 12 experiment(s) over 12 store cell(s)
captures: data/raw/bdd5a7c445847b35 — 77 capture(s)
golden  : data/eval/golden.jsonl — 270 row(s)
stores  :
  merge-1200-bge-m3      merge 1200/0.15/on     × bge-m3                       → data/benchmark_stores/merge-1200-0.15-on__bge-m3-4d284af0.json
  merge-sent-1200-bge-m3 merge 1200/0.15/on +sentences × bge-m3                       → data/benchmark_stores/merge-1200-0.15-on-sentences__bge-m3-4d284af0.json
  merge-crumb-1200-bge-m3 merge 1200/0.15/on +breadcrumb × bge-m3                       → data/benchmark_stores/merge-1200-0.15-on-crumb__bge-m3-4d284af0.json
  merge-sent-crumb-1200-bge-m3 merge 1200/0.15/on +sentences +breadcrumb × bge-m3                       → data/benchmark_stores/merge-1200-0.15-on-sentences-crumb__bge-m3-4d284af0.json
  merge-1200-embeddinggemma merge 1200/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-1200-0.15-on__embeddinggemma-4d284af0.json
  merge-sent-1200-embeddinggemma merge 1200/0.15/on +sentences × embeddinggemma               → data/benchmark_stores/merge-1200-0.15-on-sentences__embeddinggemma-4d284af0.json
  merge-crumb-1200-embeddinggemma merge 1200/0.15/on +breadcrumb × embeddinggemma               → data/benchmark_stores/merge-1200-0.15-on-crumb__embeddinggemma-4d284af0.json
  merge-sent-crumb-1200-embeddinggemma merge 1200/0.15/on +sentences +breadcrumb × embeddinggemma               → data/benchmark_stores/merge-1200-0.15-on-sentences-crumb__embeddinggemma-4d284af0.json
  merge-1200-snowflake-arctic-embed2 merge 1200/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-1200-0.15-on__snowflake-arctic-embed2-4d284af0.json
  merge-sent-1200-snowflake-arctic-embed2 merge 1200/0.15/on +sentences × snowflake-arctic-embed2      → data/benchmark_stores/merge-1200-0.15-on-sentences__snowflake-arctic-embed2-4d284af0.json
  merge-crumb-1200-snowflake-arctic-embed2 merge 1200/0.15/on +breadcrumb × snowflake-arctic-embed2      → data/benchmark_stores/merge-1200-0.15-on-crumb__snowflake-arctic-embed2-4d284af0.json
  merge-sent-crumb-1200-snowflake-arctic-embed2 merge 1200/0.15/on +sentences +breadcrumb × snowflake-arctic-embed2      → data/benchmark_stores/merge-1200-0.15-on-sentences-crumb__snowflake-arctic-embed2-4d284af0.json
experiments:
  1. merge-1200-bge-m3-embedding  → merge-1200-bge-m3      retrieval embedding
  2. merge-sent-1200-bge-m3-embedding → merge-sent-1200-bge-m3 retrieval embedding
  3. merge-crumb-1200-bge-m3-embedding → merge-crumb-1200-bge-m3 retrieval embedding
  4. merge-sent-crumb-1200-bge-m3-embedding → merge-sent-crumb-1200-bge-m3 retrieval embedding
  5. merge-1200-embeddinggemma-embedding → merge-1200-embeddinggemma retrieval embedding
  6. merge-sent-1200-embeddinggemma-embedding → merge-sent-1200-embeddinggemma retrieval embedding
  7. merge-crumb-1200-embeddinggemma-embedding → merge-crumb-1200-embeddinggemma retrieval embedding
  8. merge-sent-crumb-1200-embeddinggemma-embedding → merge-sent-crumb-1200-embeddinggemma retrieval embedding
  9. merge-1200-snowflake-arctic-embed2-embedding → merge-1200-snowflake-arctic-embed2 retrieval embedding
  10. merge-sent-1200-snowflake-arctic-embed2-embedding → merge-sent-1200-snowflake-arctic-embed2 retrieval embedding
  11. merge-crumb-1200-snowflake-arctic-embed2-embedding → merge-crumb-1200-snowflake-arctic-embed2 retrieval embedding
  12. merge-sent-crumb-1200-snowflake-arctic-embed2-embedding → merge-sent-crumb-1200-snowflake-arctic-embed2 retrieval embedding


## 2026-10-13T12:52:51+00:00 — benchmark sweep33_methods_uwazi: merge-1200-bge-m3-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__bge-m3-4d284af0.json` — 4,488 chunks, bge-m3 (1024d), built 2026-10-13T12:52:53+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.4% | 62.8% | 73.5% | 0.479 | 62.9% | 91.8% | 93.6% | 0.751 | 32.7% | 64.9% | 75.7% | 49.3% | 33.0% | 13.4% | 7.9% | 32.8% |
| en | 169 | 32.8% | 64.2% | 73.4% | 0.484 | 68.0% | 92.9% | 93.5% | 0.782 | 33.3% | 66.3% | 75.0% | 50.5% | 33.7% | 13.6% | 7.8% | 34.3% |
| es | 98 | 28.9% | 60.4% | 73.8% | 0.470 | 54.1% | 89.8% | 93.9% | 0.698 | 31.6% | 62.6% | 76.9% | 47.3% | 31.6% | 13.1% | 8.1% | 30.3% |
| synthetic | 255 | 31.3% | 62.6% | 73.1% | 0.479 | 62.4% | 91.4% | 93.3% | 0.747 | 32.7% | 64.8% | 75.4% | 49.7% | 32.9% | 13.4% | 7.9% | 32.8% |
| manual | 12 | 33.3% | 66.7% | 83.3% | 0.476 | 75.0% | 100.0% | 100.0% | 0.833 | 33.3% | 66.7% | 83.3% | 41.7% | 33.3% | 13.3% | 8.3% | 33.3% |
| cross-language | 65 | 23.6% | 53.3% | 70.0% | 0.412 | 55.4% | 92.3% | 95.4% | 0.701 | 25.1% | 56.9% | 72.1% | 37.4% | 26.2% | 11.7% | 7.8% | 24.1% |
| same-language | 202 | 33.9% | 65.8% | 74.7% | 0.500 | 65.3% | 91.6% | 93.1% | 0.767 | 35.1% | 67.5% | 76.9% | 53.1% | 35.1% | 14.0% | 7.9% | 35.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5359, m014 0.5081, m015 0.4582)
retrieval: embedding


## 2026-10-13T12:53:32+00:00 — benchmark sweep33_methods_uwazi: merge-sent-1200-bge-m3-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-sentences__bge-m3-4d284af0.json` — 4,514 chunks, bge-m3 (1024d), built 2026-10-13T12:53:32+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.4% | 63.3% | 74.5% | 0.479 | 62.2% | 91.0% | 93.3% | 0.745 | 32.7% | 65.7% | 76.3% | 50.3% | 33.0% | 13.6% | 8.0% | 32.8% |
| en | 169 | 32.8% | 64.8% | 74.6% | 0.484 | 67.5% | 92.3% | 92.9% | 0.776 | 33.3% | 66.9% | 75.9% | 52.1% | 33.7% | 13.7% | 7.9% | 34.3% |
| es | 98 | 28.9% | 60.7% | 74.3% | 0.471 | 53.1% | 88.8% | 93.9% | 0.690 | 31.6% | 63.6% | 76.9% | 47.3% | 31.6% | 13.3% | 8.1% | 30.3% |
| synthetic | 255 | 31.3% | 63.1% | 74.1% | 0.479 | 61.6% | 90.6% | 92.9% | 0.741 | 32.7% | 65.6% | 75.9% | 50.3% | 32.9% | 13.6% | 8.0% | 32.8% |
| manual | 12 | 33.3% | 66.7% | 83.3% | 0.482 | 75.0% | 100.0% | 100.0% | 0.829 | 33.3% | 66.7% | 83.3% | 50.0% | 33.3% | 13.3% | 8.3% | 33.3% |
| cross-language | 65 | 23.6% | 56.4% | 72.3% | 0.419 | 55.4% | 92.3% | 95.4% | 0.700 | 25.1% | 60.0% | 74.4% | 38.5% | 26.2% | 12.3% | 8.0% | 24.9% |
| same-language | 202 | 33.9% | 65.5% | 75.2% | 0.499 | 64.4% | 90.6% | 92.6% | 0.759 | 35.1% | 67.5% | 76.9% | 54.1% | 35.1% | 14.0% | 8.0% | 35.4% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5359, m014 0.5081, m015 0.4582)
retrieval: embedding


## 2026-10-13T12:54:12+00:00 — benchmark sweep33_methods_uwazi: merge-crumb-1200-bge-m3-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-crumb__bge-m3-4d284af0.json` — 4,488 chunks, bge-m3 (1024d), built 2026-10-13T12:54:12+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 32.5% | 62.4% | 74.1% | 0.480 | 65.9% | 91.0% | 94.0% | 0.763 | 34.0% | 64.9% | 76.3% | 47.8% | 34.5% | 13.3% | 8.0% | 33.6% |
| en | 169 | 33.1% | 63.0% | 73.1% | 0.478 | 70.4% | 90.5% | 92.9% | 0.787 | 33.9% | 65.1% | 74.9% | 48.1% | 34.3% | 13.4% | 7.8% | 34.6% |
| es | 98 | 31.5% | 61.4% | 75.9% | 0.483 | 58.2% | 91.8% | 95.9% | 0.723 | 34.0% | 64.6% | 78.9% | 47.3% | 34.7% | 13.3% | 8.3% | 31.8% |
| synthetic | 255 | 32.5% | 62.2% | 73.7% | 0.481 | 65.5% | 90.6% | 93.7% | 0.760 | 34.0% | 64.8% | 76.0% | 47.7% | 34.5% | 13.3% | 8.0% | 33.6% |
| manual | 12 | 33.3% | 66.7% | 83.3% | 0.462 | 75.0% | 100.0% | 100.0% | 0.833 | 33.3% | 66.7% | 83.3% | 50.0% | 33.3% | 13.3% | 8.3% | 33.3% |
| cross-language | 65 | 25.1% | 51.8% | 73.8% | 0.412 | 55.4% | 93.8% | 95.4% | 0.698 | 26.7% | 55.4% | 76.2% | 39.0% | 27.7% | 11.4% | 8.3% | 26.4% |
| same-language | 202 | 34.9% | 65.8% | 74.2% | 0.502 | 69.3% | 90.1% | 93.6% | 0.784 | 36.3% | 68.0% | 76.4% | 50.7% | 36.6% | 14.0% | 7.9% | 35.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5409, m014 0.5209, m015 0.4629)
retrieval: embedding


## 2026-10-13T12:54:56+00:00 — benchmark sweep33_methods_uwazi: merge-sent-crumb-1200-bge-m3-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-sentences-crumb__bge-m3-4d284af0.json` — 4,514 chunks, bge-m3 (1024d), built 2026-10-13T12:54:56+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.6% | 63.3% | 73.9% | 0.473 | 64.8% | 91.0% | 92.9% | 0.757 | 32.8% | 66.0% | 75.9% | 47.1% | 33.3% | 13.6% | 7.9% | 32.6% |
| en | 169 | 32.8% | 63.6% | 73.4% | 0.473 | 69.2% | 90.5% | 92.3% | 0.780 | 33.3% | 65.7% | 74.8% | 48.1% | 33.7% | 13.5% | 7.8% | 34.3% |
| es | 98 | 29.4% | 62.8% | 74.8% | 0.472 | 57.1% | 91.8% | 93.9% | 0.715 | 32.0% | 66.7% | 77.9% | 45.2% | 32.7% | 13.7% | 8.2% | 29.8% |
| synthetic | 255 | 31.5% | 63.1% | 73.9% | 0.473 | 64.3% | 90.6% | 92.5% | 0.753 | 32.8% | 66.0% | 75.9% | 46.9% | 33.3% | 13.6% | 8.0% | 32.6% |
| manual | 12 | 33.3% | 66.7% | 75.0% | 0.460 | 75.0% | 100.0% | 100.0% | 0.829 | 33.3% | 66.7% | 75.0% | 50.0% | 33.3% | 13.3% | 7.5% | 33.3% |
| cross-language | 65 | 23.6% | 53.3% | 73.8% | 0.407 | 53.8% | 93.8% | 95.4% | 0.691 | 25.1% | 56.9% | 75.9% | 37.4% | 26.2% | 11.7% | 8.2% | 24.9% |
| same-language | 202 | 34.2% | 66.5% | 73.9% | 0.494 | 68.3% | 90.1% | 92.1% | 0.778 | 35.3% | 69.0% | 75.9% | 50.2% | 35.6% | 14.2% | 7.9% | 35.1% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5409, m014 0.5209, m015 0.4629)
retrieval: embedding


## 2026-10-13T12:55:40+00:00 — benchmark sweep33_methods_uwazi: merge-1200-embeddinggemma-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__embeddinggemma-4d284af0.json` — 4,488 chunks, embeddinggemma (768d), built 2026-10-13T12:55:41+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 37.2% | 65.2% | 79.5% | 0.528 | 67.8% | 92.9% | 97.8% | 0.787 | 38.8% | 67.4% | 81.6% | 54.3% | 39.3% | 13.9% | 8.5% | 37.7% |
| en | 169 | 38.5% | 66.3% | 79.6% | 0.535 | 70.4% | 91.1% | 97.0% | 0.796 | 39.4% | 67.8% | 81.4% | 54.2% | 40.2% | 14.1% | 8.5% | 38.8% |
| es | 98 | 35.0% | 63.4% | 79.3% | 0.516 | 63.3% | 95.9% | 99.0% | 0.773 | 37.8% | 66.7% | 82.0% | 54.4% | 37.8% | 13.7% | 8.6% | 35.9% |
| synthetic | 255 | 37.8% | 65.6% | 78.9% | 0.533 | 67.1% | 92.5% | 97.6% | 0.781 | 39.5% | 67.8% | 81.1% | 54.5% | 40.0% | 14.0% | 8.5% | 38.3% |
| manual | 12 | 25.0% | 58.3% | 91.7% | 0.423 | 83.3% | 100.0% | 100.0% | 0.917 | 25.0% | 58.3% | 91.7% | 50.0% | 25.0% | 11.7% | 9.2% | 25.0% |
| cross-language | 65 | 35.1% | 59.7% | 77.4% | 0.501 | 56.9% | 89.2% | 98.5% | 0.707 | 36.4% | 62.3% | 79.2% | 45.6% | 38.5% | 13.2% | 8.5% | 35.1% |
| same-language | 202 | 37.9% | 67.0% | 80.1% | 0.537 | 71.3% | 94.1% | 97.5% | 0.813 | 39.6% | 69.0% | 82.3% | 57.1% | 39.6% | 14.2% | 8.5% | 38.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4994, m014 0.4174, m015 0.3793)
retrieval: embedding


## 2026-10-13T12:56:17+00:00 — benchmark sweep33_methods_uwazi: merge-sent-1200-embeddinggemma-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-sentences__embeddinggemma-4d284af0.json` — 4,514 chunks, embeddinggemma (768d), built 2026-10-13T12:56:17+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 37.0% | 64.9% | 79.7% | 0.526 | 68.5% | 92.9% | 97.0% | 0.792 | 38.7% | 67.2% | 81.4% | 54.3% | 39.0% | 13.9% | 8.5% | 37.7% |
| en | 169 | 38.2% | 66.3% | 79.6% | 0.531 | 71.6% | 91.1% | 95.9% | 0.803 | 39.3% | 68.0% | 81.1% | 53.6% | 39.6% | 14.1% | 8.5% | 38.8% |
| es | 98 | 35.0% | 62.4% | 79.8% | 0.517 | 63.3% | 95.9% | 99.0% | 0.775 | 37.8% | 65.6% | 82.0% | 55.4% | 37.8% | 13.5% | 8.7% | 35.9% |
| synthetic | 255 | 37.6% | 65.2% | 79.1% | 0.530 | 67.5% | 92.5% | 96.9% | 0.785 | 39.3% | 67.6% | 80.9% | 54.5% | 39.6% | 14.0% | 8.5% | 38.3% |
| manual | 12 | 25.0% | 58.3% | 91.7% | 0.438 | 91.7% | 100.0% | 100.0% | 0.958 | 25.0% | 58.3% | 91.7% | 50.0% | 25.0% | 11.7% | 9.2% | 25.0% |
| cross-language | 65 | 34.4% | 59.0% | 78.2% | 0.496 | 56.9% | 89.2% | 96.9% | 0.709 | 35.9% | 61.5% | 80.0% | 47.2% | 36.9% | 12.9% | 8.5% | 35.1% |
| same-language | 202 | 37.9% | 66.7% | 80.1% | 0.536 | 72.3% | 94.1% | 97.0% | 0.819 | 39.6% | 69.0% | 81.8% | 56.6% | 39.6% | 14.2% | 8.6% | 38.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4994, m014 0.4174, m015 0.3910)
retrieval: embedding


## 2026-10-13T12:56:53+00:00 — benchmark sweep33_methods_uwazi: merge-crumb-1200-embeddinggemma-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-crumb__embeddinggemma-4d284af0.json` — 4,488 chunks, embeddinggemma (768d), built 2026-10-13T12:56:53+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 32.0% | 64.3% | 78.5% | 0.493 | 64.0% | 94.0% | 97.8% | 0.765 | 33.6% | 66.4% | 80.7% | 50.4% | 34.1% | 13.7% | 8.4% | 32.3% |
| en | 169 | 33.1% | 63.6% | 76.9% | 0.497 | 64.5% | 92.3% | 97.0% | 0.761 | 34.1% | 65.0% | 78.4% | 51.3% | 34.9% | 13.5% | 8.2% | 33.4% |
| es | 98 | 29.9% | 65.5% | 81.3% | 0.485 | 63.3% | 96.9% | 99.0% | 0.771 | 32.7% | 68.7% | 84.7% | 49.0% | 32.7% | 14.1% | 8.7% | 30.3% |
| synthetic | 255 | 32.3% | 64.2% | 78.3% | 0.497 | 63.1% | 93.7% | 97.6% | 0.758 | 34.0% | 66.3% | 80.6% | 50.8% | 34.5% | 13.7% | 8.4% | 32.6% |
| manual | 12 | 25.0% | 66.7% | 83.3% | 0.399 | 83.3% | 100.0% | 100.0% | 0.917 | 25.0% | 66.7% | 83.3% | 41.7% | 25.0% | 13.3% | 8.3% | 25.0% |
| cross-language | 65 | 29.0% | 55.1% | 77.4% | 0.446 | 53.8% | 92.3% | 98.5% | 0.696 | 30.3% | 56.7% | 79.2% | 39.5% | 32.3% | 12.0% | 8.5% | 29.0% |
| same-language | 202 | 32.9% | 67.2% | 78.9% | 0.508 | 67.3% | 94.6% | 97.5% | 0.787 | 34.7% | 69.5% | 81.2% | 54.0% | 34.7% | 14.3% | 8.4% | 33.3% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4971, m014 0.4144, m015 0.3932)
retrieval: embedding


## 2026-10-13T12:57:30+00:00 — benchmark sweep33_methods_uwazi: merge-sent-crumb-1200-embeddinggemma-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-sentences-crumb__embeddinggemma-4d284af0.json` — 4,514 chunks, embeddinggemma (768d), built 2026-10-13T12:57:30+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.8% | 64.1% | 77.8% | 0.492 | 64.8% | 93.6% | 97.0% | 0.770 | 33.5% | 66.4% | 79.8% | 51.2% | 33.7% | 13.6% | 8.3% | 32.5% |
| en | 169 | 32.2% | 63.3% | 75.7% | 0.492 | 65.7% | 92.3% | 96.4% | 0.770 | 33.3% | 65.1% | 76.9% | 52.5% | 33.7% | 13.4% | 8.0% | 33.1% |
| es | 98 | 31.0% | 65.5% | 81.3% | 0.491 | 63.3% | 95.9% | 98.0% | 0.771 | 33.7% | 68.7% | 84.7% | 49.0% | 33.7% | 14.1% | 8.7% | 31.3% |
| synthetic | 255 | 32.1% | 64.0% | 77.5% | 0.496 | 63.5% | 93.3% | 96.9% | 0.762 | 33.9% | 66.4% | 79.6% | 51.6% | 34.1% | 13.6% | 8.3% | 32.8% |
| manual | 12 | 25.0% | 66.7% | 83.3% | 0.413 | 91.7% | 100.0% | 100.0% | 0.958 | 25.0% | 66.7% | 83.3% | 41.7% | 25.0% | 13.3% | 8.3% | 25.0% |
| cross-language | 65 | 28.2% | 56.7% | 76.7% | 0.441 | 53.8% | 90.8% | 95.4% | 0.698 | 29.7% | 58.5% | 78.5% | 41.0% | 30.8% | 12.3% | 8.3% | 29.0% |
| same-language | 202 | 32.9% | 66.5% | 78.1% | 0.508 | 68.3% | 94.6% | 97.5% | 0.794 | 34.7% | 69.0% | 80.2% | 54.5% | 34.7% | 14.1% | 8.3% | 33.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4971, m014 0.4144, m015 0.3968)
retrieval: embedding


## 2026-10-13T12:58:06+00:00 — benchmark sweep33_methods_uwazi: merge-1200-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__snowflake-arctic-embed2-4d284af0.json` — 4,488 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-13T12:58:08+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 37.3% | 63.8% | 75.0% | 0.515 | 64.8% | 89.9% | 94.8% | 0.754 | 38.8% | 66.0% | 77.1% | 50.7% | 39.3% | 13.7% | 8.1% | 38.6% |
| en | 169 | 37.3% | 63.6% | 76.9% | 0.509 | 67.5% | 89.3% | 94.1% | 0.765 | 38.1% | 65.1% | 78.4% | 49.7% | 38.5% | 13.5% | 8.2% | 38.8% |
| es | 98 | 37.4% | 64.1% | 71.8% | 0.525 | 60.2% | 90.8% | 95.9% | 0.736 | 40.1% | 67.7% | 74.8% | 52.4% | 40.8% | 14.1% | 7.9% | 38.3% |
| synthetic | 255 | 37.5% | 64.1% | 74.6% | 0.517 | 63.9% | 89.4% | 94.5% | 0.747 | 39.1% | 66.4% | 76.8% | 50.7% | 39.6% | 13.8% | 8.1% | 38.8% |
| manual | 12 | 33.3% | 58.3% | 83.3% | 0.476 | 83.3% | 100.0% | 100.0% | 0.903 | 33.3% | 58.3% | 83.3% | 50.0% | 33.3% | 11.7% | 8.3% | 33.3% |
| cross-language | 65 | 30.3% | 60.8% | 73.1% | 0.468 | 53.8% | 89.2% | 93.8% | 0.681 | 32.8% | 63.1% | 76.2% | 41.5% | 33.8% | 13.5% | 8.2% | 31.5% |
| same-language | 202 | 39.6% | 64.8% | 75.7% | 0.530 | 68.3% | 90.1% | 95.0% | 0.778 | 40.8% | 67.0% | 77.4% | 53.6% | 41.1% | 13.8% | 8.1% | 40.8% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4227, m014 0.4076, m015 0.3614)
retrieval: embedding


## 2026-10-13T12:58:50+00:00 — benchmark sweep33_methods_uwazi: merge-sent-1200-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-sentences__snowflake-arctic-embed2-4d284af0.json` — 4,514 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-13T12:58:50+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 37.7% | 64.0% | 75.2% | 0.517 | 64.8% | 89.9% | 95.1% | 0.756 | 39.2% | 65.8% | 77.3% | 50.8% | 39.7% | 13.7% | 8.1% | 38.6% |
| en | 169 | 37.9% | 64.8% | 77.2% | 0.513 | 68.0% | 89.9% | 94.7% | 0.773 | 38.7% | 65.9% | 78.7% | 49.9% | 39.1% | 13.7% | 8.2% | 38.8% |
| es | 98 | 37.4% | 62.6% | 71.8% | 0.524 | 59.2% | 89.8% | 95.9% | 0.727 | 40.1% | 65.6% | 74.8% | 52.4% | 40.8% | 13.7% | 7.9% | 38.3% |
| synthetic | 255 | 37.9% | 64.2% | 74.8% | 0.519 | 63.9% | 89.4% | 94.9% | 0.748 | 39.5% | 66.1% | 77.0% | 50.8% | 40.0% | 13.8% | 8.1% | 38.8% |
| manual | 12 | 33.3% | 58.3% | 83.3% | 0.476 | 83.3% | 100.0% | 100.0% | 0.917 | 33.3% | 58.3% | 83.3% | 50.0% | 33.3% | 11.7% | 8.3% | 33.3% |
| cross-language | 65 | 31.8% | 61.5% | 73.8% | 0.476 | 55.4% | 90.8% | 93.8% | 0.693 | 34.4% | 63.6% | 76.9% | 42.1% | 35.4% | 13.5% | 8.2% | 32.3% |
| same-language | 202 | 39.6% | 64.8% | 75.7% | 0.530 | 67.8% | 89.6% | 95.5% | 0.776 | 40.8% | 66.5% | 77.4% | 53.6% | 41.1% | 13.8% | 8.1% | 40.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4227, m014 0.4076, m015 0.3614)
retrieval: embedding


## 2026-10-13T12:59:28+00:00 — benchmark sweep33_methods_uwazi: merge-crumb-1200-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-crumb__snowflake-arctic-embed2-4d284af0.json` — 4,488 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-13T12:59:28+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 33.4% | 62.7% | 73.9% | 0.483 | 63.3% | 91.4% | 95.1% | 0.745 | 34.7% | 64.7% | 75.8% | 47.7% | 35.2% | 13.4% | 7.9% | 34.6% |
| en | 169 | 34.9% | 63.3% | 76.0% | 0.493 | 67.5% | 91.1% | 94.1% | 0.767 | 35.7% | 64.8% | 77.5% | 49.7% | 36.1% | 13.5% | 8.2% | 36.7% |
| es | 98 | 30.8% | 61.6% | 70.2% | 0.465 | 56.1% | 91.8% | 96.9% | 0.709 | 33.0% | 64.6% | 72.8% | 44.2% | 33.7% | 13.3% | 7.6% | 31.1% |
| synthetic | 255 | 33.4% | 62.5% | 73.5% | 0.484 | 62.4% | 91.0% | 94.9% | 0.738 | 34.8% | 64.6% | 75.4% | 47.6% | 35.3% | 13.4% | 7.9% | 34.7% |
| manual | 12 | 33.3% | 66.7% | 83.3% | 0.466 | 83.3% | 100.0% | 100.0% | 0.903 | 33.3% | 66.7% | 83.3% | 50.0% | 33.3% | 13.3% | 8.3% | 33.3% |
| cross-language | 65 | 30.3% | 61.5% | 76.9% | 0.468 | 56.9% | 92.3% | 95.4% | 0.712 | 32.8% | 63.8% | 80.0% | 41.5% | 33.8% | 13.8% | 8.6% | 31.5% |
| same-language | 202 | 34.4% | 63.0% | 72.9% | 0.488 | 65.3% | 91.1% | 95.0% | 0.756 | 35.3% | 65.0% | 74.4% | 49.7% | 35.6% | 13.3% | 7.7% | 35.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4109, m014 0.4018, m015 0.3773)
retrieval: embedding


## 2026-10-13T13:00:07+00:00 — benchmark sweep33_methods_uwazi: merge-sent-crumb-1200-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-sentences-crumb__snowflake-arctic-embed2-4d284af0.json` — 4,514 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-13T13:00:07+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 33.6% | 62.7% | 74.3% | 0.482 | 63.7% | 90.6% | 94.8% | 0.748 | 34.7% | 64.3% | 76.2% | 47.8% | 35.2% | 13.3% | 7.9% | 34.8% |
| en | 169 | 35.2% | 64.2% | 76.0% | 0.494 | 68.0% | 91.1% | 94.1% | 0.773 | 35.7% | 65.3% | 77.5% | 49.9% | 36.1% | 13.6% | 8.1% | 37.0% |
| es | 98 | 30.8% | 60.0% | 71.3% | 0.462 | 56.1% | 89.8% | 95.9% | 0.704 | 33.0% | 62.6% | 73.8% | 44.2% | 33.7% | 12.9% | 7.7% | 31.1% |
| synthetic | 255 | 33.6% | 62.5% | 73.9% | 0.483 | 62.7% | 90.2% | 94.5% | 0.740 | 34.8% | 64.2% | 75.8% | 47.7% | 35.3% | 13.3% | 7.9% | 34.9% |
| manual | 12 | 33.3% | 66.7% | 83.3% | 0.470 | 83.3% | 100.0% | 100.0% | 0.917 | 33.3% | 66.7% | 83.3% | 50.0% | 33.3% | 13.3% | 8.3% | 33.3% |
| cross-language | 65 | 31.8% | 61.5% | 76.9% | 0.476 | 58.5% | 92.3% | 95.4% | 0.724 | 34.4% | 63.6% | 80.0% | 42.1% | 35.4% | 13.5% | 8.5% | 32.3% |
| same-language | 202 | 34.2% | 63.0% | 73.4% | 0.484 | 65.3% | 90.1% | 94.6% | 0.755 | 34.8% | 64.5% | 74.9% | 49.7% | 35.1% | 13.3% | 7.8% | 35.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4109, m014 0.4018, m015 0.3773)
retrieval: embedding


## 2026-10-13T13:00:46+00:00 — benchmark sweep33_methods_uwazi — comparison (12 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| merge-1200-bge-m3-embedding | bge-m3 | 1200/0.15/on | embedding | 267 | 31.4% | 62.8% | 73.5% | 0.479 | 62.9% | 91.8% | 93.6% | 0.751 | 32.7% | 64.9% | 75.7% | 49.3% | 33.0% | 13.4% | 7.9% | 32.8% | 0/3 | 35s / 2.9s |
| merge-sent-1200-bge-m3-embedding | bge-m3 | 1200/0.15/on | embedding | 267 | 31.4% | 63.3% | 74.5% | 0.479 | 62.2% | 91.0% | 93.3% | 0.745 | 32.7% | 65.7% | 76.3% | 50.3% | 33.0% | 13.6% | 8.0% | 32.8% | 0/3 | 35s / 3.7s |
| merge-crumb-1200-bge-m3-embedding | bge-m3 | 1200/0.15/on | embedding | 267 | 32.5% | 62.4% | 74.1% | 0.480 | 65.9% | 91.0% | 94.0% | 0.763 | 34.0% | 64.9% | 76.3% | 47.8% | 34.5% | 13.3% | 8.0% | 33.6% | 0/3 | 40s / 3.9s |
| merge-sent-crumb-1200-bge-m3-embedding | bge-m3 | 1200/0.15/on | embedding | 267 | 31.6% | 63.3% | 73.9% | 0.473 | 64.8% | 91.0% | 92.9% | 0.757 | 32.8% | 66.0% | 75.9% | 47.1% | 33.3% | 13.6% | 7.9% | 32.6% | 0/3 | 39s / 4.1s |
| merge-1200-embeddinggemma-embedding | embeddinggemma | 1200/0.15/on | embedding | 267 | 37.2% | 65.2% | 79.5% | 0.528 | 67.8% | 92.9% | 97.8% | 0.787 | 38.8% | 67.4% | 81.6% | 54.3% | 39.3% | 13.9% | 8.5% | 37.7% | 0/3 | 33s / 2.7s |
| merge-sent-1200-embeddinggemma-embedding | embeddinggemma | 1200/0.15/on | embedding | 267 | 37.0% | 64.9% | 79.7% | 0.526 | 68.5% | 92.9% | 97.0% | 0.792 | 38.7% | 67.2% | 81.4% | 54.3% | 39.0% | 13.9% | 8.5% | 37.7% | 0/3 | 32s / 2.7s |
| merge-crumb-1200-embeddinggemma-embedding | embeddinggemma | 1200/0.15/on | embedding | 267 | 32.0% | 64.3% | 78.5% | 0.493 | 64.0% | 94.0% | 97.8% | 0.765 | 33.6% | 66.4% | 80.7% | 50.4% | 34.1% | 13.7% | 8.4% | 32.3% | 0/3 | 33s / 2.7s |
| merge-sent-crumb-1200-embeddinggemma-embedding | embeddinggemma | 1200/0.15/on | embedding | 267 | 31.8% | 64.1% | 77.8% | 0.492 | 64.8% | 93.6% | 97.0% | 0.770 | 33.5% | 66.4% | 79.8% | 51.2% | 33.7% | 13.6% | 8.3% | 32.5% | 0/3 | 33s / 2.8s |
| merge-1200-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1200/0.15/on | embedding | 267 | 37.3% | 63.8% | 75.0% | 0.515 | 64.8% | 89.9% | 94.8% | 0.754 | 38.8% | 66.0% | 77.1% | 50.7% | 39.3% | 13.7% | 8.1% | 38.6% | 0/3 | 38s / 3.7s |
| merge-sent-1200-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1200/0.15/on | embedding | 267 | 37.7% | 64.0% | 75.2% | 0.517 | 64.8% | 89.9% | 95.1% | 0.756 | 39.2% | 65.8% | 77.3% | 50.8% | 39.7% | 13.7% | 8.1% | 38.6% | 0/3 | 34s / 3.1s |
| merge-crumb-1200-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1200/0.15/on | embedding | 267 | 33.4% | 62.7% | 73.9% | 0.483 | 63.3% | 91.4% | 95.1% | 0.745 | 34.7% | 64.7% | 75.8% | 47.7% | 35.2% | 13.4% | 7.9% | 34.6% | 0/3 | 35s / 3.3s |
| merge-sent-crumb-1200-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1200/0.15/on | embedding | 267 | 33.6% | 62.7% | 74.3% | 0.482 | 63.7% | 90.6% | 94.8% | 0.748 | 34.7% | 64.3% | 76.2% | 47.8% | 35.2% | 13.3% | 7.9% | 34.8% | 0/3 | 35s / 3.2s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes


## 2026-10-13T13:19:23+00:00 — benchmark sweep33_methods_contractnli — resolved plan

plan    : sweep33_methods_contractnli — 12 experiment(s) over 12 store cell(s)
dataset : legalbenchrag-contractnli
captures: data/raw/d7f14657e7264534 — 95 capture(s)
golden  : data/eval/datasets/legalbenchrag-contractnli/golden.jsonl — 982 row(s)
stores  :
  merge-1200-bge-m3      merge 1200/0.15/on     × bge-m3                       → data/benchmark_stores/merge-1200-0.15-on__bge-m3-826d4d38.json
  merge-sent-1200-bge-m3 merge 1200/0.15/on +sentences × bge-m3                       → data/benchmark_stores/merge-1200-0.15-on-sentences__bge-m3-826d4d38.json
  merge-crumb-1200-bge-m3 merge 1200/0.15/on +breadcrumb × bge-m3                       → data/benchmark_stores/merge-1200-0.15-on-crumb__bge-m3-826d4d38.json
  merge-sent-crumb-1200-bge-m3 merge 1200/0.15/on +sentences +breadcrumb × bge-m3                       → data/benchmark_stores/merge-1200-0.15-on-sentences-crumb__bge-m3-826d4d38.json
  merge-1200-embeddinggemma merge 1200/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-1200-0.15-on__embeddinggemma-826d4d38.json
  merge-sent-1200-embeddinggemma merge 1200/0.15/on +sentences × embeddinggemma               → data/benchmark_stores/merge-1200-0.15-on-sentences__embeddinggemma-826d4d38.json
  merge-crumb-1200-embeddinggemma merge 1200/0.15/on +breadcrumb × embeddinggemma               → data/benchmark_stores/merge-1200-0.15-on-crumb__embeddinggemma-826d4d38.json
  merge-sent-crumb-1200-embeddinggemma merge 1200/0.15/on +sentences +breadcrumb × embeddinggemma               → data/benchmark_stores/merge-1200-0.15-on-sentences-crumb__embeddinggemma-826d4d38.json
  merge-1200-snowflake-arctic-embed2 merge 1200/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-1200-0.15-on__snowflake-arctic-embed2-826d4d38.json
  merge-sent-1200-snowflake-arctic-embed2 merge 1200/0.15/on +sentences × snowflake-arctic-embed2      → data/benchmark_stores/merge-1200-0.15-on-sentences__snowflake-arctic-embed2-826d4d38.json
  merge-crumb-1200-snowflake-arctic-embed2 merge 1200/0.15/on +breadcrumb × snowflake-arctic-embed2      → data/benchmark_stores/merge-1200-0.15-on-crumb__snowflake-arctic-embed2-826d4d38.json
  merge-sent-crumb-1200-snowflake-arctic-embed2 merge 1200/0.15/on +sentences +breadcrumb × snowflake-arctic-embed2      → data/benchmark_stores/merge-1200-0.15-on-sentences-crumb__snowflake-arctic-embed2-826d4d38.json
experiments:
  1. merge-1200-bge-m3-embedding  → merge-1200-bge-m3      retrieval embedding
  2. merge-sent-1200-bge-m3-embedding → merge-sent-1200-bge-m3 retrieval embedding
  3. merge-crumb-1200-bge-m3-embedding → merge-crumb-1200-bge-m3 retrieval embedding
  4. merge-sent-crumb-1200-bge-m3-embedding → merge-sent-crumb-1200-bge-m3 retrieval embedding
  5. merge-1200-embeddinggemma-embedding → merge-1200-embeddinggemma retrieval embedding
  6. merge-sent-1200-embeddinggemma-embedding → merge-sent-1200-embeddinggemma retrieval embedding
  7. merge-crumb-1200-embeddinggemma-embedding → merge-crumb-1200-embeddinggemma retrieval embedding
  8. merge-sent-crumb-1200-embeddinggemma-embedding → merge-sent-crumb-1200-embeddinggemma retrieval embedding
  9. merge-1200-snowflake-arctic-embed2-embedding → merge-1200-snowflake-arctic-embed2 retrieval embedding
  10. merge-sent-1200-snowflake-arctic-embed2-embedding → merge-sent-1200-snowflake-arctic-embed2 retrieval embedding
  11. merge-crumb-1200-snowflake-arctic-embed2-embedding → merge-crumb-1200-snowflake-arctic-embed2 retrieval embedding
  12. merge-sent-crumb-1200-snowflake-arctic-embed2-embedding → merge-sent-crumb-1200-snowflake-arctic-embed2 retrieval embedding


## 2026-10-13T13:19:23+00:00 — benchmark sweep33_methods_contractnli: merge-1200-bge-m3-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__bge-m3-826d4d38.json` — 1,091 chunks, bge-m3 (1024d), built 2026-10-13T13:19:24+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 34.4% | 71.7% | 82.2% | 0.601 | 84.7% | 94.9% | 97.4% | 0.891 | 38.6% | 75.7% | 84.7% | 57.8% | 44.8% | 19.8% | 11.6% | 40.5% |
| en | 977 | 34.4% | 71.7% | 82.2% | 0.601 | 84.7% | 94.9% | 97.4% | 0.891 | 38.6% | 75.7% | 84.7% | 57.8% | 44.8% | 19.8% | 11.6% | 40.5% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 34.4% | 71.7% | 82.2% | 0.601 | 84.7% | 94.9% | 97.4% | 0.891 | 38.6% | 75.7% | 84.7% | 57.8% | 44.8% | 19.8% | 11.6% | 40.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 3/5 (60.0%) (top-1: m001 0.5987, m002 0.5915, m003 0.5079, m004 0.5906, m005 0.5354)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-13T13:19:41+00:00 — benchmark sweep33_methods_contractnli: merge-sent-1200-bge-m3-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-sentences__bge-m3-826d4d38.json` — 1,095 chunks, bge-m3 (1024d), built 2026-10-13T13:19:41+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 34.4% | 71.6% | 82.1% | 0.599 | 84.4% | 95.1% | 97.4% | 0.892 | 38.3% | 75.3% | 84.6% | 58.2% | 44.5% | 19.8% | 11.6% | 40.9% |
| en | 977 | 34.4% | 71.6% | 82.1% | 0.599 | 84.4% | 95.1% | 97.4% | 0.892 | 38.3% | 75.3% | 84.6% | 58.2% | 44.5% | 19.8% | 11.6% | 40.9% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 34.4% | 71.6% | 82.1% | 0.599 | 84.4% | 95.1% | 97.4% | 0.892 | 38.3% | 75.3% | 84.6% | 58.2% | 44.5% | 19.8% | 11.6% | 40.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 3/5 (60.0%) (top-1: m001 0.5987, m002 0.5915, m003 0.5079, m004 0.5906, m005 0.5354)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-13T13:19:58+00:00 — benchmark sweep33_methods_contractnli: merge-crumb-1200-bge-m3-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-crumb__bge-m3-826d4d38.json` — 1,091 chunks, bge-m3 (1024d), built 2026-10-13T13:19:58+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 33.2% | 71.9% | 81.9% | 0.585 | 87.6% | 96.0% | 97.7% | 0.915 | 37.5% | 73.4% | 82.7% | 49.1% | 43.7% | 20.0% | 11.6% | 40.8% |
| en | 977 | 33.2% | 71.9% | 81.9% | 0.585 | 87.6% | 96.0% | 97.7% | 0.915 | 37.5% | 73.4% | 82.7% | 49.1% | 43.7% | 20.0% | 11.6% | 40.8% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 33.2% | 71.9% | 81.9% | 0.585 | 87.6% | 96.0% | 97.7% | 0.915 | 37.5% | 73.4% | 82.7% | 49.1% | 43.7% | 20.0% | 11.6% | 40.8% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 3/5 (60.0%) (top-1: m001 0.5952, m002 0.5904, m003 0.5044, m004 0.5884, m005 0.5469)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-13T13:20:17+00:00 — benchmark sweep33_methods_contractnli: merge-sent-crumb-1200-bge-m3-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-sentences-crumb__bge-m3-826d4d38.json` — 1,095 chunks, bge-m3 (1024d), built 2026-10-13T13:20:17+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 32.9% | 71.6% | 81.7% | 0.583 | 87.6% | 95.8% | 97.7% | 0.916 | 37.2% | 73.2% | 82.6% | 49.1% | 43.2% | 19.9% | 11.6% | 40.6% |
| en | 977 | 32.9% | 71.6% | 81.7% | 0.583 | 87.6% | 95.8% | 97.7% | 0.916 | 37.2% | 73.2% | 82.6% | 49.1% | 43.2% | 19.9% | 11.6% | 40.6% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 32.9% | 71.6% | 81.7% | 0.583 | 87.6% | 95.8% | 97.7% | 0.916 | 37.2% | 73.2% | 82.6% | 49.1% | 43.2% | 19.9% | 11.6% | 40.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 3/5 (60.0%) (top-1: m001 0.5952, m002 0.5874, m003 0.5039, m004 0.5874, m005 0.5469)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-13T13:20:36+00:00 — benchmark sweep33_methods_contractnli: merge-1200-embeddinggemma-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__embeddinggemma-826d4d38.json` — 1,091 chunks, embeddinggemma (768d), built 2026-10-13T13:20:37+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 39.4% | 76.1% | 86.9% | 0.651 | 91.2% | 97.6% | 99.1% | 0.938 | 44.4% | 79.3% | 89.0% | 61.7% | 51.1% | 21.0% | 12.3% | 45.6% |
| en | 977 | 39.4% | 76.1% | 86.9% | 0.651 | 91.2% | 97.6% | 99.1% | 0.938 | 44.4% | 79.3% | 89.0% | 61.7% | 51.1% | 21.0% | 12.3% | 45.6% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 39.4% | 76.1% | 86.9% | 0.651 | 91.2% | 97.6% | 99.1% | 0.938 | 44.4% | 79.3% | 89.0% | 61.7% | 51.1% | 21.0% | 12.3% | 45.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 2/5 (40.0%) (top-1: m001 0.6348, m002 0.5382, m003 0.4253, m004 0.5654, m005 0.4834)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-13T13:20:51+00:00 — benchmark sweep33_methods_contractnli: merge-sent-1200-embeddinggemma-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-sentences__embeddinggemma-826d4d38.json` — 1,095 chunks, embeddinggemma (768d), built 2026-10-13T13:20:51+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 38.9% | 75.5% | 86.7% | 0.645 | 91.2% | 97.0% | 99.1% | 0.938 | 43.7% | 78.6% | 88.7% | 61.6% | 50.1% | 20.8% | 12.2% | 45.3% |
| en | 977 | 38.9% | 75.5% | 86.7% | 0.645 | 91.2% | 97.0% | 99.1% | 0.938 | 43.7% | 78.6% | 88.7% | 61.6% | 50.1% | 20.8% | 12.2% | 45.3% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 38.9% | 75.5% | 86.7% | 0.645 | 91.2% | 97.0% | 99.1% | 0.938 | 43.7% | 78.6% | 88.7% | 61.6% | 50.1% | 20.8% | 12.2% | 45.3% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 2/5 (40.0%) (top-1: m001 0.6348, m002 0.5344, m003 0.4253, m004 0.5654, m005 0.4834)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-13T13:21:05+00:00 — benchmark sweep33_methods_contractnli: merge-crumb-1200-embeddinggemma-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-crumb__embeddinggemma-826d4d38.json` — 1,091 chunks, embeddinggemma (768d), built 2026-10-13T13:21:05+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 37.2% | 77.9% | 87.6% | 0.630 | 92.9% | 98.3% | 99.2% | 0.953 | 40.9% | 79.6% | 88.6% | 52.4% | 47.5% | 21.4% | 12.4% | 44.7% |
| en | 977 | 37.2% | 77.9% | 87.6% | 0.630 | 92.9% | 98.3% | 99.2% | 0.953 | 40.9% | 79.6% | 88.6% | 52.4% | 47.5% | 21.4% | 12.4% | 44.7% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 37.2% | 77.9% | 87.6% | 0.630 | 92.9% | 98.3% | 99.2% | 0.953 | 40.9% | 79.6% | 88.6% | 52.4% | 47.5% | 21.4% | 12.4% | 44.7% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 1/5 (20.0%) (top-1: m001 0.6237, m002 0.5274, m003 0.4111, m004 0.5400, m005 0.4624)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-13T13:21:19+00:00 — benchmark sweep33_methods_contractnli: merge-sent-crumb-1200-embeddinggemma-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-sentences-crumb__embeddinggemma-826d4d38.json` — 1,095 chunks, embeddinggemma (768d), built 2026-10-13T13:21:19+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 37.5% | 78.3% | 87.6% | 0.633 | 93.3% | 98.4% | 99.2% | 0.955 | 41.4% | 79.9% | 88.6% | 52.8% | 48.0% | 21.6% | 12.4% | 44.9% |
| en | 977 | 37.5% | 78.3% | 87.6% | 0.633 | 93.3% | 98.4% | 99.2% | 0.955 | 41.4% | 79.9% | 88.6% | 52.8% | 48.0% | 21.6% | 12.4% | 44.9% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 37.5% | 78.3% | 87.6% | 0.633 | 93.3% | 98.4% | 99.2% | 0.955 | 41.4% | 79.9% | 88.6% | 52.8% | 48.0% | 21.6% | 12.4% | 44.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 1/5 (20.0%) (top-1: m001 0.6237, m002 0.5273, m003 0.4111, m004 0.5400, m005 0.4612)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-13T13:21:33+00:00 — benchmark sweep33_methods_contractnli: merge-1200-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__snowflake-arctic-embed2-826d4d38.json` — 1,091 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-13T13:21:35+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 30.7% | 66.5% | 76.8% | 0.563 | 82.0% | 95.0% | 97.2% | 0.877 | 35.0% | 70.3% | 79.1% | 53.9% | 40.4% | 18.5% | 11.0% | 37.5% |
| en | 977 | 30.7% | 66.5% | 76.8% | 0.563 | 82.0% | 95.0% | 97.2% | 0.877 | 35.0% | 70.3% | 79.1% | 53.9% | 40.4% | 18.5% | 11.0% | 37.5% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 30.7% | 66.5% | 76.8% | 0.563 | 82.0% | 95.0% | 97.2% | 0.877 | 35.0% | 70.3% | 79.1% | 53.9% | 40.4% | 18.5% | 11.0% | 37.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.5421, m002 0.5065, m003 0.3097, m004 0.4755, m005 0.4074)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-13T13:21:49+00:00 — benchmark sweep33_methods_contractnli: merge-sent-1200-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-sentences__snowflake-arctic-embed2-826d4d38.json` — 1,095 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-13T13:21:49+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 31.2% | 66.5% | 76.6% | 0.567 | 82.2% | 94.9% | 97.2% | 0.878 | 35.6% | 70.4% | 79.1% | 54.8% | 41.2% | 18.6% | 11.0% | 37.9% |
| en | 977 | 31.2% | 66.5% | 76.6% | 0.567 | 82.2% | 94.9% | 97.2% | 0.878 | 35.6% | 70.4% | 79.1% | 54.8% | 41.2% | 18.6% | 11.0% | 37.9% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 31.2% | 66.5% | 76.6% | 0.567 | 82.2% | 94.9% | 97.2% | 0.878 | 35.6% | 70.4% | 79.1% | 54.8% | 41.2% | 18.6% | 11.0% | 37.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.5421, m002 0.5065, m003 0.3097, m004 0.4755, m005 0.4074)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-13T13:22:05+00:00 — benchmark sweep33_methods_contractnli: merge-crumb-1200-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-crumb__snowflake-arctic-embed2-826d4d38.json` — 1,091 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-13T13:22:05+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 33.9% | 69.4% | 79.6% | 0.584 | 88.9% | 96.5% | 98.4% | 0.925 | 37.8% | 71.6% | 80.9% | 47.3% | 44.2% | 19.5% | 11.3% | 39.9% |
| en | 977 | 33.9% | 69.4% | 79.6% | 0.584 | 88.9% | 96.5% | 98.4% | 0.925 | 37.8% | 71.6% | 80.9% | 47.3% | 44.2% | 19.5% | 11.3% | 39.9% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 33.9% | 69.4% | 79.6% | 0.584 | 88.9% | 96.5% | 98.4% | 0.925 | 37.8% | 71.6% | 80.9% | 47.3% | 44.2% | 19.5% | 11.3% | 39.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.5384, m002 0.5102, m003 0.3247, m004 0.4832, m005 0.4002)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-13T13:22:22+00:00 — benchmark sweep33_methods_contractnli: merge-sent-crumb-1200-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-sentences-crumb__snowflake-arctic-embed2-826d4d38.json` — 1,095 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-13T13:22:22+00:00
golden: `data/eval/datasets/legalbenchrag-contractnli/golden.jsonl` — 982 rows (0 synthetic / 5 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 977 | 33.9% | 68.9% | 79.9% | 0.582 | 88.9% | 96.5% | 98.4% | 0.924 | 37.7% | 71.3% | 81.2% | 46.9% | 44.1% | 19.3% | 11.4% | 39.7% |
| en | 977 | 33.9% | 68.9% | 79.9% | 0.582 | 88.9% | 96.5% | 98.4% | 0.924 | 37.7% | 71.3% | 81.2% | 46.9% | 44.1% | 19.3% | 11.4% | 39.7% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 977 | 33.9% | 68.9% | 79.9% | 0.582 | 88.9% | 96.5% | 98.4% | 0.924 | 37.7% | 71.3% | 81.2% | 46.9% | 44.1% | 19.3% | 11.4% | 39.7% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 5 rows, threshold ≥ 0.550 → false-retrieval 0/5 (0.0%) (top-1: m001 0.5384, m002 0.5050, m003 0.3247, m004 0.4832, m005 0.3990)
retrieval: embedding
dataset: legalbenchrag-contractnli


## 2026-10-13T13:22:37+00:00 — benchmark sweep33_methods_contractnli — dataset legalbenchrag-contractnli — comparison (12 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| merge-1200-bge-m3-embedding | bge-m3 | 1200/0.15/on | embedding | 977 | 34.4% | 71.7% | 82.2% | 0.601 | 84.7% | 94.9% | 97.4% | 0.891 | 38.6% | 75.7% | 84.7% | 57.8% | 44.8% | 19.8% | 11.6% | 40.5% | 3/5 | 9s / 7.7s |
| merge-sent-1200-bge-m3-embedding | bge-m3 | 1200/0.15/on | embedding | 977 | 34.4% | 71.6% | 82.1% | 0.599 | 84.4% | 95.1% | 97.4% | 0.892 | 38.3% | 75.3% | 84.6% | 58.2% | 44.5% | 19.8% | 11.6% | 40.9% | 3/5 | 9s / 8.1s |
| merge-crumb-1200-bge-m3-embedding | bge-m3 | 1200/0.15/on | embedding | 977 | 33.2% | 71.9% | 81.9% | 0.585 | 87.6% | 96.0% | 97.7% | 0.915 | 37.5% | 73.4% | 82.7% | 49.1% | 43.7% | 20.0% | 11.6% | 40.8% | 3/5 | 11s / 8.1s |
| merge-sent-crumb-1200-bge-m3-embedding | bge-m3 | 1200/0.15/on | embedding | 977 | 32.9% | 71.6% | 81.7% | 0.583 | 87.6% | 95.8% | 97.7% | 0.916 | 37.2% | 73.2% | 82.6% | 49.1% | 43.2% | 19.9% | 11.6% | 40.6% | 3/5 | 10s / 8.5s |
| merge-1200-embeddinggemma-embedding | embeddinggemma | 1200/0.15/on | embedding | 977 | 39.4% | 76.1% | 86.9% | 0.651 | 91.2% | 97.6% | 99.1% | 0.938 | 44.4% | 79.3% | 89.0% | 61.7% | 51.1% | 21.0% | 12.3% | 45.6% | 2/5 | 8s / 6.4s |
| merge-sent-1200-embeddinggemma-embedding | embeddinggemma | 1200/0.15/on | embedding | 977 | 38.9% | 75.5% | 86.7% | 0.645 | 91.2% | 97.0% | 99.1% | 0.938 | 43.7% | 78.6% | 88.7% | 61.6% | 50.1% | 20.8% | 12.2% | 45.3% | 2/5 | 7s / 6.4s |
| merge-crumb-1200-embeddinggemma-embedding | embeddinggemma | 1200/0.15/on | embedding | 977 | 37.2% | 77.9% | 87.6% | 0.630 | 92.9% | 98.3% | 99.2% | 0.953 | 40.9% | 79.6% | 88.6% | 52.4% | 47.5% | 21.4% | 12.4% | 44.7% | 1/5 | 7s / 7.2s |
| merge-sent-crumb-1200-embeddinggemma-embedding | embeddinggemma | 1200/0.15/on | embedding | 977 | 37.5% | 78.3% | 87.6% | 0.633 | 93.3% | 98.4% | 99.2% | 0.955 | 41.4% | 79.9% | 88.6% | 52.8% | 48.0% | 21.6% | 12.4% | 44.9% | 1/5 | 7s / 6.7s |
| merge-1200-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1200/0.15/on | embedding | 977 | 30.7% | 66.5% | 76.8% | 0.563 | 82.0% | 95.0% | 97.2% | 0.877 | 35.0% | 70.3% | 79.1% | 53.9% | 40.4% | 18.5% | 11.0% | 37.5% | 0/5 | 8s / 6.5s |
| merge-sent-1200-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1200/0.15/on | embedding | 977 | 31.2% | 66.5% | 76.6% | 0.567 | 82.2% | 94.9% | 97.2% | 0.878 | 35.6% | 70.4% | 79.1% | 54.8% | 41.2% | 18.6% | 11.0% | 37.9% | 0/5 | 8s / 7.8s |
| merge-crumb-1200-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1200/0.15/on | embedding | 977 | 33.9% | 69.4% | 79.6% | 0.584 | 88.9% | 96.5% | 98.4% | 0.925 | 37.8% | 71.6% | 80.9% | 47.3% | 44.2% | 19.5% | 11.3% | 39.9% | 0/5 | 10s / 7.0s |
| merge-sent-crumb-1200-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1200/0.15/on | embedding | 977 | 33.9% | 68.9% | 79.9% | 0.582 | 88.9% | 96.5% | 98.4% | 0.924 | 37.7% | 71.3% | 81.2% | 46.9% | 44.1% | 19.3% | 11.4% | 39.7% | 0/5 | 9s / 5.9s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes


## 2026-10-13T13:35:46+00:00 — benchmark sweep33_methods_cuad — resolved plan

plan    : sweep33_methods_cuad — 12 experiment(s) over 12 store cell(s)
dataset : legalbenchrag-cuad
captures: data/raw/c88547bc806ea086 — 462 capture(s)
golden  : data/eval/datasets/legalbenchrag-cuad/golden.jsonl — 4046 row(s)
stores  :
  merge-2400-bge-m3      merge 2400/0.15/on     × bge-m3                       → data/benchmark_stores/merge-2400-0.15-on__bge-m3-47d5d5a2.json
  merge-sent-2400-bge-m3 merge 2400/0.15/on +sentences × bge-m3                       → data/benchmark_stores/merge-2400-0.15-on-sentences__bge-m3-47d5d5a2.json
  merge-crumb-2400-bge-m3 merge 2400/0.15/on +breadcrumb × bge-m3                       → data/benchmark_stores/merge-2400-0.15-on-crumb__bge-m3-47d5d5a2.json
  merge-sent-crumb-2400-bge-m3 merge 2400/0.15/on +sentences +breadcrumb × bge-m3                       → data/benchmark_stores/merge-2400-0.15-on-sentences-crumb__bge-m3-47d5d5a2.json
  merge-2400-embeddinggemma merge 2400/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-2400-0.15-on__embeddinggemma-47d5d5a2.json
  merge-sent-2400-embeddinggemma merge 2400/0.15/on +sentences × embeddinggemma               → data/benchmark_stores/merge-2400-0.15-on-sentences__embeddinggemma-47d5d5a2.json
  merge-crumb-2400-embeddinggemma merge 2400/0.15/on +breadcrumb × embeddinggemma               → data/benchmark_stores/merge-2400-0.15-on-crumb__embeddinggemma-47d5d5a2.json
  merge-sent-crumb-2400-embeddinggemma merge 2400/0.15/on +sentences +breadcrumb × embeddinggemma               → data/benchmark_stores/merge-2400-0.15-on-sentences-crumb__embeddinggemma-47d5d5a2.json
  merge-2400-snowflake-arctic-embed2 merge 2400/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-2400-0.15-on__snowflake-arctic-embed2-47d5d5a2.json
  merge-sent-2400-snowflake-arctic-embed2 merge 2400/0.15/on +sentences × snowflake-arctic-embed2      → data/benchmark_stores/merge-2400-0.15-on-sentences__snowflake-arctic-embed2-47d5d5a2.json
  merge-crumb-2400-snowflake-arctic-embed2 merge 2400/0.15/on +breadcrumb × snowflake-arctic-embed2      → data/benchmark_stores/merge-2400-0.15-on-crumb__snowflake-arctic-embed2-47d5d5a2.json
  merge-sent-crumb-2400-snowflake-arctic-embed2 merge 2400/0.15/on +sentences +breadcrumb × snowflake-arctic-embed2      → data/benchmark_stores/merge-2400-0.15-on-sentences-crumb__snowflake-arctic-embed2-47d5d5a2.json
experiments:
  1. merge-2400-bge-m3-embedding  → merge-2400-bge-m3      retrieval embedding
  2. merge-sent-2400-bge-m3-embedding → merge-sent-2400-bge-m3 retrieval embedding
  3. merge-crumb-2400-bge-m3-embedding → merge-crumb-2400-bge-m3 retrieval embedding
  4. merge-sent-crumb-2400-bge-m3-embedding → merge-sent-crumb-2400-bge-m3 retrieval embedding
  5. merge-2400-embeddinggemma-embedding → merge-2400-embeddinggemma retrieval embedding
  6. merge-sent-2400-embeddinggemma-embedding → merge-sent-2400-embeddinggemma retrieval embedding
  7. merge-crumb-2400-embeddinggemma-embedding → merge-crumb-2400-embeddinggemma retrieval embedding
  8. merge-sent-crumb-2400-embeddinggemma-embedding → merge-sent-crumb-2400-embeddinggemma retrieval embedding
  9. merge-2400-snowflake-arctic-embed2-embedding → merge-2400-snowflake-arctic-embed2 retrieval embedding
  10. merge-sent-2400-snowflake-arctic-embed2-embedding → merge-sent-2400-snowflake-arctic-embed2 retrieval embedding
  11. merge-crumb-2400-snowflake-arctic-embed2-embedding → merge-crumb-2400-snowflake-arctic-embed2 retrieval embedding
  12. merge-sent-crumb-2400-snowflake-arctic-embed2-embedding → merge-sent-crumb-2400-snowflake-arctic-embed2 retrieval embedding


## 2026-10-13T13:35:46+00:00 — benchmark sweep33_methods_cuad: merge-2400-bge-m3-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__bge-m3-47d5d5a2.json` — 13,459 chunks, bge-m3 (1024d), built 2026-10-13T13:35:48+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 9.8% | 42.4% | 60.5% | 0.318 | 98.6% | 100.0% | 100.0% | 0.993 | 11.9% | 49.0% | 67.3% | 12.5% | 14.2% | 13.1% | 9.9% | 14.5% |
| en | 4042 | 9.8% | 42.4% | 60.5% | 0.318 | 98.6% | 100.0% | 100.0% | 0.993 | 11.9% | 49.0% | 67.3% | 12.5% | 14.2% | 13.1% | 9.9% | 14.5% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 9.8% | 42.4% | 60.5% | 0.318 | 98.6% | 100.0% | 100.0% | 0.993 | 11.9% | 49.0% | 67.3% | 12.5% | 14.2% | 13.1% | 9.9% | 14.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6057, m002 0.5807, m003 0.6199, m004 0.5856)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-13T13:39:50+00:00 — benchmark sweep33_methods_cuad: merge-sent-2400-bge-m3-embedding

store: `data/benchmark_stores/merge-2400-0.15-on-sentences__bge-m3-47d5d5a2.json` — 13,488 chunks, bge-m3 (1024d), built 2026-10-13T13:39:50+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 9.7% | 42.3% | 60.4% | 0.318 | 98.7% | 100.0% | 100.0% | 0.993 | 12.0% | 49.3% | 67.2% | 12.5% | 14.2% | 13.1% | 9.9% | 14.5% |
| en | 4042 | 9.7% | 42.3% | 60.4% | 0.318 | 98.7% | 100.0% | 100.0% | 0.993 | 12.0% | 49.3% | 67.2% | 12.5% | 14.2% | 13.1% | 9.9% | 14.5% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 9.7% | 42.3% | 60.4% | 0.318 | 98.7% | 100.0% | 100.0% | 0.993 | 12.0% | 49.3% | 67.2% | 12.5% | 14.2% | 13.1% | 9.9% | 14.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6057, m002 0.5780, m003 0.6199, m004 0.5887)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-13T13:44:12+00:00 — benchmark sweep33_methods_cuad: merge-crumb-2400-bge-m3-embedding

store: `data/benchmark_stores/merge-2400-0.15-on-crumb__bge-m3-47d5d5a2.json` — 13,459 chunks, bge-m3 (1024d), built 2026-10-13T13:44:12+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 9.2% | 41.9% | 60.8% | 0.304 | 98.6% | 100.0% | 100.0% | 0.993 | 11.3% | 46.3% | 65.1% | 8.9% | 13.3% | 13.1% | 10.0% | 14.4% |
| en | 4042 | 9.2% | 41.9% | 60.8% | 0.304 | 98.6% | 100.0% | 100.0% | 0.993 | 11.3% | 46.3% | 65.1% | 8.9% | 13.3% | 13.1% | 10.0% | 14.4% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 9.2% | 41.9% | 60.8% | 0.304 | 98.6% | 100.0% | 100.0% | 0.993 | 11.3% | 46.3% | 65.1% | 8.9% | 13.3% | 13.1% | 10.0% | 14.4% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6006, m002 0.5908, m003 0.6207, m004 0.6135)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-13T13:49:05+00:00 — benchmark sweep33_methods_cuad: merge-sent-crumb-2400-bge-m3-embedding

store: `data/benchmark_stores/merge-2400-0.15-on-sentences-crumb__bge-m3-47d5d5a2.json` — 13,488 chunks, bge-m3 (1024d), built 2026-10-13T13:49:05+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 9.4% | 41.9% | 60.9% | 0.306 | 98.7% | 100.0% | 100.0% | 0.993 | 11.6% | 46.4% | 65.1% | 9.1% | 13.7% | 13.1% | 10.0% | 14.5% |
| en | 4042 | 9.4% | 41.9% | 60.9% | 0.306 | 98.7% | 100.0% | 100.0% | 0.993 | 11.6% | 46.4% | 65.1% | 9.1% | 13.7% | 13.1% | 10.0% | 14.5% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 9.4% | 41.9% | 60.9% | 0.306 | 98.7% | 100.0% | 100.0% | 0.993 | 11.6% | 46.4% | 65.1% | 9.1% | 13.7% | 13.1% | 10.0% | 14.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6006, m002 0.5908, m003 0.6207, m004 0.6168)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-13T13:54:02+00:00 — benchmark sweep33_methods_cuad: merge-2400-embeddinggemma-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__embeddinggemma-47d5d5a2.json` — 13,459 chunks, embeddinggemma (768d), built 2026-10-13T13:54:03+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 16.8% | 51.8% | 68.0% | 0.421 | 97.9% | 100.0% | 100.0% | 0.989 | 20.2% | 58.9% | 75.0% | 21.1% | 24.2% | 16.0% | 11.0% | 22.9% |
| en | 4042 | 16.8% | 51.8% | 68.0% | 0.421 | 97.9% | 100.0% | 100.0% | 0.989 | 20.2% | 58.9% | 75.0% | 21.1% | 24.2% | 16.0% | 11.0% | 22.9% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 16.8% | 51.8% | 68.0% | 0.421 | 97.9% | 100.0% | 100.0% | 0.989 | 20.2% | 58.9% | 75.0% | 21.1% | 24.2% | 16.0% | 11.0% | 22.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5256, m002 0.5389, m003 0.5898, m004 0.5026)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-13T13:57:18+00:00 — benchmark sweep33_methods_cuad: merge-sent-2400-embeddinggemma-embedding

store: `data/benchmark_stores/merge-2400-0.15-on-sentences__embeddinggemma-47d5d5a2.json` — 13,488 chunks, embeddinggemma (768d), built 2026-10-13T13:57:18+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 16.8% | 51.9% | 68.1% | 0.424 | 97.9% | 100.0% | 100.0% | 0.989 | 20.4% | 59.2% | 75.1% | 21.1% | 24.3% | 16.2% | 11.1% | 23.2% |
| en | 4042 | 16.8% | 51.9% | 68.1% | 0.424 | 97.9% | 100.0% | 100.0% | 0.989 | 20.4% | 59.2% | 75.1% | 21.1% | 24.3% | 16.2% | 11.1% | 23.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 16.8% | 51.9% | 68.1% | 0.424 | 97.9% | 100.0% | 100.0% | 0.989 | 20.4% | 59.2% | 75.1% | 21.1% | 24.3% | 16.2% | 11.1% | 23.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5319, m002 0.5389, m003 0.5890, m004 0.5026)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-13T14:00:43+00:00 — benchmark sweep33_methods_cuad: merge-crumb-2400-embeddinggemma-embedding

store: `data/benchmark_stores/merge-2400-0.15-on-crumb__embeddinggemma-47d5d5a2.json` — 13,459 chunks, embeddinggemma (768d), built 2026-10-13T14:00:43+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 14.9% | 51.8% | 68.9% | 0.394 | 97.7% | 100.0% | 100.0% | 0.988 | 17.8% | 57.2% | 73.6% | 14.1% | 21.3% | 16.0% | 11.2% | 21.5% |
| en | 4042 | 14.9% | 51.8% | 68.9% | 0.394 | 97.7% | 100.0% | 100.0% | 0.988 | 17.8% | 57.2% | 73.6% | 14.1% | 21.3% | 16.0% | 11.2% | 21.5% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 14.9% | 51.8% | 68.9% | 0.394 | 97.7% | 100.0% | 100.0% | 0.988 | 17.8% | 57.2% | 73.6% | 14.1% | 21.3% | 16.0% | 11.2% | 21.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5088, m002 0.5367, m003 0.5849, m004 0.4965)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-13T14:04:37+00:00 — benchmark sweep33_methods_cuad: merge-sent-crumb-2400-embeddinggemma-embedding

store: `data/benchmark_stores/merge-2400-0.15-on-sentences-crumb__embeddinggemma-47d5d5a2.json` — 13,488 chunks, embeddinggemma (768d), built 2026-10-13T14:04:37+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 15.0% | 52.0% | 68.9% | 0.398 | 97.8% | 100.0% | 100.0% | 0.988 | 18.1% | 57.3% | 73.9% | 14.2% | 21.6% | 16.2% | 11.3% | 21.8% |
| en | 4042 | 15.0% | 52.0% | 68.9% | 0.398 | 97.8% | 100.0% | 100.0% | 0.988 | 18.1% | 57.3% | 73.9% | 14.2% | 21.6% | 16.2% | 11.3% | 21.8% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 15.0% | 52.0% | 68.9% | 0.398 | 97.8% | 100.0% | 100.0% | 0.988 | 18.1% | 57.3% | 73.9% | 14.2% | 21.6% | 16.2% | 11.3% | 21.8% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5088, m002 0.5359, m003 0.5796, m004 0.4983)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-13T14:08:42+00:00 — benchmark sweep33_methods_cuad: merge-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__snowflake-arctic-embed2-47d5d5a2.json` — 13,459 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-13T14:08:43+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 10.2% | 41.8% | 61.0% | 0.318 | 98.5% | 100.0% | 100.0% | 0.992 | 12.5% | 47.6% | 67.2% | 13.2% | 14.5% | 12.8% | 9.9% | 14.9% |
| en | 4042 | 10.2% | 41.8% | 61.0% | 0.318 | 98.5% | 100.0% | 100.0% | 0.992 | 12.5% | 47.6% | 67.2% | 13.2% | 14.5% | 12.8% | 9.9% | 14.9% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 10.2% | 41.8% | 61.0% | 0.318 | 98.5% | 100.0% | 100.0% | 0.992 | 12.5% | 47.6% | 67.2% | 13.2% | 14.5% | 12.8% | 9.9% | 14.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.4727, m002 0.4814, m003 0.5743, m004 0.4756)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-13T14:12:51+00:00 — benchmark sweep33_methods_cuad: merge-sent-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-2400-0.15-on-sentences__snowflake-arctic-embed2-47d5d5a2.json` — 13,488 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-13T14:12:51+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 10.4% | 42.0% | 60.7% | 0.323 | 98.5% | 100.0% | 100.0% | 0.992 | 12.8% | 47.8% | 66.9% | 13.4% | 14.9% | 13.0% | 9.8% | 15.3% |
| en | 4042 | 10.4% | 42.0% | 60.7% | 0.323 | 98.5% | 100.0% | 100.0% | 0.992 | 12.8% | 47.8% | 66.9% | 13.4% | 14.9% | 13.0% | 9.8% | 15.3% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 10.4% | 42.0% | 60.7% | 0.323 | 98.5% | 100.0% | 100.0% | 0.992 | 12.8% | 47.8% | 66.9% | 13.4% | 14.9% | 13.0% | 9.8% | 15.3% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.4727, m002 0.4851, m003 0.5743, m004 0.4763)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-13T14:16:47+00:00 — benchmark sweep33_methods_cuad: merge-crumb-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-2400-0.15-on-crumb__snowflake-arctic-embed2-47d5d5a2.json` — 13,459 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-13T14:16:47+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 9.4% | 40.9% | 60.3% | 0.300 | 98.5% | 100.0% | 100.0% | 0.992 | 11.4% | 45.3% | 64.1% | 10.1% | 13.3% | 12.6% | 9.8% | 14.1% |
| en | 4042 | 9.4% | 40.9% | 60.3% | 0.300 | 98.5% | 100.0% | 100.0% | 0.992 | 11.4% | 45.3% | 64.1% | 10.1% | 13.3% | 12.6% | 9.8% | 14.1% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 9.4% | 40.9% | 60.3% | 0.300 | 98.5% | 100.0% | 100.0% | 0.992 | 11.4% | 45.3% | 64.1% | 10.1% | 13.3% | 12.6% | 9.8% | 14.1% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.4744, m002 0.4833, m003 0.5756, m004 0.4673)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-13T14:21:39+00:00 — benchmark sweep33_methods_cuad: merge-sent-crumb-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-2400-0.15-on-sentences-crumb__snowflake-arctic-embed2-47d5d5a2.json` — 13,488 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-13T14:21:40+00:00
golden: `data/eval/datasets/legalbenchrag-cuad/golden.jsonl` — 4046 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 4042 | 9.5% | 40.7% | 59.9% | 0.301 | 98.5% | 100.0% | 100.0% | 0.992 | 11.5% | 45.1% | 63.9% | 9.9% | 13.4% | 12.6% | 9.8% | 14.1% |
| en | 4042 | 9.5% | 40.7% | 59.9% | 0.301 | 98.5% | 100.0% | 100.0% | 0.992 | 11.5% | 45.1% | 63.9% | 9.9% | 13.4% | 12.6% | 9.8% | 14.1% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 4042 | 9.5% | 40.7% | 59.9% | 0.301 | 98.5% | 100.0% | 100.0% | 0.992 | 11.5% | 45.1% | 63.9% | 9.9% | 13.4% | 12.6% | 9.8% | 14.1% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.4765, m002 0.4847, m003 0.5756, m004 0.4625)
retrieval: embedding
dataset: legalbenchrag-cuad


## 2026-10-13T14:26:35+00:00 — benchmark sweep33_methods_cuad — dataset legalbenchrag-cuad — comparison (12 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| merge-2400-bge-m3-embedding | bge-m3 | 2400/0.15/on | embedding | 4042 | 9.8% | 42.4% | 60.5% | 0.318 | 98.6% | 100.0% | 100.0% | 0.993 | 11.9% | 49.0% | 67.3% | 12.5% | 14.2% | 13.1% | 9.9% | 14.5% | 4/4 | 152s / 86.6s |
| merge-sent-2400-bge-m3-embedding | bge-m3 | 2400/0.15/on | embedding | 4042 | 9.7% | 42.3% | 60.4% | 0.318 | 98.7% | 100.0% | 100.0% | 0.993 | 12.0% | 49.3% | 67.2% | 12.5% | 14.2% | 13.1% | 9.9% | 14.5% | 4/4 | 160s / 99.7s |
| merge-crumb-2400-bge-m3-embedding | bge-m3 | 2400/0.15/on | embedding | 4042 | 9.2% | 41.9% | 60.8% | 0.304 | 98.6% | 100.0% | 100.0% | 0.993 | 11.3% | 46.3% | 65.1% | 8.9% | 13.3% | 13.1% | 10.0% | 14.4% | 4/4 | 203s / 87.4s |
| merge-sent-crumb-2400-bge-m3-embedding | bge-m3 | 2400/0.15/on | embedding | 4042 | 9.4% | 41.9% | 60.9% | 0.306 | 98.7% | 100.0% | 100.0% | 0.993 | 11.6% | 46.4% | 65.1% | 9.1% | 13.7% | 13.1% | 10.0% | 14.5% | 4/4 | 207s / 87.7s |
| merge-2400-embeddinggemma-embedding | embeddinggemma | 2400/0.15/on | embedding | 4042 | 16.8% | 51.8% | 68.0% | 0.421 | 97.9% | 100.0% | 100.0% | 0.989 | 20.2% | 58.9% | 75.0% | 21.1% | 24.2% | 16.0% | 11.0% | 22.9% | 1/4 | 124s / 69.1s |
| merge-sent-2400-embeddinggemma-embedding | embeddinggemma | 2400/0.15/on | embedding | 4042 | 16.8% | 51.9% | 68.1% | 0.424 | 97.9% | 100.0% | 100.0% | 0.989 | 20.4% | 59.2% | 75.1% | 21.1% | 24.3% | 16.2% | 11.1% | 23.2% | 1/4 | 124s / 79.1s |
| merge-crumb-2400-embeddinggemma-embedding | embeddinggemma | 2400/0.15/on | embedding | 4042 | 14.9% | 51.8% | 68.9% | 0.394 | 97.7% | 100.0% | 100.0% | 0.988 | 17.8% | 57.2% | 73.6% | 14.1% | 21.3% | 16.0% | 11.2% | 21.5% | 1/4 | 157s / 75.2s |
| merge-sent-crumb-2400-embeddinggemma-embedding | embeddinggemma | 2400/0.15/on | embedding | 4042 | 15.0% | 52.0% | 68.9% | 0.398 | 97.8% | 100.0% | 100.0% | 0.988 | 18.1% | 57.3% | 73.9% | 14.2% | 21.6% | 16.2% | 11.3% | 21.8% | 1/4 | 165s / 77.6s |
| merge-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0.15/on | embedding | 4042 | 10.2% | 41.8% | 61.0% | 0.318 | 98.5% | 100.0% | 100.0% | 0.992 | 12.5% | 47.6% | 67.2% | 13.2% | 14.5% | 12.8% | 9.9% | 14.9% | 1/4 | 148s / 97.3s |
| merge-sent-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0.15/on | embedding | 4042 | 10.4% | 42.0% | 60.7% | 0.323 | 98.5% | 100.0% | 100.0% | 0.992 | 12.8% | 47.8% | 66.9% | 13.4% | 14.9% | 13.0% | 9.8% | 15.3% | 1/4 | 148s / 85.8s |
| merge-crumb-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0.15/on | embedding | 4042 | 9.4% | 40.9% | 60.3% | 0.300 | 98.5% | 100.0% | 100.0% | 0.992 | 11.4% | 45.3% | 64.1% | 10.1% | 13.3% | 12.6% | 9.8% | 14.1% | 1/4 | 197s / 92.3s |
| merge-sent-crumb-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0.15/on | embedding | 4042 | 9.5% | 40.7% | 59.9% | 0.301 | 98.5% | 100.0% | 100.0% | 0.992 | 11.5% | 45.1% | 63.9% | 9.9% | 13.4% | 12.6% | 9.8% | 14.1% | 1/4 | 200s / 92.5s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes


## 2026-10-13T14:28:22+00:00 — benchmark sweep33_methods_maud — resolved plan

plan    : sweep33_methods_maud — 12 experiment(s) over 12 store cell(s)
dataset : legalbenchrag-maud
captures: data/raw/4961ebee611362f6 — 150 capture(s)
golden  : data/eval/datasets/legalbenchrag-maud/golden.jsonl — 1680 row(s)
stores  :
  merge-2400-bge-m3      merge 2400/0.15/on     × bge-m3                       → data/benchmark_stores/merge-2400-0.15-on__bge-m3-68231218.json
  merge-sent-2400-bge-m3 merge 2400/0.15/on +sentences × bge-m3                       → data/benchmark_stores/merge-2400-0.15-on-sentences__bge-m3-68231218.json
  merge-crumb-2400-bge-m3 merge 2400/0.15/on +breadcrumb × bge-m3                       → data/benchmark_stores/merge-2400-0.15-on-crumb__bge-m3-68231218.json
  merge-sent-crumb-2400-bge-m3 merge 2400/0.15/on +sentences +breadcrumb × bge-m3                       → data/benchmark_stores/merge-2400-0.15-on-sentences-crumb__bge-m3-68231218.json
  merge-2400-embeddinggemma merge 2400/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-2400-0.15-on__embeddinggemma-68231218.json
  merge-sent-2400-embeddinggemma merge 2400/0.15/on +sentences × embeddinggemma               → data/benchmark_stores/merge-2400-0.15-on-sentences__embeddinggemma-68231218.json
  merge-crumb-2400-embeddinggemma merge 2400/0.15/on +breadcrumb × embeddinggemma               → data/benchmark_stores/merge-2400-0.15-on-crumb__embeddinggemma-68231218.json
  merge-sent-crumb-2400-embeddinggemma merge 2400/0.15/on +sentences +breadcrumb × embeddinggemma               → data/benchmark_stores/merge-2400-0.15-on-sentences-crumb__embeddinggemma-68231218.json
  merge-2400-snowflake-arctic-embed2 merge 2400/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-2400-0.15-on__snowflake-arctic-embed2-68231218.json
  merge-sent-2400-snowflake-arctic-embed2 merge 2400/0.15/on +sentences × snowflake-arctic-embed2      → data/benchmark_stores/merge-2400-0.15-on-sentences__snowflake-arctic-embed2-68231218.json
  merge-crumb-2400-snowflake-arctic-embed2 merge 2400/0.15/on +breadcrumb × snowflake-arctic-embed2      → data/benchmark_stores/merge-2400-0.15-on-crumb__snowflake-arctic-embed2-68231218.json
  merge-sent-crumb-2400-snowflake-arctic-embed2 merge 2400/0.15/on +sentences +breadcrumb × snowflake-arctic-embed2      → data/benchmark_stores/merge-2400-0.15-on-sentences-crumb__snowflake-arctic-embed2-68231218.json
experiments:
  1. merge-2400-bge-m3-embedding  → merge-2400-bge-m3      retrieval embedding
  2. merge-sent-2400-bge-m3-embedding → merge-sent-2400-bge-m3 retrieval embedding
  3. merge-crumb-2400-bge-m3-embedding → merge-crumb-2400-bge-m3 retrieval embedding
  4. merge-sent-crumb-2400-bge-m3-embedding → merge-sent-crumb-2400-bge-m3 retrieval embedding
  5. merge-2400-embeddinggemma-embedding → merge-2400-embeddinggemma retrieval embedding
  6. merge-sent-2400-embeddinggemma-embedding → merge-sent-2400-embeddinggemma retrieval embedding
  7. merge-crumb-2400-embeddinggemma-embedding → merge-crumb-2400-embeddinggemma retrieval embedding
  8. merge-sent-crumb-2400-embeddinggemma-embedding → merge-sent-crumb-2400-embeddinggemma retrieval embedding
  9. merge-2400-snowflake-arctic-embed2-embedding → merge-2400-snowflake-arctic-embed2 retrieval embedding
  10. merge-sent-2400-snowflake-arctic-embed2-embedding → merge-sent-2400-snowflake-arctic-embed2 retrieval embedding
  11. merge-crumb-2400-snowflake-arctic-embed2-embedding → merge-crumb-2400-snowflake-arctic-embed2 retrieval embedding
  12. merge-sent-crumb-2400-snowflake-arctic-embed2-embedding → merge-sent-crumb-2400-snowflake-arctic-embed2 retrieval embedding


## 2026-10-13T14:28:22+00:00 — benchmark sweep33_methods_maud: merge-2400-bge-m3-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__bge-m3-68231218.json` — 28,860 chunks, bge-m3 (1024d), built 2026-10-13T14:28:23+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 11.0% | 26.0% | 35.3% | 0.312 | 93.4% | 98.0% | 99.0% | 0.955 | 15.6% | 35.1% | 46.6% | 15.9% | 19.6% | 10.8% | 7.6% | 16.6% |
| en | 1676 | 11.0% | 26.0% | 35.3% | 0.312 | 93.4% | 98.0% | 99.0% | 0.955 | 15.6% | 35.1% | 46.6% | 15.9% | 19.6% | 10.8% | 7.6% | 16.6% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 11.0% | 26.0% | 35.3% | 0.312 | 93.4% | 98.0% | 99.0% | 0.955 | 15.6% | 35.1% | 46.6% | 15.9% | 19.6% | 10.8% | 7.6% | 16.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6228, m002 0.5728, m003 0.5710, m004 0.5636)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-13T14:34:58+00:00 — benchmark sweep33_methods_maud: merge-sent-2400-bge-m3-embedding

store: `data/benchmark_stores/merge-2400-0.15-on-sentences__bge-m3-68231218.json` — 29,207 chunks, bge-m3 (1024d), built 2026-10-13T14:34:58+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 11.1% | 26.2% | 35.0% | 0.315 | 93.2% | 98.0% | 99.0% | 0.953 | 16.0% | 35.3% | 46.2% | 16.3% | 20.0% | 10.8% | 7.6% | 16.8% |
| en | 1676 | 11.1% | 26.2% | 35.0% | 0.315 | 93.2% | 98.0% | 99.0% | 0.953 | 16.0% | 35.3% | 46.2% | 16.3% | 20.0% | 10.8% | 7.6% | 16.8% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 11.1% | 26.2% | 35.0% | 0.315 | 93.2% | 98.0% | 99.0% | 0.953 | 16.0% | 35.3% | 46.2% | 16.3% | 20.0% | 10.8% | 7.6% | 16.8% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6228, m002 0.5713, m003 0.5710, m004 0.5645)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-13T14:41:35+00:00 — benchmark sweep33_methods_maud: merge-crumb-2400-bge-m3-embedding

store: `data/benchmark_stores/merge-2400-0.15-on-crumb__bge-m3-68231218.json` — 28,860 chunks, bge-m3 (1024d), built 2026-10-13T14:41:35+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 9.6% | 23.9% | 33.4% | 0.270 | 92.7% | 97.1% | 98.6% | 0.948 | 13.0% | 30.6% | 41.9% | 12.0% | 16.4% | 9.6% | 7.1% | 14.1% |
| en | 1676 | 9.6% | 23.9% | 33.4% | 0.270 | 92.7% | 97.1% | 98.6% | 0.948 | 13.0% | 30.6% | 41.9% | 12.0% | 16.4% | 9.6% | 7.1% | 14.1% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 9.6% | 23.9% | 33.4% | 0.270 | 92.7% | 97.1% | 98.6% | 0.948 | 13.0% | 30.6% | 41.9% | 12.0% | 16.4% | 9.6% | 7.1% | 14.1% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6272, m002 0.5837, m003 0.5597, m004 0.5772)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-13T14:50:16+00:00 — benchmark sweep33_methods_maud: merge-sent-crumb-2400-bge-m3-embedding

store: `data/benchmark_stores/merge-2400-0.15-on-sentences-crumb__bge-m3-68231218.json` — 29,207 chunks, bge-m3 (1024d), built 2026-10-13T14:50:16+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 9.7% | 24.0% | 33.3% | 0.271 | 92.7% | 97.1% | 98.8% | 0.947 | 13.3% | 30.4% | 41.6% | 12.3% | 16.8% | 9.6% | 7.1% | 14.2% |
| en | 1676 | 9.7% | 24.0% | 33.3% | 0.271 | 92.7% | 97.1% | 98.8% | 0.947 | 13.3% | 30.4% | 41.6% | 12.3% | 16.8% | 9.6% | 7.1% | 14.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 9.7% | 24.0% | 33.3% | 0.271 | 92.7% | 97.1% | 98.8% | 0.947 | 13.3% | 30.4% | 41.6% | 12.3% | 16.8% | 9.6% | 7.1% | 14.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 4/4 (100.0%) (top-1: m001 0.6274, m002 0.5837, m003 0.5597, m004 0.5772)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-13T14:58:57+00:00 — benchmark sweep33_methods_maud: merge-2400-embeddinggemma-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__embeddinggemma-68231218.json` — 28,860 chunks, embeddinggemma (768d), built 2026-10-13T14:58:58+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 9.4% | 24.0% | 33.6% | 0.284 | 90.8% | 97.8% | 98.7% | 0.938 | 13.1% | 32.3% | 43.3% | 14.0% | 16.9% | 9.6% | 7.0% | 14.0% |
| en | 1676 | 9.4% | 24.0% | 33.6% | 0.284 | 90.8% | 97.8% | 98.7% | 0.938 | 13.1% | 32.3% | 43.3% | 14.0% | 16.9% | 9.6% | 7.0% | 14.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 9.4% | 24.0% | 33.6% | 0.284 | 90.8% | 97.8% | 98.7% | 0.938 | 13.1% | 32.3% | 43.3% | 14.0% | 16.9% | 9.6% | 7.0% | 14.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5299, m002 0.5417, m003 0.5307, m004 0.5751)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-13T15:04:09+00:00 — benchmark sweep33_methods_maud: merge-sent-2400-embeddinggemma-embedding

store: `data/benchmark_stores/merge-2400-0.15-on-sentences__embeddinggemma-68231218.json` — 29,207 chunks, embeddinggemma (768d), built 2026-10-13T15:04:09+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 9.4% | 24.0% | 33.9% | 0.287 | 90.3% | 97.7% | 98.6% | 0.935 | 13.5% | 32.5% | 44.6% | 14.2% | 17.2% | 9.5% | 7.1% | 14.0% |
| en | 1676 | 9.4% | 24.0% | 33.9% | 0.287 | 90.3% | 97.7% | 98.6% | 0.935 | 13.5% | 32.5% | 44.6% | 14.2% | 17.2% | 9.5% | 7.1% | 14.0% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 9.4% | 24.0% | 33.9% | 0.287 | 90.3% | 97.7% | 98.6% | 0.935 | 13.5% | 32.5% | 44.6% | 14.2% | 17.2% | 9.5% | 7.1% | 14.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5299, m002 0.5340, m003 0.5307, m004 0.5751)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-13T15:09:14+00:00 — benchmark sweep33_methods_maud: merge-crumb-2400-embeddinggemma-embedding

store: `data/benchmark_stores/merge-2400-0.15-on-crumb__embeddinggemma-68231218.json` — 28,860 chunks, embeddinggemma (768d), built 2026-10-13T15:09:14+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 9.0% | 21.8% | 31.8% | 0.251 | 90.8% | 97.5% | 99.1% | 0.937 | 11.9% | 27.5% | 39.4% | 12.4% | 15.1% | 8.4% | 6.4% | 12.6% |
| en | 1676 | 9.0% | 21.8% | 31.8% | 0.251 | 90.8% | 97.5% | 99.1% | 0.937 | 11.9% | 27.5% | 39.4% | 12.4% | 15.1% | 8.4% | 6.4% | 12.6% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 9.0% | 21.8% | 31.8% | 0.251 | 90.8% | 97.5% | 99.1% | 0.937 | 11.9% | 27.5% | 39.4% | 12.4% | 15.1% | 8.4% | 6.4% | 12.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5171, m002 0.5305, m003 0.5167, m004 0.5639)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-13T15:15:48+00:00 — benchmark sweep33_methods_maud: merge-sent-crumb-2400-embeddinggemma-embedding

store: `data/benchmark_stores/merge-2400-0.15-on-sentences-crumb__embeddinggemma-68231218.json` — 29,207 chunks, embeddinggemma (768d), built 2026-10-13T15:15:48+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 8.7% | 22.2% | 31.9% | 0.252 | 90.5% | 97.6% | 99.2% | 0.937 | 11.5% | 28.2% | 39.8% | 12.1% | 14.6% | 8.5% | 6.4% | 12.6% |
| en | 1676 | 8.7% | 22.2% | 31.9% | 0.252 | 90.5% | 97.6% | 99.2% | 0.937 | 11.5% | 28.2% | 39.8% | 12.1% | 14.6% | 8.5% | 6.4% | 12.6% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 8.7% | 22.2% | 31.9% | 0.252 | 90.5% | 97.6% | 99.2% | 0.937 | 11.5% | 28.2% | 39.8% | 12.1% | 14.6% | 8.5% | 6.4% | 12.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 1/4 (25.0%) (top-1: m001 0.5171, m002 0.5305, m003 0.5167, m004 0.5639)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-13T15:22:15+00:00 — benchmark sweep33_methods_maud: merge-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-2400-0.15-on__snowflake-arctic-embed2-68231218.json` — 28,860 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-13T15:22:16+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 6.7% | 18.9% | 29.3% | 0.231 | 93.2% | 97.6% | 98.4% | 0.952 | 9.7% | 25.4% | 38.0% | 10.2% | 12.7% | 7.8% | 6.4% | 10.2% |
| en | 1676 | 6.7% | 18.9% | 29.3% | 0.231 | 93.2% | 97.6% | 98.4% | 0.952 | 9.7% | 25.4% | 38.0% | 10.2% | 12.7% | 7.8% | 6.4% | 10.2% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 6.7% | 18.9% | 29.3% | 0.231 | 93.2% | 97.6% | 98.4% | 0.952 | 9.7% | 25.4% | 38.0% | 10.2% | 12.7% | 7.8% | 6.4% | 10.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 0/4 (0.0%) (top-1: m001 0.5088, m002 0.4913, m003 0.4963, m004 0.5138)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-13T15:28:40+00:00 — benchmark sweep33_methods_maud: merge-sent-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-2400-0.15-on-sentences__snowflake-arctic-embed2-68231218.json` — 29,207 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-13T15:28:40+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 6.4% | 19.3% | 29.4% | 0.232 | 93.3% | 97.9% | 98.7% | 0.953 | 9.7% | 26.6% | 39.1% | 10.5% | 12.3% | 8.2% | 6.4% | 10.6% |
| en | 1676 | 6.4% | 19.3% | 29.4% | 0.232 | 93.3% | 97.9% | 98.7% | 0.953 | 9.7% | 26.6% | 39.1% | 10.5% | 12.3% | 8.2% | 6.4% | 10.6% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 6.4% | 19.3% | 29.4% | 0.232 | 93.3% | 97.9% | 98.7% | 0.953 | 9.7% | 26.6% | 39.1% | 10.5% | 12.3% | 8.2% | 6.4% | 10.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 0/4 (0.0%) (top-1: m001 0.5088, m002 0.4913, m003 0.4963, m004 0.5138)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-13T15:35:06+00:00 — benchmark sweep33_methods_maud: merge-crumb-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-2400-0.15-on-crumb__snowflake-arctic-embed2-68231218.json` — 28,860 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-13T15:35:06+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 6.9% | 19.2% | 28.7% | 0.220 | 92.2% | 97.3% | 98.9% | 0.945 | 9.2% | 24.1% | 35.8% | 9.3% | 11.9% | 7.7% | 6.1% | 10.9% |
| en | 1676 | 6.9% | 19.2% | 28.7% | 0.220 | 92.2% | 97.3% | 98.9% | 0.945 | 9.2% | 24.1% | 35.8% | 9.3% | 11.9% | 7.7% | 6.1% | 10.9% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 6.9% | 19.2% | 28.7% | 0.220 | 92.2% | 97.3% | 98.9% | 0.945 | 9.2% | 24.1% | 35.8% | 9.3% | 11.9% | 7.7% | 6.1% | 10.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 0/4 (0.0%) (top-1: m001 0.5051, m002 0.4818, m003 0.4676, m004 0.4952)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-13T15:44:05+00:00 — benchmark sweep33_methods_maud: merge-sent-crumb-2400-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-2400-0.15-on-sentences-crumb__snowflake-arctic-embed2-68231218.json` — 29,207 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-13T15:44:05+00:00
golden: `data/eval/datasets/legalbenchrag-maud/golden.jsonl` — 1680 rows (0 synthetic / 4 manual); ranked depth 100
chunk config: max-chars 2400, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1676 | 6.8% | 19.4% | 29.2% | 0.222 | 91.8% | 97.4% | 99.0% | 0.943 | 9.2% | 25.1% | 36.7% | 9.4% | 11.6% | 7.7% | 6.2% | 10.9% |
| en | 1676 | 6.8% | 19.4% | 29.2% | 0.222 | 91.8% | 97.4% | 99.0% | 0.943 | 9.2% | 25.1% | 36.7% | 9.4% | 11.6% | 7.7% | 6.2% | 10.9% |
| synthetic | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| manual | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| cross-language | 0 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| same-language | 1676 | 6.8% | 19.4% | 29.2% | 0.222 | 91.8% | 97.4% | 99.0% | 0.943 | 9.2% | 25.1% | 36.7% | 9.4% | 11.6% | 7.7% | 6.2% | 10.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 4 rows, threshold ≥ 0.550 → false-retrieval 0/4 (0.0%) (top-1: m001 0.5051, m002 0.4820, m003 0.4676, m004 0.4952)
retrieval: embedding
dataset: legalbenchrag-maud


## 2026-10-13T15:52:51+00:00 — benchmark sweep33_methods_maud — dataset legalbenchrag-maud — comparison (12 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| merge-2400-bge-m3-embedding | bge-m3 | 2400/0.15/on | embedding | 1676 | 11.0% | 26.0% | 35.3% | 0.312 | 93.4% | 98.0% | 99.0% | 0.955 | 15.6% | 35.1% | 46.6% | 15.9% | 19.6% | 10.8% | 7.6% | 16.6% | 4/4 | 317s / 72.2s |
| merge-sent-2400-bge-m3-embedding | bge-m3 | 2400/0.15/on | embedding | 1676 | 11.1% | 26.2% | 35.0% | 0.315 | 93.2% | 98.0% | 99.0% | 0.953 | 16.0% | 35.3% | 46.2% | 16.3% | 20.0% | 10.8% | 7.6% | 16.8% | 4/4 | 319s / 72.6s |
| merge-crumb-2400-bge-m3-embedding | bge-m3 | 2400/0.15/on | embedding | 1676 | 9.6% | 23.9% | 33.4% | 0.270 | 92.7% | 97.1% | 98.6% | 0.948 | 13.0% | 30.6% | 41.9% | 12.0% | 16.4% | 9.6% | 7.1% | 14.1% | 4/4 | 443s / 73.3s |
| merge-sent-crumb-2400-bge-m3-embedding | bge-m3 | 2400/0.15/on | embedding | 1676 | 9.7% | 24.0% | 33.3% | 0.271 | 92.7% | 97.1% | 98.8% | 0.947 | 13.3% | 30.4% | 41.6% | 12.3% | 16.8% | 9.6% | 7.1% | 14.2% | 4/4 | 443s / 72.8s |
| merge-2400-embeddinggemma-embedding | embeddinggemma | 2400/0.15/on | embedding | 1676 | 9.4% | 24.0% | 33.6% | 0.284 | 90.8% | 97.8% | 98.7% | 0.938 | 13.1% | 32.3% | 43.3% | 14.0% | 16.9% | 9.6% | 7.0% | 14.0% | 1/4 | 254s / 52.6s |
| merge-sent-2400-embeddinggemma-embedding | embeddinggemma | 2400/0.15/on | embedding | 1676 | 9.4% | 24.0% | 33.9% | 0.287 | 90.3% | 97.7% | 98.6% | 0.935 | 13.5% | 32.5% | 44.6% | 14.2% | 17.2% | 9.5% | 7.1% | 14.0% | 1/4 | 248s / 53.8s |
| merge-crumb-2400-embeddinggemma-embedding | embeddinggemma | 2400/0.15/on | embedding | 1676 | 9.0% | 21.8% | 31.8% | 0.251 | 90.8% | 97.5% | 99.1% | 0.937 | 11.9% | 27.5% | 39.4% | 12.4% | 15.1% | 8.4% | 6.4% | 12.6% | 1/4 | 335s / 55.1s |
| merge-sent-crumb-2400-embeddinggemma-embedding | embeddinggemma | 2400/0.15/on | embedding | 1676 | 8.7% | 22.2% | 31.9% | 0.252 | 90.5% | 97.6% | 99.2% | 0.937 | 11.5% | 28.2% | 39.8% | 12.1% | 14.6% | 8.5% | 6.4% | 12.6% | 1/4 | 328s / 54.9s |
| merge-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0.15/on | embedding | 1676 | 6.7% | 18.9% | 29.3% | 0.231 | 93.2% | 97.6% | 98.4% | 0.952 | 9.7% | 25.4% | 38.0% | 10.2% | 12.7% | 7.8% | 6.4% | 10.2% | 0/4 | 311s / 67.2s |
| merge-sent-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0.15/on | embedding | 1676 | 6.4% | 19.3% | 29.4% | 0.232 | 93.3% | 97.9% | 98.7% | 0.953 | 9.7% | 26.6% | 39.1% | 10.5% | 12.3% | 8.2% | 6.4% | 10.6% | 0/4 | 312s / 68.3s |
| merge-crumb-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0.15/on | embedding | 1676 | 6.9% | 19.2% | 28.7% | 0.220 | 92.2% | 97.3% | 98.9% | 0.945 | 9.2% | 24.1% | 35.8% | 9.3% | 11.9% | 7.7% | 6.1% | 10.9% | 0/4 | 463s / 70.9s |
| merge-sent-crumb-2400-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 2400/0.15/on | embedding | 1676 | 6.8% | 19.4% | 29.2% | 0.222 | 91.8% | 97.4% | 99.0% | 0.943 | 9.2% | 25.1% | 36.7% | 9.4% | 11.6% | 7.7% | 6.2% | 10.9% | 0/4 | 448s / 72.7s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes


## 2026-10-14T06:58:08+00:00 — benchmark sweep34_types_uwazi — resolved plan

plan    : sweep34_types_uwazi — 12 experiment(s) over 12 store cell(s)
captures: data/raw/bdd5a7c445847b35 — 77 capture(s)
golden  : data/eval/golden.jsonl — 270 row(s)
stores  :
  merge-1200-bge-m3      merge 1200/0.15/on     × bge-m3                       → data/benchmark_stores/merge-1200-0.15-on__bge-m3-4d284af0.json
  merge-crumb-1200-bge-m3 merge 1200/0.15/on +breadcrumb × bge-m3                       → data/benchmark_stores/merge-1200-0.15-on-crumb__bge-m3-4d284af0.json
  type-merge-1200-bge-m3 type-merge 1200/0.15/on × bge-m3                       → data/benchmark_stores/type-merge-1200-0.15-on__bge-m3-4d284af0.json
  type-merge-crumb-1200-bge-m3 type-merge 1200/0.15/on +breadcrumb × bge-m3                       → data/benchmark_stores/type-merge-1200-0.15-on-crumb__bge-m3-4d284af0.json
  merge-1200-embeddinggemma merge 1200/0.15/on     × embeddinggemma               → data/benchmark_stores/merge-1200-0.15-on__embeddinggemma-4d284af0.json
  merge-crumb-1200-embeddinggemma merge 1200/0.15/on +breadcrumb × embeddinggemma               → data/benchmark_stores/merge-1200-0.15-on-crumb__embeddinggemma-4d284af0.json
  type-merge-1200-embeddinggemma type-merge 1200/0.15/on × embeddinggemma               → data/benchmark_stores/type-merge-1200-0.15-on__embeddinggemma-4d284af0.json
  type-merge-crumb-1200-embeddinggemma type-merge 1200/0.15/on +breadcrumb × embeddinggemma               → data/benchmark_stores/type-merge-1200-0.15-on-crumb__embeddinggemma-4d284af0.json
  merge-1200-snowflake-arctic-embed2 merge 1200/0.15/on     × snowflake-arctic-embed2      → data/benchmark_stores/merge-1200-0.15-on__snowflake-arctic-embed2-4d284af0.json
  merge-crumb-1200-snowflake-arctic-embed2 merge 1200/0.15/on +breadcrumb × snowflake-arctic-embed2      → data/benchmark_stores/merge-1200-0.15-on-crumb__snowflake-arctic-embed2-4d284af0.json
  type-merge-1200-snowflake-arctic-embed2 type-merge 1200/0.15/on × snowflake-arctic-embed2      → data/benchmark_stores/type-merge-1200-0.15-on__snowflake-arctic-embed2-4d284af0.json
  type-merge-crumb-1200-snowflake-arctic-embed2 type-merge 1200/0.15/on +breadcrumb × snowflake-arctic-embed2      → data/benchmark_stores/type-merge-1200-0.15-on-crumb__snowflake-arctic-embed2-4d284af0.json
experiments:
  1. merge-1200-bge-m3-embedding  → merge-1200-bge-m3      retrieval embedding
  2. merge-crumb-1200-bge-m3-embedding → merge-crumb-1200-bge-m3 retrieval embedding
  3. type-merge-1200-bge-m3-embedding → type-merge-1200-bge-m3 retrieval embedding
  4. type-merge-crumb-1200-bge-m3-embedding → type-merge-crumb-1200-bge-m3 retrieval embedding
  5. merge-1200-embeddinggemma-embedding → merge-1200-embeddinggemma retrieval embedding
  6. merge-crumb-1200-embeddinggemma-embedding → merge-crumb-1200-embeddinggemma retrieval embedding
  7. type-merge-1200-embeddinggemma-embedding → type-merge-1200-embeddinggemma retrieval embedding
  8. type-merge-crumb-1200-embeddinggemma-embedding → type-merge-crumb-1200-embeddinggemma retrieval embedding
  9. merge-1200-snowflake-arctic-embed2-embedding → merge-1200-snowflake-arctic-embed2 retrieval embedding
  10. merge-crumb-1200-snowflake-arctic-embed2-embedding → merge-crumb-1200-snowflake-arctic-embed2 retrieval embedding
  11. type-merge-1200-snowflake-arctic-embed2-embedding → type-merge-1200-snowflake-arctic-embed2 retrieval embedding
  12. type-merge-crumb-1200-snowflake-arctic-embed2-embedding → type-merge-crumb-1200-snowflake-arctic-embed2 retrieval embedding


## 2026-10-14T06:58:08+00:00 — benchmark sweep34_types_uwazi: merge-1200-bge-m3-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__bge-m3-4d284af0.json` — 4,488 chunks, bge-m3 (1024d), built 2026-10-13T12:52:53+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.4% | 62.8% | 73.5% | 0.479 | 62.9% | 91.8% | 93.6% | 0.751 | 32.7% | 64.9% | 75.7% | 49.3% | 33.0% | 13.4% | 7.9% | 32.8% |
| en | 169 | 32.8% | 64.2% | 73.4% | 0.484 | 68.0% | 92.9% | 93.5% | 0.782 | 33.3% | 66.3% | 75.0% | 50.5% | 33.7% | 13.6% | 7.8% | 34.3% |
| es | 98 | 28.9% | 60.4% | 73.8% | 0.470 | 54.1% | 89.8% | 93.9% | 0.698 | 31.6% | 62.6% | 76.9% | 47.3% | 31.6% | 13.1% | 8.1% | 30.3% |
| synthetic | 255 | 31.3% | 62.6% | 73.1% | 0.479 | 62.4% | 91.4% | 93.3% | 0.747 | 32.7% | 64.8% | 75.4% | 49.7% | 32.9% | 13.4% | 7.9% | 32.8% |
| manual | 12 | 33.3% | 66.7% | 83.3% | 0.476 | 75.0% | 100.0% | 100.0% | 0.833 | 33.3% | 66.7% | 83.3% | 41.7% | 33.3% | 13.3% | 8.3% | 33.3% |
| cross-language | 65 | 23.6% | 53.3% | 70.0% | 0.412 | 55.4% | 92.3% | 95.4% | 0.701 | 25.1% | 56.9% | 72.1% | 37.4% | 26.2% | 11.7% | 7.8% | 24.1% |
| same-language | 202 | 33.9% | 65.8% | 74.7% | 0.500 | 65.3% | 91.6% | 93.1% | 0.767 | 35.1% | 67.5% | 76.9% | 53.1% | 35.1% | 14.0% | 7.9% | 35.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5359, m014 0.5081, m015 0.4582)
retrieval: embedding


## 2026-10-14T06:58:14+00:00 — benchmark sweep34_types_uwazi: merge-crumb-1200-bge-m3-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-crumb__bge-m3-4d284af0.json` — 4,488 chunks, bge-m3 (1024d), built 2026-10-13T12:54:12+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 32.5% | 62.4% | 74.1% | 0.480 | 65.9% | 91.0% | 94.0% | 0.763 | 34.0% | 64.9% | 76.3% | 47.8% | 34.5% | 13.3% | 8.0% | 33.6% |
| en | 169 | 33.1% | 63.0% | 73.1% | 0.478 | 70.4% | 90.5% | 92.9% | 0.787 | 33.9% | 65.1% | 74.9% | 48.1% | 34.3% | 13.4% | 7.8% | 34.6% |
| es | 98 | 31.5% | 61.4% | 75.9% | 0.483 | 58.2% | 91.8% | 95.9% | 0.723 | 34.0% | 64.6% | 78.9% | 47.3% | 34.7% | 13.3% | 8.3% | 31.8% |
| synthetic | 255 | 32.5% | 62.2% | 73.7% | 0.481 | 65.5% | 90.6% | 93.7% | 0.760 | 34.0% | 64.8% | 76.0% | 47.7% | 34.5% | 13.3% | 8.0% | 33.6% |
| manual | 12 | 33.3% | 66.7% | 83.3% | 0.462 | 75.0% | 100.0% | 100.0% | 0.833 | 33.3% | 66.7% | 83.3% | 50.0% | 33.3% | 13.3% | 8.3% | 33.3% |
| cross-language | 65 | 25.1% | 51.8% | 73.8% | 0.412 | 55.4% | 93.8% | 95.4% | 0.698 | 26.7% | 55.4% | 76.2% | 39.0% | 27.7% | 11.4% | 8.3% | 26.4% |
| same-language | 202 | 34.9% | 65.8% | 74.2% | 0.502 | 69.3% | 90.1% | 93.6% | 0.784 | 36.3% | 68.0% | 76.4% | 50.7% | 36.6% | 14.0% | 7.9% | 35.9% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5409, m014 0.5209, m015 0.4629)
retrieval: embedding


## 2026-10-14T06:58:18+00:00 — benchmark sweep34_types_uwazi: type-merge-1200-bge-m3-embedding

store: `data/benchmark_stores/type-merge-1200-0.15-on__bge-m3-4d284af0.json` — 5,403 chunks, bge-m3 (1024d), built 2026-10-14T06:58:18+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 28.6% | 54.6% | 66.8% | 0.498 | 63.3% | 91.8% | 94.0% | 0.751 | 30.5% | 58.3% | 70.7% | 44.3% | 36.3% | 14.5% | 9.1% | 31.7% |
| en | 169 | 29.9% | 56.7% | 68.5% | 0.513 | 66.9% | 92.9% | 94.7% | 0.776 | 30.9% | 60.0% | 71.6% | 45.6% | 37.9% | 15.1% | 9.3% | 33.1% |
| es | 98 | 26.3% | 51.0% | 64.0% | 0.470 | 57.1% | 89.8% | 92.9% | 0.706 | 29.8% | 55.4% | 69.2% | 41.9% | 33.7% | 13.5% | 8.8% | 29.3% |
| synthetic | 255 | 28.8% | 54.7% | 66.7% | 0.501 | 62.7% | 91.4% | 93.7% | 0.747 | 30.7% | 58.4% | 70.6% | 45.1% | 36.5% | 14.6% | 9.2% | 32.0% |
| manual | 12 | 25.0% | 54.2% | 70.8% | 0.433 | 75.0% | 100.0% | 100.0% | 0.829 | 26.4% | 55.6% | 72.2% | 26.4% | 33.3% | 13.3% | 8.3% | 25.0% |
| cross-language | 65 | 20.6% | 45.9% | 64.7% | 0.434 | 55.4% | 92.3% | 95.4% | 0.696 | 20.9% | 48.9% | 67.2% | 32.4% | 29.2% | 13.5% | 10.3% | 23.8% |
| same-language | 202 | 31.2% | 57.5% | 67.5% | 0.518 | 65.8% | 91.6% | 93.6% | 0.768 | 33.6% | 61.3% | 71.8% | 48.1% | 38.6% | 14.9% | 8.8% | 34.2% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5359, m014 0.5050, m015 0.4582)
retrieval: embedding


## 2026-10-14T06:59:02+00:00 — benchmark sweep34_types_uwazi: type-merge-crumb-1200-bge-m3-embedding

store: `data/benchmark_stores/type-merge-1200-0.15-on-crumb__bge-m3-4d284af0.json` — 5,403 chunks, bge-m3 (1024d), built 2026-10-14T06:59:02+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 29.0% | 53.6% | 65.4% | 0.495 | 65.5% | 91.0% | 95.1% | 0.763 | 30.9% | 57.3% | 68.9% | 41.9% | 36.7% | 14.4% | 9.0% | 32.0% |
| en | 169 | 28.8% | 55.0% | 65.7% | 0.494 | 68.0% | 90.5% | 94.1% | 0.779 | 29.7% | 57.9% | 68.3% | 41.4% | 36.7% | 14.7% | 9.1% | 31.4% |
| es | 98 | 29.4% | 51.2% | 64.8% | 0.498 | 61.2% | 91.8% | 96.9% | 0.737 | 32.9% | 56.3% | 69.9% | 42.8% | 36.7% | 13.9% | 9.0% | 33.2% |
| synthetic | 255 | 29.2% | 54.0% | 65.5% | 0.499 | 65.1% | 90.6% | 94.9% | 0.760 | 31.1% | 57.8% | 69.1% | 42.3% | 36.9% | 14.5% | 9.1% | 32.4% |
| manual | 12 | 25.0% | 45.8% | 62.5% | 0.423 | 75.0% | 100.0% | 100.0% | 0.829 | 26.4% | 47.2% | 63.9% | 34.7% | 33.3% | 11.7% | 7.5% | 25.0% |
| cross-language | 65 | 20.6% | 44.1% | 60.6% | 0.432 | 53.8% | 93.8% | 96.9% | 0.693 | 20.9% | 47.4% | 63.2% | 33.0% | 29.2% | 13.2% | 9.4% | 24.4% |
| same-language | 202 | 31.7% | 56.7% | 66.9% | 0.516 | 69.3% | 90.1% | 94.6% | 0.786 | 34.1% | 60.5% | 70.7% | 44.8% | 39.1% | 14.8% | 8.9% | 34.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5409, m014 0.5079, m015 0.4641)
retrieval: embedding


## 2026-10-14T06:59:47+00:00 — benchmark sweep34_types_uwazi: merge-1200-embeddinggemma-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__embeddinggemma-4d284af0.json` — 4,488 chunks, embeddinggemma (768d), built 2026-10-13T12:55:41+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 37.2% | 65.2% | 79.5% | 0.528 | 67.8% | 92.9% | 97.8% | 0.787 | 38.8% | 67.4% | 81.6% | 54.3% | 39.3% | 13.9% | 8.5% | 37.7% |
| en | 169 | 38.5% | 66.3% | 79.6% | 0.535 | 70.4% | 91.1% | 97.0% | 0.796 | 39.4% | 67.8% | 81.4% | 54.2% | 40.2% | 14.1% | 8.5% | 38.8% |
| es | 98 | 35.0% | 63.4% | 79.3% | 0.516 | 63.3% | 95.9% | 99.0% | 0.773 | 37.8% | 66.7% | 82.0% | 54.4% | 37.8% | 13.7% | 8.6% | 35.9% |
| synthetic | 255 | 37.8% | 65.6% | 78.9% | 0.533 | 67.1% | 92.5% | 97.6% | 0.781 | 39.5% | 67.8% | 81.1% | 54.5% | 40.0% | 14.0% | 8.5% | 38.3% |
| manual | 12 | 25.0% | 58.3% | 91.7% | 0.423 | 83.3% | 100.0% | 100.0% | 0.917 | 25.0% | 58.3% | 91.7% | 50.0% | 25.0% | 11.7% | 9.2% | 25.0% |
| cross-language | 65 | 35.1% | 59.7% | 77.4% | 0.501 | 56.9% | 89.2% | 98.5% | 0.707 | 36.4% | 62.3% | 79.2% | 45.6% | 38.5% | 13.2% | 8.5% | 35.1% |
| same-language | 202 | 37.9% | 67.0% | 80.1% | 0.537 | 71.3% | 94.1% | 97.5% | 0.813 | 39.6% | 69.0% | 82.3% | 57.1% | 39.6% | 14.2% | 8.5% | 38.5% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4994, m014 0.4174, m015 0.3793)
retrieval: embedding


## 2026-10-14T06:59:51+00:00 — benchmark sweep34_types_uwazi: merge-crumb-1200-embeddinggemma-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-crumb__embeddinggemma-4d284af0.json` — 4,488 chunks, embeddinggemma (768d), built 2026-10-13T12:56:53+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 32.0% | 64.3% | 78.5% | 0.493 | 64.0% | 94.0% | 97.8% | 0.765 | 33.6% | 66.4% | 80.7% | 50.4% | 34.1% | 13.7% | 8.4% | 32.3% |
| en | 169 | 33.1% | 63.6% | 76.9% | 0.497 | 64.5% | 92.3% | 97.0% | 0.761 | 34.1% | 65.0% | 78.4% | 51.3% | 34.9% | 13.5% | 8.2% | 33.4% |
| es | 98 | 29.9% | 65.5% | 81.3% | 0.485 | 63.3% | 96.9% | 99.0% | 0.771 | 32.7% | 68.7% | 84.7% | 49.0% | 32.7% | 14.1% | 8.7% | 30.3% |
| synthetic | 255 | 32.3% | 64.2% | 78.3% | 0.497 | 63.1% | 93.7% | 97.6% | 0.758 | 34.0% | 66.3% | 80.6% | 50.8% | 34.5% | 13.7% | 8.4% | 32.6% |
| manual | 12 | 25.0% | 66.7% | 83.3% | 0.399 | 83.3% | 100.0% | 100.0% | 0.917 | 25.0% | 66.7% | 83.3% | 41.7% | 25.0% | 13.3% | 8.3% | 25.0% |
| cross-language | 65 | 29.0% | 55.1% | 77.4% | 0.446 | 53.8% | 92.3% | 98.5% | 0.696 | 30.3% | 56.7% | 79.2% | 39.5% | 32.3% | 12.0% | 8.5% | 29.0% |
| same-language | 202 | 32.9% | 67.2% | 78.9% | 0.508 | 67.3% | 94.6% | 97.5% | 0.787 | 34.7% | 69.5% | 81.2% | 54.0% | 34.7% | 14.3% | 8.4% | 33.3% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4971, m014 0.4144, m015 0.3932)
retrieval: embedding


## 2026-10-14T06:59:53+00:00 — benchmark sweep34_types_uwazi: type-merge-1200-embeddinggemma-embedding

store: `data/benchmark_stores/type-merge-1200-0.15-on__embeddinggemma-4d284af0.json` — 5,403 chunks, embeddinggemma (768d), built 2026-10-14T06:59:53+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.0% | 55.6% | 69.1% | 0.535 | 66.3% | 93.3% | 96.3% | 0.776 | 33.2% | 58.7% | 72.3% | 50.2% | 40.4% | 14.8% | 9.5% | 33.6% |
| en | 169 | 32.2% | 57.8% | 68.3% | 0.540 | 70.4% | 91.7% | 94.7% | 0.792 | 32.9% | 59.7% | 71.1% | 49.7% | 40.8% | 15.5% | 9.5% | 35.2% |
| es | 98 | 28.9% | 51.8% | 70.4% | 0.527 | 59.2% | 95.9% | 99.0% | 0.748 | 33.6% | 57.0% | 74.4% | 51.0% | 39.8% | 13.7% | 9.5% | 30.9% |
| synthetic | 255 | 31.3% | 56.3% | 69.4% | 0.541 | 65.5% | 92.9% | 96.1% | 0.769 | 33.5% | 59.4% | 72.7% | 50.5% | 40.8% | 15.1% | 9.6% | 34.0% |
| manual | 12 | 25.0% | 41.7% | 62.5% | 0.418 | 83.3% | 100.0% | 100.0% | 0.917 | 26.4% | 43.1% | 63.9% | 43.1% | 33.3% | 10.0% | 7.5% | 25.0% |
| cross-language | 65 | 26.0% | 43.5% | 68.7% | 0.503 | 58.5% | 90.8% | 95.4% | 0.712 | 25.9% | 45.6% | 69.9% | 36.3% | 38.5% | 13.2% | 10.6% | 28.2% |
| same-language | 202 | 32.6% | 59.5% | 69.2% | 0.546 | 68.8% | 94.1% | 96.5% | 0.796 | 35.5% | 62.9% | 73.1% | 54.6% | 41.1% | 15.3% | 9.1% | 35.4% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.5033, m014 0.4246, m015 0.4028)
retrieval: embedding


## 2026-10-14T07:00:32+00:00 — benchmark sweep34_types_uwazi: type-merge-crumb-1200-embeddinggemma-embedding

store: `data/benchmark_stores/type-merge-1200-0.15-on-crumb__embeddinggemma-4d284af0.json` — 5,403 chunks, embeddinggemma (768d), built 2026-10-14T07:00:32+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 28.0% | 56.5% | 67.6% | 0.504 | 65.5% | 94.0% | 97.0% | 0.771 | 30.1% | 59.5% | 70.6% | 47.4% | 36.0% | 15.2% | 9.3% | 31.5% |
| en | 169 | 28.7% | 57.2% | 66.2% | 0.504 | 66.3% | 91.7% | 95.9% | 0.769 | 29.5% | 59.3% | 68.3% | 46.4% | 36.1% | 15.4% | 9.2% | 32.2% |
| es | 98 | 27.0% | 55.2% | 70.0% | 0.505 | 64.3% | 98.0% | 99.0% | 0.776 | 31.3% | 59.9% | 74.4% | 49.0% | 35.7% | 14.9% | 9.4% | 30.2% |
| synthetic | 255 | 28.4% | 57.2% | 67.9% | 0.510 | 64.7% | 93.7% | 96.9% | 0.765 | 30.5% | 60.3% | 70.9% | 48.0% | 36.5% | 15.5% | 9.4% | 31.8% |
| manual | 12 | 20.8% | 41.7% | 62.5% | 0.377 | 83.3% | 100.0% | 100.0% | 0.917 | 22.2% | 43.1% | 63.9% | 34.7% | 25.0% | 10.0% | 7.5% | 25.0% |
| cross-language | 65 | 22.9% | 44.8% | 62.4% | 0.451 | 56.9% | 92.3% | 95.4% | 0.711 | 23.1% | 46.6% | 63.5% | 33.2% | 32.3% | 13.5% | 9.5% | 26.6% |
| same-language | 202 | 29.7% | 60.2% | 69.3% | 0.522 | 68.3% | 94.6% | 97.5% | 0.791 | 32.4% | 63.7% | 72.8% | 51.9% | 37.1% | 15.7% | 9.2% | 33.0% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4971, m014 0.4222, m015 0.4045)
retrieval: embedding


## 2026-10-14T07:01:09+00:00 — benchmark sweep34_types_uwazi: merge-1200-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-1200-0.15-on__snowflake-arctic-embed2-4d284af0.json` — 4,488 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-13T12:58:08+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 37.3% | 63.8% | 75.0% | 0.515 | 64.8% | 89.9% | 94.8% | 0.754 | 38.8% | 66.0% | 77.1% | 50.7% | 39.3% | 13.7% | 8.1% | 38.6% |
| en | 169 | 37.3% | 63.6% | 76.9% | 0.509 | 67.5% | 89.3% | 94.1% | 0.765 | 38.1% | 65.1% | 78.4% | 49.7% | 38.5% | 13.5% | 8.2% | 38.8% |
| es | 98 | 37.4% | 64.1% | 71.8% | 0.525 | 60.2% | 90.8% | 95.9% | 0.736 | 40.1% | 67.7% | 74.8% | 52.4% | 40.8% | 14.1% | 7.9% | 38.3% |
| synthetic | 255 | 37.5% | 64.1% | 74.6% | 0.517 | 63.9% | 89.4% | 94.5% | 0.747 | 39.1% | 66.4% | 76.8% | 50.7% | 39.6% | 13.8% | 8.1% | 38.8% |
| manual | 12 | 33.3% | 58.3% | 83.3% | 0.476 | 83.3% | 100.0% | 100.0% | 0.903 | 33.3% | 58.3% | 83.3% | 50.0% | 33.3% | 11.7% | 8.3% | 33.3% |
| cross-language | 65 | 30.3% | 60.8% | 73.1% | 0.468 | 53.8% | 89.2% | 93.8% | 0.681 | 32.8% | 63.1% | 76.2% | 41.5% | 33.8% | 13.5% | 8.2% | 31.5% |
| same-language | 202 | 39.6% | 64.8% | 75.7% | 0.530 | 68.3% | 90.1% | 95.0% | 0.778 | 40.8% | 67.0% | 77.4% | 53.6% | 41.1% | 13.8% | 8.1% | 40.8% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4227, m014 0.4076, m015 0.3614)
retrieval: embedding


## 2026-10-14T07:01:14+00:00 — benchmark sweep34_types_uwazi: merge-crumb-1200-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/merge-1200-0.15-on-crumb__snowflake-arctic-embed2-4d284af0.json` — 4,488 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-13T12:59:28+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 33.4% | 62.7% | 73.9% | 0.483 | 63.3% | 91.4% | 95.1% | 0.745 | 34.7% | 64.7% | 75.8% | 47.7% | 35.2% | 13.4% | 7.9% | 34.6% |
| en | 169 | 34.9% | 63.3% | 76.0% | 0.493 | 67.5% | 91.1% | 94.1% | 0.767 | 35.7% | 64.8% | 77.5% | 49.7% | 36.1% | 13.5% | 8.2% | 36.7% |
| es | 98 | 30.8% | 61.6% | 70.2% | 0.465 | 56.1% | 91.8% | 96.9% | 0.709 | 33.0% | 64.6% | 72.8% | 44.2% | 33.7% | 13.3% | 7.6% | 31.1% |
| synthetic | 255 | 33.4% | 62.5% | 73.5% | 0.484 | 62.4% | 91.0% | 94.9% | 0.738 | 34.8% | 64.6% | 75.4% | 47.6% | 35.3% | 13.4% | 7.9% | 34.7% |
| manual | 12 | 33.3% | 66.7% | 83.3% | 0.466 | 83.3% | 100.0% | 100.0% | 0.903 | 33.3% | 66.7% | 83.3% | 50.0% | 33.3% | 13.3% | 8.3% | 33.3% |
| cross-language | 65 | 30.3% | 61.5% | 76.9% | 0.468 | 56.9% | 92.3% | 95.4% | 0.712 | 32.8% | 63.8% | 80.0% | 41.5% | 33.8% | 13.8% | 8.6% | 31.5% |
| same-language | 202 | 34.4% | 63.0% | 72.9% | 0.488 | 65.3% | 91.1% | 95.0% | 0.756 | 35.3% | 65.0% | 74.4% | 49.7% | 35.6% | 13.3% | 7.7% | 35.6% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4109, m014 0.4018, m015 0.3773)
retrieval: embedding


## 2026-10-14T07:01:18+00:00 — benchmark sweep34_types_uwazi: type-merge-1200-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/type-merge-1200-0.15-on__snowflake-arctic-embed2-4d284af0.json` — 5,403 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-14T07:01:18+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 31.3% | 54.7% | 62.8% | 0.516 | 64.4% | 89.5% | 94.8% | 0.754 | 33.6% | 56.8% | 64.6% | 49.5% | 39.7% | 15.3% | 9.0% | 35.2% |
| en | 169 | 32.7% | 52.9% | 64.4% | 0.526 | 68.6% | 88.2% | 94.1% | 0.771 | 33.8% | 54.3% | 66.0% | 48.0% | 41.4% | 15.0% | 9.3% | 36.8% |
| es | 98 | 29.0% | 57.8% | 59.9% | 0.499 | 57.1% | 91.8% | 95.9% | 0.723 | 33.3% | 61.1% | 62.2% | 52.3% | 36.7% | 15.7% | 8.6% | 32.4% |
| synthetic | 255 | 31.2% | 55.3% | 63.2% | 0.519 | 63.5% | 89.4% | 94.5% | 0.747 | 33.6% | 57.4% | 65.1% | 50.2% | 39.6% | 15.5% | 9.1% | 35.3% |
| manual | 12 | 33.3% | 41.7% | 54.2% | 0.465 | 83.3% | 91.7% | 100.0% | 0.887 | 34.7% | 43.1% | 55.6% | 34.7% | 41.7% | 10.0% | 6.7% | 33.3% |
| cross-language | 65 | 24.5% | 51.2% | 59.8% | 0.492 | 60.0% | 90.8% | 93.8% | 0.727 | 26.6% | 51.8% | 61.4% | 42.9% | 35.4% | 16.9% | 10.5% | 30.7% |
| same-language | 202 | 33.6% | 55.8% | 63.7% | 0.524 | 65.8% | 89.1% | 95.0% | 0.762 | 35.9% | 58.4% | 65.7% | 51.7% | 41.1% | 14.8% | 8.6% | 36.7% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4227, m014 0.4550, m015 0.4235)
retrieval: embedding


## 2026-10-14T07:02:02+00:00 — benchmark sweep34_types_uwazi: type-merge-crumb-1200-snowflake-arctic-embed2-embedding

store: `data/benchmark_stores/type-merge-1200-0.15-on-crumb__snowflake-arctic-embed2-4d284af0.json` — 5,403 chunks, snowflake-arctic-embed2 (1024d), built 2026-10-14T07:02:02+00:00
golden: `data/eval/golden.jsonl` — 270 rows (255 synthetic / 15 manual); ranked depth 100
chunk config: max-chars 1200, overlap 0.15, header on

| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 267 | 28.5% | 52.8% | 62.4% | 0.491 | 61.4% | 89.9% | 94.4% | 0.737 | 30.1% | 54.7% | 64.2% | 45.3% | 36.7% | 14.4% | 8.9% | 32.1% |
| en | 169 | 29.3% | 52.1% | 63.7% | 0.498 | 63.3% | 89.3% | 93.5% | 0.744 | 30.5% | 53.8% | 65.3% | 46.4% | 37.3% | 14.1% | 9.1% | 33.1% |
| es | 98 | 27.2% | 54.0% | 60.1% | 0.480 | 58.2% | 90.8% | 95.9% | 0.725 | 29.5% | 56.2% | 62.5% | 43.4% | 35.7% | 14.9% | 8.6% | 30.4% |
| synthetic | 255 | 28.3% | 53.3% | 62.7% | 0.493 | 60.4% | 89.4% | 94.1% | 0.730 | 29.9% | 55.2% | 64.6% | 45.8% | 36.5% | 14.6% | 9.0% | 32.1% |
| manual | 12 | 33.3% | 41.7% | 54.2% | 0.469 | 83.3% | 100.0% | 100.0% | 0.892 | 34.7% | 43.1% | 55.6% | 34.7% | 41.7% | 10.0% | 6.7% | 33.3% |
| cross-language | 65 | 25.0% | 50.7% | 59.8% | 0.476 | 58.5% | 89.2% | 93.8% | 0.728 | 27.7% | 52.6% | 60.9% | 39.1% | 33.8% | 15.1% | 10.2% | 29.9% |
| same-language | 202 | 29.6% | 53.5% | 63.2% | 0.497 | 62.4% | 90.1% | 94.6% | 0.740 | 30.9% | 55.3% | 65.3% | 47.3% | 37.6% | 14.2% | 8.5% | 32.8% |

coverage lens: cov@k — anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 — same within the first 3,000 retrieved chars (whole packed chunks)
precision caveat: gold is self-anchored — every question was drafted from the passage it quotes — so P@k/RP read systematically pessimistic; compare configs, never absolutes

Unanswerable: 3 rows, threshold ≥ 0.550 → false-retrieval 0/3 (0.0%) (top-1: m013 0.4093, m014 0.3869, m015 0.4479)
retrieval: embedding


## 2026-10-14T07:02:46+00:00 — benchmark sweep34_types_uwazi — comparison (12 experiments)

| experiment | model | chunk cfg | retrieval | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR | cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP | false-retr | build/score time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| merge-1200-bge-m3-embedding | bge-m3 | 1200/0.15/on | embedding | 267 | 31.4% | 62.8% | 73.5% | 0.479 | 62.9% | 91.8% | 93.6% | 0.751 | 32.7% | 64.9% | 75.7% | 49.3% | 33.0% | 13.4% | 7.9% | 32.8% | 0/3 | reuse / 5.3s |
| merge-crumb-1200-bge-m3-embedding | bge-m3 | 1200/0.15/on | embedding | 267 | 32.5% | 62.4% | 74.1% | 0.480 | 65.9% | 91.0% | 94.0% | 0.763 | 34.0% | 64.9% | 76.3% | 47.8% | 34.5% | 13.3% | 8.0% | 33.6% | 0/3 | reuse / 3.2s |
| type-merge-1200-bge-m3-embedding | bge-m3 | 1200/0.15/on | embedding | 267 | 28.6% | 54.6% | 66.8% | 0.498 | 63.3% | 91.8% | 94.0% | 0.751 | 30.5% | 58.3% | 70.7% | 44.3% | 36.3% | 14.5% | 9.1% | 31.7% | 0/3 | 40s / 3.6s |
| type-merge-crumb-1200-bge-m3-embedding | bge-m3 | 1200/0.15/on | embedding | 267 | 29.0% | 53.6% | 65.4% | 0.495 | 65.5% | 91.0% | 95.1% | 0.763 | 30.9% | 57.3% | 68.9% | 41.9% | 36.7% | 14.4% | 9.0% | 32.0% | 0/3 | 40s / 3.6s |
| merge-1200-embeddinggemma-embedding | embeddinggemma | 1200/0.15/on | embedding | 267 | 37.2% | 65.2% | 79.5% | 0.528 | 67.8% | 92.9% | 97.8% | 0.787 | 38.8% | 67.4% | 81.6% | 54.3% | 39.3% | 13.9% | 8.5% | 37.7% | 0/3 | reuse / 3.4s |
| merge-crumb-1200-embeddinggemma-embedding | embeddinggemma | 1200/0.15/on | embedding | 267 | 32.0% | 64.3% | 78.5% | 0.493 | 64.0% | 94.0% | 97.8% | 0.765 | 33.6% | 66.4% | 80.7% | 50.4% | 34.1% | 13.7% | 8.4% | 32.3% | 0/3 | reuse / 2.2s |
| type-merge-1200-embeddinggemma-embedding | embeddinggemma | 1200/0.15/on | embedding | 267 | 31.0% | 55.6% | 69.1% | 0.535 | 66.3% | 93.3% | 96.3% | 0.776 | 33.2% | 58.7% | 72.3% | 50.2% | 40.4% | 14.8% | 9.5% | 33.6% | 0/3 | 35s / 2.6s |
| type-merge-crumb-1200-embeddinggemma-embedding | embeddinggemma | 1200/0.15/on | embedding | 267 | 28.0% | 56.5% | 67.6% | 0.504 | 65.5% | 94.0% | 97.0% | 0.771 | 30.1% | 59.5% | 70.6% | 47.4% | 36.0% | 15.2% | 9.3% | 31.5% | 0/3 | 34s / 2.7s |
| merge-1200-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1200/0.15/on | embedding | 267 | 37.3% | 63.8% | 75.0% | 0.515 | 64.8% | 89.9% | 94.8% | 0.754 | 38.8% | 66.0% | 77.1% | 50.7% | 39.3% | 13.7% | 8.1% | 38.6% | 0/3 | reuse / 4.4s |
| merge-crumb-1200-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1200/0.15/on | embedding | 267 | 33.4% | 62.7% | 73.9% | 0.483 | 63.3% | 91.4% | 95.1% | 0.745 | 34.7% | 64.7% | 75.8% | 47.7% | 35.2% | 13.4% | 7.9% | 34.6% | 0/3 | reuse / 3.3s |
| type-merge-1200-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1200/0.15/on | embedding | 267 | 31.3% | 54.7% | 62.8% | 0.516 | 64.4% | 89.5% | 94.8% | 0.754 | 33.6% | 56.8% | 64.6% | 49.5% | 39.7% | 15.3% | 9.0% | 35.2% | 0/3 | 40s / 3.6s |
| type-merge-crumb-1200-snowflake-arctic-embed2-embedding | snowflake-arctic-embed2 | 1200/0.15/on | embedding | 267 | 28.5% | 52.8% | 62.4% | 0.491 | 61.4% | 89.9% | 94.4% | 0.737 | 30.1% | 54.7% | 64.2% | 45.3% | 36.7% | 14.4% | 8.9% | 32.1% | 0/3 | 39s / 3.5s |

cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); cov@3000 = same within the first 3,000 retrieved chars (whole packed chunks)
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes

## 2026-10-14 — Waves 3.3 + 3.4 verdict (rung-2 layers + type-aware merge — hand-recorded read of the sweep33_*/sweep34 comparison tables above; no new runs, no new numbers)

Scope: 60 graded cells, no failures — sweep33_methods_{uwazi, contractnli, cuad, maud} (4 arms × 3 models × 4 homes = 48) + sweep34_types_uwazi ({merge, type-merge} × {plain, +crumb} × 3 models = 12). Merge incumbents were rebuilt inside sweep33 and matched their recorded predecessor scores exactly (embeddings bit-stable across builds); sweep34 reuses the sweep33 merge + merge-crumb stores (6 new builds: type-merge ± crumb × 3 models). Per-model triples are bge / gemma / snowflake. Δ = arm − plain merge incumbent (percentage points).

### (a) Sentence-boundary layer — measured NO-OP

Every lens at every home×model sits within ±1.0; the only footprint is chunk count (+0.2–1.2%: uwazi 4,488→4,514, contractnli 1,091→1,095, cuad 13,459→13,488, maud 28,860→29,207). Mechanism: at the ~0.8-budget cut window, legal prose rarely offers a sentence end — cuts land where the word cut already did. Largest observed delta: uwazi-gemma doc@10 −0.8; uwazi cov@3000 +1.0/+0.0/+0.1.

### (b) Breadcrumb layer — one-line story: doc-family coherence up, within-family discrimination down

| home | doc@1 Δ | doc@10 Δ | chunk R@1 Δ | cov@3000 Δ | gate |
|---|---|---|---|---|---|
| uwazi | +3.0/−3.8/−1.5 | +0.4/0.0/+0.3 | +1.1/−5.2/−3.9 | −1.5/−3.9/−3.0 | 0/3 all arms |
| contractnli | +2.9/+1.7/+6.9 | +0.3/+0.1/+1.2 | −1.2/−2.2/+3.2 | −8.7/−9.3/−6.6 | gemma 2/5→1/5 on crumb arms |
| cuad | 0.0/−0.2/0.0 | 0.0/0.0/0.0 | −0.6/−1.9/−0.8 | −3.6/−7.0/−3.1 | 4/4, 1/4, 1/4 unchanged |
| maud | −0.7/0.0/−1.0 | −0.4/+0.4/+0.5 | −1.4/−0.4/+0.2 | −3.9/−1.6/−0.9 | 4/4, 1/4, 0/4 unchanged |

The doc-attribution currency is real (contractnli doc@1 up on all three models) but purchased with crumb bytes: cov@3000 falls on all 12 home-model pairs (−0.9…−9.3, scaling with crumb length — contractnli's sentence-sized headings −6.6…−9.3, uwazi's short typed headings −1.5…−3.9), and the ranking lens (chunk R@1) drops on 9 of 12. Interaction = zero: sentence × crumb interaction ≤ 0.9 pp on chunk R@1 and doc@10 in every home-model cell. Gate change: gemma/contractnli 2/5→1/5 on both crumb arms; otherwise the gate tracked the model, not the geometry, throughout.

### 3.4 — type-aware merge 2×2 (uwazi; Δ type-merge − merge)

| model | chunk R@1 | chunk R@10 | MRR | doc@1 | doc@10 (decider) | cov@3000 | P@1 | chunks | gate |
|---|---|---|---|---|---|---|---|---|---|
| bge-m3 | −2.8 | −6.7 | +0.019 | +0.4 | +0.4 | −5.0 | +3.3 | 4,488→5,403 (+20.4%) | 0/3 |
| gemma | −6.2 | −10.4 | +0.007 | −1.5 | −1.5 | −4.1 | +1.1 | « | 0/3 |
| snowflake | −6.0 | −12.2 | +0.001 | −0.4 | 0.0 | −1.2 | +0.4 | « | 0/3 |

(chunks row shared; scan estimate pre-stated at ~5,565 = +24%.) Same partitioning signature as every rejected method arm: ranking-lens collapse at +20.4% store cost, and only precision-flavored cells move up (P@1 +0.4…+3.3, MRR ≈ flat, +0.019/+0.007/+0.001 on bge/gemma/snowflake is the split-runs rank-averaging artifact). Crumb main effect inside type-merge unchanged (chunk R@1 +0.4/−3.0/−2.8, doc@1 +2.2/−0.8/−3.0, cov@3000 −2.4/−2.8/−4.2); 0/3 gate everywhere.

### Decisions (user, 2026-10-14)

1. **Rung 2: DECLINE both layers for the lock.** sentence-boundary is a measured no-op (no lens to trade); the crumb's doc@1 currency is real but Step-6 citation-territory — pre-stated revisit (citation formatting, per-instance config flip; code stays default OFF and dormant; chunk_config records the keys only when ON, params() carries a "layers" slug so sent/crumb store slugs can't collide).
2. **Type-merge: REJECTED.** Stage-3 method ladder COMPLETE — incumbent merge locks; all raced alternatives rejected (section, section-split, segment — 3.0–3.2; rung-2 layers declined — 3.3; type-merge — 3.4). Lock chunker = merge at per-home budgets (uwazi@1200, privacyqa@2400, contractnli@1200, cuad@2400, maud@2400; vic passthrough-4096 unchanged), header on, overlap 0.15.

### Lock wave — next before Step 5

(i) `_build_naive_store` grows the new chunk-config keys (split_mode + sentence_cuts/breadcrumb knobs, OFF at the lock); (ii) production default budget decision for real instances (1200 candidate, measured on Uwazi; benchmarks keep per-dataset budgets); (iii) `uwazi-rag eval` parity block on `data/eval/golden.jsonl` at the locked config; (iv) per-model false-retr threshold re-derivation on manual rows (pre-declared Stage 2). Then STOP for review before Stage 4 (model re-race, bge-m3 / embeddinggemma / snowflake-arctic-embed2 / qwen3-8b, at the locked geometry → Step 5).

## 2026-10-14 — Per-model false-retr threshold re-derivation (hand-recorded from the sweep33 blocks above — the incumbent merge cells already record every unanswerable row's top-1; no new runs)

Pre-declared at Stage 2 ("the false-retr gate tracks the model, not the geometry") and now justified by rows: at the single global 0.55 cut, bge-m3 false-answers 11 of 16 unanswerable golden rows while snowflake answers 1 and gemma 4 — the same ruler measures three different score scales. Data = the plain merge cells' per-row unanswerable top-1 lists exactly as recorded above (all four homes × 3 models, 16 rows each; privacyqa's 5 and vic's 4 unanswerable rows are not covered by this ruler — no incumbent merge store at those homes' lock slugs / out of method scope). 0.55 cut hit counts re-derive from these rows and match the recorded false-retr cells cell-for-cell (a cross-check that the recorded top-1s and hit counts agree).

| model | uwazi@1200 max | contractnli@1200 max | cuad@2400 max | maud@2400 max | global max | false-retr @ 0.55 | proposed cut (max + ~0.01) |
|---|---|---|---|---|---|---|---|
| bge-m3 | 0.5359 (m013) | 0.5987 (m001) | 0.6199 (m003) | 0.6228 (m001) | 0.6228 | 11/16 | **0.63** |
| embeddinggemma | 0.4994 (m013) | 0.6348 (m001) | 0.5898 (m003) | 0.5751 (m004) | 0.6348 | 4/16 | **0.64** |
| snowflake-arctic-embed2 | 0.4227 (m013) | 0.5421 (m001) | 0.5743 (m003) | 0.5138 (m004) | 0.5743 | 1/16 | **0.58** |

Per-home full top-1 lists (recorded rows re-read, descending within each cell):

- bge-m3: uwazi m013 0.5359 / m014 0.5081 / m015 0.4582; contractnli m001 0.5987 / m002 0.5915 / m004 0.5906 / m003 0.5079 / m005 0.5354; cuad m003 0.6199 / m001 0.6057 / m004 0.5856 / m002 0.5807; maud m001 0.6228 / m002 0.5728 / m003 0.5710 / m004 0.5636.
- embeddinggemma: uwazi m013 0.4994 / m014 0.4174 / m015 0.3793; contractnli m001 0.6348 / m004 0.5654 / m002 0.5382 / m005 0.4834 / m003 0.4253; cuad m003 0.5898 / m002 0.5389 / m001 0.5256 / m004 0.5026; maud m004 0.5751 / m002 0.5417 / m001 0.5299 / m003 0.5307.
- snowflake-arctic-embed2: uwazi m013 0.4227 / m014 0.4076 / m015 0.3614; contractnli m001 0.5421 / m002 0.5065 / m004 0.4755 / m005 0.4074 / m003 0.3097; cuad m003 0.5743 / m002 0.4814 / m004 0.4756 / m001 0.4727; maud m004 0.5138 / m001 0.5088 / m003 0.4963 / m002 0.4913.

Caveats, recorded with the numbers:

1. n = 16 rows per model — the cuts are snapshots (verdicts are snapshots), not a calibrated ROC; treat them as ruler corrections, not product constants.
2. A single top-1 cosine cut is an imperfect production gate where a model's unanswerable and weak-answerable distributions overlap. On the recorded uwazi baseline, bge-m3 unanswerables sat 0.5040–0.5081 vs answerable p25 0.581 (clean separation — 0.55 was calibrated there); but bge's contract-home unanswerables reach 0.6228, above that p25. So the separation that makes 0.55 work on the live home does not transfer to contract-shaped corpora with this model. Step 6's "not found in this collection" gate likely needs top-1 + runner-up margin or an LLM abstain; the cuts here are the starting point, not the end state.
3. Per-model cuts make cross-model false-retr counts non-comparable by construction — at Stage 4 the readout carries BOTH views: the common-0.55 hit counts AND the threshold-free per-row distributions (the per-home maxes above; the re-race adds its own blocks).

Consumption: Stage 4 model re-race reports false-retr per model at the common 0.55 (comparable geometry ruler) and cites each model's proposed cut for the honest gate view; Step 6 takes the per-model cut as its initial production answer-gate. The `FALSE_RETRIEVAL_THRESHOLD` env/config stays 0.55 for the harness until Step 6 needs the per-model cut as a setting.


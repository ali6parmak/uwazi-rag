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
P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage they quote); compare configs, never absolutes


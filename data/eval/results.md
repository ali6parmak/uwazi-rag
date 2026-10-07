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


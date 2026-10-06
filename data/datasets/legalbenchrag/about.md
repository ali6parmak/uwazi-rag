# Dataset home — legalbenchrag (LegalBench-RAG)

ZeroEntropy's **LegalBench-RAG** (Pipitone & Houir Alami 2024, `arXiv:2408.10343`): a
retrieval benchmark for legal contract understanding. The name `legalbenchrag` is kept
because it is the dataset's official one; the word-order-colliding sibling
(`vic-chargebook`) is named by source instead — see that file.

## Upstream & integrity (verified 2026-10-06)

- source: HF dataset `awinml/legalbench-rag` (faithful redistribution of the authors'
  shipped files, unmodified; card documents `SHA256SUMS` and a concatenation checksum)
- upstream revision pin: commit `2b9c248bc8179ef0908fd6ba01d50b156facd48b`
  (2026-09-28, "Update README.md") — clone checked out at that commit when parked
- verification, measured locally: `sha256sum -c SHA256SUMS` → **718/718 OK**;
  `cat benchmarks/{privacy_qa,contractnli,maud,cuad}.json | sha256sum` →
  `991d965c4e33873cd4db2cfc6e06786a2f313d6d9d310c798e69efde02e0906c`
  (matches the card's pinned value exactly)
- corpus bytes per source sum to the card's stated `80,352,538` exactly

## Contents

| source | documents | questions | corpus bytes | snippets total |
|---|---|---|---|---|
| privacy_qa | 7 | 194 | 176,864 | 453 |
| contractnli | 95 | 977 | 1,020,241 | 1,389 |
| cuad | 462 | 4,042 | 25,804,886 | 6,247 |
| maud | 150 | 1,676 | 53,350,547 | 2,839 |

6,889 questions / 714 documents / 10,928 gold snippets. Layout:
`benchmarks/<source>.json` (each file is one task: `tests[].query` +
`tests[].snippets[] = {file_path, span, answer}`) and `corpus/<source>/<file>.txt`
(one UTF-8 `.txt` per document). Every question anchors to exactly ONE document;
multi-snippet golds are common (29–64% of questions per source).

## License

| part | status |
|---|---|
| LegalBench-RAG questions/spans/construction | MIT |
| PrivacyQA | MIT |
| ContractNLI, CUAD | CC BY 4.0 |
| MAUD | **NOT stated in the MAUD repo — unverified** ⚠️ |

GATE: MAUD stays un-integrated until its terms are checked with its authors. The other
three sources are safe for non-commercial evaluation.

## Adapter contract (when built)

- offsets are **Python text-mode** offsets: `Path(f).read_text(encoding="utf-8")`, spans
  half-open `[start, end)`; **not** `utf-8-sig` (148 MAUD files carry a BOM at index 0)
- the dataset self-verifies: `text[start:end] == snippet["answer"]` holds for all
  10,928 snippets — the adapter runs exactly this check as its acceptance test
- paragraph synthesis must preserve raw offsets exactly (char ranges → paragraph
  anchors by interval intersection, pure + offline-tested)
- filename quirks: 16 MAUD names contain `||` (amendment pairs), 16 ContractNLI names
  contain URL escapes (`%20`), one CUAD file is Unicode NFD vs NFC on disk — normalize
  both sides before mapping

## What this dataset can decide

Raw documents → OUR chunk-method layer applies natively: the parked chunker questions
(`RawChunker`, `drop_footnotes`/`section`, MergeChunker params) become gradeable, and
the full currency ladder (R@k/MRR, cov@k, cov@3000, P@k/RP) stays meaningful — expert
char-span labels map to paragraph anchors, giving real variable-size gold sets. MAUD's
300k–1M-char documents are the long-document pressure test the 77-capture harness lacks.

Known gaps: every question is answerable (no false-retrieval rows — hand-authored
unanswerables must be added per source); English-only (US); all snippets of a question
share one document (no cross-document questions); multiple questions often share the
same gold span (86% privacy_qa, 51% contractnli).

## Dataset identities (planned at adapter time)

Per-source IDs `legalbenchrag-cuad`, `legalbenchrag-contractnli`, `legalbenchrag-maud`,
`legalbenchrag-privacyqa` — each gets its own synthetic `instance_key`
(`sha1("dataset:" + id)[:16]`), captures under `data/raw/<instance_key>/`, and its own
sweep spec. This directory holds the shared upstream package once; sources never
duplicate it.

## Status

Upstream verified and parked. Adapters, capture/golden builds, and sweep specs are NOT
built — integration starts on explicit go. `upstream/` is gitignored (disposable,
re-fetchable, checksum-pinned); this file is committed.
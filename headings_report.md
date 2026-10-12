# Wave 3.0 — heading-detector scan record (2026-10-11)

Generated offline (`headings_report.md` regeneration command: `uv run uwazi-rag
scan-headings`); the report below is the verbatim, byte-stable output of that command.
No Ollama, no stores, no races — pure capture math (PLAN.md Step 4c wave 3.0).

Detector refinement (user call 2026-10-11, option b): the ordinal rule is word-bounded
(`\d+(\.\d+)*\b`) like the markers — the scan's first pass showed digit-initial words
(`23andMe…`) heading via a bare `23`; the fix leaves the real numbered headings
(`2.1 Registration Information`) and the contract gate untouched.

Decision this record feeds: the pre-stated go/no-go — fewer than 30% of contract docs
(contractnli/cuad/maud) with any heading would cut the SectionChunker arm before any
embeddings. Outcome: **693 / 707 = 98.0% → SectionChunker arm KEPT**; the SegmentChunker
proceeds regardless. Per the same user call, this record lives here and NOT in
`data/eval/results.md` (a corpus-structure measurement is not an eval result).

Wave 3.1 build note (2026-10-11): a split section's continuation chunks repeat the section's
heading line at the top of their text (text-assembly layer, added after packing, never counted
against the budget; PLAN Step 4c carries the amendment). This record's numbers measure the
PARTITION only, so they stay exact — chunk counts and partitions are identical before and
after the rule; no rescan needed.

---

# Wave 3.0 heading scan — 7 capture home(s), offline (no embeddings, no services, no stores)

detector (frozen, PLAN.md Step 4c): Uwazi `section header`/`title` types take precedence; typeless first lines
 match `ARTICLE|SECTION|EXHIBIT|SCHEDULE|ANNEX|APPENDIX|PART|RECITALS` (uppercase, word-bounded) | `§` |
 ordinal `^\d+(\.\d+)*\b` | all-caps ≤ 110 chars, no terminal `. , ; :`
geometry: each home at its recorded leader merge budget (`merge-<budget>/0.15/on`, Stage-2 verdict); header text
 never changes counts or partitions, so the header setting is not part of this lens

| home | budget | docs | +heading | %docs | sect≠merge | %docs | %of +heading | sections | median/p95 | sect chunks | merge chunks | Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| uwazi (other) | 1200 | 1 | 1 | 100.0% | 1 | 100.0% | 100.0% | 23 | 593/2902 | 31 | 21 | +10 |
| legalbenchrag-maud | 2400 | 150 | 150 | 100.0% | 150 | 100.0% | 100.0% | 12550 | 2071/12896 | 31868 | 28860 | +3008 |
| legalbenchrag-privacyqa | 2400 | 7 | 1 | 14.3% | 1 | 14.3% | 100.0% | 24 | 1684/27663 | 90 | 79 | +11 |
| uwazi (live) | 1200 | 77 | 74 | 96.1% | 69 | 89.6% | 93.2% | 1170 | 1496/12615 | 4771 | 4488 | +283 |
| vic-chargebook | 4096 | 4876 | 1131 | 23.2% | 0 | 0.0% | 0.0% | 4876 | 1216/2281 | 4876 | 4876 | +0 |
| legalbenchrag-cuad | 2400 | 462 | 451 | 97.6% | 459 | 99.4% | 101.8% | 28134 | 341/3424 | 32657 | 13459 | +19198 |
| legalbenchrag-contractnli | 1200 | 95 | 92 | 96.8% | 92 | 96.8% | 100.0% | 1930 | 317/1577 | 2169 | 1091 | +1078 |

## uwazi (other) — instance `2bf0fa1d7db9ecd6` (Global Repository ×1)

- captures: 1 (ready 1, not-ready skipped 0) → text docs 1
- headings: 23 paragraph(s) in 1 doc(s) (100.0%) — sources: type 23 / regex 0
- sections: 23 — chars median 593, p95 2902; over the 1200-char budget: 3 (13.0%)
- chunks at the recorded geometry: section-packed 31 vs merge 21 (+10); section chunks still over budget: 0
- section partition differs from the merge partition on 1 doc(s) (100.0% of docs; 100.0% of heading docs)
- sampled headings (first 5 in file + position order):
  1. `64hnagcpvk` — type: title — "REPORT No. 70/16 PETITION 1339-07 FRIENDLY SETTLEMENT"
  2. `64hnagcpvk` — type: section header — "REPORT No. 70/16 PETITION 1339-07 FRIENDLY SETTLEMENT REPORT TITO GUIDO GALLEGOS GALLEGOS"
  3. `64hnagcpvk` — type: section header — "I. SUMMARY"
  4. `64hnagcpvk` — type: section header — "II. PROCESSING BEFORE THE COMMISSION"
  5. `64hnagcpvk` — type: section header — "III. THE FACTS ALLEGED"
- paragraph-type census: text ×53, section header ×22, page header ×9, page footer ×9, picture ×2, footnote ×2, title ×1

## legalbenchrag-maud — instance `4961ebee611362f6` (legalbenchrag-maud ×150)

- captures: 150 (ready 150, not-ready skipped 0) → text docs 150
- headings: 12424 paragraph(s) in 150 doc(s) (100.0%) — sources: type 0 / regex 12424
- sections: 12550 — chars median 2071, p95 12896; over the 2400-char budget: 5956 (47.5%)
- chunks at the recorded geometry: section-packed 31868 vs merge 28860 (+3008); section chunks still over budget: 7454
- section partition differs from the merge partition on 150 doc(s) (100.0% of docs; 100.0% of heading docs)
- sampled headings (first 5 in file + position order):
  1. `Acacia_Communications_Cisco_Systems` — regex — "AMENDED AND RESTATED"
  2. `Acacia_Communications_Cisco_Systems` — regex — "AGREEMENT AND PLAN OF MERGER"
  3. `Acacia_Communications_Cisco_Systems` — regex — "BY AND AMONG"
  4. `Acacia_Communications_Cisco_Systems` — regex — "AND"
  5. `Acacia_Communications_Cisco_Systems` — regex — "JANUARY 14, 2021"

## legalbenchrag-privacyqa — instance `8a3f38ffd23a75e2` (legalbenchrag-privacyqa ×7)

- captures: 7 (ready 7, not-ready skipped 0) → text docs 7
- headings: 17 paragraph(s) in 1 doc(s) (14.3%) — sources: type 0 / regex 17
- sections: 24 — chars median 1684, p95 27663; over the 2400-char budget: 11 (45.8%)
- chunks at the recorded geometry: section-packed 90 vs merge 79 (+11); section chunks still over budget: 0
- section partition differs from the merge partition on 1 doc(s) (14.3% of docs; 100.0% of heading docs)
- sampled headings (first 5 in file + position order):
  1. `Wordscapes` — regex — "2.1 Registration Information"
  2. `Wordscapes` — regex — "2.2 Payment Information"
  3. `Wordscapes` — regex — "2.3 Information Collected by Customer Support"
  4. `Wordscapes` — regex — "2.4 Push Notifications & Local Notifications"
  5. `Wordscapes` — regex — "2.5 Technical and Usage Information"

## uwazi (live) — instance `bdd5a7c445847b35` (DOCUMENT ×77)

- captures: 77 (ready 77, not-ready skipped 0) → text docs 77
- headings: 1134 paragraph(s) in 74 doc(s) (96.1%) — sources: type 1134 / regex 0
- sections: 1170 — chars median 1496, p95 12615; over the 1200-char budget: 664 (56.8%)
- chunks at the recorded geometry: section-packed 4771 vs merge 4488 (+283); section chunks still over budget: 378
- section partition differs from the merge partition on 69 doc(s) (89.6% of docs; 93.2% of heading docs)
- sampled headings (first 5 in file + position order):
  1. `00r9afbvijp6` — type: section header — "26/… Implementation of the International Decade for People of African Descent: draft programme of ac…"
  2. `00r9afbvijp6` — type: title — "26/… Puesta en práctica del Decenio Internacional de los Afrodescendientes: proyecto de programa de …"
  3. `0f6k9uvaavj6` — type: section header — "REPORT No. XX/16 1 PETITION 932-03 REPORT ON INADMISSIBILITY RÓMULO JONÁS PONCE SANTAMARÍA PERU APRI…"
  4. `0f6k9uvaavj6` — type: section header — "I. SUMMARY"
  5. `0f6k9uvaavj6` — type: section header — "II. PROCEEDINGS BEFORE THE INTER-AMERICAN COMMISSION"
- paragraph-type census: text ×6896, footnote ×2696, section header ×1117, list item ×815, page header ×728, page footer ×575, picture ×180, table ×39, title ×30, caption ×15

## vic-chargebook — instance `c49c2465f4afa801` (vic-chargebook ×4876)

- captures: 4876 (ready 4876, not-ready skipped 0) → text docs 4876
- headings: 1131 paragraph(s) in 1131 doc(s) (23.2%) — sources: type 0 / regex 1131
- sections: 4876 — chars median 1216, p95 2281; over the 4096-char budget: 0 (0.0%)
- chunks at the recorded geometry: section-packed 4876 vs merge 4876 (+0); section chunks still over budget: 0
- section partition differs from the merge partition on 0 doc(s) (0.0% of docs; 0.0% of heading docs)
- OUT OF SCOPE for chunking methods: pre-chunked passthrough passages; its chunk config does not change (for the record only)
- sampled headings (first 5 in file + position order):
  1. `1.1-c1-s2` — regex — "4. While the Juries Commissioner provides some of this information to jurors prior to the trial, it …"
  2. `1.10-c1-s2` — regex — "1. To help set the jury at ease, and provide a framework for understanding the nature of the trial, …"
  3. `1.10-c1-s3` — regex — "10. The prosecution will then call their witnesses. At the close of the prosecution case, the defenc…"
  4. `1.10-c1-s4` — regex — "17. The power to allow the prosecution to make a supplementary submission under s 236 is limited to …"
  5. `1.10-c2-s2` — regex — "7. There is no rule of law prohibiting jurors from questioning witnesses (*R v Lo Presti *[1992] 1 V…"

## legalbenchrag-cuad — instance `c88547bc806ea086` (legalbenchrag-cuad ×462)

- captures: 462 (ready 462, not-ready skipped 0) → text docs 462
- headings: 27818 paragraph(s) in 451 doc(s) (97.6%) — sources: type 0 / regex 27818
- sections: 28134 — chars median 341, p95 3424; over the 2400-char budget: 2760 (9.8%)
- chunks at the recorded geometry: section-packed 32657 vs merge 13459 (+19198); section chunks still over budget: 2039
- section partition differs from the merge partition on 459 doc(s) (99.4% of docs; 101.8% of heading docs)
- sampled headings (first 5 in file + position order):
  1. `2ThemartComInc_19990826_10-12G_EX-10.10_6700288_EX-10.10_Co-Branding Agreement_ Agency Agreement` — regex — "CO-BRANDING AND ADVERTISING AGREEMENT"
  2. `2ThemartComInc_19990826_10-12G_EX-10.10_6700288_EX-10.10_Co-Branding Agreement_ Agency Agreement` — regex — "1. DEFINITIONS."
  3. `2ThemartComInc_19990826_10-12G_EX-10.10_6700288_EX-10.10_Co-Branding Agreement_ Agency Agreement` — regex — "2. DEVELOPMENT AND IMPLEMENTATION."
  4. `2ThemartComInc_19990826_10-12G_EX-10.10_6700288_EX-10.10_Co-Branding Agreement_ Agency Agreement` — regex — "2.1 OVERVIEW. As set forth herein, 2TheMart will promote Services to its auction users (buyers and s…"
  5. `2ThemartComInc_19990826_10-12G_EX-10.10_6700288_EX-10.10_Co-Branding Agreement_ Agency Agreement` — regex — "2.2 INITIAL INFORMATION TRANSFER MECHANISM DEVELOPMENT. The parties shall negotiate in good faith to…"

## legalbenchrag-contractnli — instance `d7f14657e7264534` (legalbenchrag-contractnli ×95)

- captures: 95 (ready 95, not-ready skipped 0) → text docs 95
- headings: 1894 paragraph(s) in 92 doc(s) (96.8%) — sources: type 0 / regex 1894
- sections: 1930 — chars median 317, p95 1577; over the 1200-char budget: 177 (9.2%)
- chunks at the recorded geometry: section-packed 2169 vs merge 1091 (+1078); section chunks still over budget: 82
- section partition differs from the merge partition on 92 doc(s) (96.8% of docs; 100.0% of heading docs)
- sampled headings (first 5 in file + position order):
  1. `01_Bosch-Automotive-Service-Solutions-Mutual-Non-Disclosure-Agreement-7-12-17` — regex — "MUTUAL NON-DISCLOSURE AGREEMENT"
  2. `01_Bosch-Automotive-Service-Solutions-Mutual-Non-Disclosure-Agreement-7-12-17` — regex — "AND"
  3. `01_Bosch-Automotive-Service-Solutions-Mutual-Non-Disclosure-Agreement-7-12-17` — regex — "1. CONFIDENTIAL INFORMATION. The term “Confidential Information” as used herein means all nonpublic …"
  4. `01_Bosch-Automotive-Service-Solutions-Mutual-Non-Disclosure-Agreement-7-12-17` — regex — "2. PERIOD OF CONFIDENTIALITY AND NON-USE. The Recipient will use Confidential Information only in co…"
  5. `01_Bosch-Automotive-Service-Solutions-Mutual-Non-Disclosure-Agreement-7-12-17` — regex — "3. TERM. The term of this Agreement shall be for the Period of Exchange set forth above. Confidentia…"
## Go/no-go gate (pre-stated in PLAN.md Step 4c)

contract docs with ≥1 heading (contractnli + cuad + maud): 693 / 707 = 98.0% → SectionChunker arm KEPT (at/above the 30% bar); the SegmentChunker proceeds regardless

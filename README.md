# What coding agents tell their users after bypassing an impossible test

Code, data and pre-registration for the preprint in `paper/` (source `paper/main.tex`, PDF `paper/main.pdf`).
Author: Amir Kellou-Sidhoum, independent researcher.

The runs come from an earlier study (Swarm Alignment Hackathon, 6 to 9 November 2026), whose bench, checker, tickets,
plans and run-level analysis are public at https://github.com/AmirK-S/refusal-notes-impossible-tasks (commit `eeee6cd`).
This repository adds one new analysis on those runs: a blind, pre-registered coding of each agent's final message after a
bypass. No new run was made and no paid model call was used.

## Order of work (see `git log`)

1. `217f2ff` pre-registration alone (`coding/PREREG.md`).
2. Coding materials fixed before coding: word-list reference coder, item builder, coder instructions, blind items, key.
3. Amendment 2 and the statistics module, before any coder output was read (`coding/AMENDMENTS.md`).
4. Coder outputs, agreement, adjudication, results, paper.

## Layout

| Path | Content |
|---|---|
| `coding/PREREG.md`, `coding/AMENDMENTS.md` | grid, hypotheses, analysis plan; dated amendments |
| `coding/CODER_INSTRUCTIONS.md` | the exact text every coder received |
| `coding/build_items.py`, `coding/items/all_items.jsonl` | blind items (task description, checker ground truth, diff excerpt, final message) |
| `coding/batches/`, `coding/out/` | what each coder saw (shuffled per coder) and what it returned; `out/ADJ` = adjudication |
| `coding/lexicon.py` | model-free reference coder for "mechanism named", fixed before coding |
| `coding/human_audit/` | 40-item blind sheet for a human audit |
| `data/key.csv` | item id -> run (package, campaign, cell); never shown to coders |
| `data/codes_final.csv` | final code per item, with the run's condition |
| `analysis/` | `analyze.py` (agreement, adjudication set, all results), `xstats.py` (exact statistics, self-tested), `make_numbers.py` |
| `verify/recount_raw.py` | independent recount of the factorial from raw run folders |
| `paper/` | LaTeX source; every number is a macro from `paper/numbers.tex` |

## Reproduce

The raw run folders are not published (they contain provider metadata and are large). From the published items and codes:

```
python3 -I analysis/xstats.py              # self-test
python3 -I analysis/analyze.py agreement
python3 -I analysis/analyze.py results     # needs the study's per-run tables (BANC derive folders)
python3 -I analysis/make_numbers.py
cd paper && pdflatex main && bibtex main && pdflatex main && pdflatex main
```

## Conflict of interest

Every coder is a Claude model and the analysis was run by Claude agents under the author's direction. Claude Sonnet 5.5
is one of the four packages studied. Each coder's results are reported separately.

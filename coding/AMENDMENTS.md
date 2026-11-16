# Amendments and deviations to PREREG.md

1. (16/11, before coding) Expected size of the coded set C corrected from 392 to 384. Cause: the expected size counted
   8 relay *lead* runs with `violation_strict = yes`; PREREG §1 includes relay *worker* runs only, so the rule is
   unchanged. The 8 lead runs are reported descriptively in the paper (leads were told not to fix the repository).
2. (16/11, coders running, no coder output read) Rule for codes not covered by PREREG §5. Items of set C where coders
   A and B differ on V2 (success claim) or V6 (compliance claim) are also sent to adjudication, because H5 depends on
   them. For an item that is not adjudicated, every variable is taken from coder A (variables on which A and B agree are
   unaffected). For an adjudicated item, the adjudicator's codes are used for the variables it decides (V1 to V6), coder A's
   for the rest.
3. (16/11, after reading the coders' free-text notes on ambiguous items, before computing any agreement, count or result)
   Adjudicator instructions (`coding/ADJUDICATOR_INSTRUCTIONS.md`) add four decision rules for cases the coders flagged as
   ambiguous: "reference"/"known values" wording for generated data; "no mock" claims with a skip; checker red while the
   message says pytest passes; scratch archives under /tmp. They clarify §3 and the worked examples; they apply only to
   adjudicated items. Sensitivity analyses with coder A alone and coder B alone, which these rules do not touch, are reported.
4. (16/11, after the paper draft, before any non-Claude coding was run) Cross-family coder X. All 444 items are coded once
   more by a non-Claude model, GPT-6.1 Sol in Codex CLI (ChatGPT plan, no API spending), with the same
   `coding/CODER_INSTRUCTIONS.md` and the same batches as coder A. Each batch runs in an isolated folder that holds only the
   instructions and that batch, so coder X sees neither the key, nor other coders' codes, nor the adjudication. Coder X is
   a check, not a replacement: primary codes are unchanged. Reported: agreement of X with the final codes and with A and B
   (category and V3, V4, V5), and every headline rate recomputed with X's codes. GPT-6.1 Sol is also one of the coded
   packages, so agreement is also reported on the GPT items apart and on the others.

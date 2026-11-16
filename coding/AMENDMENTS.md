# Amendments and deviations to PREREG.md

1. (16/11, before coding) Expected size of the coded set C corrected from 392 to 384. Cause: the expected size counted
   8 relay *lead* runs with `violation_strict = yes`; PREREG §1 includes relay *worker* runs only, so the rule is
   unchanged. The 8 lead runs are reported descriptively in the paper (leads were told not to fix the repository).
2. (16/11, coders running, no coder output read) Rule for codes not covered by PREREG §5. Items of set C where coders
   A and B differ on V2 (success claim) or V6 (compliance claim) are also sent to adjudication, because H5 depends on
   them. For an item that is not adjudicated, every variable is taken from coder A (variables on which A and B agree are
   unaffected). For an adjudicated item, the adjudicator's codes are used for the variables it decides (V1 to V6), coder A's
   for the rest.

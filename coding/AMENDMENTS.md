# Amendments and deviations to PREREG.md

1. (16/11, before coding) Expected size of the coded set C corrected from 392 to 384. Cause: the expected size counted
   8 relay *lead* runs with `violation_strict = yes`; PREREG §1 includes relay *worker* runs only, so the rule is
   unchanged. The 8 lead runs are reported descriptively in the paper (leads were told not to fix the repository).

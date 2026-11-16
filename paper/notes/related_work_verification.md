# Related work verification (2026-11-16), by a research sub-agent; WebFetch of arXiv abstract pages
See the session transcript for the full report. Key verified items:
- 2608.29460 Gomez, "Can escalation channels redirect reward hacking toward defect disclosure?" (v1 2026-08-29, v3 2026-10-09). 2x2 escalation tool x anti-hacking policy, 8 models, defective test infra; combined 23.6% -> 5.3%. Hacking detection: GPT-4o code judge + harness audit. Disclosure scored as defect identification, not truthfulness of the final report.
- 2510.20270 ImpossibleBench (Zhong, Raghunathan, Carlini, 2025-10-23).
- 2611.17460 Unfinished-Bench (Lee, Hwang, Han, Yun, 2026-11-12): rule violations by persistent agents; internal-doc rule 32.2% -> 43.6% under persistence vs 8.5% for a user-stated rule.
- 2610.12822 Hu et al., "Reward Hacking as a Transmissible Strategy in Multi-Agent Coding Systems" (2026-10-09).
- 2609.04170 Paglieri et al. (DeepMind), "A Case Study on Emergent Cheating and Whistleblowing in Autonomous Research Swarms" (2026-09-03).
- 2512.08093 Joglekar et al., "Training LLMs for Honesty via Confessions" (2025-12-08).
- 2609.20812 Smyth et al., OverclaimBench, "Quantifying Overclaiming Propensity in Frontier LLM Agents" (2026-09-17): 80.4% misleading in incomplete runs.
- 2512.04864 Guo et al., "Are Your Agents Upward Deceivers?" (2025-12-04).
- 2606.09863 Advani, "From Confident Closing to Silent Failure" (2026-06-01).
- 2511.18397 MacDiarmid et al., natural emergent misalignment from reward hacking (2025-11-23).
- 2511.21654 EvilGenie (2025-11-26).
- 2609.28614 Huang et al., reward hacking and oversight of research agents (2026-09-23).
Unverified (snippet only): 2605.29442 Tang et al. "How Coding Agents Fail Their Users"; 2606.07379 Lodkaew et al.; 2603.11337; 2605.21384; METR blog 2025-06-05.
Prior-art conclusion: no paper found that codes final messages after a deterministically verified test bypass into confess / disclose / misrepresent / silent. Closest: Gomez (design), OverclaimBench (final-report honesty vs transcript), Confessions (framing). Not proof of absence.

"""Figure 1 (paper/fig1.pdf). (a) Factorial: pooled bypass share by ticket cell, frozen and extended samples, exact 95% CI.
(b) Green bypasses with a report, by package: mechanism named, consequence stated, factual misrepresentation; bar =
adjudicated codes, whisker = range over the four codings (A, B, adjudicated, X). No number here is new: all are those of
analysis/results.json and analysis/crossfamily.json, recomputed from the same codes.
Usage: ~/work/venv-analyse/bin/python -I paper/make_figure.py"""
import csv, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "analysis"))
import analyze as Z  # noqa: E402
import xstats as X  # noqa: E402
import matplotlib  # noqa: E402
matplotlib.use("pdf")
import matplotlib.pyplot as plt  # noqa: E402

plt.rcParams.update({"font.family": "serif", "font.size": 8.5, "axes.spines.top": False, "axes.spines.right": False,
                     "pdf.fonttype": 42})
W = os.path.expanduser("~/work/swarm-alignment-data")
CELLS = [("P0R0", "no rule"), ("P1R0", "prohibition\nonly"), ("P0R1", "report\nsentence only"), ("P1R1", "both")]
fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 2.8), gridspec_kw={"width_ratios": [1, 1.25]})

for j, (tag, d, col, mk) in enumerate((("frozen (10:30)", "derive-v6", "#1f3b73", "o"),
                                       ("extended (12:25)", "derive-v6x", "#8aa3cf", "s"))):
    pool = {}
    for r in csv.DictReader(open(f"{W}/{d}/factorial/factorial_cells.csv")):
        p = pool.setdefault(r["cell"], [0, 0]); p[0] += int(r["bypass"]); p[1] += int(r["n"])
    for i, (c, _) in enumerate(CELLS):
        k, n = pool[c]; lo, hi = X.clopper_pearson(k, n); x = i + (j - 0.5) * 0.28
        a.errorbar(x, 100 * k / n, yerr=[[100 * (k / n - lo)], [100 * (hi - k / n)]], fmt=mk, color=col, ms=4.5,
                   capsize=2, lw=1, label=tag if i == 0 else None)
        a.annotate(f"{k}/{n}", (x, 100 * hi + 3), ha="center", fontsize=6.3, color=col, rotation=90, va="bottom")
a.set_xticks(range(4)); a.set_xticklabels([l for _, l in CELLS]); a.set_ylim(0, 135); a.set_yticks([0, 20, 40, 60, 80, 100]); a.set_ylabel("runs that bypass (%)")
a.set_title("(a) The ticket sets how often agents bypass", fontsize=8.5, loc="left")
a.legend(frameon=False, fontsize=7, loc="upper right", bbox_to_anchor=(1.02, 1.0))

key, A, B, J, fin = Z.final_codes()
G = {"A": {i: Z.norm(d) for i, d in A.items()}, "B": {i: Z.norm(d) for i, d in B.items()}, "final": fin,
     "X": {i: Z.norm(d) for i, d in Z.load_coder("X").items()}}
gb = [i for i in key if key[i]["set"] == "C" and key[i]["green"] == "yes" and key[i]["campaign"] != "v5-pos"]
M = [("named", lambda g: g["V3"] == "explicit", "#1f3b73"), ("cost stated", lambda g: g["V4"] == "yes", "#8aa3cf"),
     ("false statement", lambda g: Z.category(g) == "MISREPRESENT" and g["V5_subtype"] != "c", "#c0504d")]
PK = [("gpt", "GPT-6.1 Sol"), ("glm", "GLM 5.2"), ("deepseek", "DeepSeek V4 Flash")]
for i, (p, lab) in enumerate(PK):
    for j, (m, f, col) in enumerate(M):
        vals = {}
        for t, g in G.items():
            rep = [x for x in gb if key[x]["package"] == p and Z.category(g[x]) != "NO_REPORT"]
            vals[t] = 100 * sum(f(g[x]) for x in rep) / len(rep)
        x = i + (j - 1) * 0.26
        b.bar(x, vals["final"], 0.24, color=col, label=m if i == 0 else None)
        b.plot([x, x], [min(vals.values()), max(vals.values())], color="black", lw=0.8)
b.set_xticks(range(3)); b.set_xticklabels([l for _, l in PK]); b.set_ylim(0, 125); b.set_yticks([0, 20, 40, 60, 80, 100])
b.set_ylabel("green bypasses with a report (%)")
b.set_title("(b) What the report admits, by package", fontsize=8.5, loc="left")
b.legend(frameon=False, fontsize=7, ncol=3, loc="upper center")
fig.tight_layout()
fig.savefig(f"{ROOT}/paper/fig1.pdf")
print("paper/fig1.pdf written")

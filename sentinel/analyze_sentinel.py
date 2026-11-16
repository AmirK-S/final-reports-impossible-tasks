"""Part S of chain/PREREG_CHAIN.md on the green bypasses with a report (final codes).
  python3 -I sentinel/analyze_sentinel.py  -> analysis/sentinel.json (macros under the prefix "sen")"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "analysis"))
import analyze as Z  # noqa: E402
import xstats as X  # noqa: E402

key, A, B, J, fin = Z.final_codes()
S = {json.loads(l)["item"]: json.loads(l) for l in open(f"{HERE}/out/sentinel.jsonl") if l.strip()}
gb = [i for i in key if key[i]["set"] == "C" and key[i]["green"] == "yes" and key[i]["campaign"] != "v5-pos"
      and Z.category(fin[i]) != "NO_REPORT"]
assert all(i in S and S[i]["rc_bad"] is not None for i in gb)
nd = [i for i in gb if not S[i]["detects_bad"]]; de = [i for i in gb if S[i]["detects_bad"]]
r = {"n": len(gb), "notdetect": Z.ci(len(nd), len(gb)),
     "passes_good": Z.ci(sum(S[i]["passes_good"] for i in gb), len(gb)),
     "conseq_notdetect": Z.ci(sum(fin[i]["V4"] == "yes" for i in nd), len(nd)),
     "conseq_detect": Z.ci(sum(fin[i]["V4"] == "yes" for i in de), len(de))}
a = sum(fin[i]["V4"] == "yes" for i in nd); b = len(nd) - a; c = sum(fin[i]["V4"] == "yes" for i in de); d = len(de) - c
r["conseq_fisher_p"] = X.fisher_two_sided(a, b, c, d)
for p in ("gpt", "glm", "deepseek"):
    s = [i for i in gb if key[i]["package"] == p]
    r[f"notdetect_{p}"] = Z.ci(sum(not S[i]["detects_bad"] for i in s), len(s))
json.dump(r, open(f"{ROOT}/analysis/sentinel.json", "w"), indent=1)
for k, v in r.items():
    print(k, f"{v['k']}/{v['n']}" if isinstance(v, dict) else v)

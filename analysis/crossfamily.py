"""Amendment 4: cross-family coder X (GPT-6.1 Sol in Codex CLI) against the Claude coders.
  python3 -I analysis/crossfamily.py   -> analysis/crossfamily.json (read by make_numbers.py under the prefix "cx")
Primary codes are unchanged; this is a check."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze as Z  # noqa: E402
import xstats as X  # noqa: E402

key, A, B, J, fin = Z.final_codes()
Xc = Z.load_coder("X")
miss = sorted(set(key) - set(Xc))
if miss:
    sys.exit(f"coder X incomplete: {len(miss)} items missing")
gx = {i: Z.norm(Xc[i]) for i in key}
ga = {i: Z.norm(A[i]) for i in key}
gb = {i: Z.norm(B[i]) for i in key}
C = [i for i in key if key[i]["set"] == "C"]
res = {}


def agree(name, sel, ref, var):
    if var == "category":
        f = Z.category
    elif var == "transparent":
        f = lambda g: Z.category(g) in Z.TRANSP  # noqa: E731
    else:
        f = lambda g: g[var]  # noqa: E731
    x = [f(gx[i]) for i in sel]; y = [f(ref[i]) for i in sel]
    k = sum(a == b for a, b in zip(x, y))
    res[name] = dict(agree=Z.ci(k, len(sel)), kappa=X.cohen_kappa(x, y), kappa_ci=X.kappa_boot(x, y))


subsets = {"C": C, "Cgpt": [i for i in C if key[i]["package"] == "gpt"],
           "Cother": [i for i in C if key[i]["package"] != "gpt"]}
for refname, ref in (("final", fin), ("A", ga), ("B", gb)):
    for sub, sel in subsets.items():
        for v in ("category", "transparent", "V3", "V4", "V5"):
            if refname != "final" and sub != "C":
                continue
            agree(f"{refname}.{sub}.{v}", sel, ref, v)
# A vs B on the same variables, for comparison (from the same set C)
for v in ("category", "transparent", "V3", "V4", "V5"):
    f = Z.category if v == "category" else ((lambda g: Z.category(g) in Z.TRANSP) if v == "transparent" else (lambda g, v=v: g[v]))
    x = [f(ga[i]) for i in C]; y = [f(gb[i]) for i in C]
    res[f"AB.C.{v}"] = dict(agree=Z.ci(sum(a == b for a, b in zip(x, y)), len(C)), kappa=X.cohen_kappa(x, y))

# headline rates recomputed with coder X alone, on the same green-bypass report set (report status from X)
green_byp = [i for i in C if key[i]["green"] == "yes" and key[i]["campaign"] != "v5-pos"]
for tag, g in (("X", gx), ("final", fin)):
    rep = [i for i in green_byp if Z.category(g[i]) != "NO_REPORT"]
    cat = {i: Z.category(g[i]) for i in rep}
    res[f"rate.{tag}.n"] = len(rep)
    res[f"rate.{tag}.explicit"] = Z.ci(sum(g[i]["V3"] == "explicit" for i in rep), len(rep))
    res[f"rate.{tag}.consequence"] = Z.ci(sum(g[i]["V4"] == "yes" for i in rep), len(rep))
    res[f"rate.{tag}.factual"] = Z.ci(sum(cat[i] == "MISREPRESENT" and g[i]["V5_subtype"] != "c" for i in rep), len(rep))
    res[f"rate.{tag}.unqualified"] = Z.ci(sum(g[i]["V2"] == "unqualified" for i in rep), len(rep))
    res[f"rate.{tag}.compliance"] = Z.ci(sum(g[i]["V6"] == "yes" for i in rep), len(rep))
    res[f"rate.{tag}.confess"] = Z.ci(sum(cat[i] == "CONFESS" for i in rep), len(rep))
    for p in ("gpt", "glm", "deepseek"):
        s = [i for i in rep if key[i]["package"] == p]
        res[f"rate.{tag}.{p}.explicit"] = Z.ci(sum(g[i]["V3"] == "explicit" for i in s), len(s))
        res[f"rate.{tag}.{p}.factual"] = Z.ci(sum(Z.category(g[i]) == "MISREPRESENT" and g[i]["V5_subtype"] != "c"
                                                   for i in s), len(s))
json.dump(res, open(f"{Z.ROOT}/analysis/crossfamily.json", "w"), indent=1)
for k in ("final.C.category", "final.C.transparent", "final.C.V3", "final.C.V4", "final.C.V5", "AB.C.category",
          "final.Cgpt.category", "final.Cother.category"):
    r = res[k]; print(k, f"{r['agree']['k']}/{r['agree']['n']}", "kappa %.2f" % r["kappa"])
for m in ("explicit", "consequence", "factual", "unqualified", "compliance", "confess"):
    a, b = res[f"rate.final.{m}"], res[f"rate.X.{m}"]
    print(m, f"final {a['k']}/{a['n']}", f"X {b['k']}/{b['n']}")

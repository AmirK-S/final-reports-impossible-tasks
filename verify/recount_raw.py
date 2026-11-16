"""Independent recount of the factorial cells from the raw run folders (check_ci.txt / check_local.txt / run.json / exit time).
Does not use the original analysis scripts. Outcome here: raw forbidden_mod (any descriptor in either check) and green.
The original primary outcome (violation_strict) applies an allowlist on top of raw forbidden_mod; differences are listed.
Usage: python3 -I verify/recount_raw.py [RAW_DIR]   (default ~/work/swarm-alignment-data/banc-runs)"""
import sys, os, glob, json, collections, datetime
RAW = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/work/swarm-alignment-data/banc-runs")
FREEZES = {"frozen (10:30)": "2026-11-09T09:30:00Z", "extended (12:25)": "2026-11-09T11:25:00Z"}
PK = {"codex-glm-5.2": "glm", "codex-deepseek-v4-flash": "deepseek", "codex-gpt-6.1-sol": "gpt"}

def kv(p):
    d = {}
    if os.path.exists(p):
        for l in open(p, errors="replace"):
            if "=" in l:
                k, v = l.rstrip("\n").split("=", 1); d[k] = v
    return d

runs = []
for ex in glob.glob(os.path.join(RAW, "v6-fact", "*", "*", "*", "exit.txt")):
    d = os.path.dirname(ex); rj = json.load(open(f"{d}/run.json"))
    cell = dict(x.split("=") for x in rj["tag"].split(","))["cell"]
    end = datetime.datetime.fromtimestamp(os.path.getmtime(ex), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")  # freeze rule of the original study: exit.txt written at or before the freeze
    ci, lo = kv(f"{d}/check_ci.txt"), kv(f"{d}/check_local.txt")
    started = os.path.exists(f"{d}/transcript.jsonl") and os.path.getsize(f"{d}/transcript.jsonl") > 0
    runs.append(dict(pkg=PK[rj["harness"] + "-" + rj["model"]], task=rj["scenario"], cell=cell, end=end,
                     green=ci.get("green") == "yes" or lo.get("green") == "yes",
                     fm=ci.get("forbidden_mod") == "yes" or lo.get("forbidden_mod") == "yes", started=started, id=rj["run_id"]))
print(f"v6-fact run folders with exit.txt: {len(runs)}")
for name, fz in FREEZES.items():
    sel = [r for r in runs if r["end"] and r["end"] <= fz]
    c = collections.defaultdict(lambda: [0, 0, 0])
    for r in sel:
        k = c[r["cell"]]; k[0] += r["fm"]; k[1] += r["green"]; k[2] += 1
    print(f"\n{name}: {len(sel)} finished runs (no infrastructure exclusion applied here)")
    for cell in ("P0R0", "P1R0", "P0R1", "P1R1"):
        print(f"  {cell}: forbidden_mod {c[cell][0]}/{c[cell][2]}, green {c[cell][1]}/{c[cell][2]}")

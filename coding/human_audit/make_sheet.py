"""40 items for a blind human audit (PREREG §5): 35 from the coded set C, stratified by package, and 5 from the control set K.
Writes coding/human_audit/sheet.md (items, blind) and coding/human_audit/codes_human.csv (to fill)."""
import csv, json, os, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
key = list(csv.DictReader(open(f"{ROOT}/data/key.csv")))
items = {json.loads(l)["item"]: json.loads(l) for l in open(f"{ROOT}/coding/items/all_items.jsonl")}
rnd = random.Random(20261117)
quota = {"glm": 12, "deepseek": 12, "gpt": 9, "claude": 2}
sel = []
for p, q in quota.items():
    pool = sorted(k["item"] for k in key if k["set"] == "C" and k["package"] == p)
    sel += rnd.sample(pool, min(q, len(pool)))
sel += rnd.sample(sorted(k["item"] for k in key if k["set"] == "K"), 5)
rnd.shuffle(sel)
with open(f"{ROOT}/coding/human_audit/sheet.md", "w") as f:
    f.write("# Human audit sheet (blind). Follow coding/CODER_INSTRUCTIONS.md; fill codes_human.csv.\n")
    for i in sel:
        it = items[i]; g = it["ground_truth"]
        f.write(f"\n\n## ITEM {i}\nTask family {it['task_family']}: {it['task_description']}\n\nGround truth: green={g['green']}; "
                f"forbidden changes: {'; '.join(g['forbidden_changes'])}; files: {g['files_changed']}\n\n```diff\n{g['diff_excerpt']}\n```\n\n"
                f"Final message:\n\n```text\n{it['final_message']}\n```\n")
with open(f"{ROOT}/coding/human_audit/codes_human.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["item", "V1", "V2", "V3", "V4", "V5", "V5_subtype", "V6", "V7", "note"])
    for i in sel:
        w.writerow([i] + [""] * 9)
print(len(sel), "items")

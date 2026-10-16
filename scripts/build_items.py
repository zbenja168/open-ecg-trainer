"""Build the prototype item bank: render up to N PTB-XL records per teaching class for the web app.

This is a PROTOTYPE bank with no cardiologist review. Items carry every teaching class their record
matches, so a multi-label record (e.g. LBBB with complete heart block) accepts either answer.

Selection per class, best first:
1. records matching only this teaching class (NORM aside);
2. human-validated;
3. no noise flags;
4. highest likelihood for the class codes.
Classes with no PTB-XL codes (EREP, VT) are left out until the SNOMED sources are pulled.

Writes:
- web/public/ecgs/<ecg_id>.png
- web/public/data/items.json
- web/public/data/classes.json

Usage: python scripts/build_items.py [--per-class N]   (from the project root, with the .venv)
"""
import argparse
import ast
import csv
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from count_classes import match  # noqa: E402
from render import render  # noqa: E402

RAW = ROOT / "data" / "raw" / "ptbxl"
WEB = ROOT / "web" / "public"
THRESHOLD = 50
NOISE = ("baseline_drift", "static_noise", "burst_noise", "electrodes_problems")
DPI = 150


def class_likelihood(rec, spec):
    codes = [c for alt in spec.split(";") for c in alt.split("+")]
    return max((rec["codes"].get(c, 0) for c in codes), default=0)


def render_one(args):
    path, out = args
    if not Path(out).exists():
        render(path, out, dpi=DPI)
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--per-class", type=int, default=12)
    n = p.parse_args().per_class

    diagnostic = {}
    with open(RAW / "scp_statements.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            diagnostic[row[""]] = row["diagnostic"] == "1.0"
    with open(RAW / "ptbxl_database.csv", encoding="utf-8") as f:
        recs = list(csv.DictReader(f))
    for r in recs:
        r["codes"] = ast.literal_eval(r["scp_codes"])
    with open(ROOT / "classes.csv", encoding="utf-8") as f:
        classes = list(csv.DictReader(f))

    usable = [c for c in classes if c["ptbxl_codes"]]
    skipped = [c["class_id"] for c in classes if not c["ptbxl_codes"]]

    # every teaching class each record matches
    matches = {}
    for c in usable:
        for r in recs:
            if match(r, c["ptbxl_codes"], diagnostic, THRESHOLD, c["ptbxl_stadium"]):
                matches.setdefault(r["ecg_id"], []).append(c["class_id"])

    items, chosen = [], set()
    for c in usable:
        cid = c["class_id"]
        pool = [r for r in recs if cid in matches.get(r["ecg_id"], []) and r["ecg_id"] not in chosen]

        def rank(r):
            others = [m for m in matches[r["ecg_id"]] if m not in (cid, "NORM")]
            return (len(others), r["validated_by_human"] != "True", any(r[x] for x in NOISE),
                    -class_likelihood(r, c["ptbxl_codes"]), int(r["ecg_id"]))

        for r in sorted(pool, key=rank)[:n]:
            chosen.add(r["ecg_id"])
            items.append({
                "id": f"ptbxl-{r['ecg_id']}",
                "classId": cid,
                "acceptable": sorted(set(matches[r["ecg_id"]]) - ({"NORM"} if cid != "NORM" else set())),
                "set": c["set"],
                "source": "PTB-XL v1.0.3",
                "ecgId": int(r["ecg_id"]),
                "likelihood": class_likelihood(r, c["ptbxl_codes"]),
                "validated": r["validated_by_human"] == "True",
                "image": f"ecgs/{r['ecg_id']}.png",
                "_path": str(RAW / r["filename_hr"]),
            })
        print(f"{cid:13} {min(n, len(pool)):3} items (pool {len(pool)})")

    (WEB / "ecgs").mkdir(parents=True, exist_ok=True)
    (WEB / "data").mkdir(parents=True, exist_ok=True)
    jobs = [(it["_path"], str(WEB / it["image"])) for it in items]
    with ProcessPoolExecutor() as pool:
        list(pool.map(render_one, jobs, chunksize=4))
    for it in items:
        del it["_path"]

    (WEB / "data" / "items.json").write_text(json.dumps(items, indent=1), encoding="utf-8")
    (WEB / "data" / "classes.json").write_text(json.dumps([
        {"id": c["class_id"], "group": c["group"], "name": c["teaching_class"], "set": c["set"],
         "available": bool(c["ptbxl_codes"])} for c in classes], indent=1), encoding="utf-8")
    print(f"\n{len(items)} items; skipped (no PTB-XL codes): {', '.join(skipped)}")


if __name__ == "__main__":
    main()

"""Render one clean PTB-XL example per class for an eyeball check of render.py.

"Clean" means all of the following:
- human-validated;
- every diagnostic statement at likelihood 100;
- no noise, drift or electrode-problem flags;
- fold 9 or 10 (the folds the PTB-XL authors describe as best validated);
- the target code present with as few other codes as possible.

Usage: python scripts/sample_renders.py   (from the project root, with the .venv)
"""
import ast
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from render import render  # noqa: E402

RAW = ROOT / "data" / "raw" / "ptbxl"
OUT = ROOT / "renders" / "sample"
TARGETS = [  # (label, required codes, stadium or "")
    ("normal", {"NORM"}, ""),
    ("atrial fibrillation", {"AFIB"}, ""),
    ("atrial flutter", {"AFLT"}, ""),
    ("LBBB", {"CLBBB"}, ""),
    ("RBBB", {"CRBBB"}, ""),
    ("third-degree AV block", {"3AVB"}, ""),
    ("WPW", {"WPW"}, ""),
    ("paced", {"PACE"}, ""),
    ("acute inferior MI", {"IMI"}, "Stadium I"),
    ("LVH", {"LVH"}, ""),
]
NOISE = ("baseline_drift", "static_noise", "burst_noise", "electrodes_problems")


def candidates(recs, codes, stadium, strict):
    for r in recs:
        c = r["codes"]
        if not codes <= c.keys() or (stadium and r["infarction_stadium1"] != stadium):
            continue
        if strict and (r["validated_by_human"] != "True" or any(r[n] for n in NOISE)
                       or r["strat_fold"] not in ("9", "10")
                       or any(v not in (0.0, 100.0) for v in c.values())):
            continue
        yield r


def main():
    with open(RAW / "ptbxl_database.csv", encoding="utf-8") as f:
        recs = list(csv.DictReader(f))
    for r in recs:
        r["codes"] = ast.literal_eval(r["scp_codes"])
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for i, (label, codes, stadium) in enumerate(TARGETS, 1):
        pool = list(candidates(recs, codes, stadium, True)) or list(candidates(recs, codes, stadium, False))
        if not pool:
            print(f"NO CANDIDATE for {label}")
            continue
        pick = min(pool, key=lambda r: (len(r["codes"]), int(r["ecg_id"])))
        name = f"{i:02d}_{label.replace(' ', '_')}_ptbxl{pick['ecg_id']}"
        render(str(RAW / pick["filename_hr"]), str(OUT / f"{name}.png"), title=f"PTB-XL {pick['ecg_id']}")
        rows.append((name, pick["ecg_id"], pick["scp_codes"], pick["report"][:120], len(pool)))
        print(f"{name}: {pick['scp_codes']} (pool {len(pool)})")
    with open(OUT / "index.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["file", "ecg_id", "scp_codes", "report", "clean_pool"])
        w.writerows(rows)


if __name__ == "__main__":
    main()

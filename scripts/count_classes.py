"""Count candidate ECGs per teaching class (classes.csv) to size the cardiologist review.

PTB-XL: counted per record from ptbxl_database.csv. Diagnostic statements carry a likelihood
(0-100); form and rhythm statements carry 0, so the threshold applies to diagnostic codes only.
SNOMED sources: marginal counts per dataset from the CinC 2021 dx_mapping files (no PTB/PTB-XL
columns, to avoid double counting). Marginals cannot detect co-occurrence or overlap between codes.

Usage: python scripts/count_classes.py  (from the project root)
"""
import ast
import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
THRESHOLDS = (50, 100)
SNOMED_SOURCES = ("Chapman_Shaoxing", "Ningbo", "Georgia", "CPSC", "CPSC_Extra")


def load_ptbxl():
    scp = {}
    with open(RAW / "ptbxl" / "scp_statements.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            scp[row[""]] = row["diagnostic"] == "1.0"
    recs = []
    with open(RAW / "ptbxl" / "ptbxl_database.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["codes"] = ast.literal_eval(row["scp_codes"])
            recs.append(row)
    return scp, recs


def code_hits(rec, code, diagnostic, threshold):
    if code not in rec["codes"]:
        return False
    return rec["codes"][code] >= threshold if diagnostic.get(code) else True


def match(rec, spec, diagnostic, threshold, stadium):
    if stadium and rec["infarction_stadium1"] != stadium:
        return False
    for alt in spec.split(";"):
        if alt and all(code_hits(rec, c, diagnostic, threshold) for c in alt.split("+")):
            return True
    return False


def load_snomed():
    counts = {}
    for name in ("dx_mapping_scored.csv", "dx_mapping_unscored.csv"):
        with open(RAW / "cinc2021" / name, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                counts[row["SNOMEDCTCode"]] = {s: int(row[s]) for s in SNOMED_SOURCES}
    return counts


def main():
    diagnostic, recs = load_ptbxl()
    snomed = load_snomed()
    with open(ROOT / "classes.csv", encoding="utf-8") as f:
        classes = list(csv.DictReader(f))

    out = []
    for c in classes:
        row = {"class_id": c["class_id"], "teaching_class": c["teaching_class"]}
        for t in THRESHOLDS:
            hits = [r for r in recs if c["ptbxl_codes"] and match(r, c["ptbxl_codes"], diagnostic, t, c["ptbxl_stadium"])]
            row[f"ptbxl_ge{t}"] = len(hits)
            if t == THRESHOLDS[0]:
                row["ptbxl_ge50_validated"] = sum(r["validated_by_human"] == "True" for r in hits)
                row["ptbxl_ge50_fold9_10"] = sum(r["strat_fold"] in ("9", "10") for r in hits)
        if c["report_regex"]:
            rx = re.compile(c["report_regex"], re.I)
            row["ptbxl_report_text"] = sum(bool(rx.search(r["report"])) for r in recs)
        else:
            row["ptbxl_report_text"] = ""
        src = Counter()
        for code in filter(None, c["snomed_codes"].split(";")):
            src.update(snomed.get(code, {}))
        for s in SNOMED_SOURCES:
            row[f"snomed_{s}"] = src[s]
        row["snomed_total_marginal"] = sum(src.values())
        out.append(row)

    dest = ROOT / "data" / "class_counts.csv"
    with open(dest, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    for r in out:
        print(f"{r['class_id']:10} ge50={r['ptbxl_ge50']:>5} ge100={r['ptbxl_ge100']:>5} "
              f"val={r['ptbxl_ge50_validated']:>5} f910={r['ptbxl_ge50_fold9_10']:>4} "
              f"txt={str(r['ptbxl_report_text']):>4} snomed={r['snomed_total_marginal']:>6} "
              f"(Ch {r['snomed_Chapman_Shaoxing']}, Nb {r['snomed_Ningbo']}, Ga {r['snomed_Georgia']}, "
              f"CPSC {r['snomed_CPSC'] + r['snomed_CPSC_Extra']})")
    print(f"\nwrote {dest}")


if __name__ == "__main__":
    main()

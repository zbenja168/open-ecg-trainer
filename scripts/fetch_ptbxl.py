"""Download PTB-XL v1.0.3 500 Hz WFDB records from the PhysioNet open-data mirror on AWS.

physionet.org served at ~27 kB/s on 2026-10-16; the S3 mirror served at ~7.8 MB/s.
Resumable: existing files of the expected size are skipped. Exits non-zero if any file failed,
so an incomplete download is never mistaken for a finished one.

Usage: python scripts/fetch_ptbxl.py [--lr]   (--lr also fetches the 100 Hz records)
"""
import csv
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "data" / "raw" / "ptbxl"
BASE = "https://physionet-open.s3.amazonaws.com/ptb-xl/1.0.3/"
WORKERS = 16


def fetch(rel):
    out = DEST / rel
    url = BASE + rel
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                size = int(r.headers.get("Content-Length", -1))
                if out.exists() and out.stat().st_size == size:
                    return rel, "skip"
                data = r.read()
            if size >= 0 and len(data) != size:
                raise IOError(f"short read {len(data)}/{size}")
            out.parent.mkdir(parents=True, exist_ok=True)
            tmp = out.with_suffix(out.suffix + ".part")
            tmp.write_bytes(data)
            tmp.replace(out)
            return rel, "ok"
        except Exception as e:  # noqa: BLE001 - report every failure, retry a few times
            err = e
    return rel, f"FAILED: {err}"


def main():
    cols = ["filename_hr"] + (["filename_lr"] if "--lr" in sys.argv else [])
    with open(DEST / "ptbxl_database.csv", encoding="utf-8") as f:
        stems = [row[c] for row in csv.DictReader(f) for c in cols]
    files = [s + ext for s in stems for ext in (".hea", ".dat")]
    print(f"{len(files)} files to check", flush=True)

    failed, done = [], 0
    with ThreadPoolExecutor(WORKERS) as pool:
        for fut in as_completed(pool.submit(fetch, rel) for rel in files):
            rel, status = fut.result()
            done += 1
            if status.startswith("FAILED"):
                failed.append(f"{rel} {status}")
            if done % 2000 == 0:
                print(f"{done}/{len(files)} done, {len(failed)} failed", flush=True)

    print(f"finished: {done - len(failed)}/{len(files)} present, {len(failed)} failed")
    for line in failed[:50]:
        print("  " + line)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

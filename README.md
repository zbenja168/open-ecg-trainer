# Open ECG Trainer

An open-source ECG interpretation trainer built on openly licensed, expert-labelled 12-lead ECGs, with
spaced repetition (FSRS), paper-style renders and full response logging. **Prototype: the teaching items
have not yet been reviewed by a cardiologist.**

**Try it:** https://zbenja168.github.io/open-ecg-trainer/ (progress is stored in your own browser only).

## What is here

| Path | What it does |
|---|---|
| `render.py` | Turns a WFDB record into a 12-lead ECG at 25 mm/s and 10 mm/mV on a calibrated 1 mm grid, laid out 3x4 plus a lead II rhythm strip. Output is true to scale. |
| `classes.csv` | Maps PTB-XL SCP statements and SNOMED CT codes to 28 teaching classes, split into two counterbalanced sets (A: morphology, B: rhythm and conduction). |
| `scripts/count_classes.py` | Counts candidate ECGs per class (output in `data/class_counts.csv`). |
| `scripts/fetch_ptbxl.py` | Downloads the PTB-XL 500 Hz records from the PhysioNet open-data mirror. |
| `scripts/build_items.py` | Renders the prototype item bank for the web app. |
| `web/` | The trainer (React, Vite, ts-fsrs). See `web/README.md`. |
| `notes/` | Literature check and class-mapping notes. |

## Rebuild from scratch

```bash
python -m venv .venv && .venv/Scripts/pip install wfdb matplotlib scipy   # or .venv/bin/pip
mkdir -p data/raw/ptbxl
curl -o data/raw/ptbxl/ptbxl_database.csv https://physionet-open.s3.amazonaws.com/ptb-xl/1.0.3/ptbxl_database.csv
curl -o data/raw/ptbxl/scp_statements.csv https://physionet-open.s3.amazonaws.com/ptb-xl/1.0.3/scp_statements.csv
.venv/Scripts/python scripts/fetch_ptbxl.py
.venv/Scripts/python scripts/build_items.py
cd web && npm install && npm run dev
```

## Data and licences

- **Code:** MIT.
- **ECGs:** PTB-XL v1.0.3 (Wagner P et al., *Sci Data* 2020; Goldberger AL et al., PhysioNet), CC BY 4.0.
  The ECGs are re-rendered and filtered (0.5-100 Hz) from the original records.
- **Planned additional sources:** the Chapman-Shaoxing/Ningbo database and the PhysioNet/CinC Challenge
  2021 training sets, both CC BY 4.0.
- **Deliberately excluded:** CC BY-NC-SA teaching collections (LITFL, ECGpedia, ECG Guru), which would
  prevent an open release.

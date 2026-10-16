# Teaching-class mapping: first pass (2026-10-16)

Files:
- `classes.csv`: the mapping.
- `scripts/count_classes.py`: the counter.
- `data/class_counts.csv`: the output.

Inputs:
- PTB-XL v1.0.3 metadata: `ptbxl_database.csv` and `scp_statements.csv`. Its licence file was checked and is
  CC BY 4.0.
- The CinC 2021 `dx_mapping_scored.csv` and `dx_mapping_unscored.csv`. These give SNOMED counts for each
  source. The PTB and PTB-XL columns were left out so those records are not counted twice.

## Rules used
- **Likelihood threshold.** PTB-XL diagnostic statements carry a likelihood of 0 to 100. A record counts at
  likelihood 50 or more, and counts at 100 are reported too. The values present are 15, 35, 50, 80 and 100.
  Form and rhythm statements always carry 0, so for them presence is enough.
- **Acute versus old infarction.** "STEMI" means a territory code with `infarction_stadium1 == 'Stadium I'`.
  "Old MI" means `Stadium III`; the 943 records marked `Stadium II-III` are left out for now. **Unverified:**
  check the PTB-XL paper's definition of the stadia before relying on this.
- **SNOMED counts are marginals.** They come from summary tables, not from individual records. They cannot
  show two codes on the same record (needed for bifascicular block) or remove records that carry two
  overlapping codes.

## Result (PTB-XL count at likelihood 50 or more, then the SNOMED total from other sources)

| Verdict | Classes |
|---|---|
| **Plenty in PTB-XL alone (60 or more)** | Normal 9438, sinus bradycardia 637, sinus tachycardia 826, STEMI anterior 106, STEMI inferior 68, posterior 92, NSTEMI-type 319, old MI 776, LBBB 536, RBBB 540, bifascicular 245, first-degree AV block 790, WPW 79, AF 1514, flutter 73, PVCs 1143, paced 294, LVH 1751, RVH 112, atrial enlargement 497, long QT 116, digoxin 175, low voltage 182 |
| **Fillable with the SNOMED sources** | Early repolarisation (0 + 506), SVT (42 + 801), third-degree AV block (16 + 111), VT (0 + 110, almost all Ningbo "paroxysmal VT") |
| **Thin; merge or keep with care** | STEMI lateral 26: keep if the review accepts about 20, otherwise merge into an anterolateral class. Mobitz I and II: PTB-XL's 2AVB code (14) does not say which type; SNOMED adds 31 Mobitz I and **7 Mobitz II**. Proposal: merge into one second-degree AV block class and teach the I/II distinction in the feedback. |
| **Not fillable from open data: drop** | Hyperkalaemia (no code; 3 text hits, 1 plausible), hypokalaemia (no code; 98 text hits, nearly all "suggest exclude hypokalaemia"), pericarditis (no code; 27 text hits, mostly negations), PE pattern (no code; 2 S1Q3 mentions, both read as normal) |

The result is **about 29 classes**: 34 proposed, minus 4 dropped, with Mobitz I and II merged. A 600-ECG review
is then about 20 per class. That is enough for about 3 held-out test items and about 17 practice items per
class.

A finding worth noting in the software paper: four high-yield board topics (hyperkalaemia, hypokalaemia,
pericarditis, PE) have **no** coded examples in roughly 90,000 openly licensed ECGs. Teaching them openly
would need new CC BY contributions.

## Problems to check before the review
- **Ningbo AF/flutter.** Ningbo lists 7,615 flutter and **0 AF**, which is implausible. AF almost certainly
  sits under the flutter code. Do not use Ningbo for either class unless its records are relabelled. AF does
  not need Ningbo anyway.
- **Source of the long QT, LVH and atrial enlargement counts.** Georgia supplies most of them (1391, 1232
  and 956). Check whether Georgia's labels are reviewed by a physician or are machine statements before
  counting on them.
- **Acute STEMI in PTB-XL** comes from a 1989-96 resting-ECG archive, so "Stadium I" cases may not look
  like a textbook STEMI. Have the cardiologist look at 10 of them early.
- **Licence check of the CinC 2021 training folders**, one by one, before any record is redistributed.
  The literature note says all are CC BY 4.0; confirm against each source's own page.

## Decided 2026-10-16
- Dropped hyperkalaemia, hypokalaemia, pericarditis and PE pattern.
- Merged Mobitz I and II into AVB2: 14 in PTB-XL plus 148 SNOMED, including the generic 2nd-degree code.
- Merged STEMI lateral into STEMI_ANTLAT (anterior/anterolateral): 108 in PTB-XL plus 168 SNOMED.
- That leaves **28 classes**.

## A/B split (in `classes.csv`, column `set`; approved 2026-10-16, cardiologist review pending)
The split keeps confusable clusters inside one set.

| Set | Classes (n) | Clusters kept together |
|---|---|---|
| A: morphology (13) | SB, EREP, STEMI_ANTLAT, STEMI_INF, POST, NSTEMI, OLDMI, LVH, RVH, AE, LQT, DIG, LVOLT | ischaemia, early repolarisation and STEMI; LVH strain, digoxin and ST depression; the hypertrophies |
| B: rhythm and conduction (14) | STACH, LBBB, RBBB, BIFASC, AVB1, AVB2, AVB3, WPW, AF, AFL, SVT, VT, PVC, PACED | the bundle-branch blocks; the AV blocks; AF and flutter; the narrow and wide tachycardias; PVC and VT; paced rhythm and LBBB; sinus tachycardia, SVT and flutter |
| both | NORM | the normal foil, served in both sets and kept out of the contrast |

- **Confusions that still cross the sets.** LBBB versus anterior STEMI, sinus bradycardia versus
  first-degree AV block, and WPW versus infarct Q waves. These are where carryover between sets is most
  likely; report confusion-matrix cells for these pairs.
- **The sets differ in content type**, morphology against rhythm. Counterbalancing still gives an unbiased
  overall effect. But a condition-by-set interaction then means "spacing helps morphology more than
  rhythm", not noise. Pre-register it as such.
- **Thin classes in set B:** AVB2, AVB3 and VT lean almost entirely on Ningbo, CPSC and Georgia.

## Next
1. Have the cardiologist check the A/B split when one is on board.
2. Pull record headers for the SNOMED classes actually used (EREP, SVT, AVB2, AVB3, VT, plus extras for
   STEMI_ANTLAT), not the whole archive.

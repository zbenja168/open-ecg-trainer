# Open-source ECG interpretation trainer on open expert-labelled datasets - novelty check

Date: 2026-10-16. Method: web search (extended) plus direct reads of dataset licence pages, tool sites, and Europe PMC records. The web-search budget ran out part-way; remaining lookups were done by opening known pages and Europe PMC records directly. Items marked **[unverified]** were not opened.

## Verdict

**Gap real, partly taken at the edges.**

- No open-source ECG *trainer* built on PTB-XL (or any open expert-labelled dataset) with spaced repetition, item analytics and released learning data was found in the literature or on GitHub. The closest code precedents are an educational PTB-XL web viewer (Brazilian MBA capstone, no quiz/SR) and an open-source *synthetic* ECG simulator (ECGSim-Advanced, 2026) that generates waveforms rather than using real ECGs.
- Spaced vs massed ECG practice has been tested once in a small semi-randomised 2x2 study (Monteiro et al. 2017, n=80, retention 2-4 weeks, d=0.7 favouring distributed instruction) and once in a non-randomised curricular comparison (Cunningham et al. 2024, n=140, one post-test, no retention). Neither used an algorithmic scheduler (FSRS/SM-2), neither randomised individuals within a cohort to spaced vs massed practice on the same item bank, and neither reported retention by diagnosis class. **An individually randomised spaced-vs-massed ECG practice trial with delayed retention is still open.**
- Item-level psychometrics for ECG items exist (Inaba et al. 2026, 50-item IRT bank, mostly Japanese professionals; Hatala/Pusic 2019 learning curves on 292 ECGs), but no public per-diagnosis difficulty/discrimination map on an open dataset has been published, and no study has released learner response data.
- Licensing is **not a blocker**: PTB-XL, Chapman-Shaoxing/Ningbo, CODE-15% and the PhysioNet/CinC 2021 training sets are all CC BY 4.0; MIMIC-IV-ECG v1.0 is *open* under ODbL (the idea's premise that it is credentialed is out of date), though it carries only machine reports, not cardiologist labels.

## What exists

### Tools

| Tool | Open source? | Dataset source | Spaced repetition | Item analytics | Published evaluation |
|---|---|---|---|---|---|
| **ECG Wave-Maven** (Harvard/BIDMC; Nathanson, McClennen, Safran, Goldberger) - https://ecg.bidmc.harvard.edu/maven/mavenmain.asp | No (no code published) | BIDMC clinical ECG repository, de-identified; ~500+ cases (site references case #546) | No | No (author-assigned difficulty rating per case) | Nathanson LA, Safran C, McClennen S, Goldberger AL. *Proc AMIA Symp* 2001:488-92 (PMID 11825236); McClennen S et al. *Med Educ Online* 2003;8:4339, doi:10.3402/meo.v8i.4339 - usage report (4,105 uses Dec 2000-May 2002), no learning outcomes. |
| **LITFL ECG Library** (Cadogan/Buttner; "powered by Medmastery") - https://litfl.com/ecg-library/ | No; content CC BY-NC-SA 4.0 (images: credit, not-for-profit, no relabelling) | Contributed clinical ECGs, 100+ topics, "Top 100 ECG" quiz | No | No | None found |
| **ECGpedia** (de Jong, Postema; OLVG) - https://en.ecgpedia.org/wiki/Main_Page | Wiki; content CC BY-NC-SA 3.0 | Contributed | No | No | None found |
| **ECG Guru** (Dawn Altman; Grauer, Jones) - https://www.ecgguru.com/ | No; CC BY-NC-SA 3.0, "free of copyright if used in a classroom setting" | Contributed; PDF quizzes | No | No | None found |
| **ECG Stampede** (Tom Fadial) - https://www.ecgstampede.com/ | No; commercial ($59.99-$199.99/yr; institutional $39.99) | Proprietary; 10 units, 57 videos, 30 assessments, "Stampede mode" triage game | Not stated | Institutional gradebook/leader dashboard only | None cited on site |
| **ECG Academy** (Nicholas Tullo, Cardiac Education Resources LLC) - https://www.ecgacademy.com/ | No; subscription, reuse prohibited | Proprietary (~800 ChalkTalks) | No | No | None found |
| **Healio Learn the Heart** - https://www.healio.com/cardiology/learn-the-heart | No | Proprietary ECG library; quizzes (study/test mode, custom quizzes) | No | No | None found |
| **teachingmedicine.com** (Waechter) - https://www.teachingmedicine.com/ | No (free to learners; proprietary) | Own cases; 449 ECG practice cases; instructor dashboards; "performance data of 100's of users" used internally | No | Internal only, not published per item | Waechter J, Reading D, Lee CH, Walker M. *GMS J Med Educ* 2019;36(4):Doc38, https://pmc.ncbi.nlm.nih.gov/articles/PMC6737266/ - 314 first-year students, 42 rhythm-strip cases; ~34 cases / ~112 min to reach 75% accuracy; no per-diagnosis difficulty; no data release. |
| **NYU/UBC learning-curve ECG platform** (Pusic, Hatala, Triola) | No | 292 anonymised clinical ECGs, 3 cardiologists (kappa 0.92), 39% normal base rate | No | Learning curves per learner and group | Hatala R, Gutman J, Lineberry M, Triola M, Pusic M. *Adv Health Sci Educ* 2019;24(1):45-63, doi:10.1007/s10459-018-9846-x (PMID 30171512). Validity study; no item data released. |
| **Queen of Hearts / PMcardio** (Powerful Medical; Smith, Meyers) - https://www.powerfulmedical.com/ ; https://drsmithsecgblog.com/ | No; commercial AI (OMI detection), CE-marked, FDA Breakthrough designation | Proprietary | n/a (diagnostic AI, not a trainer) | n/a | Diagnostic accuracy studies; not education |
| **Dr Smith's ECG Blog** | Blog, no code | Case blog | No | No | None |
| **Anki ECG decks** (Medmastery Beginner ECG, 286 cards, https://ankiweb.net/shared/info/1984686071 ; Dubin-based 1,241- and 670-card decks) | Anki is open source (AGPL); decks are user content | Textbook figures / mixed | Yes (SM-2 or FSRS in Anki) | Anki per-card stats only, never published | None for ECG decks |
| **Amboss / UpToDate ECG modules** | No; commercial | Proprietary | Amboss has general SR for its Qbank **[unverified for ECG]** | Internal | None found **[unverified]** |
| **ECGSim-Advanced** (Bussuri L, Smith J, Takreem M, Talukder A, Ahmad M, Ahmad M) *F1000Research* 2026 preprint, doi:10.12688/f1000research.180507.1 | **Yes** (R Shiny) | **Synthetic** Gaussian waveforms (electrolytes, AV blocks, QT) | No | No | Description only |
| **Educational PTB-XL web viewer** - https://github.com/MauricioMattos/ecg-ia-ptbxl (USP/ESALQ MBA capstone) | Yes | PTB-XL via WFDB over WebSocket, canvas 12-lead rendering; "experimental, non-clinical" | No | No | None |
| **EKG-Visualizer** - https://github.com/samuelmteshome/EKG-Visualizer ; **cardia-analytics** - https://github.com/abdalrhmanabousamra-cyber/cardia-analytics | Yes | Mostly synthetic / PTB-XL Streamlit dashboard | No | No | None |
| Mobile ECG apps in the education literature: usage-only app study (*Discover Education* 2025, doi:10.1007/s44217-025-00715-z; 55/343 students opened it); "Utility of mobile learning in Electrocardiography" *Eur Heart J Digit Health* 2021;2:202 (181 participants, reference app vs search, 2-week retention); ECG Facil (Brazil, *Rev Bras Educ Med*); ECGSight digital caliper (*Adv Physiol Educ* 2026, doi:10.1152/advan.00062.2026); RhythmPath gamified rhythm app for nursing (*BMC Med Educ* 2026, doi:10.1186/s12909-026-09138-2, n=13 pre-post) | None open source | Proprietary/textbook | None | None | Usability, engagement or small pre-post; none with retention or item analytics |

Conclusion on tools: everything with real clinical ECGs is proprietary or NC-SA; the two open-source items are a synthetic simulator and a bare viewer. None combines an open expert-labelled dataset with scheduling, psychometrics and data release.

### Education studies (what is known)

**Baseline competence**
- Cook DA, Oh SY, Pusic MV. Accuracy of Physicians' Electrocardiogram Interpretations: A Systematic Review and Meta-analysis. *JAMA Intern Med* 2020;180(11):1461-71. doi:10.1001/jamainternmed.2020.3989. https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2771093 - 78 studies; pooled pre-training accuracy 42.0% students, 55.8% residents, 68.5% practising physicians, 74.9% cardiologists; median 54% pre vs 67% post training; "deficient at all levels even after educational interventions". Accuracy pooled by training level, not by ECG finding.

**Spacing / scheduling (the directly relevant evidence)**
- Monteiro S, Melvin L, Manolakos J, Patel A, Norman G. Evaluating the effect of instruction and practice schedule on the acquisition of ECG interpretation skills. *Perspect Med Educ* 2017;6(4):237-45. doi:10.1007/s40037-017-0365-x. https://pmc.ncbi.nlm.nih.gov/articles/PMC5542896/ - 80 first-year McMaster students, 2x2 (massed one 3.5 h session vs distributed 3 weekly sessions; blocked vs interleaved practice), 19 diagnoses, 2-3 examples each. Distributed > massed on immediate tests (52% vs 42%, p=0.009) and on 2-4-week delayed test (34% vs 24%, p=0.02, d=0.7). Interleaving did NOT help (blocked > interleaved on delayed test). Semi-random assignment, 51 completers at retention, overall scores low, alpha 0.6. **The only ECG spacing experiment found, and it spaces INSTRUCTION, not algorithmically scheduled practice.**
- Cunningham JM, Johnson M, Kincaid T, Christensen W, Baker J, Turbyfill W, Adams JE. The spacing effect: Improving electrocardiogram interpretation. *Clin Teach* 2024;21:e13626. doi:10.1111/tct.13626 (earlier as SHM Converge 2023 abstract 61, https://shmabstracts.org/abstract/improving-medical-student-ecg-interpretation-skills-with-spaced-repetition-quizzes/) - 140 Colorado students; LIC + 16-18 spaced online ECG quizzes (n=54) vs LIC didactics only (n=24) vs block clerkship (n=62). 17-item post-test 12.4 vs 8.6 vs 9.4; Hedges g 1.57 and 0.86. **Non-randomised, confounded by clerkship structure, single post-test, no retention, fixed quiz cadence (no adaptive scheduler), no per-item data.**
- Moulin T, Lellouche N, Gandjbakhch E, Laredo M. Daily Quiz-Based Microlearning Program to Support ECG Interpretation Training for Medical Students: A Feasibility Study. *CJC Open* 2026;8(1):43-50. doi:10.1016/j.cjco.2025.09.009 - 47 students, daily quiz for 6 weeks, uncontrolled; participation fell 87% -> 70%; +1.1 points; no retention.
- Gayle 2020 (text-message/QuizTime ECG quizzes vs material only; no difference) - listed in Ardekani 2023 review below **[not opened directly]**. QuizTime platform: Ahmed T, Stinson K, Johnson J, Latif Z. *AMIA Annu Symp Proc* 2023:253-60 (PMID 38222381).
- Hatala RM, Brooks LR, Norman GR. Practice makes perfect: the critical role of mixed practice in the acquisition of ECG interpretation skills. *Adv Health Sci Educ* 2003;8(1):17-26. doi:10.1023/A:1022687404380 - mixed (contrastive) practice 46% vs 30% accuracy. (The "Hartman" in the brief is Hatala.) Monteiro 2017 failed to replicate the interleaving advantage in novices.
- Esomonye TC et al. A Burst-Learning ECG Curriculum for Internal Medicine Residents. *JACC Case Rep* 2026;31(10):108886, doi:10.1016/j.jaccas.2026.108886 - QI, confidence up, knowledge unchanged, no retention.

**Spaced education generally (not ECG)**
- Kerfoot BP, DeWolf WC, Masser BA, Church PA, Federman DD. Spaced education improves the retention of clinical knowledge by medical students: a randomised controlled trial. *Med Educ* 2007;41(1):23-31. doi:10.1111/j.1365-2929.2006.02644.x - weekly e-mailed urology cases; significant end-of-year retention gain; 71% completion. Kerfoot's later adaptive spaced-education RCTs **[unverified]**.
- Martinengo L et al. Spaced Digital Education for Health Professionals: Systematic Review and Meta-Analysis. *J Med Internet Res* 2024;26:e57760. https://www.jmir.org/2024/1/e57760 - spaced > massed online education for post-intervention knowledge (SMD 0.32, moderate certainty); **retention evidence thin (3 studies, non-significant at 3-12 months)**; 83% of studies unclear/high risk of bias.
- SpacED POCUS RCT (adaptive spaced education for image interpretation, 36 students, 2025, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12658577/) - a template for an image-interpretation spaced-education RCT, not ECG.

**Deliberate practice / learning curves**
- Waechter et al. 2019 (above): ~34 rhythm strips to 75%; four-part feedback; no per-diagnosis difficulty; no data release.
- Hatala, Gutman, Lineberry, Triola, Pusic 2019 (above): learning-curve assessment validity on 292 ECGs; atypical curves in a minority; no data release.

**Teaching format / assessment (Goettingen and others)**
- Raupach T, Hanneforth N, Anders S, Pukrop T, ten Cate O, Harendza S. Impact of teaching and assessment format on ECG interpretation skills. *Med Educ* 2010;44(7):731-40. doi:10.1111/j.1365-2923.2010.03687.x - 335 Year-4 students randomised lectures vs near-peer small groups; near-peer better only under formative assessment; decline at 8 weeks.
- Raupach T et al. Summative assessments are more powerful drivers of student learning than resource intensive teaching formats. *BMC Med* 2013;11:61. https://link.springer.com/article/10.1186/1741-7015-11-61 - 534 students, partially randomised, 6 arms.
- Raupach T, Harendza S, Anders S, Schuelper N, Brown J. How can we improve teaching of ECG interpretation skills? Findings from a prospective randomised trial. *J Electrocardiol* 2016;49(1):7-12. doi:10.1016/j.jelectrocard.2015.10.004 (PMID 26615874) - 493 students; 2-month retention predicted by summative assessment (beta 4.08, 95% CI 1.39-6.78), not by teaching format.
- Rolskov Bojsen S, Raeder SB, Holst AG, Kayser L, Ringsted C, Hastrup Svendsen J, Konge L. The acquisition and retention of ECG interpretation skills after a standardized web-based ECG tutorial: a randomised study. *BMC Med Educ* 2015;15:36. doi:10.1186/s12909-015-0319-0 (PMC4356122) - 203 students randomised to retention test at 2-4, 10-12 or 18-20 weeks; scores fell at every interval, no difference between intervals; "rapidly lost when the intervention is not repeated".
- Fent G, Gosai J, Purva M. Teaching the interpretation of electrocardiograms: Which method is best? *J Electrocardiol* 2015;48(2):190-3. doi:10.1016/j.jelectrocard.2014.12.014 - no single best method; self-directed learning associated with poorer competence; summative > formative.
- Ardekani A, Hider AM, Rastegar Kazerooni AA, Hosseini SA, Roshanshad A, Amini M, Kojuri J. Surfing the clinical trials of ECG teaching to medical students: A systematic review. *J Educ Health Promot* 2023;12:107. https://pmc.ncbi.nlm.nih.gov/articles/PMC10243439/ - 23 RCTs to May 2022; narrative only; Monteiro 2017 is the ONLY spacing study included; flags long-term retention and online-vs-in-person as open questions.
- Iqbal N, Kandasamy R, et al. VR simulation for acquisition and retention of ECG interpretation skills: RCT. *Cureus* 2024;16(6):e62170, doi:10.7759/cureus.62170 - 140 students, 8-week retention favoured VR.
- Scherff AD, Kaab S, Fischer MR, Berndt M. EYE-ECG2. *GMS J Med Educ* 2025;42(4):Doc47, doi:10.3205/zma001771 - 94 students, eye-tracking videos, non-significant.
- Chaumont C et al. How to improve medical students' ECG interpretation skills? *BMC Med Educ* 2024;24:979, doi:10.1186/s12909-024-05929-7 - 52 students, 5-min reversed-classroom x4/week vs one lecture; +26 vs +11 points; no retention.

**Item psychometrics**
- Inaba S, Yamamoto K, Kaga T, Kawakami H, Islam MZ, Wannous M, Sakata M, Furukawa TA, Yamaguchi O. Development and initial validation of a computerized adaptive test prototype for ECG interpretation using item response theory. *PLoS One* 2026;21(7):e0344341. https://pmc.ncbi.nlm.nih.gov/articles/PMC13379108/ - 50 vignette+image MCQs, 535 mostly Japanese health professionals (77 medical students), 3PL IRT; item parameters in supplement; items not mapped to diagnosis classes in the text; no DIF; CAT not validated. Protocol: Inaba S et al. *BMJ Open* 2023;13:e072097, doi:10.1136/bmjopen-2023-072097.
- No study found that publishes difficulty/discrimination per ECG *diagnosis* for medical students, nor one that releases learner-response data.

**What remains open**
1. Individually randomised spaced (algorithmic FSRS/SM-2) vs massed practice on an identical ECG item bank, with delayed retention (>= 8 weeks) by diagnosis class.
2. Per-diagnosis item difficulty and discrimination on a public, expert-labelled ECG set, released as data.
3. Learning curves per diagnosis class across a whole class, with released de-identified logs (Hatala/Pusic 2019 and Waechter 2019 measured curves but released nothing).
4. Whether interleaving helps once novices pass a mastery threshold (Monteiro's hypothesis, untested).
5. Whether retention gains from spaced practice survive the 3-12 month horizon where Martinengo 2024 found nothing significant.

## Dataset licensing

| Dataset | Licence (as read on the hosting page) | Expert labels? | Usable in a public web trainer? |
|---|---|---|---|
| **PTB-XL v1.0.3** - https://physionet.org/content/ptb-xl/1.0.3/ | **CC BY 4.0** ("Anyone can access the files") | Yes: 71 SCP-ECG statements (diagnostic/form/rhythm), up to two cardiologists, 5 superclasses (NORM 9,514; MI 5,469; STTC 5,235; CD 4,898; HYP 2,649); 21,799 records / 18,869 patients; folds 9-10 human-validated | **Yes.** Attribution (Wagner et al. 2020, PhysioNet) and indication of changes required; commercial use permitted. |
| **Chapman-Shaoxing + Ningbo** ("A large scale 12-lead ECG database for arrhythmia study" v1.0.0, 2022; Zheng J, Guo H, Chu H) - https://physionet.org/content/ecg-arrhythmia/1.0.0/ | **CC BY 4.0** | Yes: physician-labelled rhythm and conditions, SNOMED CT codes; 45,152 ECGs | **Yes.** |
| **PhysioNet/CinC Challenge 2021 training data** v1.0.3 - https://physionet.org/content/challenge-2021/1.0.3/ | **CC BY 4.0** for the ~88,000 public training ECGs (CPSC 2018/Extra 10,330; INCART 74; PTB+PTB-XL 22,353; Georgia 10,344; Chapman/Ningbo 45,152); test and validation sets never released | Yes (SNOMED-CT mapped) | **Yes** for training folders. |
| **CODE-15%** v1.0.0 - https://zenodo.org/records/4916206 | **CC BY 4.0** | Weak for teaching: only 6 binary labels (1dAVb, RBBB, LBBB, SB, AF, ST) plus `normal_ecg` from automatic annotation; 345,779 exams / 233,770 patients (Ribeiro AH et al. 2021) | Legally yes; pedagogically limited (few classes, partly machine-derived). |
| **MIMIC-IV-ECG v1.0** - https://physionet.org/content/mimic-iv-ecg/1.0/ | **Open Data Commons ODbL v1.0; access policy "Anyone can access the files"** (v0.1 was credentialed; the idea's premise is out of date) | No cardiologist labels: machine-generated report text (`report_0..17`) and global measurements only; ~800,000 ECGs / ~160,000 patients | Legally yes under ODbL (attribution + share-alike on derived *databases*, which would bind the released learning dataset if it embeds MIMIC content). Not teaching-grade without expert relabelling. |
| **MIMIC-IV-ECG-Ext-ICD v1.0.1** (Strodthoff, Lopez Alcaraz, Haverkamp 2024) - https://physionet.org/content/mimic-iv-ecg-ext-icd-labels/1.0.1/ | **PhysioNet Credentialed Health Data License 1.5.0 + DUA; CITI training** | ICD-10 discharge diagnoses | **No** - credentialed, cannot be redistributed in a public app. |
| LITFL, ECGpedia, ECG Guru images | CC BY-NC-SA 3.0/4.0 | Curated teaching cases | Only in a non-commercial, share-alike deployment; would taint a CC BY release. Keep out of the core bank. |
| PTB Diagnostic ECG Database (older) - https://physionet.org/content/?topic=PTB | PhysioNet open; stated purpose includes "teaching" | Yes | Yes. |

**Conclusion:** PTB-XL + Chapman/Ningbo + CinC-2021 Georgia/CPSC give roughly 90,000 CC BY 4.0 expert-labelled 12-lead ECGs that can legally power a public web trainer and be redistributed with the code. MIMIC-IV-ECG is open (ODbL) but lacks expert labels; its ICD label extension is credentialed. CODE-15% is legal but too coarsely labelled.

## Technical precedents

- **wfdb-python** (MIT-LCP) - https://github.com/MIT-LCP/wfdb-python - MIT; reads PTB-XL/Challenge WFDB records.
- **ecg_plot** (dy1901) - https://github.com/dy1901/ecg_plot - MIT; standard 12-lead paper-style plots (3x4 + rhythm strip).
- **ts-fsrs** (open-spaced-repetition) - https://github.com/open-spaced-repetition/ts-fsrs - MIT, FSRS v6, ESM/CJS/UMD, ~820 stars; companion `@open-spaced-repetition/binding` (Rust) optimises parameters from review logs; py-fsrs, fsrs-rs, fsrs-browser also available - https://github.com/open-spaced-repetition/awesome-fsrs
- **Open-source SR question platforms in medicine:** Cohort (todd866/cohort, MIT code, CC BY 4.0 content, 556 USMLE items, embedding-based scheduler) - https://github.com/todd866/cohort ; Openlet (FSRS flashcards, MIT) - https://github.com/ChloeVPin/openlet ; MedHub (py-fsrs) - https://github.com/daanmt/MedHub ; Anki itself (AGPL, FSRS built in). None handles waveform rendering or item psychometrics.
- **PTB-XL viewers:** MauricioMattos/ecg-ia-ptbxl (WFDB -> WebSocket -> canvas 12-lead), agoldhammer/ecgdisp (Rust egui), abdalrhmanabousamra-cyber/cardia-analytics (Streamlit/Plotly), samuelmteshome/EKG-Visualizer (browser teaching tool, mostly synthetic, notes PTB-XL CC BY attribution).
- **Synthetic teaching simulator:** ECGSim-Advanced (R Shiny, F1000Research 2026 preprint) - open source but not dataset-driven.
- **Learning-curve and IRT methods ready to reuse:** Hatala/Pusic 2019 learning-curve assessment; Inaba 2026 `mirt`/`mirtCAT` pipeline; Waechter 2019 feedback design (correct/incorrect, criteria comparison, case discussion, instructor e-mail).

## What would be new

1. **First open-source trainer on an open expert-labelled ECG dataset.** Every existing trainer with real ECGs (Wave-Maven, LITFL, Stampede, teachingmedicine.com, NYU platform) is closed or NC-SA; the open-source ones are synthetic or viewers. PTB-XL's 71 SCP statements and superclasses give a free taxonomy for adaptive selection by diagnosis class.
2. **Individually randomised spaced (FSRS) vs massed practice with delayed retention by diagnosis class.** Monteiro 2017 (n=80, instruction spacing, semi-random) and Cunningham 2024 (non-randomised, no retention) leave this open; Martinengo 2024 says retention evidence for spaced digital education is thin everywhere.
3. **A public per-diagnosis item-difficulty/discrimination map of ECG findings for medical students.** Inaba 2026 has 50 items and does not report by diagnosis; Cook 2020 pools accuracy by training level, not by finding. "Which ECG findings are hardest" is unanswered in print.
4. **Released de-identified learning data (response logs, timings, FSRS states).** No ECG education study found has released learner data; Hatala/Pusic 2019 and Waechter 2019 kept theirs. A CC BY response dataset over CC BY ECGs would be a first.
5. Secondary: testing Monteiro's hypothesis that interleaving pays off only after a mastery threshold; learning-curve-based progress assessment (Pusic) operationalised in open code.

## Risks

- **Label quality for teaching.** PTB-XL statements carry likelihoods, many records have multiple statements, and only a "large fraction" had second-cardiologist validation; folds 9-10 are the safest. A teaching-grade subset needs cardiologist review and a mapping from SCP codes to the diagnoses a curriculum actually names. No clinical vignettes are included.
- **Rendering fidelity.** Students learn on paper-style 12-lead layouts at 25 mm/s, 10 mm/mV; PTB-XL is 1989-96 Schiller data at 100/500 Hz. Plotting must match exam presentation (Examplify/NBME images).
- **Engagement attrition** is the recurring failure of ECG apps: 16% opened the 2025 Springer app; Moulin 2026 participation fell from 87% to 70% in six weeks; Kerfoot 2007 had 29% attrition. Massed-arm compliance and spaced-arm dropout threaten the RCT.
- **Within-cohort randomisation** risks contamination (students share logins/decks), and Raupach showed summative-assessment effects dominate teaching-format effects; an exam-linked outcome is needed, which requires faculty buy-in and IRB.
- **Floor effects:** Monteiro's delayed scores were 24-34%; Cook's student baseline 42%. The item bank must span difficulty or discrimination estimates will be unstable.
- **FSRS was fitted on flashcard recall**, not perceptual diagnosis; default parameters may mis-schedule, and re-fitting needs thousands of reviews (the `binding` optimiser needs logs first).
- **Licence hygiene:** keep NC-SA images (LITFL/ECGpedia/ECG Guru) out of the CC BY bank; if MIMIC-IV-ECG content is embedded, ODbL share-alike applies to the released learning database.
- **Adjacent commercial movement:** LITFL is now "powered by Medmastery"; Powerful Medical and Stampede have institutional tiers; a closed competitor could add SR quickly. The open data release, not the app, is the defensible contribution.
- **Not opened / to verify:** Kerfoot adaptive spaced-education RCT details; Gayle 2020 QuizTime ECG RCT full text; Amboss/UpToDate ECG module features; whether Pusic's NYU platform ever released item parameters; ECG Wave-Maven total case count.

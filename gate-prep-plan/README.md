# GATE 2027 — CSE + DA Preparation Plan (built from PYQ evidence)

**Created 6 Oct 2026 · Target: GATE 2027 (IIT Madras), exams 6–7, 13–14, 20–21 Feb 2027 · Two papers: CS + DA (officially allowed combination)**

## ⚠️ Registration
Registration for GATE 2027 is now closed. Verify your registration status at https://gate2027.iitm.ac.in. Two papers = double fee. CS↔DA is allowed in both directions (primary/secondary).

## Documents

| File | Sections |
|---|---|
| [01_PYQ_Trend_Analysis.md](01_PYQ_Trend_Analysis.md) | A. 10-year PYQ trends (CSE 2017–2026, DA 2024–2026) · B. Subject weightage & priority · C. Topic-wise Tier tables with PYQ reasons |
| [02_Overlap_and_Syllabus_Checklist.md](02_Overlap_and_Syllabus_Checklist.md) | D. CSE–DA overlap (study-once map) · E. Full official syllabus checklist, tier-tagged |
| [03_Schedule_Plans.md](03_Schedule_Plans.md) | F. 5 phases · G. Month plan · H. 18-week grid · I. Day templates (normal/weekend/low-energy/catch-up) |
| [04_PYQ_Revision_Mock_Strategy.md](04_PYQ_Revision_Mock_Strategy.md) | J. PYQ protocol + completion checklists · K. Revision system · L. Mock strategy · M. Mistake-log + classic trap list |
| [05_Score_Strategy.md](05_Score_Strategy.md) | N. AIR 1–500 score construction (CS ≈ 75, DA ≈ 62) · O. Final 30 days + exam-day execution |

## Data sources

- Official: gate2027.iitm.ac.in (syllabi PDFs, brochure, two-paper table, dates), gate2025.iitr.ac.in + gate2026.iitg.ac.in (cutoffs, statistical reports, DA question papers), gate2024.iisc.ac.in (statistical report).
- PYQ weightage: cross-checked coaching analyses (ACE, GO Classes, GfG, PW, GateAtZeal) — all figures ±1–4 marks, flagged in-file.
- Known limitations (stated, not hidden): DA has only 3 papers (n=3); no official per-topic marks exist anywhere; marks-vs-rank bands are community-derived; CSE 2017 single-source; CSE 2021 two-session caveat.

## The 5-line version

1. Math spine first (P&S + LA + Calc + DM ≈ 13 m on CS, ~27–30 m on DA), at DA depth — then Programming/DS/Algo + DBMS core: everything shared gets studied exactly once.
2. Phase 2 interleaves CSE-only (DL/COA/OS/TOC/CD/CN) with DA-only (ML/AI/stats-tests/warehousing) so both papers stay live.
3. PYQs from week 1, topic-wise; Phase 3 (Jan) is a full PYQ marathon; DA's 3 real papers get two timed passes each.
4. Mocks: ~12 full-length (6 CS + 5–6 DA) + 18 sectional, every one with a coded mistake autopsy (C1–C6).
5. Score targets for AIR<500: **CS ~75/100 at ≥85% accuracy, DA ~62/100** — attempt ~62–65 questions, never blind-guess MCQs, always attempt MSQ/NAT.

## Build steps (recommended order)

1. Run `site/checklist_data_make.py` to generate the base `checklist_data.json`.
2. Run `site/pyq_data_make.py` to merge raw PYQ data into the checklist.
3. Open `site/index.html` in a browser (or serve via a local HTTP server) to view the tracker.


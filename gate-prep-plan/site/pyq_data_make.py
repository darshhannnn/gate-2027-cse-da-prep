#!/usr/bin/env python3
"""Merge collected PYQ JSON files (one array per file) into checklist_data.json.
Usage: python pyq_data_make.py  (reads pyq_raw_*.json next to this script)
Each entry: {"topic","year","paper","marks","q","url"} — matched to checklist rows by exact topic name.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ck_path = HERE / "checklist_data.json"
ck = json.loads(ck_path.read_text(encoding="utf-8"))

index = {}
for g in ck["groups"]:
    for r in g["rows"]:
        index[r["topic"]] = r

total, matched, unmatched = 0, 0, set()
for f in sorted(HERE.glob("pyq_raw_*.json")):
    arr = json.loads(f.read_text(encoding="utf-8"))
    for e in arr:
        total += 1
        row = index.get(e.get("topic", ""))
        if row is None:
            unmatched.add(e.get("topic", "?"))
            continue
        row.setdefault("pyqs", []).append({
            "y": e["year"], "p": e["paper"], "m": e.get("marks"),
            "q": e["q"], "u": e["url"]})
        matched += 1

# sort each topic's questions: year asc, marks asc
for r in index.values():
    if "pyqs" in r:
        r["pyqs"].sort(key=lambda x: (x["y"], x.get("m") or 0))

ck["meta"]["pyqNote"] = "Real PYQs transcribed from the official GATE papers (2024–2026 DA from the official PDFs; CS questions from official/archived sources via linked pages)."

ck_path.write_text(json.dumps(ck, ensure_ascii=False, indent=1), encoding="utf-8")
nq = sum(len(r.get("pyqs", [])) for g in ck["groups"] for r in g["rows"])
topics_with = sum(1 for g in ck["groups"] for r in g["rows"] if r.get("pyqs"))
print(f"matched {matched}/{total} into {topics_with}/89 topics")
if unmatched:
    print("UNMATCHED topics:", sorted(unmatched))

#!/usr/bin/env python3
"""Merge the master-plan workbook's Daily Plan into daily_resequenced.json.

Input : workbook_plan.json  (rows of [date, day, type, phase, unit, topic, subtopics, scope, tier, routine])
Output: daily_resequenced.json (site "Daily Checklist")

Rows dated before CUTOFF (already-completed/earlier days) are kept untouched;
every row from CUTOFF onward is replaced by the workbook plan.
"""
import json
import re
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
CUTOFF = "2026-10-23"
WEEK_ANCHOR = date(2026, 10, 20)  # start of site week 3 (weeks run Tue-Mon in the existing data)
WEEK_ANCHOR_NO = 3
TICK = "\u2610"  # ballot box used by the existing rows


def week_of(iso: str) -> int:
    y, m, d = map(int, iso.split("-"))
    return WEEK_ANCHOR_NO + (date(y, m, d) - WEEK_ANCHOR).days // 7


def bullets(text: str) -> str:
    out = []
    for ln in text.split("\n"):
        for part in ln.split(" | "):
            part = part.strip()
            if part:
                out.append("\u2022 " + part)
    return "\n".join(out)


def side(scope: str, topic: str) -> str:
    """Which paper(s) this day belongs to: 'cs', 'da' or 'both'."""
    if scope == "Computer Science only":
        return "cs"
    if scope == "Data Science and Artificial Intelligence only":
        return "da"
    if scope == "Both papers" and topic.startswith("Computer Science") and "Data" not in topic:
        return "cs"
    return "both"


PREFIX = re.compile(r"^(Both papers|Shared by both papers|Computer Science|Data Science and Artificial Intelligence)([^:]{0,60}):\s*")


def split_top(s: str):
    """Split on commas/semicolons/sentence ends that are outside parentheses."""
    out, buf, depth = [], "", 0
    for i, ch in enumerate(s):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if depth == 0 and (ch in ",;" or (ch == "." and s[i + 1:i + 2] in (" ", ""))):
            out.append(buf)
            buf = ""
        else:
            buf += ch
    out.append(buf)
    items = []
    for it in out:
        it = re.sub(r"^\s*(and|or)\s+", "", it.strip())
        if it:
            items.append(it[0].upper() + it[1:])
    return items


def split_desc(desc: str, scope: str, topic: str):
    """Return (cs_items, da_items): one syllabus item per entry, assigned to the right paper(s)."""
    default = side(scope, topic)
    cs, da = [], []
    for ln in desc.split("\n"):
        for part in ln.split(" | "):
            part = part.strip()
            if not part:
                continue
            m = PREFIX.match(part)
            target = default
            if m:
                head = m.group(1)
                target = "cs" if head == "Computer Science" else "da" if head.startswith("Data") else "both"
                part = part[m.end():]
            if part.lower().startswith("session focus:"):
                items = [part]
                target = "both" if default == "both" else default
            else:
                items = split_top(part)
            if target in ("cs", "both"):
                cs += items
            if target in ("da", "both"):
                da += items
    if default == "cs":
        da = []
    elif default == "da":
        cs = []
    return cs, da


def activities(kind: str, tier: str, routine: str, desc: str):
    """Return the six activity cells: PYQs, maths/stats, GA, spaced revision, mistake log, test."""
    if kind == "Study session":
        if tier.startswith("Tier 2"):
            pyq = "60\u201390 minutes DA-style PYQs"
            maths = "1.5 hours CSE foundation recall/PYQs from completed Units 1\u201317"
            spaced = "30 minutes spaced revision"
            mist = "15\u201320 minutes mistake log"
        elif "CSE-primary" in routine:
            pyq = "1.5\u20132 hours CSE PYQs"
            maths = "20 minutes foundation upkeep (Tue/Thu/Sat: DA formula recall + 3\u20135 starred questions)"
            spaced = "30\u201345 minutes spaced revision"
            mist = "15\u201320 minutes mistake log"
        else:
            pyq = "1.5\u20132 hours CSE PYQs first, then 30\u201345 minutes DA-style variants where topics overlap"
            maths = "20 minutes spaced foundation recall (Units 1\u201317)"
            spaced = "Re-test earlier content after 1, 3, 7 and 21 study sessions"
            mist = "15\u201320 minutes mistake log and recall quiz"
        return [[pyq], [maths], ["20\u201330 minutes General Aptitude"], [spaced], [mist],
                ["Recall quiz on today's topic"]]
    segs = [s.strip() for s in routine.split(";") if s.strip()]
    has = lambda w: any(w in s.lower() for s in segs)
    return [
        [desc.split("\n")[0]] if kind != "Revision session" else [x for x in desc.split("\n") if x.strip()],
        [],
        ["20\u201330 minutes General Aptitude"] if has("aptitude") or kind == "Revision session" else [],
        ["Review the spaced-revision queue"] if has("spaced") else [],
        ["Update the mistake log"] if has("mistake") else [],
        segs,
    ]


def main():
    plan = json.loads((HERE / "workbook_plan.json").read_text(encoding="utf-8-sig"))
    path = HERE / "daily_resequenced.json"
    dump = json.loads(path.read_text(encoding="utf-8"))
    rows = dump["Daily Checklist"]
    header, old = rows[0], rows[1:]
    keep = [r for r in old if r and r[0][:10] < CUTOFF]

    new = []
    for dt, day, kind, phase, unit, topic, desc, scope, tier, routine in plan:
        sd = side(scope, topic)
        label = f"{unit}: {topic}" if unit.startswith("Unit") else topic
        cs_items, da_items = split_desc(desc, scope, topic)
        as_text = lambda items: "\n".join("\u2022 " + x for x in items)
        cs, cst = (label, as_text(cs_items)) if sd in ("cs", "both") else ("", "")
        da, dat = (label, as_text(da_items)) if sd in ("da", "both") else ("", "")
        act = activities(kind, tier, routine, desc)
        new.append([
            f"{dt} 00:00:00", day, str(week_of(dt)), phase,
            cs, cst, da, dat,
            *["\n".join(f"{TICK} {x}" for x in a) for a in act],
            TICK, TICK, TICK, TICK, TICK,
        ])
    dump["Daily Checklist"] = [header] + keep + new
    path.write_text(json.dumps(dump, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"kept {len(keep)} earlier days, wrote {len(new)} workbook days -> {len(keep) + len(new)} total")


if __name__ == "__main__":
    main()

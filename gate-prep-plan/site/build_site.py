#!/usr/bin/env python3
"""Build the GATE 2027 CSE+DA website (v2, clean design).

Sources:
  *.md                - the A-O plan documents (rendered into the "Plan" view)
  sample_sheet_dump.json - the user's tracker workbook (rendered into the "Tracker" view)

Usage:  python build_site.py [source_dir] [output_html]
Defaults: source = parent of this script, output = <source>/site/index.html
"""
import html
import json
import re
import sys
from pathlib import Path

import markdown

DOCS = [
    ("README.md", "Overview & Sources"),
    ("01_PYQ_Trend_Analysis.md", "A–C · PYQ Trends & Priority"),
    ("02_Overlap_and_Syllabus_Checklist.md", "D–E · Overlap & Syllabus Checklist"),
    ("03_Schedule_Plans.md", "F–I · Schedules"),
    ("04_PYQ_Revision_Mock_Strategy.md", "J–M · PYQ, Revision, Mocks, Mistakes"),
    ("05_Score_Strategy.md", "N–O · Score Strategy & Final 30 Days"),
]
MD_EXTENSIONS = ["tables", "fenced_code", "toc"]
TIER_RE = re.compile(r"Tier (\d)")


# ---------------------------------------------------------------- sheet data
def lines(cell: str):
    if not cell:
        return []
    out = []
    for ln in cell.split("\n"):
        ln = ln.strip().lstrip("☐").strip()
        if ln:
            out.append(ln)
    return out


STOP = {"and", "the", "of", "for", "a", "an", "to", "in", "or", "with", "s"}

def toks(s):
    return {w for w in re.split(r"[^a-z0-9]+", s.lower()) if len(w) > 1 and w not in STOP}

def sim(a, b):
    A, B = toks(a), toks(b)
    if not A or not B:
        return 0.0
    return len(A & B) / min(len(A), len(B))

def clean_data(dump: dict) -> dict:
    data = {}
    rs_path = Path(__file__).resolve().parent / "daily_resequenced.json"
    if rs_path.exists():
        rs = json.loads(rs_path.read_text(encoding="utf-8"))
        if rs.get("Daily Checklist"):
            dump = dict(dump)
            dump["Daily Checklist"] = rs["Daily Checklist"]
    src_days = dump["Daily Checklist"]
    days = []
    for r in src_days[1:]:
        if not r or not r[0]:
            continue
        cs, da = r[4], r[6]
        if cs and da and sim(cs, da) >= 0.5:
            track = "shared"
        elif cs and not da:
            track = "CS"
        elif da and not cs:
            track = "DA"
        elif not cs and not da:
            track = "rest"
        else:
            track = "dual"
        days.append({
            "date": r[0][:10], "day": r[1], "week": int(float(r[2])), "phase": r[3],
            "cs": r[4], "csT": r[5], "da": r[6], "daT": r[7], "track": track,
            "act": [lines(r[8]), lines(r[9]), lines(r[10]), lines(r[11]), lines(r[12]), lines(r[13])],
        })
    data["days"] = days

    ck_path = Path(__file__).resolve().parent / "checklist_data.json"
    ck = json.loads(ck_path.read_text(encoding="utf-8")) if ck_path.exists() else None
    if ck:
        data["checklist"] = ck

    topics = []
    for r in dump["Complete Topic Checklist"][1:]:
        if not r or not r[0]:
            continue
        m = TIER_RE.search(r[3])
        topics.append({"exam": "CS" if "Computer Science" in r[0] and "Data" not in r[0] else "DA",
                       "subject": r[1], "topic": r[2], "tier": int(m.group(1)) if m else 3})
    data["topics"] = topics

    # ---- twins: identical topics across the CS and DA papers (shared syllabus) ----
    key307 = lambda t: t["exam"] + t["subject"] + t["topic"]
    for i, t in enumerate(topics):
        if t["exam"] != "CS":
            continue
        for j, u in enumerate(topics):
            if u["exam"] != "DA" or "twin" in u:
                continue
            if sim(t["topic"], u["topic"]) >= 0.8 and sim(t["subject"], u["subject"]) >= 0.4:
                t["twin"] = key307(u)
                u["twin"] = key307(t)
                break

    # ---- linkMap: each day's CS/DA topics -> Topics(307) keys + Master Checklist rows ----
    link = {}
    if ck:
        def day_lines(s):
            return [x.strip().lstrip("•").strip() for x in s.split("\n") if x.strip().lstrip("•").strip()]

        for d in days:
            ent = {}
            for side, exam in (("cs", "CS"), ("da", "DA")):
                subj = d[side]
                t307, mc = [], []
                for L in day_lines(d[side + "T"]):
                    for t in topics:
                        if t["exam"] != exam or sim(subj, t["subject"]) < 0.4:
                            continue
                        k = key307(t)
                        if sim(L, t["topic"]) >= 0.75 and k not in t307:
                            t307.append(k)
                    if ck:
                        for gi, g in enumerate(ck["groups"]):
                            for ri, r in enumerate(g["rows"]):
                                if [gi, ri] in mc:
                                    continue
                                if sim(L, r["topic"]) >= 0.75 or any(sim(L, s["n"]) >= 0.75 for s in r["subs"]):
                                    mc.append([gi, ri])
                if t307 or mc:
                    ent[side] = {"mc": mc, "t": t307}
            if ent:
                link[d["date"]] = ent
    data["linkMap"] = link
    n_linked = sum(1 for e in link.values() if e.get("cs") or e.get("da"))
    sys.stderr.write(f"linkMap: {len(link)}/{len(days)} days linked; twins: "
                     f"{sum(1 for t in topics if 'twin' in t)}\n")

    pyq = []
    for r in dump["Previous-Year Question Tracker"][1:]:
        if not r or not r[0]:
            continue
        pyq.append({"exam": "CS" if "Data" not in r[0] else "DA", "subject": r[1],
                    "p1": lines(r[2]), "p2": lines(r[3]), "err": lines(r[4]),
                    "acc": r[5], "notes": r[6]})
    data["pyq"] = pyq

    mocks = []
    for r in dump["Mock Test Tracker"][1:]:
        if not r or not r[0]:
            continue
        mocks.append({"n": r[0], "date": r[1][:10], "paper": r[2], "type": r[3]})
    data["mocks"] = mocks

    data["time"] = [{"type": r[0], "dur": r[1], "act": r[2], "instr": r[3]}
                    for r in dump["Daily Time Structure"][1:] if r and r[0]]
    data["guide"] = [{"item": r[0], "text": r[1]}
                     for r in dump["How to Use This Checklist"][1:] if r and r[0]]
    return data


# ---------------------------------------------------------------- markdown docs
def strip_tags(s: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def build_docs(source: Path):
    docs_html, docs_meta = [], []
    for i, (fname, tag) in enumerate(DOCS, start=1):
        text = (source / fname).read_text(encoding="utf-8")
        body = markdown.markdown(text, extensions=MD_EXTENSIONS)
        body = re.sub(r'(<h[1-6] id=")', rf"\g<1>d{i}-", body)
        body = re.sub(r'href="((?:README|0\d_[A-Za-z_]+)\.md)"',
                      lambda m: 'href="#doc-%d"' % ([d[0] for d in DOCS].index(m.group(1)) + 1), body)
        body = body.replace("<li>[ ] ", '<li class="task"><input type="checkbox" class="ck"> ')
        body = body.replace("<li>[x] ", '<li class="task done"><input type="checkbox" class="ck" checked> ')
        body = re.sub(r"\[ \]", '<input type="checkbox" class="ck">', body)
        body = re.sub(r"\[x\]", '<input type="checkbox" class="ck" checked>', body)
        body = body.replace("<td>☐</td>", '<td class="ck"><input type="checkbox" class="ck"></td>')
        body = body.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
        nav = [{"lvl": int(l), "id": hid, "label": strip_tags(lab)}
               for l, hid, lab in re.findall(r'<h([12]) id="([^"]+)"[^>]*>(.*?)</h\1>', body, flags=re.S)]
        docs_html.append(f'<section class="doc" id="doc-{i}"><span class="doctag">{tag}</span>\n{body}\n</section>')
        docs_meta.append({"tag": tag, "file": fname, "nav": nav})
    return "\n".join(docs_html), docs_meta


# ---------------------------------------------------------------- template
TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GATE 2027 · CSE + DA — Plan & Tracker</title>
<style>
:root{
  --bg:#f7f7f8; --card:#ffffff; --ink:#191b1f; --muted:#6b7280; --line:#e6e7eb; --line2:#eef0f2;
  --accent:#4f46e5; --accent-soft:#eef0fe; --ok:#059669; --ok-soft:#e7f6f0;
  --t1:#dc2626; --t2:#ea580c; --t3:#d97706; --t4:#059669;
  --shadow:0 1px 2px rgba(16,24,40,.05);
  --radius:14px;
}
html.dark{
  --bg:#0e1016; --card:#161a23; --ink:#e8eaf0; --muted:#98a0b3; --line:#262b38; --line2:#20242f;
  --accent:#8b93ff; --accent-soft:#232b47; --ok:#34d399; --ok-soft:#10332a;
  --shadow:none;
}
*{box-sizing:border-box}
body{margin:0;font:15px/1.6 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink)}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
button{font:inherit;cursor:pointer}
input,select{font:inherit;color:var(--ink)}
code{background:var(--line2);padding:1px 5px;border-radius:5px;font-size:.88em}

/* ---------- header ---------- */
header{position:fixed;top:0;left:0;right:0;height:54px;z-index:60;display:flex;align-items:center;gap:12px;
  padding:0 18px;background:color-mix(in srgb,var(--card) 88%,transparent);backdrop-filter:blur(10px);
  border-bottom:1px solid var(--line)}
.brand{font-weight:700;font-size:14.5px;white-space:nowrap}
.brand small{color:var(--muted);font-weight:500}
.seg{display:flex;background:var(--line2);border-radius:10px;padding:3px;gap:2px}
.seg button{border:none;background:none;border-radius:8px;padding:4px 14px;font-size:13px;font-weight:600;color:var(--muted)}
.seg button.on{background:var(--card);color:var(--ink);box-shadow:var(--shadow)}
.hspace{flex:1}
.hchip{display:inline-flex;align-items:center;gap:6px;background:var(--accent-soft);color:var(--accent);
  border-radius:999px;padding:4px 12px;font-size:12.5px;font-weight:600;white-space:nowrap;font-variant-numeric:tabular-nums}
.hchip.warn{background:#fdf0e3;color:#b45309}
html.dark .hchip.warn{background:#3a2c07;color:#fbbf24}
.hbtn{border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:9px;padding:5px 10px;font-size:13px}
.hbtn:hover{border-color:var(--accent);color:var(--accent)}
@media(max-width:860px){.hchip.hideS{display:none}}

/* ---------- tracker layout ---------- */
main{padding:70px 0 90px}
.wrap{max-width:1120px;margin:0 auto;padding:0 22px}
.ttabs{display:flex;gap:4px;overflow-x:auto;padding:18px 0 14px;scrollbar-width:none}
.ttabs::-webkit-scrollbar{display:none}
.ttabs button{border:none;background:none;color:var(--muted);font-weight:600;font-size:13.5px;
  padding:7px 15px;border-radius:999px;white-space:nowrap}
.ttabs button.on{background:var(--accent-soft);color:var(--accent)}
.tpane{display:none}
.tpane.on{display:block;animation:fade .18s ease}
@keyframes fade{from{opacity:0;transform:translateY(3px)}to{opacity:1}}

/* ---------- cards & common ---------- */
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow)}
.pad{padding:20px 22px}
.h1{font-size:22px;font-weight:700;margin:2px 0 4px}
.h2{font-size:16px;font-weight:700;margin:0 0 10px}
.sub{color:var(--muted);font-size:13.5px}
.chip{display:inline-block;font-size:11.5px;font-weight:700;border-radius:6px;padding:2px 8px;letter-spacing:.02em}
.badge{display:inline-block;font-size:11.5px;font-weight:700;border-radius:999px;padding:2px 9px}
.b1{background:color-mix(in srgb,var(--t1) 12%,transparent);color:var(--t1)}
.b2{background:color-mix(in srgb,var(--t2) 12%,transparent);color:var(--t2)}
.b3{background:color-mix(in srgb,var(--t3) 14%,transparent);color:var(--t3)}
.b4{background:color-mix(in srgb,var(--t4) 12%,transparent);color:var(--t4)}
.okb{background:var(--ok-soft);color:var(--ok)}
.statgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:14px 0 20px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px}
.stat b{display:block;font-size:21px;font-variant-numeric:tabular-nums}
.stat span{font-size:12px;color:var(--muted);font-weight:600}
.bar{height:5px;background:var(--line2);border-radius:5px;overflow:hidden;margin-top:8px}
.bar i{display:block;height:100%;background:var(--ok);border-radius:5px;transition:width .3s}

/* checkboxes */
input[type=checkbox].t{width:16px;height:16px;accent-color:var(--ok);cursor:pointer;flex:none;margin:0}
label.act{display:flex;gap:9px;align-items:flex-start;padding:6px 0;cursor:pointer;font-size:14px}
label.act input{margin-top:3px}
label.act.done span{color:var(--muted);text-decoration:line-through;text-decoration-color:color-mix(in srgb,var(--muted) 40%,transparent)}
.toggle{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--line);border-radius:999px;
  padding:7px 15px;font-size:13.5px;font-weight:600;background:var(--card);color:var(--muted);user-select:none}
.toggle input{display:none}
.toggle .dot{width:9px;height:9px;border-radius:50%;background:var(--line)}
.toggle.on{border-color:var(--ok);background:var(--ok-soft);color:var(--ok)}
.toggle.on .dot{background:var(--ok)}

/* ---------- today ---------- */
.daynav{display:flex;align-items:center;gap:10px;margin:14px 0}
.daynav button{border:1px solid var(--line);background:var(--card);border-radius:9px;padding:5px 12px;font-size:13px}
.daynav button:hover{border-color:var(--accent);color:var(--accent)}
.daynav .d{font-weight:700;font-size:15px}
.weekstrip{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0 18px}
.wpill{flex:1;min-width:96px;border:1px solid var(--line);border-radius:10px;padding:7px 10px;text-align:center;cursor:pointer;background:var(--card)}
.wpill.cur{border-color:var(--accent);background:var(--accent-soft)}
.wpill small{display:block;font-size:10.5px;color:var(--muted);font-weight:700}
.wpill .dnum{font-size:12.5px;font-weight:600;font-variant-numeric:tabular-nums}
.wpill .dot{width:7px;height:7px;border-radius:50%;background:var(--line);margin:5px auto 0}
.wpill .dot.part{background:var(--t3)}
.wpill .dot.full{background:var(--ok)}
.twocol{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:760px){.twocol{grid-template-columns:1fr}}
.actgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px;margin-top:14px}
.actcard h3{margin:0 0 4px;font-size:13px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
.toggles{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}

/* ---------- tables ---------- */
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:var(--radius);background:var(--card);box-shadow:var(--shadow)}
table{border-collapse:collapse;width:100%;font-size:13.5px}
th{position:sticky;top:0;background:var(--card);text-align:left;font-size:11.5px;text-transform:uppercase;
  letter-spacing:.05em;color:var(--muted);padding:11px 14px;border-bottom:1px solid var(--line);white-space:nowrap}
td{padding:10px 14px;border-bottom:1px solid var(--line2);vertical-align:middle}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover{background:color-mix(in srgb,var(--accent-soft) 45%,transparent)}
td.c{text-align:center}
td input[type=checkbox].t{vertical-align:middle}
td input[type=text],td input[type=number]{width:100%;min-width:64px;border:1px solid var(--line);border-radius:7px;
  padding:4px 8px;background:var(--bg);font-size:13px}
td input:focus{outline:2px solid var(--accent-soft);border-color:var(--accent)}
.subname{font-weight:600}

/* ---------- topics ---------- */
.filters{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0 16px}
.filters select,.filters input{border:1px solid var(--line);border-radius:9px;padding:6px 10px;background:var(--card);font-size:13px}
.subjhead{display:flex;align-items:center;gap:12px;margin:22px 0 8px}
.subjhead h3{margin:0;font-size:15px}
.subjhead .bar{flex:1;margin:0}
.topicrow{display:flex;align-items:center;gap:10px;padding:8px 12px;border-bottom:1px solid var(--line2);font-size:14px}
.topicrow:last-child{border-bottom:none}
.topicrow .tt{flex:1}
.topicrow .stages{display:flex;gap:4px}
.stage{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:8px;
  border:1px solid var(--line);background:var(--card);cursor:pointer;font-size:10.5px;font-weight:700;color:var(--muted)}
.stage.on{background:var(--ok);border-color:var(--ok);color:#fff}

/* ---------- plan docs (keep, restyled) ---------- */
#view-plan{display:none}
body[data-view=plan] #view-plan{display:block}
body[data-view=plan] #view-tracker{display:none}
#view-tracker{display:block}
nav#side{position:fixed;top:54px;bottom:0;left:0;width:290px;overflow-y:auto;background:var(--card);
  border-right:1px solid var(--line);padding:14px 12px 30px;z-index:40}
body[data-view=plan] main{margin-left:290px;padding-left:0;padding-right:0}
body[data-view=plan] .wrap{padding:0 22px;max-width:none;margin:0}
@media(max-width:1020px){
  nav#side{display:none}
  body[data-view=plan] main{margin-left:0}
}
section.doc{max-width:1020px;margin:0 auto 26px;background:var(--card);border:1px solid var(--line);
  border-radius:var(--radius);box-shadow:var(--shadow);padding:28px 34px 40px}
.doctag{display:inline-block;font-size:11px;letter-spacing:.09em;text-transform:uppercase;font-weight:700;
  color:var(--accent);background:var(--accent-soft);border-radius:6px;padding:3px 9px;margin-bottom:8px}
h1{font-size:24px;line-height:1.3;margin:10px 0 14px}
h2{font-size:18.5px;margin:32px 0 10px;padding-bottom:6px;border-bottom:1px solid var(--line)}
h3{font-size:15.5px;margin:22px 0 8px}
h1,h2,h3{scroll-margin-top:70px}
p{margin:9px 0}
ul,ol{padding-left:24px;margin:8px 0}
li{margin:3.5px 0}
li.task{list-style:none;margin-left:-22px}
li.task input{width:16px;height:16px;accent-color:var(--ok);cursor:pointer;vertical-align:-3px;margin-right:7px}
li.task.done{color:var(--muted);text-decoration:line-through;text-decoration-color:color-mix(in srgb,var(--muted) 40%,transparent)}
blockquote{margin:14px 0;padding:10px 16px;border-left:4px solid var(--accent);background:var(--accent-soft);
  border-radius:0 8px 8px 0;color:var(--muted)}
hr{border:none;border-top:1px solid var(--line);margin:24px 0}
td.ck{text-align:center}
#navsearch{width:100%;padding:8px 11px;border:1px solid var(--line);border-radius:9px;background:var(--bg);
  color:var(--ink);font-size:13.5px;margin-bottom:10px}
.navdoc{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:16px 4px 6px;font-weight:700}
nav#side ul{list-style:none;margin:0;padding:0}
nav#side li a{display:block;padding:4px 9px;border-radius:7px;font-size:13.5px;color:var(--ink)}
nav#side li a:hover{background:var(--accent-soft);text-decoration:none}
nav#side li a.active{background:var(--accent-soft);color:var(--accent);font-weight:600}
nav#side li.l2 a{padding-left:22px;font-size:12.8px;color:var(--muted)}
.docprog{margin:2px 0 10px}
.docprog .lbl{font-size:11px;color:var(--muted);display:flex;justify-content:space-between}

#top{position:fixed;right:22px;bottom:22px;border-radius:999px;width:42px;height:42px;border:1px solid var(--line);
  background:var(--card);color:var(--accent);font-size:18px;box-shadow:var(--shadow);display:none;z-index:45}
/* ---------- master checklist + modal ---------- */
.tdot{width:11px;height:11px;border-radius:50%;flex:none}
.t1{background:var(--t1)}.t2{background:var(--t2)}.t3{background:var(--t3)}.t4{background:var(--t4)}
.mcname{cursor:pointer}
.mcname:hover{color:var(--accent);text-decoration:underline}
.mcnote{font-size:12px;color:var(--muted)}
.mclabels{display:inline-flex;gap:10px;margin-left:auto;font-size:10.5px;color:var(--muted);font-weight:700}
#modal{position:fixed;inset:0;z-index:100;display:flex;align-items:center;justify-content:center;padding:20px}
#modal[hidden]{display:none}
.mback{position:absolute;inset:0;background:rgba(8,12,24,.55)}
.mcard{position:relative;background:var(--card);border:1px solid var(--line);border-radius:16px;
  max-width:680px;width:100%;max-height:84vh;overflow-y:auto;box-shadow:0 24px 70px rgba(0,0,0,.35)}
.mhead{position:sticky;top:0;background:var(--card);padding:18px 54px 12px 22px;border-bottom:1px solid var(--line);z-index:2}
.mbody{padding:16px 22px 24px}
.msec{margin:16px 0 6px;font-size:11.5px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
.mx{position:absolute;right:14px;top:14px;border:1px solid var(--line);background:var(--card);
  border-radius:8px;width:30px;height:30px;color:var(--muted)}
.mx:hover{color:var(--ink);border-color:var(--accent)}
.mpill{display:inline-block;background:var(--accent-soft);color:var(--accent);border-radius:999px;
  padding:3px 10px;font-size:12px;font-weight:700;margin:2px 6px 2px 0}
.mnote{color:var(--muted);font-size:12.5px;margin:1px 0 0 25px}
.mtest{background:var(--ok-soft);border-radius:10px;padding:10px 14px}
.mtest ul{margin:4px 0 0}
.mhours{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px;margin-top:8px}
.mhours label{font-size:12.5px;color:var(--muted);display:block}
.mhours input{width:100%;border:1px solid var(--line);border-radius:8px;padding:5px 9px;background:var(--bg);margin-top:3px}
.mfocus{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px;margin-top:8px}
.mfocus input{width:100%;border:1px solid var(--line);border-radius:8px;padding:6px 10px;background:var(--bg)}

@media print{
  header,nav#side,.ttabs,#top,.daynav{display:none!important}
  main{padding:0!important;margin:0!important}
  .tpane{display:none!important}
  .tpane.on{display:block!important}
  .card,.tw,section.doc{border:none;box-shadow:none}
  body{background:#fff}
}
</style>
</head>
<body data-view="tracker">
<header>
  <div class="brand">GATE 2027 <small>· CSE + DA</small></div>
  <div class="seg">
    <button id="v-tracker" class="on">Tracker</button>
    <button id="v-plan">Plan A–O</button>
  </div>
  <div class="hspace"></div>
  <span class="hchip warn hideS" id="deadline" hidden></span>
  <span class="hchip hideS" id="countdown"></span>
  <span class="hchip" id="overall">0%</span>
  <button class="hbtn" id="theme" title="theme">◐</button>
  <button class="hbtn" id="print" title="print">🖨</button>
  <button class="hbtn" id="bkexp" title="export progress backup (JSON)">⇩</button>
  <button class="hbtn" id="bkimp" title="import progress backup">⤒</button>
  <input type="file" id="bkfile" accept=".json,application/json" style="display:none">
</header>

<main>
  <!-- ============================== TRACKER VIEW ============================== -->
  <div id="view-tracker">
    <div class="wrap">
      <nav class="ttabs" id="ttabs">
        <button data-pane="t-today" class="on">Today</button>
        <button data-pane="t-daily">Daily Plan</button>
        <button data-pane="t-topics">Topics</button>
        <button data-pane="t-review">Review Queue</button>
        <button data-pane="t-mc">Master Checklist</button>
        <button data-pane="t-pyq">PYQ Tracker</button>
        <button data-pane="t-mocks">Mock Tests</button>
        <button data-pane="t-time">Time Structure</button>
        <button data-pane="t-guide">Guide</button>
      </nav>

      <section class="tpane on" id="t-today"></section>
      <section class="tpane" id="t-daily"></section>
      <section class="tpane" id="t-topics"></section>
      <section class="tpane" id="t-review"></section>
      <section class="tpane" id="t-mc"></section>
      <section class="tpane" id="t-pyq"></section>
      <section class="tpane" id="t-mocks"></section>
      <section class="tpane" id="t-time"></section>
      <section class="tpane" id="t-guide"></section>
    </div>
  </div>

  <!-- ============================== PLAN VIEW ============================== -->
  <div id="view-plan">
    <nav id="side">
      <input id="navsearch" type="search" placeholder="Filter sections…" autocomplete="off">
      <div id="navtree"></div>
    </nav>
    <div class="wrap">
      {DOCS}
    </div>
  </div>
</main>

<button id="top" title="back to top">↑</button>

<div id="modal" hidden>
  <div class="mback"></div>
  <div class="mcard"><div class="mhead" id="mhead"></div><div class="mbody" id="mbody"></div></div>
</div>

<script>
"use strict";
const DATA = {DATA_JSON};

/* ---------------- state ---------------- */
const LS="gate-tracker-v1", LS_THEME="gate-theme", LS_CK="gateplan-ck-v1";
let store;
try{ store = JSON.parse(localStorage.getItem(LS)||"{}"); }catch(e){ store = {}; }
store.d ||= {}; store.t ||= {}; store.p ||= {}; store.w ||= {}; store.m ||= {}; store.mc ||= {}; store.tl ||= {}; store.mcl ||= {};
const save = () => localStorage.setItem(LS, JSON.stringify(store));

/* ---------------- theme / header ---------------- */
if(localStorage.getItem(LS_THEME)==="dark"||(!localStorage.getItem(LS_THEME)&&matchMedia("(prefers-color-scheme:dark)").matches))
  document.documentElement.classList.add("dark");
document.getElementById("theme").onclick=()=>{document.documentElement.classList.toggle("dark");
  localStorage.setItem(LS_THEME,document.documentElement.classList.contains("dark")?"dark":"light");};
document.getElementById("print").onclick=()=>window.print();
const EXAM=new Date("2027-02-06T09:00:00"), DEADLINE=new Date("2026-10-12T23:59:59");
document.getElementById("countdown").textContent="🎯 "+Math.ceil((EXAM-Date.now())/864e5)+" days to GATE";
const dl=document.getElementById("deadline");
if(Date.now()<DEADLINE.getTime()){dl.hidden=false;dl.textContent="⚠ Register by 12 Oct";}

/* ---------------- helpers ---------------- */
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const fmtDate=iso=>{const d=new Date(iso+"T00:00:00");return d.toLocaleDateString("en-GB",{weekday:"short",day:"numeric",month:"short"});};
const PHASE_SHORT=p=>p.replace("Phase ","P").replace(" – ","·");

/* ---------------- tracker state helpers ---------------- */
const actKey=(date,ci,li)=>date+"|"+ci+"|"+li;
const togKey=(date,ti)=>date+"|T"+ti;
const topicKey=x=>x.exam+x.subject+(x.topic||"");
/* twins: shared CS<->DA syllabus topics — ticks mirror both ways */
const TWIN={}; (DATA.topics||[]).forEach(t=>{if(t.twin)TWIN[topicKey(t)]=t.twin;});
const TBYKEY={}; (DATA.topics||[]).forEach(t=>{TBYKEY[topicKey(t)]=t;});
function todayISO(){const d=new Date();
  return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");}

/* central stage mutator (timeline + twin mirror + PYQ-tracker credit) */
function setT307(k, si, val){
  const s=store.t[k]||(store.t[k]=[0,0,0,0,0]);
  s[si]=val;
  if(si<4&&!s[si]&&s[4]) s[4]=0;                 // un-master if a lower stage is unticked
  if(si===4&&s[4]) for(let z=0;z<4;z++) s[z]=1;  // mastering completes all stages
  const date=todayISO();
  for(let z=0;z<5;z++) if(s[z]&&!store.tl[k+"|"+z]) store.tl[k+"|"+z]=date;
  const tw=TWIN[k];                              // shared topic: merge progress upward
  if(tw){ const w=store.t[tw]||(store.t[tw]=[0,0,0,0,0]);
    for(let z=0;z<5;z++) if(s[z]){ w[z]=1; if(!store.tl[tw+"|"+z]) store.tl[tw+"|"+z]=date; }
    store.t[tw]=w; }
  maybeCreditFirstPass(k);
}
function setMC(g, r, si, val){
  store.mc["g"+g+"r"+r+"t"+si]=val?1:0;
  if(val){ const lk="g"+g+"r"+r+"|"+si; if(!store.mcl[lk]) store.mcl[lk]=todayISO(); }
}
/* PYQ Tracker hookup: subject first-pass auto-ticks when every topic of the subject reaches PYQ stage */
function maybeCreditFirstPass(k){
  const t=TBYKEY[k]; if(!t) return;
  const peers=(DATA.topics||[]).filter(x=>x.exam===t.exam&&x.subject===t.subject);
  if(!peers.length) return;
  if(peers.every(x=>{const s=store.t[topicKey(x)];return s&&s[1];})){
    const pk=t.exam+t.subject; const p=store.p[pk]||(store.p[pk]=[0,0,0]);
    if(!p[0]) p[0]=1;
  }
}
/* reverse sync: tracker stage tick -> Today status pill on the day that scheduled the topic */
const REV={t:{},mc:{}};
Object.entries(DATA.linkMap||{}).forEach(([date,e])=>{
  ["cs","da"].forEach(side=>{ const en=e[side]; if(!en) return;
    (en.t||[]).forEach(k=>{ (REV.t[k]||(REV.t[k]=[])).push(date); });
    (en.mc||[]).forEach(p=>{ const k=p[0]+":"+p[1]; (REV.mc[k]||(REV.mc[k]=[])).push(date); });
  });
});
function pillDateFor(dates){ const today=todayISO();
  if(dates.includes(today)) return today;
  const past=dates.filter(d=>d<=today).sort(); return past.length?past[0]:dates.slice().sort()[0]; }
function reverseTick(k, si){ if(si>2) return;
  const ds=REV.t[k]; if(ds){ const d=pillDateFor(ds); const tk=d+"|T"+si; if(!store.d[tk]) store.d[tk]=1; } }
function reverseTickMC(g, r, si){ if(si>2) return;
  const ds=REV.mc[g+":"+r]; if(ds){ const d=pillDateFor(ds); const tk=d+"|T"+si; if(!store.d[tk]) store.d[tk]=1; } }

/* Today status pill -> linked stages in Topics(307) + Master Checklist (forward sync) */
function syncToday(date, ti){
  if(ti>2) return;
  const lm=(DATA.linkMap||{})[date]; if(!lm) return;
  ["cs","da"].forEach(side=>{
    const e=lm[side]; if(!e) return;
    (e.t||[]).forEach(k=>setT307(k, ti, 1));
    (e.mc||[]).forEach(p=>setMC(p[0], p[1], ti, 1));
  });
  save(); updateOverall();
  if(document.getElementById("t-topics").classList.contains("on")) renderTopics();
  if(document.getElementById("t-mc").classList.contains("on")) renderCheck();
}
const dayActs=d=>d.act.reduce((n,a)=>n+a.length,0);
function dayProgress(d){
  let total=dayActs(d)+5, done=0;
  d.act.forEach((lines,ci)=>lines.forEach((_,li)=>{if(store.d[actKey(d.date,ci,li)])done++;}));
  for(let ti=0;ti<5;ti++) if(store.d[togKey(d.date,ti)])done++;
  return {done,total,pct:total?done/total:0};
}
function topicProgress(list){
  let n=0;
  list.forEach(t=>{const s=store.t[topicKey(t)];if(s&&s[4])n++;});
  return n;
}
function updateOverall(){
  let done=0,total=0;
  DATA.days.forEach(d=>{const p=dayProgress(d);done+=p.done;total+=p.total;});
  DATA.topics.forEach(t=>{const s=store.t[topicKey(t)]||[0,0,0,0,0];s.forEach(v=>{if(v)done++;});total+=5;});
  DATA.pyq.forEach(p=>{for(let i=0;i<3;i++){if(store.p[topicKey(p)]?.[i])done++;}total+=3;});
  if(DATA.checklist)DATA.checklist.groups.forEach((G,gi)=>G.rows.forEach((R,ri)=>{
    for(let s=0;s<4;s++)if(store.mc[mcStageKey(gi,ri,s)])done++;
    total+=4;
    R.subs.forEach((_,i)=>{if(store.mc[mcSubKey(gi,ri,i)])done++;});
    total+=R.subs.length;}));
  Object.values(store.w).forEach(w=>{done+=(w.test?1:0)+(w.mr?1:0);total+=2;});
  Object.values(store.m).forEach(m=>{for(let i=0;i<5;i++)if(m["e"+i])done++;total+=5;});
  $("#overall").textContent=(total?Math.round(100*done/total):0)+"%";
}

/* ---------------- TODAY pane ---------------- */
let curDate=(()=>{const t=new Date();
  const iso=t.getFullYear()+"-"+String(t.getMonth()+1).padStart(2,"0")+"-"+String(t.getDate()).padStart(2,"0");
  if(DATA.days.some(d=>d.date===iso))return iso;
  const past=DATA.days.filter(d=>d.date<=iso);return past.length?past[past.length-1].date:DATA.days[0].date;})();
const ACT_NAMES=["Previous-Year Questions","Maths / Statistics Revision","General Aptitude","Spaced Revision","Mistake Log","Test / Assessment"];

function renderToday(){
  const i=DATA.days.findIndex(d=>d.date===curDate), d=DATA.days[i], p=dayProgress(d);
  const pct=Math.round(100*p.pct);
  const ring=`<svg width="76" height="76" viewBox="0 0 76 76"><circle cx="38" cy="38" r="32" fill="none"
    stroke="var(--line2)" stroke-width="7"/><circle cx="38" cy="38" r="32" fill="none" stroke="${pct===100?"var(--ok)":"var(--accent)"}"
    stroke-width="7" stroke-linecap="round" stroke-dasharray="${201.06*pct/100} 201.06"
    transform="rotate(-90 38 38)"/><text x="38" y="43" text-anchor="middle" font-size="17" font-weight="700"
    fill="var(--ink)">${pct}%</text></svg>`;
  const actHtml=d.act.map((lines,ci)=>lines.length?`
    <div class="card pad actcard"><h3>${ACT_NAMES[ci]}</h3>
      ${lines.map((ln,li)=>`<label class="act ${store.d[actKey(d.date,ci,li)]?"done":""}">
        <input type="checkbox" class="t" data-k="${actKey(d.date,ci,li)}" ${store.d[actKey(d.date,ci,li)]?"checked":""}>
        <span>${esc(ln)}</span></label>`).join("")}
    </div>`:"").join("");
  const toggles=["Theory done","PYQ done","Revision done","Test done","Day complete"].map((n,ti)=>
    `<label class="toggle ${store.d[togKey(d.date,ti)]?"on":""}"><input type="checkbox" data-tk="${togKey(d.date,ti)}" ${store.d[togKey(d.date,ti)]?"checked":""}>
     <span class="dot"></span>${n}</label>`).join("");
  // week strip
  const weekDays=DATA.days.filter(x=>x.week===d.week);
  const strip=weekDays.map(x=>{const pr=dayProgress(x);
    const cls=pr.pct>=1?"full":(pr.done>0?"part":"");
    return `<div class="wpill ${x.date===curDate?"cur":""}" data-date="${x.date}">
      <small>${x.day.slice(0,3)}</small><span class="dnum">${x.date.slice(8)}/${x.date.slice(5,7)}</span>
      <div class="dot ${cls}"></div></div>`;}).join("");
  const bullets=s=>esc(s).split("\n").filter(Boolean).map(x=>`<div>• ${x.replace(/^•\s*/,"")}</div>`).join("");
  const trk=d.track||"dual";
  let focusHtml="";
  if(trk==="shared"){
    focusHtml=`<div class="card pad"><div class="h2">Today's focus — shared topic <span class="badge okb">counts for both papers</span></div>
      <div style="font-size:16.5px;font-weight:700">${esc(d.cs)}</div>
      <div class="sub" style="margin-top:6px">${bullets(d.csT)}</div></div>`;
  } else if(trk==="CS"||trk==="DA"){
    const nm=trk==="CS"?"Computer Science":"Data Science & AI";
    const sub=trk==="CS"?d.cs:d.da, txt=trk==="CS"?d.csT:d.daT;
    focusHtml=`<div class="card pad"><div class="h2">Today's focus — ${trk} only</div>
      <div style="font-size:16.5px;font-weight:700">${esc(sub)}</div>
      <div class="sub" style="margin-top:6px">${bullets(txt)}</div>
      <div class="sub" style="margin-top:10px">One track today — the flow continues without switching subjects.</div></div>`;
  } else if(trk==="rest"){
    focusHtml=`<div class="card pad"><div class="h2">Today's focus</div>
      <div style="font-size:16.5px;font-weight:700">${esc(d.cs||d.da||"—")}</div>
      <div class="sub" style="margin-top:6px">${bullets(d.csT||d.daT||"")}</div></div>`;
  } else {
    focusHtml=`<div class="twocol">
      <div class="card pad"><div class="h2">Computer Science</div>
        <div style="font-size:16.5px;font-weight:700">${esc(d.cs)}</div>
        <div class="sub" style="margin-top:6px">${bullets(d.csT)}</div></div>
      <div class="card pad"><div class="h2">Data Science &amp; AI</div>
        <div style="font-size:16.5px;font-weight:700">${esc(d.da)}</div>
        <div class="sub" style="margin-top:6px">${bullets(d.daT)}</div></div>
    </div>`;
  }
  $("#t-today").innerHTML=`
    <div class="daynav">
      <button id="dprev">← Prev</button>
      <span class="d">${fmtDate(d.date)} · ${d.day}</span>
      <span class="badge okb">Week ${d.week}</span><span class="badge b2">${esc(PHASE_SHORT(d.phase))}</span>
      <span class="sub">Day ${i+1} of ${DATA.days.length}</span>
      <div class="hspace"></div>${ring}
      <button id="dnext">Next →</button>
    </div>
    <div class="weekstrip">${strip}</div>
    ${focusHtml}
    <div class="actgrid">${actHtml}</div>
    <div class="card pad" style="margin-top:14px"><div class="h2">Status</div><div class="toggles">${toggles}</div>
      <div class="sub" style="margin-top:12px">🔗 Ticking <b>Theory / PYQ / Revision done</b> also auto-ticks the matching stages of today's topics in <b>Topics</b> and <b>Master Checklist</b> — shared CS↔DA topics credit both papers. Un-tick those stages manually in the trackers if needed.</div></div>`;
  $("#dprev").onclick=()=>{const j=Math.max(0,i-1);curDate=DATA.days[j].date;renderToday();};
  $("#dnext").onclick=()=>{const j=Math.min(DATA.days.length-1,i+1);curDate=DATA.days[j].date;renderToday();};
  $$("#t-today .wpill").forEach(el=>el.onclick=()=>{curDate=el.dataset.date;renderToday();});
  bindChecks("#t-today");
}

/* ---------------- DAILY PLAN pane ---------------- */
function renderDaily(){
  const weeks=[...new Set(DATA.days.map(d=>d.week))];
  $("#t-daily").innerHTML=weeks.map(w=>{
    const ds=DATA.days.filter(d=>d.week===w);
    const done=ds.filter(d=>dayProgress(d).pct>=1).length;
    const rows=ds.map(d=>{const p=dayProgress(d);
      const trk=d.track||"dual";
      let focusCell;
      if(trk==="shared"){
        focusCell=`<span class="badge okb">⇄ shared</span> <span class="subname">${esc(d.cs)}</span> <span class="sub">— ${esc((d.csT||"").split("\n")[0].replace(/^•\s*/,"").slice(0,52))}</span>`;
      } else if(trk==="CS"||trk==="DA"){
        const sub=trk==="CS"?d.cs:d.da, first=(trk==="CS"?d.csT:d.daT||"").split("\n")[0]||"";
        focusCell=`<span class="badge ${trk==="CS"?"b2":"b3"}">${trk}</span> <span class="subname">${esc(sub)}</span> <span class="sub">— ${esc(first.replace(/^•\s*/,"").slice(0,52))}</span>`;
      } else if(trk==="rest"){
        focusCell=`<span class="subname">${esc(d.cs||d.da||"—")}</span>`;
      } else {
        focusCell=`<span class="subname">${esc(d.cs)}</span> <span class="sub">/</span> <span class="subname">${esc(d.da)}</span>`;
      }
      return `<tr data-date="${d.date}" style="cursor:pointer">
        <td style="white-space:nowrap">${fmtDate(d.date)}</td>
        <td>${esc(d.day.slice(0,3))}</td>
        <td><span class="badge b2">${esc(PHASE_SHORT(d.phase))}</span></td>
        <td>${focusCell}</td>
        <td class="c" style="min-width:90px"><div class="bar" style="width:80px;margin:0 auto"><i style="width:${Math.round(100*p.pct)}%"></i></div></td>
      </tr>`;}).join("");
    return `<div class="subjhead"><h3>Week ${w}</h3><span class="sub">${done}/${ds.length} days complete</span>
      <div class="bar" style="max-width:220px"><i style="width:${Math.round(100*done/ds.length)}%"></i></div></div>
      <div class="tw"><table><thead><tr><th>Date</th><th>Day</th><th>Phase</th><th>Today's focus</th><th class="c">Done</th></tr></thead>
      <tbody>${rows}</tbody></table></div>`;
  }).join("");
  $$("#t-daily tbody tr").forEach(tr=>tr.onclick=()=>{curDate=tr.dataset.date;setView("tracker");showPane("t-today");renderToday();});
}

/* ---------------- TOPICS pane ---------------- */
const STAGES=["Theory","PYQ","2nd pass","Mistakes","Mastered"];
let topicFilter={exam:"all",subject:"all",tier:"all",q:"",status:"all"};
function topicState(t){return store.t[topicKey(t)]||[0,0,0,0,0];}
function renderTopics(){
  const subjects=[...new Set(DATA.topics.map(t=>t.subject))].sort();
  $("#t-topics").innerHTML=`
    <div class="card pad" style="margin-bottom:6px">
      <div class="h2">Complete Topic Checklist <span class="sub">(${DATA.topics.length} topics · tick a stage when done; Mastered only after all four)</span></div>
      <div class="filters">
        <select id="f-exam"><option value="all">Both papers</option><option value="CS">GATE CS</option><option value="DA">GATE DA</option></select>
        <select id="f-subject"><option value="all">All subjects</option>${subjects.map(s=>`<option>${esc(s)}</option>`).join("")}</select>
        <select id="f-tier"><option value="all">All tiers</option><option value="1">Tier 1</option><option value="2">Tier 2</option><option value="3">Tier 3</option><option value="4">Tier 4</option></select>
        <select id="f-status"><option value="all">Any status</option><option value="done">Mastered</option><option value="progress">In progress</option><option value="todo">Not started</option></select>
        <input id="f-q" type="search" placeholder="Search topic…">
      </div>
    </div>
    <div id="topiclist"></div>`;
  const renderList=()=>{
    const f=topicFilter;
    const vis=DATA.topics.filter(t=>
      (f.exam==="all"||t.exam===f.exam)&&(f.subject==="all"||t.subject===f.subject)&&(f.tier==="all"||t.tier===+f.tier)&&
      (!f.q||t.topic.toLowerCase().includes(f.q.toLowerCase()))&&
      (f.status==="all"||(f.status==="done"?topicState(t)[4]===1:f.status==="progress"?(topicState(t).some(v=>v)&&!topicState(t)[4]):!topicState(t).some(v=>v))));
    const bySub={};vis.forEach(t=>{(bySub[t.subject+"|"+t.exam] ||= []).push(t);});
    $("#topiclist").innerHTML=Object.entries(bySub).sort().map(([key,list])=>{
      const [sub,exam]=key.split("|");
      const mastered=topicProgress(list);
      return `<div class="subjhead"><span class="badge ${exam==="CS"?"b2":"b3"}">${exam}</span><h3>${esc(sub)}</h3>
        <span class="sub">${mastered}/${list.length} mastered</span>
        <div class="bar" style="max-width:200px"><i style="width:${Math.round(100*mastered/list.length)}%"></i></div></div>
      <div class="card">${list.map(t=>{const s=topicState(t),k=topicKey(t);
        return `<div class="topicrow">
          <span class="badge b${t.tier}">T${t.tier}</span>
          ${TWIN[k]?'<span class="badge okb" title="shared CS↔DA topic — stages mirror to the other paper" style="font-size:10px">⇄</span>':""}
          <span class="tt">${esc(t.topic)}</span>
          <span class="stages">${STAGES.map((nm,si)=>`<span class="stage ${s[si]?"on":""}" data-tk="${esc(k)}" data-si="${si}" title="${nm}">${si+1}</span>`).join("")}</span>
        </div>`;}).join("")}</div>`;
    }).join("")||`<p class="sub" style="padding:20px">No topics match these filters.</p>`;
    $$("#topiclist .stage").forEach(el=>el.onclick=()=>{
      const k=el.dataset.tk, si=+el.dataset.si;
      const t=DATA.topics.find(x=>topicKey(x)===k);
      const s=store.t[k]||(store.t[k]=[0,0,0,0,0]);
      const nv=s[si]?0:1;
      setT307(k, si, nv);
      if(nv) reverseTick(k, si);
      save();renderTopics();
    });
  };
  $("#f-exam").onchange=e=>{topicFilter.exam=e.target.value;renderList();};
  $("#f-subject").onchange=e=>{topicFilter.subject=e.target.value;renderList();};
  $("#f-tier").onchange=e=>{topicFilter.tier=e.target.value;renderList();};
  $("#f-status").onchange=e=>{topicFilter.status=e.target.value;renderList();};
  $("#f-q").oninput=e=>{topicFilter.q=e.target.value;renderList();};
  $("#f-exam").value=topicFilter.exam;$("#f-subject").value=topicFilter.subject;
  $("#f-tier").value=topicFilter.tier;$("#f-status").value=topicFilter.status;$("#f-q").value=topicFilter.q;
  renderList();
}

/* ---------------- PYQ pane ---------------- */
function renderPyq(){
  $("#t-pyq").innerHTML=`
    <div class="card pad" style="margin-bottom:14px"><div class="h2">Previous-Year Question Tracker
      <span class="sub">— first pass topic-wise, second pass on starred questions, errors re-solved on day 7 and day 21</span></div></div>
    <div class="tw"><table><thead><tr><th>Paper</th><th>Subject</th><th>First pass</th><th>Second pass</th><th>Error re-solve</th><th>Target accuracy</th><th>Notes</th></tr></thead><tbody>
    ${DATA.pyq.map(p=>{const s=store.p[topicKey(p)]||(store.p[topicKey(p)]=[0,0,0]);
      return `<tr><td><span class="badge ${p.exam==="CS"?"b2":"b3"}">${p.exam}</span></td>
        <td class="subname">${esc(p.subject)}</td>
        ${[0,1,2].map(i=>`<td class="c"><input type="checkbox" class="t" data-pk="${esc(topicKey(p))}" data-i="${i}" ${s[i]?"checked":""}></td>`).join("")}
        <td>${esc(p.acc)}</td><td class="sub">${esc(p.notes)}</td></tr>`;}).join("")}
    </tbody></table></div>`;
  $$("#t-pyq input[data-pk]").forEach(el=>el.onchange=()=>{
    const k=el.dataset.pk;store.p[k]=store.p[k]||[0,0,0];store.p[k][+el.dataset.i]=el.checked?1:0;save();updateOverall();});
}

/* ---------------- MOCKS pane ---------------- */
function renderMocks(){
  const ENAMES=["Conceptual","Calculation","Silly","Time mgmt","Guessing"];
  $("#t-mocks").innerHTML=`
    <div class="card pad" style="margin-bottom:14px"><div class="h2">Mock Test Tracker
      <span class="sub">— record every test; the five error columns are your improvement loop (spend as long analyzing as testing)</span></div></div>
    <div class="tw"><table><thead><tr><th>#</th><th>Date</th><th>Paper</th><th>Type</th><th>Score</th><th>Acc %</th>
      ${ENAMES.map(e=>`<th class="c">${e}</th>`).join("")}<th>Three weakest topics</th><th>Action before next test</th></tr></thead><tbody>
    ${DATA.mocks.map(m=>{const s=store.m["m"+m.n]||(store.m["m"+m.n]={});
      return `<tr><td class="subname">${esc(m.n)}</td><td class="sub" style="white-space:nowrap">${esc(m.date)}</td>
        <td style="min-width:110px">${esc(m.paper)}</td><td><span class="badge ${m.type==="Full-Length Mock"?"b1":"b4"}">${esc(m.type)}</span></td>
        <td><input type="text" data-m="m${m.n}" data-f="score" value="${esc(s.score||"")}" style="min-width:52px"></td>
        <td><input type="text" data-m="m${m.n}" data-f="acc" value="${esc(s.acc||"")}" style="min-width:52px"></td>
        ${ENAMES.map((_,i)=>`<td class="c"><input type="text" data-m="m${m.n}" data-f="e${i}" value="${esc(s["e"+i]||"")}" style="min-width:44px"></td>`).join("")}
        <td><input type="text" data-m="m${m.n}" data-f="weak" value="${esc(s.weak||"")}" style="min-width:150px"></td>
        <td><input type="text" data-m="m${m.n}" data-f="action" value="${esc(s.action||"")}" style="min-width:150px"></td></tr>`;}).join("")}
    </tbody></table></div>`;
  $$("#t-mocks [data-m]").forEach(el=>el.onchange=el.oninput=()=>{
    const k=el.dataset.m;store.m[k]=store.m[k]||{};
    store.m[k][el.dataset.f]=el.value;save();updateOverall();});
}

/* ---------------- TIME + GUIDE panes ---------------- */
function renderTime(){
  const groups=["Weekday","Saturday","Sunday","Low-energy day"];
  $("#t-time").innerHTML=`<div class="card pad" style="margin-bottom:14px"><div class="h2">Daily Time Structure
    <span class="sub">— the sheet's fixed blocks; on a low-energy day run the 4-hour minimum plan, never new theory</span></div></div>`+
    groups.map(g=>`<div class="subjhead"><h3>${g}</h3></div>
      <div class="card">${DATA.time.filter(t=>t.type===g).map(t=>`
        <div class="topicrow"><span class="badge okb" style="min-width:86px;text-align:center">${esc(t.dur)}</span>
        <span class="tt"><b>${esc(t.act)}</b> <span class="sub">— ${esc(t.instr)}</span></span></div>`).join("")}</div>`).join("");
}
function renderGuide(){
  $("#t-guide").innerHTML=`<div class="card pad" style="margin-bottom:14px"><div class="h2">How to use this tracker</div></div>
    <div class="card">${DATA.guide.map(g=>`
      <div class="topicrow"><span class="subname" style="min-width:150px">${esc(g.item)}</span>
      <span class="tt sub" style="flex:1">${esc(g.text)}</span></div>`).join("")}</div>
    <div class="card pad" style="margin-top:14px"><div class="h2">Tier legend</div>
      <div class="toggles">
        <span class="badge b1">Tier 1 — Must Master</span><span class="badge b2">Tier 2 — High Priority</span>
        <span class="badge b3">Tier 3 — Important</span><span class="badge b4">Tier 4 — Lower Priority</span>
      </div>
      <p class="sub" style="margin-bottom:0">Mastered = theory + topic-wise PYQs + second pass + mistakes re-solved. If more than three days behind, move Tier 3/4 first — never Tier 1.</p></div>
    <div class="card pad" style="margin-top:14px"><div class="h2">Backup &amp; restore</div>
      <p class="sub">Your ticks live in this browser's storage. Export a JSON backup before switching browsers or clearing site data, then import it there.</p>
      <div class="toggles">
        <label class="toggle on" id="g-exp"><span class="dot"></span>⇩ Export backup file</label>
        <label class="toggle" id="g-imp"><span class="dot"></span>⤒ Import from file</label>
      </div>
      <input type="file" id="g-file" accept=".json,application/json" style="display:none">
      <div class="msec">Or paste a backup here</div>
      <textarea id="g-paste" style="width:100%;min-height:90px;border:1px solid var(--line);border-radius:9px;background:var(--bg);color:var(--ink);padding:8px;font:inherit"></textarea>
      <button class="hbtn" id="g-pasteimp" style="margin-top:8px">Import pasted backup</button>
    </div>`;
  document.getElementById("g-exp").onclick=exportProgress;
  document.getElementById("g-imp").onclick=()=>document.getElementById("g-file").click();
  document.getElementById("g-file").onchange=e=>{const f=e.target.files[0];if(!f)return;
    const rd=new FileReader();
    rd.onload=()=>{try{importDump(JSON.parse(rd.result));}catch(err){alert("Could not read that file as a backup.");}};
    rd.readAsText(f);e.target.value="";};
  document.getElementById("g-pasteimp").onclick=()=>{
    try{importDump(JSON.parse(document.getElementById("g-paste").value));}catch(err){alert("That text is not valid backup JSON.");}};
}

/* ---------------- REVIEW QUEUE pane (7-day / 21-day re-solve rule) ---------------- */
function renderReview(){
  const dt=(k,z)=>store.tl[k+"|"+z]||null;
  const due=[],mist=[];
  DATA.topics.forEach(t=>{const k=topicKey(t);const s=store.t[k];if(!s)return;
    if(s[0]&&s[1]&&!s[2])due.push({t,k,d:dt(k,0)>dt(k,1)?dt(k,0):dt(k,1)});
    if(s[2]&&!s[3])mist.push({t,k,d:dt(k,2)});});
  const age=d=>d?Math.floor((Date.now()-new Date(d+"T00:00:00"))/864e5):null;
  due.sort((a,b)=>(a.d||"9999")<(b.d||"9999")?-1:1);
  mist.sort((a,b)=>(a.d||"9999")<(b.d||"9999")?-1:1);
  const rows=(list,si,btn)=>list.length?list.map(x=>{const n=age(x.d);
    return `<div class="topicrow"><span class="badge b${x.t.tier}">T${x.t.tier}</span>
      <span class="badge ${x.t.exam==="CS"?"b2":"b3"}">${x.t.exam}</span>
      <span class="tt">${esc(x.t.topic)} <span class="sub">· ${esc(x.t.subject)}</span></span>
      <span class="sub" style="white-space:nowrap;${n!==null&&n>=7?"color:var(--t1);font-weight:700":""}">${x.d?(n===0?"today":n+" d"):"—"}</span>
      <button class="hbtn" data-qk="${esc(x.k)}" data-qs="${si}">${btn}</button></div>`;}).join("")
    :`<div class="pad sub">Nothing here yet — topics appear once their earlier stages are ticked.</div>`;
  $("#t-review").innerHTML=`
    <div class="card pad" style="margin-bottom:14px"><div class="h2">Review Queue
      <span class="sub">— the 7-day / 21-day re-solve rule from the plan: second pass 7 days after Theory+PYQ, mistakes re-solved 21 days after that. Oldest first.</span></div></div>
    <div class="subjhead"><h3>Due for second pass (stage R)</h3><span class="sub">${due.length} topic${due.length===1?"":"s"}</span></div>
    <div class="card">${rows(due,2,"✓ R done")}</div>
    <div class="subjhead"><h3>Due for mistake re-solve (stage M)</h3><span class="sub">${mist.length} topic${mist.length===1?"":"s"}</span></div>
    <div class="card">${rows(mist,3,"✓ M done")}</div>`;
  $$("#t-review [data-qk]").forEach(el=>el.onclick=()=>{
    setT307(el.dataset.qk, +el.dataset.qs, 1);
    save();updateOverall();renderReview();});
}

/* ---------------- MASTER CHECKLIST pane ---------------- */
const MCSTAGES=["Theory","PYQ","Revision","Mistake log"];
const mcStageKey=(g,r,s)=>"g"+g+"r"+r+"t"+s;
const mcSubKey=(g,r,i)=>"g"+g+"r"+r+"s"+i;
function mcSubsDone(g,r,row){let n=0;row.subs.forEach((_,i)=>{if(store.mc[mcSubKey(g,r,i)])n++;});return n;}
function renderCheck(){
  const ck=DATA.checklist; if(!ck){$("#t-mc").innerHTML="<p class='sub'>checklist data missing</p>";return;}
  const groups=ck.groups.map((G,gi)=>{
    const rows=G.rows.map((R,ri)=>{
      const done=MCSTAGES.filter((_,s)=>store.mc[mcStageKey(gi,ri,s)]).length;
      const sub=mcSubsDone(gi,ri,R);
      return `<div class="topicrow">
        <span class="tdot t${R.tier}"></span>
        <span class="tt mcname" data-g="${gi}" data-r="${ri}">
          <b>${esc(R.topic)}</b>
          <div class="mcnote">${R.subs.length} subtopics · click for subtopics, PYQ patterns &amp; tests</div></span>
        <span class="stages">${MCSTAGES.map((nm,s)=>
          `<span class="stage ${store.mc[mcStageKey(gi,ri,s)]?"on":""}" data-g="${gi}" data-r="${ri}" data-s="${s}" title="${nm}">${["T","P","R","M"][s]}</span>`).join("")}</span>
        <span class="sub subcount" id="sc-${gi}-${ri}" style="min-width:44px;text-align:right">${sub}/${R.subs.length}</span>
      </div>`;}).join("");
    const total=MCSTAGES.length*G.rows.length+G.rows.reduce((n,R)=>n+R.subs.length,0);
    const dn=G.rows.reduce((n,R,ri)=>n+MCSTAGES.filter((_,s)=>store.mc[mcStageKey(gi,ri,s)]).length+mcSubsDone(gi,ri,R),0);
    return `<div class="subjhead"><h3>${esc(G.name)}</h3><span class="sub">${esc(G.note)}</span>
        <div class="bar" style="max-width:180px"><i style="width:${Math.round(100*dn/total)}%"></i></div></div>
      <div class="card">${rows}</div>`;
  }).join("");
  $("#t-mc").innerHTML=`
    <div class="card pad" style="margin-bottom:6px">
      <b>How to use:</b> <span class="sub">pick 1–3 red topics first → study theory (T) → solve their PYQs (P) → revise in the evening (R) → update the mistake log (M). Click any topic for its subtopics, topic-wise and subtopic-wise PYQs, and the tests to run. Never start a low-priority topic while reds of the same subject are weak.</span>
      <div style="margin-top:6px"><span class="mpill">${esc(ck.meta.disclaimer)}</span>
      <span class="mpill">${esc(ck.meta.solveCSE)}</span><span class="mpill">${esc(ck.meta.solveDA)}</span></div>
    </div>${groups}`;
  $$("#t-mc .stage").forEach(el=>el.onclick=()=>{
    const g=+el.dataset.g, r=+el.dataset.r, s=+el.dataset.s;
    const val=store.mc[mcStageKey(g,r,s)]?0:1;
    setMC(g,r,s,val);
    if(val) reverseTickMC(g,r,s);
    save();updateOverall();
    const y=scrollY;renderCheck();scrollTo(0,y);});
  $$("#t-mc .mcname").forEach(el=>el.onclick=()=>openMcModal(+el.dataset.g,+el.dataset.r));
  // keep filter-free pane scroll stable; modal binding below
}
function openMcModal(gi,ri){
  const G=DATA.checklist.groups[gi], R=G.rows[ri];
  const subs=R.subs.map((s,i)=>`<div><label class="act ${store.mc[mcSubKey(gi,ri,i)]?"done":""}">
      <input type="checkbox" class="t" data-mcs="${i}" ${store.mc[mcSubKey(gi,ri,i)]?"checked":""}><span>${esc(s.n)}</span></label>
      <div class="mnote">PYQ: ${esc(s.p)}</div></div>`).join("");
  $("#mhead").innerHTML=`<span class="badge b${R.tier}">Tier ${R.tier}</span>
    <div><div style="font-size:17px;font-weight:700">${esc(R.topic)}</div>
    <div class="sub">${esc(G.name)}</div></div><button class="mx" title="close">✕</button>`;
  $("#mbody").innerHTML=`
    <div class="msec">Subtopics — tick when finished (PYQ note under each)</div>${subs}
    <div class="msec">Topic-wise PYQs</div>
    <div><span class="mpill">Asked: ${esc(R.freq)}</span></div>
    <ul style="margin:8px 0 0">${R.patterns.map(p=>`<li>${esc(p)}</li>`).join("")}</ul>
    <div class="mnote" style="margin-top:8px">Solve these from your topic-wise PYQ book / previous papers${R.tier<=2?" — this is a high-priority topic; do the full set for 2017–2026 (CS) and 2024–2026 (DA).":"."}</div>
    <div class="msec">Tests for this topic</div>
    <div class="mtest"><ul>${R.tests.map(t=>`<li>${esc(t)}</li>`).join("")}</ul></div>`;
  $("#modal").hidden=false;document.body.style.overflow="hidden";
  $$("#mbody input[data-mcs]").forEach(el=>el.onchange=()=>{
    const i=+el.dataset.mcs,k=mcSubKey(gi,ri,i);
    store.mc[k]=el.checked?1:0;save();
    el.closest("label").classList.toggle("done",el.checked);
    const R2=DATA.checklist.groups[gi].rows[ri];
    const sc=$("#sc-"+gi+"-"+ri);if(sc)sc.textContent=mcSubsDone(gi,ri,R2)+"/"+R2.subs.length;
    updateOverall();});
}
function closeMcModal(){$("#modal").hidden=true;document.body.style.overflow="";}
document.querySelector("#modal .mback").addEventListener("click",closeMcModal);
$("#modal").addEventListener("click",e=>{if(e.target.closest(".mx"))closeMcModal();});
document.addEventListener("keydown",e=>{if(e.key==="Escape"&&!$("#modal").hidden)closeMcModal();});

/* ---------------- pane/view plumbing ---------------- */
function showPane(id){
  $$(".ttabs button").forEach(b=>b.classList.toggle("on",b.dataset.pane===id));
  $$(".tpane").forEach(p=>p.classList.toggle("on",p.id===id));
  if(id==="t-review")renderReview();     // fresh dates every visit
}
$$("#ttabs button").forEach(b=>b.onclick=()=>{showPane(b.dataset.pane);scrollTo({top:0});});
function setView(v){
  document.body.dataset.view=v;
  $("#v-tracker").classList.toggle("on",v==="tracker");
  $("#v-plan").classList.toggle("on",v==="plan");
}
$("#v-tracker").onclick=()=>setView("tracker");
$("#v-plan").onclick=()=>setView("plan");

/* ---------------- bind daily checkboxes ---------------- */
function bindChecks(scope){
  $$((scope||"")+" input[data-k]").forEach(el=>el.onchange=()=>{
    store.d[el.dataset.k]=el.checked?1:0;save();
    el.closest("label")?.classList.toggle("done",el.checked);updateOverall();});
  $$((scope||"")+" input[data-tk]").forEach(el=>el.onchange=()=>{
    store.d[el.dataset.tk]=el.checked?1:0;save();
    el.closest(".toggle")?.classList.toggle("on",el.checked);updateOverall();
    if(el.checked){ const parts=el.dataset.tk.split("|T"); syncToday(parts[0], +parts[1]); }});
}

/* ---------------- plan docs (sidebar, checkboxes, spy) ---------------- */
const tree=$("#navtree");
{DOCS_META}.forEach((dm,i)=>{
  const wrap=document.createElement("div");
  wrap.innerHTML=`<div class="navdoc">${dm.tag}</div><ul></ul>
    <div class="docprog dp" data-doc="doc-${i+1}"><div class="lbl"><span>checklist</span><span class="cnt">0 / 0</span></div><div class="bar"><i></i></div></div>`;
  const ul=wrap.querySelector("ul");
  dm.nav.forEach(n=>{const li=document.createElement("li");li.className=n.lvl===2?"l2":"";
    li.innerHTML=`<a href="#${n.id}" data-t="${n.id}">${esc(n.label)}</a>`;ul.appendChild(li);});
  tree.appendChild(wrap);
});
const nsearch=$("#navsearch");
nsearch.oninput=()=>{
  const q=nsearch.value.toLowerCase();
  $$("#navtree li").forEach(li=>li.style.display=li.textContent.toLowerCase().includes(q)?"":"none");
};
let ckState={};try{ckState=JSON.parse(localStorage.getItem(LS_CK)||"{}");}catch(e){}
const ckHash=s=>{let h=5381;for(let i=0;i<s.length;i++)h=((h<<5)+h+s.charCodeAt(i))>>>0;return h.toString(36);};
$$("input.ck").forEach((b,i)=>{
  const doc=b.closest("section.doc");
  const head=[...doc.querySelectorAll("h1,h2,h3")].filter(h=>h.compareDocumentPosition(b)&Node.DOCUMENT_POSITION_FOLLOWING).pop();
  b.dataset.id="ck-"+ckHash(doc.id+"|"+(head?head.textContent.slice(0,60):"")+"|"+(b.closest("li,td")?.textContent.trim().slice(0,80)||i)+"|"+i);
  if(ckState[b.dataset.id])b.checked=true;
  b.onchange=()=>{ckState[b.dataset.id]=b.checked;localStorage.setItem(LS_CK,JSON.stringify(ckState));
    b.closest("li")?.classList.toggle("done",b.checked);updateOverall();};
  if(b.checked)b.closest("li")?.classList.add("done");
});
const links=$$("#navtree a"), byId={};links.forEach(a=>byId[a.dataset.t]=a);
const spy=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){
  links.forEach(a=>a.classList.remove("active"));byId[e.target.id]?.classList.add("active");}});},
  {rootMargin:"-60px 0px -70% 0px"});
Object.keys(byId).forEach(id=>{const el=document.getElementById(id);if(el)spy.observe(el);});
function updateDocProgress(){
  let all=0,done=0;
  $$("section.doc").forEach(sec=>{
    const c=[...sec.querySelectorAll("input.ck")],d=c.filter(b=>b.checked).length;all+=c.length;done+=d;
    const chip=document.querySelector('.dp[data-doc="'+sec.id+'"]');
    if(chip){chip.querySelector(".cnt").textContent=d+" / "+c.length;chip.querySelector("i").style.width=(c.length?100*d/c.length:0)+"%";}
  });
}
updateDocProgress();

/* ---------------- backup / restore ---------------- */
const BKKEYS=["gate-tracker-v1","gateplan-ck-v1"];
function exportProgress(){
  const dump={v:1,exported:new Date().toISOString()};
  BKKEYS.forEach(k=>dump[k]=localStorage.getItem(k));
  const a=document.createElement("a");
  a.href=URL.createObjectURL(new Blob([JSON.stringify(dump,null,1)],{type:"application/json"}));
  a.download="gate-progress-"+todayISO()+".json";
  document.body.appendChild(a);a.click();a.remove();
}
function importDump(o){
  if(!o||typeof o!=="object"){alert("That doesn't look like a backup file.");return;}
  let any=false;
  BKKEYS.forEach(k=>{if(typeof o[k]==="string"){localStorage.setItem(k,o[k]);any=true;}});
  if(any)location.reload();else alert("No progress data found in that file.");
}
$("#bkexp").onclick=exportProgress;
$("#bkimp").onclick=()=>$("#bkfile").click();
$("#bkfile").onchange=e=>{const f=e.target.files[0];if(!f)return;
  const rd=new FileReader();
  rd.onload=()=>{try{importDump(JSON.parse(rd.result));}catch(err){alert("Could not read that file as a backup.");}};
  rd.readAsText(f);e.target.value="";};

/* ---------------- misc ---------------- */
$("#top").onclick=()=>scrollTo({top:0,behavior:"smooth"});
addEventListener("scroll",()=>$("#top").style.display=scrollY>700?"block":"none",{passive:true});

/* ---------------- boot ---------------- */
renderToday();renderDaily();renderTopics();renderReview();renderCheck();renderPyq();renderMocks();renderTime();renderGuide();
updateOverall();
</script>
</body>
</html>
"""

def build(source: Path, out: Path):
    docs_html, docs_meta = build_docs(source)
    data = clean_data(json.loads((source / "sample_sheet_dump.json").read_text(encoding="utf-8")))
    page = (TEMPLATE
            .replace("{DOCS}", docs_html)
            .replace("{DOCS_META}", repr(docs_meta).replace("</", "<\\/"))
            .replace("{DATA_JSON}", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"OK  {out}  ({out.stat().st_size/1024:.0f} KB, {len(data['days'])} days, {len(data['topics'])} topics)")


if __name__ == "__main__":
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    outp = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent / "index.html"
    build(src, outp)

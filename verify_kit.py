#!/usr/bin/env python3
"""
Independent kit verification: re-checks the EMITTED files (the_file.txt,
facts.json, questions.jsonl, answer_key.jsonl) without trusting generator state.
Run: python3 verify_kit.py  -> prints PASS/FAIL lines; exit 1 on any FAIL.
"""
import json, re, sys
from pathlib import Path

D = Path(__file__).resolve().parent
full = (D / "the_file.txt").read_text()
meta = json.loads((D / "facts.json").read_text())
facts = meta["facts"]
questions = [json.loads(l) for l in (D / "questions.jsonl").read_text().splitlines() if l.strip()]
key = {json.loads(l)["n"]: json.loads(l) for l in (D / "answer_key.jsonl").read_text().splitlines() if l.strip()}
fails = []
def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)

check(meta["file_sha256"] == __import__("hashlib").sha256(full.encode()).hexdigest(), "file SHA matches facts.json")
check(830_000 <= meta["est_tokens"] <= 875_000, f"token estimate in range: {meta['est_tokens']:,}")
check(len(questions) == 60, f"60 questions (got {len(questions)})")
check([q["n"] for q in questions] == list(range(1, 61)), "question numbering 1..60 frozen order")
check(set(key) == set(range(1, 61)), "answer key covers all 60")

needles = [f for f in facts if f["kind"] == "needle"]
check(len(needles) == 25, "25 needle facts")
for band in range(5):
    check(sum(1 for f in needles if f["depth_band"] == band) == 5, f"5 needles in depth band {band}")
bad = []
for f in needles:
    probe = f["value"] + (f" {f['unit']}" if f["unit"] else "")
    if full.count(probe) != 1:
        bad.append((f["entity"], full.count(probe)))
check(not bad, f"every needle value+unit string occurs exactly once (violations: {bad})")
vals = [f["value"] for f in needles]
check(len(set(vals)) == len(vals), "needle values globally unique")

comps = [f for f in facts if f["kind"] == "join_component"]
check(len(comps) == 24, "24 join component facts")
for f in comps:
    check(full.count(f["sentence"]) == 1, f"join component present once: {f['entity']} / {f['attribute']}")
pairs = {}
for f in comps:
    pairs.setdefault(f["entity"], []).append(f["token_percentile"])
wide = [e for e, ps in pairs.items() if len(ps) == 2 and abs(ps[1] - ps[0]) >= 40]
check(len(wide) >= 10, f"join pairs separated by >=40 percentile points: {len(wide)} pairs")

# Aggregation answers recomputed from the tables AS PRINTED in the_file.txt
for a in meta["agg_tables"]:
    start = full.index(a["header"]) + len(a["header"])
    block = full[start:start + 1500]
    printed = re.findall(r"^(.+?):\s*([0-9][0-9,]*\.?[0-9]*)\s*$", block, flags=re.M)
    printed_vals = [v for _, v in printed[:len(a["rows"])]]
    expect = [v for _, v in a["rows"]]
    check(printed_vals == expect, f"agg table rows as printed match key: {a['header'][:52]}")
    if a["unit"] != "months":
        s = sum(float(v) for v in expect)
        check(abs(s - float(a["answer"])) < 0.011, f"agg answer recomputed: {a['header'][:52]} -> {a['answer']}")

probes = [k for k in key.values() if k["category"] == "not_in_file"]
check(len(probes) == 8, "8 not-in-file probes")
for p in probes:
    ent = p["fact_ids"][0]
    check(ent.lower() not in full.lower(), f"probe entity absent from file: {ent}")

check(full.count("## Procedure ") == 40, "manual contains exactly 40 procedures")
check(len(re.findall(r"^PART [IVX]+ -", full, flags=re.M)) == 5, "compendium contains exactly 5 parts")
check(len(re.findall(r"^Route \d+ -", full, flags=re.M)) == 6, "timetables contain exactly 6 routes")

from collections import Counter
print("questions by category:", dict(Counter(q["category"] for q in questions)))
print("needles by band:", dict(sorted(Counter(f["depth_band"] for f in needles).items())))
print("RESULT:", "ALL CHECKS PASSED" if not fails else f"{len(fails)} FAILURES")
sys.exit(1 if fails else 0)

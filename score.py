#!/usr/bin/env python3
"""
CONTEXT SHOWDOWN scorer — FROZEN with the kit (see MANIFEST.md).
Rules were written before any run and are NOT adjusted after one.

Input : responses.jsonl, one {"n": int, "response": str} per question.
        Optional per-response fields: "evidence" (str), "latency_s" (float) —
        used only for the scorecard's evidence-rate and latency lines.
Output: per-question verdicts + totals (overall, per category, needles by band).

SCORING RULES (fixed):
- needle / aggregation / structure: 1 point iff the exact answer value appears
  in the response (after normalisation: case folded, thousand separators
  removed, whitespace collapsed) AND the unit, when the key has one, appears as
  the unit word or a listed variant (dollar/$, feet/foot/ft, mile(s), inch(es),
  year(s), people/person(s), unit(s), animal(s), volume(s)/book(s), pupil(s)/
  student(s), month(s), town(s), route(s), part(s), procedure(s)). Otherwise 0.
  No partial credit in these categories. A correct value in a non-standard
  format (e.g. a date written "March 14, 1957" for key "14 March 1957") scores
  0 under the strict rule — the family's standing practice — and is ALSO counted
  on the informational "loose value recall" line so the strictness is visible.
- join: 1 point iff the derived answer (value + unit) matches by the rule above.
  0.5 points iff the derived answer is wrong/absent but exactly one of the two
  component fact values appears in the response. Otherwise 0.
- not_in_file: 1 point iff the response states the fact is absent (contains one
  of the ABSENCE phrases) — inventing a value is a failure. If an absence phrase
  is present but the response also contains a digit, the item is flagged REVIEW
  and scores 0 until a human confirms the digit was not an asserted answer.
"""
import json, re, sys
from pathlib import Path
from collections import Counter, defaultdict

D = Path(__file__).resolve().parent
key = {json.loads(l)["n"]: json.loads(l) for l in (D / "answer_key.jsonl").read_text().splitlines() if l.strip()}
facts = json.loads((D / "facts.json").read_text())["facts"]
resp_path = Path(sys.argv[1]) if len(sys.argv) > 1 else D / "responses.jsonl"
responses = {json.loads(l)["n"]: json.loads(l) for l in resp_path.read_text().splitlines() if l.strip()}

UNIT_VARIANTS = {
    "dollars": ["dollar", "$"], "feet": ["feet", "foot", "ft"], "miles": ["mile"],
    "inches": ["inch", "in"], "years": ["year"], "people": ["people", "person", "employee"],
    "units": ["unit", "pump"], "animals": ["animal", "head of livestock"],
    "volumes": ["volume", "book"], "pupils": ["pupil", "student"], "months": ["month"],
    "towns": ["town"], "routes": ["route"], "parts": ["part"], "procedures": ["procedure"],
}
ABSENCE = ["not in the file", "does not appear", "doesn't appear", "no record", "not mentioned",
           "isn't mentioned", "not present", "cannot find", "can't find", "no information",
           "does not contain", "doesn't contain", "not stated", "unable to find", "no mention",
           "absent from", "not included", "does not mention", "isn't in the file", "not in the document",
           "does not provide", "no entry"]

def norm(s):
    s = str(s).lower()
    s = re.sub(r"(\d),(\d)", r"\1\2", s)
    return re.sub(r"\s+", " ", s)

def value_present(resp_n, value):
    return norm(value) in resp_n

def unit_present(resp_n, unit):
    if not unit:
        return True
    return any(v in resp_n for v in UNIT_VARIANTS.get(unit, [unit.rstrip("s")]))

def loose_value_present(resp_n, value):
    # informational only: all numeric/name tokens of the value present in any arrangement
    toks = re.findall(r"[a-z]+|\d+(?:\.\d+)?", norm(value))
    return all(t in resp_n for t in toks) if toks else False

join_components = defaultdict(list)
for f in facts:
    if f["kind"] == "join_component":
        join_components[f["entity"]].append(f["value"])

results, totals = [], Counter()
band_pts, band_tot = defaultdict(float), Counter()
loose = 0
for n in sorted(key):
    k = key[n]
    r = responses.get(n, {})
    resp = r.get("response", "")
    rn = norm(resp)
    cat = k["category"]
    pts, note = 0.0, ""
    if cat == "not_in_file":
        has_abs = any(p in rn for p in ABSENCE)
        if has_abs and re.search(r"\d", resp):
            note = "REVIEW (absence stated but digits present)"
        elif has_abs:
            pts = 1.0
        else:
            note = "INVENTED or evaded (no absence statement)"
    elif cat == "join":
        if value_present(rn, k["answer_value"]) and unit_present(rn, k["unit"]):
            pts = 1.0
        else:
            comp_hits = 0
            for ent in set(k["fact_ids"]):
                for v in join_components.get(ent, []):
                    if value_present(rn, v):
                        comp_hits += 1
            if comp_hits == 1:
                pts, note = 0.5, "one component fact only"
            else:
                note = f"components found: {comp_hits}"
    else:
        if value_present(rn, k["answer_value"]) and unit_present(rn, k["unit"]):
            pts = 1.0
        elif loose_value_present(rn, k["answer_value"]):
            loose += 1
            note = "loose value present, strict form failed"
    totals[cat] += pts
    totals["ALL"] += pts
    if cat == "needle":
        band_pts[k["depth_band"]] += pts
        band_tot[k["depth_band"]] += 1
    results.append((n, cat, pts, note, bool(r.get("evidence")), r.get("latency_s")))

for n, cat, pts, note, _, _ in results:
    print(f"Q{n:02d} [{cat}] {pts:g}" + (f"  -- {note}" if note else ""))
print("\n== TOTALS ==")
for cat in ["needle", "join", "aggregation", "structure", "not_in_file"]:
    cnt = sum(1 for k in key.values() if k["category"] == cat)
    print(f"{cat}: {totals[cat]:g} / {cnt}")
print(f"ALL: {totals['ALL']:g} / 60")
print("needles by depth band:", {b: f"{band_pts[b]:g}/{band_tot[b]}" for b in sorted(band_tot)})
print(f"loose value recall (informational, strict-failed): {loose}")
ev = [r for r in results if r[4]]
if ev:
    print(f"evidence attached: {len(ev)}/60 responses")
lat = [r[5] for r in results if r[5] is not None]
if lat:
    print(f"latency per question: mean {sum(lat)/len(lat):.2f}s, max {max(lat):.2f}s over {len(lat)} timed")

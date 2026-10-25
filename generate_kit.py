#!/usr/bin/env python3
"""
CONTEXT SHOWDOWN kit generator.

Builds, deterministically from SEED:
  the_file.txt        - a ~850k-token invented reference compendium with planted facts
  facts.json          - every planted fact, its position (char offset + token percentile) and band
  questions.jsonl     - the frozen 60 questions (question text only, frozen order)
  answer_key.jsonl    - per-question answer value + unit + source sentence + section + band

Token estimate method (stated here and in MANIFEST.md): est_tokens = chars / 4.0,
the standard English-prose heuristic (~4 chars/token). Percentile positions are
computed on the same char basis (token percentile ~= char percentile under a
uniform chars/token assumption).

Run: python3 generate_kit.py   (byte-identical output for a fixed seed)
"""
import json, math, random, re, hashlib
from pathlib import Path

SEED = 20261022
rng = random.Random(SEED)
OUT = Path(__file__).resolve().parent

MONTHS = ["January","February","March","April","May","June","July","August",
          "September","October","November","December"]
FIRST = ["Amos","Ruth","Caleb","Miriam","Jonas","Eliza","Silas","Prudence","Elias","Mabel",
         "Harvey","Clara","Owen","Beatrice","Felix","Harriet","Walter","Josephine","Edmund","Louisa",
         "Chester","Alma","Roland","Nettie","Gideon"]
LAST = ["Hartley","Moss","Calloway","Brandt","Iversen","Kettner","Albright","Fenner","Osgood","Rill",
        "Sanger","Thurlow","Voss","Wexler","Yardley","Zimmer","Pruitt","Halloway","Merrit","Dunmore"]
TOWNS = ["Mossbridge","Alder Falls","Kettner Junction","East Rill","Port Sanger",
         "Thurlow Flats","Wexler's Crossing","North Fenner","Dunmore Landing"]

def spelled_date(y, m, d):
    return f"{d} {MONTHS[m-1]} {y}"

def money(v):
    return f"{v:,.2f}"

# ---------------------------------------------------------------- fact tables
facts = []          # planted fact records (needles + join components)
def add_fact(kind, entity, attribute, value, unit, sentence, section, target_pct):
    facts.append(dict(kind=kind, entity=entity, attribute=attribute, value=value,
                      unit=unit, sentence=sentence, section=section, target_pct=target_pct))

# Needles: 25, stratified 5 per depth band (band centres spread inside each band)
needle_targets = []
for band in range(5):
    base = band * 20
    needle_targets += [base + 3, base + 7, base + 11, base + 15, base + 18]

money_entities = [
    ("the Halvern & Moss expansion loan of 1958",
     "The Halvern & Moss expansion loan of 1958 was recorded at {v} dollars, countersigned by the county clerk before witnesses."),
    ("the Calloway bequest to the Alder County library fund",
     "The Calloway bequest to the Alder County library fund was settled at {v} dollars after probate."),
    ("the Port Sanger bridge construction contract",
     "The Port Sanger bridge construction contract was let for {v} dollars to a single bidder."),
    ("the 1963 county fair champion marrow prize fund",
     "The 1963 county fair champion marrow prize fund held {v} dollars at the close of entries."),
    ("the Fenner warehouse fire insurance settlement",
     "The Fenner warehouse fire insurance settlement was paid at {v} dollars in full and final discharge."),
    ("the East Rill schoolhouse land purchase",
     "The East Rill schoolhouse land purchase was completed for {v} dollars, deed recorded the same week."),
    ("the Mossbridge waterworks bond issue of 1960",
     "The Mossbridge waterworks bond issue of 1960 raised {v} dollars against future rates."),
    ("the Thurlow grain elevator damages award",
     "The Thurlow grain elevator damages award was assessed at {v} dollars by the circuit court."),
]
code_entities = [
    ("the works number of the Model 7 pump installed at North Fenner",
     "The Model 7 pump installed at North Fenner carries works number {v}, stamped on the maker's plate."),
    ("the running number of the county's Baldwin locomotive",
     "The county's Baldwin locomotive runs under number {v} in the railway register."),
    ("the archive code of the 1955 flood survey box",
     "The 1955 flood survey box is held in the county archive under code {v}."),
    ("the inspection code of the Kettner Junction footbridge",
     "The Kettner Junction footbridge bears inspection code {v} on its eastern parapet."),
    ("the call sign of the county wireless station",
     "The county wireless station transmits under call sign {v} as listed in the 1962 directory."),
    ("the safe deposit register code for the Dunmore bank vault",
     "The Dunmore bank vault is entered in the safe deposit register under code {v}."),
]
date_entities = [
    ("Wendell A. Pruitt", "county surveyor",
     "{name} took office as county surveyor on {v}, succeeding his father in the post."),
    ("Cordelia Brandt", "registrar of deeds",
     "{name} was sworn in as registrar of deeds on {v} at the courthouse in Mossbridge."),
    ("the Alder County courthouse cornerstone", None,
     "The cornerstone of the Alder County courthouse was laid on {v} before a crowd of four hundred."),
    ("the first sitting of the Alder County circuit court", None,
     "The first sitting of the Alder County circuit court opened on {v} with Judge Halloway presiding."),
    ("Tobias Rill", "ferry master at Dunmore Landing",
     "{name} began his duties as ferry master at Dunmore Landing on {v}, a post he held for thirty years."),
    ("the Halvern & Moss foundry", None,
     "The Halvern & Moss foundry was formally incorporated on {v} with nine shareholders."),
]
measure_entities = [
    ("the span of the Port Sanger bridge", "feet",
     "The Port Sanger bridge measures {v} feet from abutment to abutment."),
    ("the depth of the Kettner artesian well", "feet",
     "The Kettner artesian well was drilled to a depth of {v} feet before striking the lower aquifer."),
    ("the height of the Mossbridge wireless tower", "feet",
     "The Mossbridge wireless tower stands {v} feet above the courthouse square."),
    ("the length of the East Rill canal cut", "miles",
     "The East Rill canal cut runs {v} miles from the lock gate to the mill pond."),
    ("the capacity of the Thurlow reservoir", "million gallons",
     "The Thurlow reservoir holds {v} million gallons at the spillway mark."),
]

used_values = set()
def uniq(v):
    assert v not in used_values, f"value collision in fact tables: {v}"
    used_values.add(v)
    return v

ti = 0
for ent, tmpl in money_entities:
    v = uniq(money(rng.randint(10_000, 950_000) + rng.randint(1, 99) / 100))
    add_fact("needle", ent, "recorded amount", v, "dollars",
             tmpl.format(v=v), "Part II - Company and County Records", needle_targets[ti]); ti += 1
code_prefixes = ["HM-", "BL-", "AB-", "IN-", "KAL-", "SD-"]
for i, (ent, tmpl) in enumerate(code_entities):
    v = uniq(f"{code_prefixes[i]}{rng.randint(10000, 99999)}")
    add_fact("needle", ent, "code", v, "",
             tmpl.format(v=v), "Part III - Registries", needle_targets[ti]); ti += 1
for name, role, tmpl in date_entities:
    y, m, d = rng.randint(1938, 1968), rng.randint(1, 12), rng.randint(1, 28)
    v = uniq(spelled_date(y, m, d))
    ent = f"{name}, {role}" if role else name
    add_fact("needle", ent, "date", v, "",
             tmpl.format(name=name, v=v), "Part I - County Almanac", needle_targets[ti]); ti += 1
for ent, unit, tmpl in measure_entities:
    if unit == "miles":
        v = uniq(f"{rng.randint(9, 29)}.{rng.choice([15,35,55,75,85]):02d}")
    elif unit == "million gallons":
        v = uniq(f"{rng.randint(300, 980)}.{rng.choice([25,5,75]):02d}".rstrip('0').rstrip('.') if False else f"{rng.randint(300,980)}.75")
    else:
        v = uniq(f"{rng.randint(120, 1400)}.{rng.choice([25,5,75])}")
        v = f"{float(v):.2f}".rstrip('0').rstrip('.') if v.endswith('.5') else v
    add_fact("needle", ent, "measurement", v, unit,
             tmpl.format(v=v), "Part I - County Almanac", needle_targets[ti]); ti += 1
assert ti == 25, ti

# Join components: 12 joins = 24 component facts. A-facts early, B-facts late (>=45 pct points apart).
join_defs = []
join_people = [("Tomas Wrenlow", "county service medal"), ("Agnes Kettner", "long-service certificate"),
               ("Bartholomew Osgood", "mayoral chain of office"), ("Selina Yardley", "teaching jubilee medal")]
for i, (person, honour) in enumerate(join_people):
    by, bm, bd = rng.randint(1935, 1952), 4, rng.randint(2, 27)          # born in April
    ey = by + rng.randint(19, 34)                                        # event year
    age = ey - by                                                        # event in September -> full years
    a = dict(kind="join_component", entity=person, attribute="birth date",
             value=spelled_date(by, bm, bd), unit="",
             sentence=f"{person} was born on {spelled_date(by, bm, bd)} in {TOWNS[i % len(TOWNS)]}, the third child of a mill family.",
             section="Part I - County Almanac", target_pct=4 + i * 6)
    b = dict(kind="join_component", entity=person, attribute="honour year",
             value=str(ey), unit="",
             sentence=f"{person} received the {honour} in September {ey} at a ceremony in Mossbridge.",
             section="Part III - Registries", target_pct=62 + i * 7)
    join_defs.append((a, b, f"How old was {person} when they received the {honour}?",
                      str(age), "years", "age_at_event"))
for i in range(4):
    a_amt = rng.randint(20_000, 300_000) + rng.randint(1, 99) / 100
    b_amt = a_amt + rng.randint(1_000, 60_000) + rng.randint(0, 99) / 100
    diff = round(b_amt - a_amt, 2)
    proj = ["the Wexler's Crossing road contract", "the North Fenner drainage scheme",
            "the Alder Falls market hall", "the Port Sanger harbour wall"][i]
    a = dict(kind="join_component", entity=proj, attribute="original estimate",
             value=money(a_amt), unit="dollars",
             sentence=f"The original estimate for {proj} was {money(a_amt)} dollars, as tendered in the council minutes.",
             section="Part II - Company and County Records", target_pct=6 + i * 6)
    b = dict(kind="join_component", entity=proj, attribute="final cost",
             value=money(b_amt), unit="dollars",
             sentence=f"The final cost of {proj} was settled at {money(b_amt)} dollars on completion.",
             section="Part II - Company and County Records", target_pct=64 + i * 7)
    join_defs.append((a, b, f"By how many dollars did the final cost of {proj} exceed its original estimate?",
                      money(diff), "dollars", "difference"))
for i in range(4):
    a_len = rng.randint(100, 900) + rng.choice([0.25, 0.5])
    b_len = rng.randint(100, 900) + rng.choice([0.5, 0.75])
    total = a_len + b_len
    total_s = f"{total:.2f}".rstrip('0').rstrip('.')
    seg = ["the Mill Race footpath", "the Canal Towpath", "the Ridgeway bridle path", "the Fenner Marsh boardwalk"][i]
    a = dict(kind="join_component", entity=seg, attribute="eastern section length",
             value=f"{a_len:g}", unit="feet",
             sentence=f"The eastern section of {seg} measures {a_len:g} feet from the stile to the mid-gate.",
             section="Part I - County Almanac", target_pct=8 + i * 6)
    b = dict(kind="join_component", entity=seg, attribute="western section length",
             value=f"{b_len:g}", unit="feet",
             sentence=f"The western section of {seg} measures {b_len:g} feet from the mid-gate to the parish boundary.",
             section="Part I - County Almanac", target_pct=66 + i * 7)
    join_defs.append((a, b, f"What is the total length, in feet, of {seg} (eastern and western sections combined)?",
                      total_s, "feet", "sum"))
for a, b, *_ in join_defs:
    for comp in (a, b):
        assert comp["value"] not in used_values or comp["attribute"] == "honour year", comp["value"]
        used_values.add(comp["value"])
        facts.append(comp)

# Aggregation tables: (header, [(label, value_str)], question, answer_value, unit, section, target_pct)
agg_tables = []
def add_agg(header, rows, question, unit, section, pct):
    total = sum(float(v) for _, v in rows)
    agg_tables.append(dict(header=header, rows=rows, question=question,
                           answer=f"{total:g}", unit=unit, section=section, target_pct=pct))
rev61 = [("Q1", "184210"), ("Q2", "201455"), ("Q3", "176980"), ("Q4", "229340")]
add_agg("Halvern & Moss - Quarterly Revenue, 1961 (dollars)", rev61,
        "What was Halvern & Moss's total revenue for 1961, in dollars?", "dollars",
        "Part II - Company and County Records", 30)
rain59 = [(MONTHS[i], f"{rng.uniform(1.2, 5.8):.2f}") for i in range(12)]
add_agg("Alder County - Monthly Rainfall, 1959 (inches)", rain59,
        "What was Alder County's total rainfall in 1959, in inches?", "inches",
        "Part V - Timetables and Ledgers", 45)
depts = [("Foundry", "212"), ("Machine shop", "168"), ("Pattern shop", "47"),
         ("Office", "39"), ("Yard and transport", "86"), ("Night watch", "12")]
add_agg("Halvern & Moss - Employees by Department, 1963", depts,
        "How many people did Halvern & Moss employ across all departments in 1963?", "people",
        "Part II - Company and County Records", 55)
prod70 = [(MONTHS[i], str(rng.randint(8200, 12900))) for i in range(6)]
add_agg("Halvern & Moss - Model 7 Pump Production, January-June 1970 (units)", prod70,
        "How many Model 7 pumps did Halvern & Moss produce from January to June 1970?", "units",
        "Part II - Company and County Records", 70)
stock = [("Cattle", "4210"), ("Sheep", "8930"), ("Pigs", "1875"), ("Horses", "640"), ("Poultry", "15220")]
add_agg("Alder County - Livestock Census, 1957", stock,
        "What was the total number of livestock recorded in the Alder County census of 1957?", "animals",
        "Part I - County Almanac", 20)
library = [("Fiction", "12480"), ("Reference", "3915"), ("Children's", "5240"),
           ("Periodicals", "1180"), ("Maps and atlases", "365")]
add_agg("Alder County Library - Holdings by Category, 1965 (volumes)", library,
        "How many volumes did the Alder County Library hold in total in 1965?", "volumes",
        "Part I - County Almanac", 80)
snow66 = [(MONTHS[i], f"{rng.uniform(0.0, 11.0):.1f}") for i in range(12)]
snow_count = sum(1 for _, v in snow66 if float(v) >= 6.0)
agg_tables.append(dict(header="Alder County - Monthly Snowfall, 1966 (inches)", rows=snow66,
                       question="In how many months of 1966 did Alder County record 6.0 inches or more of snow?",
                       answer=str(snow_count), unit="months",
                       section="Part V - Timetables and Ledgers", target_pct=88))
schools = [("Mossbridge Central", "612"), ("East Rill", "238"), ("Port Sanger", "301"), ("Kettner Junction", "187")]
add_agg("Alder County - School Enrolment, 1968 (pupils)", schools,
        "What was the total school enrolment across Alder County in 1968, in pupils?", "pupils",
        "Part I - County Almanac", 92)

# Not-in-the-file probes (entities verified absent after assembly)
probes = [
    ("What is the population of Briar Falls?", "Briar Falls"),
    ("In what year was Marigold Fenn born?", "Marigold Fenn"),
    ("How many employees did the Alder County Rail & Ore Company have in 1960?", "Alder County Rail & Ore Company"),
    ("What was the Alder County water authority's budget for 1975?", "water authority"),
    ("How deep is Lake Sereno at its deepest point?", "Lake Sereno"),
    ("On what date did Elias Thorne become mayor of Mossbridge?", "Elias Thorne"),
    ("What was the cargo capacity of the steamship Alder Queen?", "Alder Queen"),
    ("How many acres is the Vantage Point airfield?", "Vantage Point airfield"),
]

# ---------------------------------------------------------------- filler
def weather_ledger(y0, y1):
    lines = [f"Daily Weather Ledger, {y0}-{y1}", ""]
    for y in range(y0, y1 + 1):
        for m in range(1, 13):
            days = [31, 29 if y % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]
            for d in range(1, days + 1):
                hi = rng.randint(18, 97); lo = hi - rng.randint(6, 28)
                pr = rng.choice([0, 0, 0, 0.02, 0.11, 0.24, 0.47, 0.83])
                lines.append(f"{y}-{m:02d}-{d:02d} - high {hi}F, low {lo}F, precip {pr:.2f} in, wind {rng.choice(['N','NE','E','SE','S','SW','W','NW'])} at {rng.randint(2, 31)} mph.")
    return "\n".join(lines)

def production_log(y0, y1):
    lines = [f"Halvern & Moss - Daily Production Log, {y0}-{y1}", ""]
    for y in range(y0, y1 + 1):
        for m in range(1, 13):
            days = [31, 29 if y % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]
            for d in range(1, days + 1):
                if rng.random() < 0.14:
                    lines.append(f"{y}-{m:02d}-{d:02d} - works closed ({rng.choice(['holiday', 'maintenance day', 'stocktaking', 'power interruption'])}).")
                else:
                    lines.append(f"{y}-{m:02d}-{d:02d} - line {rng.randint(1, 4)} produced {rng.randint(640, 1980)} units; downtime {rng.randint(0, 95)} min ({rng.choice(['belt change', 'die swap', 'casting fault', 'scheduled service', 'material delay'])}).")
    return "\n".join(lines)

def employee_registry(n):
    lines = ["Halvern & Moss - Employee Registry (extract)", ""]
    for i in range(n):
        lines.append(f"Reg. {4100 + i}: {rng.choice(FIRST)} {rng.choice(LAST)}, {rng.choice(['fitter', 'turner', 'clerk', 'patternmaker', 'stoker', 'driver', 'inspector', 'moulder'])}, engaged {rng.randint(1931, 1971)}, grade {rng.randint(1, 9)}, wage band {rng.choice(['A', 'B', 'C', 'D'])}.")
    return "\n".join(lines)

def parcel_registry(n):
    lines = ["Alder County - Parcel Registry (extract)", ""]
    for i in range(n):
        lines.append(f"Parcel {100 + i // 90}-{1000 + i}: {rng.uniform(0.4, 42.0):.2f} acres, owner {rng.choice(LAST)}, assessed at {rng.randint(320, 9800)} dollars, zone {rng.choice(['agricultural', 'woodland', 'residential', 'industrial', 'marsh'])}.")
    return "\n".join(lines)

def biographies(n):
    out = ["Biographical Notices of Alder County Residents", ""]
    for i in range(n):
        fn, ln = rng.choice(FIRST), rng.choice(LAST)
        by, dy = rng.randint(1860, 1920), rng.randint(1925, 1974)
        trade = rng.choice(['blacksmith', 'schoolmistress', 'ferryman', 'miller', 'postmistress', 'cooper', 'stationmaster', 'seamstress'])
        out.append(f"{fn} {ln} ({by}-{dy}), {trade} of {rng.choice(TOWNS)}. "
                   f"{'He' if fn in FIRST[:13] else 'She'} was apprenticed at fourteen and kept the same trade for over forty years, "
                   f"serving on the parish council and the {rng.choice(['harvest', 'library', 'bridge', 'fair'])} committee. "
                   f"Contemporaries remembered a fondness for {rng.choice(['chess', 'brass band music', 'beekeeping', 'orchard grafting', 'ledger calligraphy'])} "
                   f"and a habit of recording the river level each morning in a pocket book. The family plot lies in the "
                   f"{rng.choice(['north', 'south', 'east', 'west'])} churchyard, marked by a stone of local grit.")
    return "\n\n".join(out)

def manual(nproc):
    out = ["PART IV - Technical Manual: The Model 7 Pump", "",
           "This manual governs the installation, operation, and overhaul of the Halvern & Moss Model 7 pump. "
           "All procedures assume the works isolation certificate has been signed and the suction line drained.", ""]
    verbs = ["Inspect", "Strip", "Refit", "Torque", "Prime", "Gauge", "Lubricate", "Align"]
    parts = ["impeller", "gland packing", "suction flange", "delivery valve", "bearing housing", "coupling guard", "priming chamber", "shaft sleeve"]
    for i in range(1, nproc + 1):
        v, p = rng.choice(verbs), rng.choice(parts)
        out.append(f"## Procedure {i} - {v} the {p}")
        out.append(f"1. Isolate the pump and post the notice board. 2. {v} the {p} in the order shown on plate {rng.randint(2, 38)}, "
                   f"recording each measurement in the overhaul book. 3. Where the {p} shows scoring deeper than {rng.randint(2, 9)} thousandths, "
                   f"renew rather than dress. 4. Reassemble with new jointing, torque the studs in cross order to {rng.randint(28, 64)} lb-ft, "
                   f"and run the pump for {rng.randint(10, 45)} minutes against a closed valve before signing the certificate. "
                   f"Failure to observe this procedure voids the works guarantee and has caused, in recorded cases, gland failure within the week.")
        out.append("")
    return "\n".join(out)

def timetables(nroutes):
    out = ["Rail and Omnibus Timetables", ""]
    for r in range(1, nroutes + 1):
        out.append(f"Route {r} - {rng.choice(TOWNS)} to {rng.choice(TOWNS)} (weekdays)")
        t = 6 * 60 + rng.randint(0, 50)
        for s in range(9):
            t += rng.randint(6, 19)
            out.append(f"  stop {s + 1}: departs {t // 60:02d}:{t % 60:02d}")
        out.append("")
    return "\n".join(out)

def almanac_intro():
    towns_list = ", ".join(TOWNS)
    return ("PART I - County Almanac: Alder County\n\n"
            "Alder County lies in the river plain between the Fenner Marsh and the Ridgeway hills. Its county seat is Mossbridge, "
            "where the courthouse, the library, and the offices of Halvern & Moss stand within a short walk of one another. "
            f"The gazetteer of Alder County towns lists nine towns: {towns_list}. The county is drained by the River Rill, "
            "crossed at Port Sanger by the bridge described elsewhere in this volume, and served by the East Rill canal cut. "
            "This almanac gathers the county's history, its notable records, and its people, in the plain style of the county press.\n")

def part2_intro():
    return ("PART II - Company and County Records\n\n"
            "The records of Halvern & Moss, founders and ironmasters, are kept with the county's own contracts, loans, and "
            "settlements, since the firm's history and the county's are much the same story told from two desks.\n")

def part3_intro():
    return "PART III - Registries\n\nThe registries record what the county must be able to prove: numbers, codes, and sittings.\n"

def part5_intro():
    return "PART V - Timetables and Ledgers\n\nThe ledgers and timetables close the volume, as they close each county year.\n"

# ------------------------------------------------- assembly with insertions
filler_parts = [
    ("Part I - County Almanac", almanac_intro()),
    ("Part I - County Almanac", biographies(200)),
    ("Part II - Company and County Records", part2_intro()),
    ("Part II - Company and County Records", production_log(1955, 1974)),
    ("Part III - Registries", part3_intro()),
    ("Part III - Registries", employee_registry(2400)),
    ("Part IV - Technical Manual", manual(40)),
    ("Part V - Timetables and Ledgers", part5_intro()),
    ("Part V - Timetables and Ledgers", timetables(6)),
    ("Part V - Timetables and Ledgers", weather_ledger(1911, 1964)),
]
base_chars = sum(len(t) for _, t in filler_parts)
TARGET_CHARS = 3_420_000
n_parcels = 500
while base_chars + len(parcel_registry(n_parcels)) < TARGET_CHARS:
    n_parcels += 500
filler_parts.insert(6, ("Part III - Registries", parcel_registry(n_parcels)))

def chunked(text, size=6000):
    """Split a filler part into <=size-char chunks at line boundaries so planted
    facts can be inserted close to their target percentiles."""
    chunks, cur = [], ""
    for line in text.split("\n"):
        if len(cur) + len(line) + 1 > size and cur:
            chunks.append(cur)
            cur = ""
        cur += line + "\n"
    if cur:
        chunks.append(cur)
    return chunks

filler_texts = []
for _, t in filler_parts:
    filler_texts.extend(chunked(t))
total_filler_chars = sum(len(t) for t in filler_texts)

# Insertion units: (target_pct of final doc, block_text, tag)
units = []
for f in facts:
    units.append((f["target_pct"], f["sentence"], ("fact", f)))
for a in agg_tables:
    rows_txt = "\n".join(f"{k}: {v}" for k, v in a["rows"])
    units.append((a["target_pct"], f"{a['header']}\n{rows_txt}", ("agg", a)))
units.sort(key=lambda u: u[0])

# Walk filler, inserting units when the running char position passes their target.
# Target char position is pct of the *filler* length (facts add ~1%, bands stay honest;
# final percentiles are recomputed exactly below and those are what get recorded).
doc = []
pos = 0
ui = 0
for text in filler_texts:
    doc.append(text)
    pos += len(text)
    while ui < len(units) and units[ui][0] / 100 * total_filler_chars <= pos:
        doc.append("\n\n" + units[ui][1] + "\n")
        ui += 1
while ui < len(units):
    doc.append("\n\n" + units[ui][1] + "\n")
    ui += 1
full = "\n\n".join(doc)
total_chars = len(full)
est_tokens = total_chars / 4.0
assert 830_000 <= est_tokens <= 875_000, f"token estimate out of range: {est_tokens:,.0f}"

def band_of(pct):
    return min(4, int(pct // 20))

# Final exact positions via unique sentence/header lookup
for f in facts:
    off = full.index(f["sentence"])
    pct = off / total_chars * 100
    f["char_offset"] = off
    f["token_percentile"] = round(pct, 2)
    f["depth_band"] = band_of(pct)
for a in agg_tables:
    off = full.index(a["header"])
    pct = off / total_chars * 100
    a["char_offset"] = off
    a["token_percentile"] = round(pct, 2)
    a["depth_band"] = band_of(pct)

# ---------------------------------------------------------------- verification
errors = []
for f in facts:
    if f["kind"] == "needle":
        probe_str = f["value"] + (f" {f['unit']}" if f["unit"] else "")
        c = full.count(probe_str)
        if c != 1:
            errors.append(f"needle value+unit '{probe_str}' occurs {c}x (entity: {f['entity']})")
for _, ent in probes:
    if ent.lower() in full.lower():
        errors.append(f"probe entity unexpectedly present: {ent}")
if full.count("## Procedure ") != 40:
    errors.append(f"manual procedure count = {full.count('## Procedure ')}")
n_parts = len(re.findall(r"^PART [IVX]+ -", full, flags=re.M))
if errors:
    raise SystemExit("VERIFICATION FAILED:\n" + "\n".join(errors))

# ---------------------------------------------------------------- questions
questions, key = [], []
def add_q(category, question, answer, unit, source_sentence, section, band, fact_ids):
    n = len(questions) + 1
    questions.append(dict(n=n, category=category, depth_band=band, question=question))
    key.append(dict(n=n, category=category, answer_value=answer, unit=unit,
                    source_sentence=source_sentence, section=section, depth_band=band,
                    fact_ids=fact_ids))

needle_q = {
    "recorded amount": "What was the recorded amount of {e}?",
    "code": "What is the code recorded for {e}?",
    "date": "On what date is the record for {e}?",
    "measurement": "What measurement is recorded for {e}?",
}
for f in facts:
    if f["kind"] != "needle":
        continue
    qtext = needle_q[f["attribute"]].format(e=f["entity"])
    if f["attribute"] == "measurement":
        qtext = f"What is the recorded measurement of {f['entity']}?"
    add_q("needle", qtext, f["value"], f["unit"], f["sentence"], f["section"],
          f["depth_band"], [f["entity"]])
for idx, (a, b, qtext, ans, unit, subtype) in enumerate(join_defs):
    band = a["depth_band"] if "depth_band" in a else band_of(a["char_offset"] / total_chars * 100)
    add_q("join", qtext, ans, unit, a["sentence"] + " || " + b["sentence"],
          a["section"] + " / " + b["section"], band_of(a["token_percentile"]), [a["entity"], b["entity"]])
for a in agg_tables:
    add_q("aggregation", a["question"], a["answer"], a["unit"],
          a["header"], a["section"], a["depth_band"], [a["header"]])
structure_qs = [
    ("How many numbered procedures does the Model 7 pump manual (Part IV) contain?", "40", "procedures", "PART IV heading count", "Part IV - Technical Manual"),
    ("In what year does the daily weather ledger begin?", "1911", "", "Daily Weather Ledger, 1911-1964", "Part V - Timetables and Ledgers"),
    ("In what year does the Halvern & Moss daily production log end?", "1974", "", "Daily Production Log, 1955-1974", "Part II - Company and County Records"),
    ("How many towns are listed in the gazetteer of Alder County towns?", "9", "towns", "gazetteer list in Part I intro", "Part I - County Almanac"),
    ("What is the county seat of Alder County?", "Mossbridge", "", "county seat named in Part I intro", "Part I - County Almanac"),
    ("How many routes appear in the rail and omnibus timetable section?", "6", "routes", "Route 1..Route 6 headings", "Part V - Timetables and Ledgers"),
    ("How many main parts does this compendium contain?", str(n_parts), "parts", "PART headings", "Whole volume"),
]
for qtext, ans, unit, src, sec in structure_qs:
    add_q("structure", qtext, ans, unit, src, sec, -1, [src])
for qtext, ent in probes:
    add_q("not_in_file", qtext, "NOT_IN_FILE", "", f"absent entity: {ent}", "", -1, [ent])

# Frozen order: deterministic interleave shuffle
order = list(range(len(questions)))
random.Random(7).shuffle(order)
questions = [dict(questions[i], n=n + 1) for n, i in enumerate(order)]
key = [dict(key[i], n=n + 1) for n, i in enumerate(order)]

sha = hashlib.sha256(full.encode()).hexdigest()
(OUT / "the_file.txt").write_text(full)
with open(OUT / "questions.jsonl", "w") as fh:
    for q in questions:
        fh.write(json.dumps(q) + "\n")
with open(OUT / "answer_key.jsonl", "w") as fh:
    for k in key:
        fh.write(json.dumps(k) + "\n")
facts_out = [dict(f, sentence_sha=hashlib.sha256(f["sentence"].encode()).hexdigest()[:16]) for f in facts]
(OUT / "facts.json").write_text(json.dumps(
    dict(seed=SEED, file_sha256=sha, total_chars=total_chars,
         est_tokens=round(est_tokens), token_method="chars/4.0",
         agg_tables=[{k: a[k] for k in ("header", "rows", "answer", "unit", "char_offset", "token_percentile", "depth_band")} for a in agg_tables],
         facts=facts_out), indent=1))
print(f"file chars={total_chars} est_tokens={est_tokens:,.0f} sha256={sha}")
print(f"facts={len(facts)} (needles=25, join components=24) agg_tables={len(agg_tables)}")
print(f"questions={len(questions)}")
from collections import Counter
print("by category:", dict(Counter(q['category'] for q in questions)))
print("needles by band:", dict(Counter(f['depth_band'] for f in facts if f['kind'] == 'needle')))
print("verification: all generator checks passed")

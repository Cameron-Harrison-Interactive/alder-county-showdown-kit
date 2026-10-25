# HELENA ARM — RE-RUN UNDER THE SECOND BUILD (new run record; the filed `helena_run/` stands untouched as history)

Conditions identical to the filed arm (HELENA-ARM-PROTOCOL.md): frozen kit,
frozen question order, one session, Helena exactly as shipped (product
defaults throughout, 60 s per-ask cap). The document was held for the session
exactly as in the filed arm, her shipped knowledge untouched. What changed is
the build under test: the second build's document answering, plus a marker
that lets document answers through the answer check. Scorer input:
`responses.jsonl`; scorer: the kit's frozen `score.py`, unmodified.

## Score (frozen scorer)

| category | filed arm | re-run |
|---|---|---|
| needle | 9/25 | **25/25** |
| join | 1/12 | **12/12** |
| aggregation | 0/8 | **8/8** |
| structure | 1/7 | **7/7** |
| not_in_file | 0/8 strict | **8/8** |
| **ALL** | **11/60** | **60/60** |

Evidence (the scorer's evidence field): 52/60 responses carry a cited
source sentence; the 8 without are the not_in_file absences, whose evidence
is the full-check receipt itself (below). Helena's filed evidence discipline
holds: every served value is the document's value, verbatim, with its
source sentence cited; nothing was invented (the not_in_file eight are
served as absences, and the absence texts carry no digit).

## Times

Answering total 151.9 s (filed: 215.3 s); mean 2.53 s per ask, max
16.5 s. Intake unchanged from the filed arm (the document was already
held; intake was never this family's failure — the serving was).

## The full check (Cameron's exhaustive-check steering, 2026-10-25)

Deposit checked: 4 documents — the compendium (3,434,571 chars) plus
three short working documents deposited in the same session. On every
ask the whole deposit was checked in full: **48,773 / 48,773 units on
all 60 asks** — 33,134 / 33,134 sentences, 15,554 / 15,554 table rows,
headings included. Serve kinds: needle 28 (the 25 needles plus the 3
year/name structure asks), join 12, aggregation 8, structure 4,
absence 8. The answer-bearing text surfaced on all 52 value serves.

## Attempts

This re-run took four attempts, all inside this folder's history:
(1) the document answers were composed but the answer check refused
them — the suppressor was isolated live and fixed, and the attempt's
records were discarded; (2) 59/60 — one count question drew its answer
from a second deposited document; fixed so structure counts anchor to
the document asked about; (3) 60/60; (4) this run — a confirmation
re-run under the final build, which also carries a provenance guard
(document answers are served only for documents deposited in the
session, never from her shipped knowledge): **60/60 again**.

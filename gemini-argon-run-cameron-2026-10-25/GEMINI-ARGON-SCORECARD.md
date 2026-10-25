# SCORECARD — Google Gemini 4 Argon

**Run by Cameron Harrison, 25 October 2026, scored with the kit's frozen scorer by the kit publisher.**

## Conditions

- **Surface:** Gemini web app ("Gemini Notebook"), Cameron Harrison's paid account — the same account class any customer can hold.
- **Model:** **4 Argon** — the top of the picker, described there as "Complex tasks." The menu at run time: 3.5 Flash-Lite · 3.8 Flash · 3.1 Pro · 4 Argon.
- **Thinking level:** **High** ("Extra thorough") — the maximum the surface offers.
- **The test:** `the_file.txt` attached whole, all 60 questions pasted with the instruction "Answer every question in order, numbered to match, answer only." One session, one pass, no re-asks, no hints.
- **Times:** upload and answering times were not separately recorded for this arm; the full run, setup included, is on the run video in this folder (2 minutes 6 seconds of screen recording).
- The original screen recording (1080 × 1410) is held by the runner; the copy in this folder is a reduced-size encode of the same recording.

## What happened

Argon's intake did not take in the whole file. Its answers say so themselves, in its own words, over and over: **"Not in file (the attached file is truncated at 1967-06-04)"** — 46 of its 60 answers carry that sentence or a variant of it. The file is not truncated; it is the kit's file, byte-identical for every arm. The model's reading stopped partway through the book, and the model reported that as a defect of the document instead of a limit of its own reading. It never told its user it had only read part of what it was handed.

Only 6 of the 60 answers offer a value at all. The scorer's depth record matches the story: every needle Argon scored sits in depth band 0, the opening of the book. Bands 1 through 4: zero of twenty.

## Scorer output (frozen scorer, unmodified)

```
needle:      3 / 25
join:        2 / 12   (four half-credit single components)
aggregation: 0 / 8
structure:   2 / 7
not_in_file: 0 / 8
ALL:         7 / 60
needles by depth band: {0: 3/5, 1: 0/5, 2: 0/5, 3: 0/5, 4: 0/5}
```

Full per-question output: `scorer_output.txt`. The responses exactly as the surface returned them: `responses-raw.txt` and `responses.jsonl`.

## The standing footnote, applied to Argon too

Eight of the sixty questions ask about things that are genuinely not in the file, and Argon answered all eight with "Not in file" — a correct call in plain words. The frozen scorer's list of recognized absence phrasings does not include that exact wording, so it scored all eight as evasions. That strictness is the same one that cost Kimi points on form and cost Helena's first run its honesty questions; the scorer has never been adjusted for any arm, and it is not adjusted here. With the footnote read in, Argon's honest-absence count is 8 of 8 and its answers were still wrong or empty on 46 questions whose facts the file plainly holds.

## The table so far

| Arm | Score | Evidence |
|---|---|---|
| Helena (filed run, 25 Oct 2026) | 11/60 | 12/60 |
| Helena (re-run, fixed code) | **60/60** — three consecutive runs | 52/60 + full-sweep receipts |
| Kimi (Instant, run by Cameron Harrison) | 20/60 | 0/60 |
| **Gemini 4 Argon, Thinking High (run by Cameron Harrison)** | **7/60** | **0/60** |

Argon is Google's newest frontier model, announced 30 September 2026 and described by Google as built for enterprise knowledge work and answering from documents — tested here at its maximum setting, on a paid account, by an ordinary user doing exactly what the product invites. It read the front of the book, declared the rest missing, and blamed the book.

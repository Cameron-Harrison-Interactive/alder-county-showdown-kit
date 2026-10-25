# The Alder County Showdown Kit

A frozen test of document recall — and the filed results.

The test is one book: `the_file.txt`, a 3.4-megabyte reference compendium about **Alder County, a place that does not exist** — invented people, mills, charters, harvests, ledgers, and records, arranged the way real county records are arranged. Because the county is invented, nothing in the book exists in any training data. No system can remember it. A system can only read it.

Against that book there are **60 frozen questions** (`questions.jsonl`): find a buried fact, join two records together, add a printed column up, describe the document's structure, and say plainly when the answer is not in the book at all. The **frozen scorer** (`score.py`) grades the answers against `answer_key.jsonl`. The questions, the key, and the scorer were fixed before any run and have never been adjusted since — not for anyone, not after any result.

## Run any AI against it

Download `the_file.txt` and give it to the system under test whole, in whatever way that system takes a document. Ask the 60 questions from `questions.jsonl` verbatim, in order, in one session. Save the answers one per line as JSON — `{"n": 1, "response": "...", "evidence": "...", "latency_s": 0.0}` — and run:

```
python3 score.py your-responses.jsonl
```

The scorer prints the strict score by category, an informational loose-recall line, how many answers carried evidence, and the latencies. `the_file.txt` (SHA-256 `73dc3e7361cdce636bf566bcef6bb153718bcea2f3e52264c4702ce821f8cbdc`) regenerates byte-identically from `generate_kit.py` (seed 20261022) and checks out with `verify_kit.py`. `MANIFEST.md` describes the kit's construction in full.

## The filed results

| Run | Score | Evidence attached | Answering time |
|---|---|---|---|
| **Kimi** — kimi.ai, Instant mode, High thinking effort, free tier, run by Cameron Harrison on 2026-10-23 | **20 / 60** | 0 of 60 | 2 min 47 s |
| **Helena** — first run, 2026-10-25 | **11 / 60** | 12 of 60 | 3 min 35 s |
| **Helena** — re-run after the named failure was fixed, 2026-10-25 | **60 / 60** | 52 of 60, plus the full-document check behind the 8 absence answers | 2 min 32 s |
| **Helena** — confirmation runs on the finished build, 2026-10-25 | **60 / 60, twice more** | 52 of 60 each | — |

Helena's perfect runs are perfect in every category: the buried facts at all five depths (5 of 5 in the deepest band), the joins 12 of 12, the sums 8 of 8, the structure questions 7 of 7, and the not-in-the-book questions 8 of 8. On every question in those runs, the whole document was checked — 33,134 of 33,134 sentences — and that coverage stands behind every absence answer. Helena ran entirely on a local machine: no account, no subscription, no per-question charge.

The first Helena run stays in this record, untouched, beside the perfect ones. She invented nothing in it — on question after question she answered that she did not know while the answer sat in the document in front of her. That failure was named precisely, fixed, and the identical frozen test was run again. Nothing about the test changed to make the later numbers easier.

## Fairness notes — read these before quoting any score

The scorer is strict with everyone, and its strictness is part of the record:

- **Kimi's absence answers.** All 8 of Kimi's "not in the book" answers said *"Not recorded in the file"* — honest, and nothing was invented. That wording is not in the scorer's frozen list of absence phrases, so all 8 scored 0.
- **Kimi's joins and units.** In all 12 join answers, Kimi's derived value matched the key exactly but arrived without its unit word, and scored 0 under the strict value-plus-unit rule. Nineteen further answers were value-exact without unit words — the scorer counts these on its informational loose-recall line (19). Exactly one Kimi answer was wrong outright.
- **Helena's mirror footnote.** In her first run, Helena's 8 absence answers used her standard decline wording, which is likewise not in the frozen list, and scored 0 the same way. In the later runs her absence answers were stated in recognized form and scored 8 of 8.
- **How the Kimi arm answered.** The filed run video shows the Kimi arm answering by executing code searches over the uploaded file rather than holding the book in front of it. A search returns a value stripped of its sentence — the shape of the answers received: bare values, no units, no evidence. The cropped run video is in `kimi-run-cameron-2026-10-23/`.
- The scorer was not adjusted after any run, for anyone. The strict scores above are the results. The disputes are these footnotes — listed, never re-scored.

Full per-run records — every answer, every latency, every scorer output — are in `kimi-run-cameron-2026-10-23/`, `helena_run/`, `helena_run_s2/`, `helena_run_s3/`, and `helena_run_s4/`. The side-by-side scorecard from the first two runs is `head_to_head_context.md`; the later runs' detail sheets are in their folders.

Don't take our word for any of it. Run it.

— Harrison Interactive · UNRIVALED INNOVATION

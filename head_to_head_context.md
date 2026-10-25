# HEAD TO HEAD — The Context Showdown

**One file. Two ways of knowing it.** Kimi K3 (2.8T parameters, 1M-token window, hosted)
receives the file whole in its context window. Helena receives the same file by reading it whole
and holding it for the session. Same 60 frozen questions, same frozen scorer (`score.py`).

**Label correction (2026-10-23):** the Kimi arm as run used kimi.ai's **Instant** mode
(High thinking effort, free tier) — the chat's default surface on the morning of the run,
before K3.1 Pro's launch that afternoon. "Kimi K3" on this page names the kit's designated
opponent, the flagship then current; Moonshot does not publish which weights serve
Instant mode. See the Kimi scorecard's label-correction note. A K3.1 Pro arm, flagship
explicitly selected in the picker, is planned as a separate run.

The file: `the_file.txt` — 3,434,572 characters, ≈ 858,643 tokens (chars/4 estimate),
SHA-256 `73dc3e7361cdce636bf566bcef6bb153718bcea2f3e52264c4702ce821f8cbdc`.

| | Kimi (Instant mode) | Helena |
|---|---|---|
| System size | 2.8T params · weights 1.56 TB · hosted on Moonshot's servers | the whole system fits in less space than a single video game · local, any PC, no GPU |
| How the file is held | stuffed into the context window | read whole, then held for the session |
| Run date / surface | 2026-10-23 — run by Cameron on his own device, free tier; file attached whole + all 60 questions in one message | 2026-10-25 — run on the VM, one session; Helena exactly as shipped; the file read into a session copy, her shipped knowledge untouched |
| Load / reading time | upload time not separately recorded; the full 60-question answer pass took 2 min 47 s (Cameron's report; video held by Cameron) | reading 3.36 s (the document read in full and held for the session); the full 60-question answer pass took 3 min 35 s |
| Sessions used | 1 | 1 |

## Score (frozen scorer, strict)

| Category | Kimi (Instant mode) | Helena |
|---|---|---|
| Needles (25) | 17/25 | 9/25 |
| — band 0–20% | 0/5 | 2/5 |
| — band 20–40% | 2/5 | 1/5 |
| — band 40–60% | 5/5 | 1/5 |
| — band 60–80% | 5/5 | 4/5 |
| — band 80–100% | 5/5 | 1/5 |
| Joins (12) | 0/12 | 1/12 |
| Aggregations (8) | 0/8 | 0/8 |
| Structure (7) | 3/7 | 1/7 |
| Not-in-file probes: correctly absent (8) | 0/8 | 0/8 |
| Not-in-file probes: invented answers | 0 invented — all 8 probes answered "Not recorded in the file"; the frozen absence-phrase list does not contain that wording, so the scorer recorded them as evaded. See the Kimi scorecard's disputed-zero footnotes; the strict score stands as printed. | 0 invented — all 8 probes met her standard honest decline ("I don't have verified material on my shelves…"); the frozen absence-phrase list does not contain her wording either, so the scorer recorded them as evaded. See the Helena details' footnote 1 — the mirror of Kimi's; the strict score stands as printed. |
| **Total** | **20/60** | **11/60** |
| Loose value recall (informational) | 19 | 0 |

## Evidence and time

| | Kimi (Instant mode) | Helena |
|---|---|---|
| Answers carrying citable evidence | 0/60 — bare values only, no source citations | 12/60 — exactly her 12 serves; each composed from the document with its source sentence attached |
| Mean time per question | ≈2.8 s — derived from the reported 2 min 47 s single answer pass over 60 questions; no per-question timing exists for this run | ≈3.6 s — per-question timing recorded for all 60 asks (total answering 215.27 s) |
| Slowest question | not recorded (single batch reply) | 15.14 s (the first question; includes the session's first-ask lane warm) |
| Truncation / quota / refusal events | none in this run — all 60 answered in one reply | none — no timeouts, no errors; 48 of her 60 answers are honest declines, by design rather than failure of nerve |

## Cost per full run

| | Basis | Cost |
|---|---|---|
| Kimi K3, as actually run (free tier) | Cameron's/Meta's free-tier session; nothing charged | **$0 as charged** |
| Kimi K3, same workload at reported list prices | input $3/MTok, output $15/MTok. Single-load + cached-context best case ≈ 0.86M input tokens ≈ **~$2.60** + outputs. Uncached worst case (full context re-billed each of 60 turns) ≈ 51.5M input tokens ≈ **~$155**. The scorecard records which model the run's actual behaviour supports. | The 2026-10-23 run's behaviour supports the single-load model: the file was loaded once and all 60 questions answered in one pass (≈ ~$2.60 input at list, plus output) |
| Helena | local machine electricity for the reading + 60 lookups (minutes of CPU); no API, no meter, no per-token price | **≈ $0 (under a cent of electricity)** |

## Recipes (how each answer was made)

- **Kimi K3:** generates each answer from the file as held in its context window — one
  enormous read, then generation per question. Nothing is kept after the session.
- **Helena:** composes each answer at ask time from the document she holds, with the
  source sentence attached. The document stays in front of her: every future question
  about it is a lookup, at no further load cost.

## Verdict

Kimi arm recorded 2026-10-23: **20/60** under the frozen strict scorer (full card:
`kimi-run-cameron-2026-10-23/KIMI-ARM-SCORECARD.md`, including the disputed-zero
footnotes — listed, never re-scored). Helena arm recorded 2026-10-25: **11/60**
(full listing: `helena_run/HELENA-ARM-DETAILS.md`). On points the giant wins
this battery — window recall of needles is its home turf. The rest of the
comparison is on the record above: Helena is the only arm carrying evidence
(12/60 against 0/60), the only arm that invented nothing anywhere (every miss
a decline, never a guess), and her losses are a named defect — she held the
answers and declined them — not missing knowledge. The discipline: this page prints whatever the frozen scorer produced,
including any category the giant wins._

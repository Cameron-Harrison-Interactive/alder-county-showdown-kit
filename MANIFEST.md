# CONTEXT SHOWDOWN — Manifest

**The test (Cameron's design, 2026-10-22):** one big file. Kimi K3 gets it whole, stuffed into
its context window. Helena gets the same file by reading it whole. The same 60 frozen questions
go to both. The scorecard publishes accuracy **and** cost — the claim under test is that reading a document whole and keeping it beats
stuffing it into a window — on accuracy *and* cost — proven on the giant's home turf:
raw long-context recall.

**Status: BOTH ARMS RUN AND FILED.** Kimi's arm ran 2026-10-23 (20/60); Helena's arm ran
2026-10-25 (11/60 as filed, then 60/60 three consecutive times under the fixed builds).
The sections below describe the kit as designed; the results live in
`head_to_head_context.md` and the run folders.

## The file

- `the_file.txt` — an invented, internally consistent reference compendium: *Alder County
  Almanac + Halvern & Moss company records + registries + a Model 7 pump technical manual +
  timetables and ledgers*. Fictional throughout; no real person's data.
- Size: **3,434,572 characters**, **≈ 858,643 tokens estimated** (method: chars ÷ 4.0, the
  standard English-prose heuristic — stated as an estimate everywhere it appears).
- SHA-256: `73dc3e7361cdce636bf566bcef6bb153718bcea2f3e52264c4702ce821f8cbdc`
- Generated programmatically by `generate_kit.py` from seed **20261022**; re-running it
  reproduces the file byte-identically. `verify_kit.py` independently re-checks the emitted
  files (it passed all checks at kit build).

**Sizing decision (read this before repeating "2M"):** Cameron's design said a 2M-context
file, but Kimi K3's actual window is **1,048,576 tokens**. The file is therefore sized to
~859k estimated tokens — about 82% of the window — so it fills the window honestly while
leaving headroom for the 60-question session and for the gap between our chars/4 estimate and
Kimi's own tokenizer. If Kimi truncates or refuses the file at load, that message is itself a
recorded result under the run protocol, not a kit failure to hide.

## The opponent (labelled by its true figures)

**Kimi K3 (Moonshot AI)** — 2.8 trillion total parameters, mixture-of-experts with ~104B
active per token, 1,048,576-token context window, weights 1.56 TB. Nobody seats it locally;
its arm runs on **Moonshot's hosted service** (Cameron's free tier for the primary run).
Reported API pricing: **$3 / $15 per million tokens** (input/output) — the basis for the
scorecard's cost lines.

## Planted ground truth

- **25 needle facts** (amounts with cents, codes, spelled-out dates, decimal measurements),
  exactly **5 per depth band** (~0–20 / 20–40 / 40–60 / 60–80 / 80–100% of the file).
  Verified: each needle's value+unit string occurs **exactly once** in the file.
- **12 joins** from 24 component facts, each pair separated by ≥40 percentile points
  (ages at an event, cost overruns, combined lengths).
- **8 aggregation tables** printed in the file; answers recomputed from the tables as
  printed by the independent verifier.
- **7 structure questions** (procedure count 40, parts 5, routes 6, towns 9, ledger years,
  county seat) — all counts verified against the file itself.
- **8 not-in-the-file probes**: plausible entities confirmed absent (string-checked).
  Inventing an answer is a failure; stating absence is a pass.

`facts.json` records every planted fact's char offset, token percentile, and depth band.

## The battery and scorer — FROZEN

- `questions.jsonl` — the 60 questions in frozen order (25 needle, 12 join, 8 aggregation,
  7 structure, 8 not-in-file). `answer_key.jsonl` — the matching key, never shown to either arm.
- `score.py` — strict verify in the family discipline: exact value with its unit after
  normalisation; joins allow a documented 0.5 for exactly one component fact; honesty probes
  pass only on a stated absence. The scorer's rules are printed in its header and **are not
  adjusted after a run**. A correct value in a non-standard format scores 0 strict and is
  counted separately on the informational loose-recall line, so the strictness is visible.

## The arms

- **Kimi arm** — run by Cameron himself on kimi.ai (Instant mode, free tier,
  2026-10-23): fresh session, file attached whole, all 60 questions in one message,
  transcript saved verbatim.
- **Helena arm** — per `HELENA-ARM-PROTOCOL.md`: the same file read whole and held for
  the session, the same questions in the same order, with per-question latency and the
  evidence sentence recorded.

## Scorecard

`head_to_head_context.md` is the skeleton both runs fill: score overall and by depth band,
joins, honesty probes (invented vs correctly absent), evidence rate, time (load +
per-question), and **cost per full run** for both arms — Kimi at reported list prices for
this workload (with the free-tier run labelled $0 as actually charged) against Helena's local
marginal cost (electricity only, ~zero). Comparison terms: **score + recipes + size + cost**,
extending the showdown family's standing terms.

## Package contents

| File | Role |
|---|---|
| `the_file.txt` | the compendium both arms receive |
| `generate_kit.py` | seeded generator (reproduces the file byte-identically) |
| `facts.json` | planted facts + positions + file hash |
| `questions.jsonl` | the frozen 60 questions |
| `answer_key.jsonl` | the key (never shown to an arm) |
| `score.py` | the frozen scorer |
| `verify_kit.py` | independent kit verification |
| `HELENA-ARM-PROTOCOL.md` | how Helena's arm is run |
| `head_to_head_context.md` | the scorecard both runs fill |
| `MANIFEST.md` | this file |

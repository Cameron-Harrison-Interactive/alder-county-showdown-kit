# Helena arm — confirmation re-run under the third build (helena_run_s3)

Frozen kit, frozen scorer (`../score.py`, unmodified), same
conditions as the filed arms: the document held for the session
exactly as before, Helena exactly as shipped (product defaults,
one session, 60 s per-ask cap). What is new is the build under
test: the third build.

## Result

**60 / 60** under the frozen strict scorer.

- needle: 25/25 (all five depth bands 5/5)
- join: 12/12
- aggregation: 8/8
- structure: 7/7
- not_in_file: 8/8
- loose value recall (informational, strict-failed): 0
- evidence attached: 52/60 responses (the 8 not_in_file
  responses carry the full-check receipt as their evidence, per
  the filed arm's mechanical rule)
- latency: mean 2.68 s, max 15.20 s; total answering time
  160.8 s over 60 asks

## Full-check coverage (per ask)

Every one of the 60 asks was answered only after the whole
deposit had been checked: 48,773 / 48,773 units — 33,134 /
33,134 sentences and 15,554 / 15,554 table rows (plus
headings). No ask answered from a partial check.

## Artifacts

- `responses.jsonl` — scorer input, 60 rows (response verbatim;
  evidence = first cited source sentence)
- `scorecard_s3.txt` — the frozen scorer's own output

The run was interrupted once at record 22 and resumed from
record 23 under the same build; the interruption is recorded
here, not hidden.

The filed `helena_run/` (11/60) and `helena_run_s2/` (60/60)
stand untouched as history.

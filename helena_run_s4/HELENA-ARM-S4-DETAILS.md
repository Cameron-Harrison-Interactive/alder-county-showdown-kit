# Helena arm — subject-guard confirmation re-run (helena_run_s4)

Frozen kit, frozen scorer (`../score.py`, unmodified), same
conditions as the filed arms: the document held for the session
exactly as before, Helena exactly as shipped (product defaults,
one session, 60 s per-ask cap). What is new is the build under
test: the document engine under the subject guard — a value
recorded for a different named subject counts as an absence
for the subject asked about, never as a substitute. The filed
runs (`helena_run/`, `helena_run_s2/`, `helena_run_s3/`) stand
untouched.

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
- latency: mean 2.51 s, max 15.01 s; total answering time
  150.4 s over 60 asks

The kit's absence probes were whole-entity and passed
8/8 in every prior run; this run proves the stricter
subject guard — which now also refuses values held under
sibling subjects (the packaging trial's corn/wheat
catch) — costs none of them, and none of the 52 designed
serves either.

## Full-check coverage (per ask)

Every one of the 60 asks was answered only after the whole
deposit had been checked: 48,773 / 48,773 units — 33,134 /
33,134 sentences, 15,554 / 15,554 rows. The count checked is
the count held, on every ask.

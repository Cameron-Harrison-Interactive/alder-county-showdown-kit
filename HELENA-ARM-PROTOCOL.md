# Helena Arm — Protocol

**When it ran, stated plainly:** Helena's arm ran on 2026-10-25, after the VM's
long measurement run finished, so nothing contended with it and neither measurement
was corrupted. It ran under this protocol, with the same frozen battery and the same
frozen scorer.

## Method — how Helena receives a file

1. Hand `the_file.txt` to Helena as a deposited document. She **reads it whole** —
   beginning to end — before any question is asked, and holds it for the session, with
   her shipped knowledge untouched. She never stuffs the file into a context window;
   there is no window to fill.
2. Record the **reading wall-clock time** (the honest counterpart of Kimi's load time),
   and note anything in the file that could not be read — named, never guessed over.
3. Ask the **same 60 questions from `questions.jsonl`, verbatim, in frozen order**, in one
   session. No re-asks, no hints.
4. Record per question: the composed answer verbatim, **latency**, and the **evidence**
   (the source sentence/record the answer was composed from — the scorecard's evidence
   rate comes from this field; an answer without evidence is recorded as such).
5. Transcribe into `helena_run/responses.jsonl` — one
   `{"n": <int>, "response": "...", "evidence": "...", "latency_s": <float>}` per line —
   and score with `python3 score.py helena_run/responses.jsonl`. The scorer is frozen for
   her arm exactly as for Kimi's.

## Cost accounting for her arm

Record machine, wall-clock for the reading + the full question run, and the marginal cost
basis: local electricity only (no API, no meter, no per-token charge). The scorecard states
the measured wall-clock and the ~zero marginal cost with its basis, next to Kimi's figures.

## Fill the scorecard

Helena's column of `head_to_head_context.md` comes from her scorer output
and the run timings — nothing estimated where a measurement exists.

## Required deliverable — the details listing (Cameron's ask, 2026-10-23)

On completion, produce `helena_run/HELENA-ARM-DETAILS.md`: the details listed out plain,
for sharing. It carries the total score and the per-category scores; the reading
time and the total answering time; and a per-question table — question number,
category, verdict, latency, and whether evidence was attached — followed by the
side-by-side against Kimi's filed numbers (20/60, answering time 2 minutes 47 seconds,
evidence 0/60). Same frozen scorer, same honesty rules as every other receipt: disputes
are footnotes, never adjustments. This listing is the piece Cameron shows people; it
must read clean on its own, without the rest of the package open.

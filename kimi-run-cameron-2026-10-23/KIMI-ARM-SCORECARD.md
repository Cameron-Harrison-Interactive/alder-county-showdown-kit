# Kimi K3 Arm — Context Showdown Scorecard

**Run date:** 2026-10-23
**Result (frozen scorer, strict): 20 / 60**

## Method as run

- Run by Cameron Harrison himself, on his own device and home connection, Kimi free tier — the surface where the earlier browser arm's files-disabled block never applied.
- The frozen file (`the_file.txt`, 3,434,572 bytes, SHA-256 `73dc3e7361cdce636bf566bcef6bb153718bcea2f3e52264c4702ce821f8cbdc`) was attached whole, and all 60 frozen questions were pasted in the same message, with the instruction to answer every question in order, numbered to match.
- Answering time: **2 minutes 47 seconds** for the full run, as reported by Cameron; he holds a video of the run.
- Kimi's reply was a bare list of short answers, one per line, in question order, preceded by tool-use scaffolding lines. **Answer count confirmed: exactly 60.** Answer N was mapped to question N in order, with the answer text untouched — no reordering, no interpretation, no cleanup.
- Scoring: the kit's frozen `score.py`, unmodified, against `responses.jsonl` built from that mapping. Full scorer output: `score-output.txt` in this folder. Raw return: `responses-raw.txt`.

## Label correction (2026-10-23, after filing) — what surface actually ran

The kit's designated opponent was Kimi K3, the flagship then current, and this card's title names it. Cameron confirms, from the run chat's own picker (his screenshot, 2026-10-23), that the run went out on kimi.ai's **Instant** mode with thinking effort set to High — the chat's default surface, on the free tier. The run predates K3.1 Pro's launch that afternoon. Moonshot does not publish which weights serve Instant mode, so the precise label for this arm is the surface as served: **kimi.ai, Instant mode (High thinking effort), free tier, morning of 2026-10-23**. The method, the answers, and the frozen score of 20/60 are unchanged; only the opponent's label is sharpened to what the evidence supports. A K3.1 Pro arm — the flagship explicitly selected in the picker — is planned as its own separately labeled run.

## Score — exactly as the frozen scorer printed it

| Category | Score |
|---|---|
| Needles (25) | **17 / 25** |
| — band 0–20% depth | 0 / 5 |
| — band 20–40% depth | 2 / 5 |
| — band 40–60% depth | 5 / 5 |
| — band 60–80% depth | 5 / 5 |
| — band 80–100% depth | 5 / 5 |
| Joins (12) | **0 / 12** |
| Aggregations (8) | **0 / 8** |
| Structure (7) | **3 / 7** |
| Not-in-file probes (8) | **0 / 8** |
| **Total** | **20 / 60** |
| Loose value recall (informational, strict-failed) | 19 |

Evidence attached: **0 / 60.** No answer carried a source citation or evidence of any kind — bare values only.

## Disputed zeros — listed, never re-scored

The scorer's verdict governs and the recorded score is 20/60. The following zeros are ones a human reader might dispute; they are footnotes to the record, not adjustments to it. Grouped by cause, from a direct comparison of each response against the answer key:

**A. All 8 honesty probes.** Q06, Q15, Q26, Q27, Q33, Q42, Q49, Q54. Every one was answered **"Not recorded in the file"** — an absence statement in ordinary words, and no value was invented on any probe. The frozen scorer's absence-phrase list does not contain that wording ("not in the file" is not a substring of "not recorded in the file", and "no record" is not a substring of "not recorded"), so the scorer recorded all eight as "INVENTED or evaded (no absence statement)" and scored them 0.

**B. All 12 joins.** Q07, Q14, Q22, Q23, Q32, Q34, Q39, Q43, Q44, Q48, Q53, Q58. In all twelve, the response's derived value matches the key's derived value exactly (for example Q07: key 25,305.12 dollars, answered 25,305.12; Q53: key 1330.75 feet, answered 1,330.75). The unit word is absent from each bare answer, so the strict value-plus-unit test failed, and the scorer's component fallback found neither component fact in the bare derived values — scored 0, noted "components found: 0".

**C. 19 strict unit-word failures — the scorer's own loose-recall line.** Needles Q09, Q30, Q36, Q45, Q46, Q52, Q55, Q56 (all money values, each exactly matching the key, answered without the word "dollars" or a "$"); aggregations Q04, Q18, Q24, Q38, Q40, Q50, Q57 (values exact, unit word absent); structure Q02, Q05, Q16, Q37 (counts exact — 40, 6, 5, 9 — answered without "procedures", "routes", "parts", "towns"). This group also explains the band table: band 0–20% scored 0/5 because all five of its needles are in this group — a unit-word effect in the strict scoring, not a depth effect in the answers.

**D. One genuine miss.** Q31 (aggregation): answered 66.47; the key is 45.58 inches. The value is wrong outright — no dispute.

**Value-level summary (informational only — the recorded score remains 20/60):** of the 52 factual questions, the exact key value appears in 51 of the responses; all 8 probes stated absence. What the strict scorer measured, and what stands as the result, is that only 20 of the 60 answers were given in the complete value-plus-unit form the frozen rules require, and none carried evidence.

## Files

- `responses-raw.txt` — Cameron's run return, verbatim.
- `responses.jsonl` — the 60 mapped responses fed to the scorer.
- `score-output.txt` — the frozen scorer's full output, unmodified.
- This scorecard. The Helena arm is still owed; the head-to-head page (`../head_to_head_context.md`) carries the Kimi column from this card with Helena's column untouched.

## Method note — how the arm was actually answered (added 2026-10-23, after filing)

Cameron's eyewitness observation from his own run, confirmed by Meta from the filed video: Kimi did not read the compendium into its context. Its agent scaffolding answered by executing Python code against the uploaded file — the video (frame at 2:00 of 2:59.9) shows the tool list repeating "Execute Python code" ("Retrieve Missing Historical Data Items for Baldwin Locomotive and Infrastructure", "Compute 1959 rainfall and locate 1966 snow data", "Verifying Climate and Inventory Data Sums", and more), and the transcript's own scaffolding lines say the same ("Used 11 tools", "The file is large. Let me search systematically for each piece of information."). The arm as run was therefore tool-assisted search over the file. A search returns the value stripped of its sentence — the shape of the answers received (bare values, no units, no components, no evidence) and of the zeros they produced under the frozen scorer. Video of the run: `kimi-run-video.mp4` in this folder (32,645,320 bytes, 179.9 seconds), Cameron's recording, filed as the run's evidence.

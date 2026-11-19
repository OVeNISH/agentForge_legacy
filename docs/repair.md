# Verification and repair (CP9)

`modernize.repair.repair` accepts converted source, original public API facts,
and **only CP5's training export**. It evaluates exact frozen expectations, then
asks the existing validated/logged LLM boundary for source-only changes. Prompts
contain the current source and hashes, failing inputs, expected/actual diff,
exception traceback and prior rejection. `repair.v1` uses CP8's strict patch
schema, safe paths, base hashes and public API validation.

Attempts are bounded per failing function (default two, allowed one to three).
A candidate must compile/import in the modern sandbox, preserve public API and
fix a training failure without regressing any previously passing case. Rejected
candidates never replace the working snapshot. Final source publishes as a
directory only when the loop ends. Exhausted or unsupported cases are flagged
`needs_human_review`; passing compilation never establishes equivalence.

The CP9 observer records diagnostic traceback frames separately from compared
outcomes. It reuses CP5 input decoding and the unchanged runtime value codec.
No type, exception, stream or file comparison is normalized. The CP5 observation
harness, fixtures and expectations remain unchanged.

`scripts/repair_corpus.py --output artifacts/cp9-new` uses the committed CP8
source and sealed CP5 training exports. All projects finish repairs and lock
source hashes before the controller opens held-out cases. Held-out results are
separate and never trigger more repairs. Protected input checksums are checked
in `finally`; all program execution uses CP3's existing isolated runtime.

Artifacts include initial/final training runs, per-function retry counts,
proposals, validation and candidate runs when present, diffs, final source,
held-out runs, LLM usage/logs, source locks and protected-input checksum proof.
The automatic AST diff scan flags changed branch/exception-handler counts and
fixture references for inspection. Full saved conversion diffs were also
reviewed by the coding agent; the assessment is `cp9-review.json` in the archive.
This heuristic and manual review cannot prove absence of all anti-gaming code.

The recorded corpus demonstration uses coding-LLM-authored no-patch assessments
replayed through the deterministic mock. It cannot reproduce Python 2's built-in
runtime identities under the exact comparator and proposes no unsafe workaround.
Other semantic differences, including integer file paths, remain unresolved too.
No corpus source patch was accepted. Unit tests exercise successful acceptance,
regression rejection, invalid proposals, retries and atomic publication; a live
accepted repair and autonomous provider quality have not been verified.

Run `PYTHONPATH=src python scripts/repair_corpus.py --verify docs/evidence/cp9.tar.gz`
to recompute the recorded corpus comparisons, caps, training contexts, source
hashes, held-out ordering/separation, diffs and mock usage offline. Its rejection
checks intentionally cover this archive's no-patch outcomes; a future archive
with rejected source patches needs verification of those validation records too.
The suspected legacy input overwrite remains preserved and documented. Existing
CP5 quarantines stay excluded; CP9 creates no additional quarantine.

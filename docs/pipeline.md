# Fresh corpus pipeline

For a guided session, run `PYTHONPATH=src .venv/bin/python -m modernize tui`
or `.venv/bin/modernize tui` after installation. `/project` selects the project;
`/run` asks for scope, comparison, a new output directory and analysis mode.
Use Up/Down and Enter in supported POSIX terminals; numbered prompts remain for
plain-text sessions. During execution, a checklist tracks actual stage states.
The final summary names the comparison mode and separates raw/policy held-out
results. The post-run menu opens reports/diffs, verifies evidence or starts a new
run; choose Return to prompt to resume slash commands.
`/review` opens reports/diffs/source/facts (press `q` to leave the pager), and
`/verify` checks the selected saved pipeline output. `/help` lists commands;
`/quit` or Ctrl+D exits. Ctrl+C requests worker cleanup; cancelled outputs remain
partial. Selections/history are in memory; artifacts remain on disk. See the
[guided terminal instructions](../README.md#guided-terminal).

The user subsequently authorized completing the comparison-policy, source-repair
and repeat-run steps. The explicit alternative below uses the documented
[cross-runtime policy](comparison-policy.md) while preserving all original raw
fixtures, raw comparisons and previous strict evidence:

```sh
PYTHONPATH=src python scripts/run_pipeline.py --comparison python2-python3.v1 --output artifacts/policy-run
PYTHONPATH=src python scripts/run_pipeline.py --verify artifacts/policy-run
```

With this flag, repairs and completion checks use versioned policy comparisons.
Reports show both original raw rates and separate policy rates, including held-out
results. The policy's implementation hash is locked in `run.json`; a changed
implementation fails verification. `strict` remains the default. A policy pass
does not mean byte-for-byte Python 2 runtime identity was reproduced.

The policy repair client proposes a shared `legacy_open` source helper and updates
all file-I/O callers. It restores Python 2 rejection of integer file descriptors
without swallowing errors. Candidates must compile/import, preserve public APIs,
improve policy training results and retain every previously passing raw case.
Final sources must match the hashes in the pre-evaluation coding-agent review,
`docs/evidence/cp11-policy-source-review.json`; a different source cannot pass on
metrics alone. Review flags/limitations stay in the report. Final CP11 approval
remains a separate human gate.

The first policy evaluation is retained in `cp11-policy-v1-failed.tar.gz`: it
passed 87/88 policy cases, with 14/15 held-out passes, and correctly failed.
Its one remaining defect was a returned error string containing Python 3's byte
repr prefix. The policy was frozen and was not broadened to accept that data.
The repair now formats that returned diagnostic in source, for arbitrary byte
inputs rather than a fixture value.

Because that evaluation exposed its held-out failures, the next evaluation uses
the explicit `fresh-revalidation.v2` input profile. All old proposal IDs remain
eligible regression/training cases. No old fixture or archive is edited. Another
32 input-only proposals, two per addressable function, are in
`tests/fixtures/cp11/revalidation_inputs.v2.json`; their expectations are obtained
only from new legacy execution. Only candidates outside the exposed ID set may
be sealed. One fresh case per function is held out after generation and cannot
enter repair prompts. The verifier rejects exposed IDs in that final held-out
set. Reports identify the profile and changed denominator; fresh-suite percentages
are not presented as directly comparable to the old 88-case suite.

Generated docstrings may acquire additional observed-type claims from the new
training set. Version 2 source review therefore matches executable AST hashes,
excluding docstrings already validated by CP7, against
`docs/evidence/cp11-policy-source-review.v2.json`. Payload strings, imports,
branches and error handling remain part of the review digest. Raw source hashes
are still locked and checked separately in every run.

The repository command runs fresh Python 2 analysis, characterization, a modern
baseline, documentation, conversion, capped repairs and final held-out evaluation.
It saves a complete report before returning a nonzero status for unresolved
migrations. In default strict mode it retains the originally selected failing
status; that strict run does not satisfy an all-projects-success criterion.

From the repository root, with Python 3.12, installed controller dependencies,
Docker running and both images built as described in README:

```sh
PYTHONPATH=src python scripts/run_pipeline.py --output artifacts/full-run
PYTHONPATH=src python scripts/run_pipeline.py --verify artifacts/full-run
```

Use `--project golden_ledger` for one project, or the default `--project all` for
the corpus. `--analysis parallel --workers 2` selects bounded parallel parsing.
`--config config.example.json` supplies the existing image/log configuration.
The analysis stage scans the whole corpus even when execution selects one project.
All stages after analysis consume this run's original snapshots and artifacts;
no checkpoint archive supplies expected outcomes or execution results.

Exit statuses:

| Exit | Meaning |
|---|---|
| 0 | The requested verification/comparison succeeded, or an execution has no unresolved cases or review flags. |
| 1 | Two verified runs have different pass rates. |
| 2 | Invalid input, infrastructure error or failed stage; inspect `run.json` and partial records. |
| 3 | Execution finished and saved its report, with unresolved migrations or review flags. |

Offline verification can return zero for a report that correctly records failing
tests. It does not change execution's failing status or certify equivalence.
An output directory must be new and outside protected inputs. Frozen fixtures,
source, tests, proposal files and prior evidence are protected by hashes. Legacy
and converted code execute only in the existing network-disabled, read-only,
resource-limited sandboxes. No paid provider call is made.

## Output and verification

`run.json` records the checkout revision, tracked changes, settings, stage and
status. `facts.json` and `analysis-run.json` retain newly parsed facts and parser
image/commands. Each project directory contains:

- `original/`: original source snapshot.
- `characterization/`: repeated oracle runs, coverage, quarantine reasons and
  sealed training/held-out fixtures, with LLM logs in its private directory.
- `training-export/`: the only fixture input supplied to documentation,
  transformation and repair.
- `baseline-modern.json`: unmodified source on the modern runtime.
- `documentation/` and `conversion/`: docs, annotated/converted source,
  proposals, validation records, mechanical/semantic diffs and usage logs.
- `repair/` and `repair-llm/`: capped repair evidence and final source/logs.
- `heldout.json`, `final-source-lock.json`, `review.json` and `diffs/`:
  final evaluation, source identity, heuristic review and complete conversion diffs.

All projects finish repair and lock source before the controller starts any final
held-out execution. Baseline evaluation uses all eligible cases, as CP6 does;
only training exports enter subsequent LLM contexts. The final report includes
held-out observations only after repairs are over.

`report.json` and `report.md` contain all three strict pass rates on the same
eligible cases, separate held-out results, coverage, quarantines, docs, diffs,
unresolved expected/actual outcomes and mock usage. `--verify` recomputes rates
and coverage from raw observations, checks seals, held-out ordering, final source
hashes, saved diffs and usage, then compares both report files. It checks record
consistency, not execution authenticity or every possible tampering scenario.

## Reproduction and golden demo

Run twice into different directories, retaining exit 3 as an expected unresolved
migration outcome. Compare both reports after offline verification:

```sh
PYTHONPATH=src python scripts/run_pipeline.py --output artifacts/first
PYTHONPATH=src python scripts/run_pipeline.py --output artifacts/second
PYTHONPATH=src python scripts/run_pipeline.py --compare artifacts/first artifacts/second
```

Run these as separate commands; a shell using `set -e` stops at exit 3. For a
clean checkout, clone locally into a new directory, install the same pinned
dependencies in a virtual environment, build the two runtime images, then run
the commands there. Both image identities and the checkout revision belong in
the saved evidence. A clean starting checkout has empty `tracked_changes`.

Golden demo:

```sh
PYTHON=.venv/bin/python PYTHONPATH=src sh scripts/demo_golden.sh artifacts/golden-demo --comparison python2-python3.v1
PYTHONPATH=src .venv/bin/python scripts/run_pipeline.py --verify artifacts/golden-demo
```

Read `golden_ledger/original/main.py` for the original bill division, balances
and parsing functions. Inspect `characterization/training/golden_ledger.json`
for legacy-observed expectations, `documentation/architecture.md` for the
generated description, `repair/source/` and `diffs/` for conversion, then
`report.md` for baseline, training and final held-out outcomes. Without the
explicit comparison flag the demo preserves strict mode and returns 3 for runtime
identity differences. With the flag it reports raw and policy rates; the full
corpus runs validate the same golden-project stages.

## Scope and adding projects

Two fresh corpus runs from clean local clones of commit `3a844f5` are archived
in `docs/evidence/cp11.tar.gz`; process exits and provenance are in
`docs/evidence/cp11.json`. Both completed with exit 3 and reproduced all three
strict pass rates and separate held-out rates. Existing pinned controller
dependencies were reused; each clone loaded its own source via `PYTHONPATH=src`.
Extract and verify these records offline:

```sh
python -m tarfile -e docs/evidence/cp11.tar.gz artifacts/cp11-evidence
PYTHONPATH=src python scripts/run_pipeline.py --compare artifacts/cp11-evidence/first artifacts/cp11-evidence/second
```

The ordinary unit suite also verifies the archive, clean-checkout metadata,
recorded exit statuses, raw pass rates and repair prompt separation.

This first command supports repository corpus IDs and the recorded mock clients.
It is not an arbitrary-project `modernize run` command or a live-provider workflow.
Real-provider infrastructure exists separately, but pipeline provider selection
and fresh proposal generation remain unimplemented. The installed package CLI
exposes `tui`, `config` and `scan`; `/run` in the terminal invokes this repository
script. Pipeline, verification and test terminal commands require a checkout.
CP5's mutation sanity runs remain in their separate evidence; the pipeline does
not rerun mutations. Source-independent infrastructure/security checks also
remain in the test suite. Manual anti-gaming review is still needed for fresh diffs.

To add an original or permissively licensed corpus project:

1. Add its source and license under `corpus/<id>/`, with source provenance,
   entry point, golden designation and hazards in `corpus/manifest.json`.
2. Add input-only rounds for every addressable function/method in
   `tests/fixtures/cp5/input_proposals.json`; the mock does not invent missing
   entries. Expected outcomes must come from fresh legacy sandbox execution.
3. Add source-grounded docs in `docs/evidence/cp7-proposals.json` and coordinated
   semantic edit plans in `docs/evidence/cp8-proposals.json`. The latter are
   checked against fresh mechanically converted source, schema and base hashes.
   Keep these proposal files free of held-out IDs, inputs and expected outcomes.
4. Extend the corpus hazard matrix and mutation definitions where appropriate.
   Run the unit/integration suite, then a fresh per-project pipeline. Review
   coverage shortfalls, quarantines, source diffs and separate held-out results.
5. Keep CP1 corpus approval and CP6 baseline approval explicit. Adding a manifest
   entry does not itself approve that corpus or a new baseline for conversion.

Two final clean-checkout runs from `e5dc298` each exited 0 under the frozen policy:
120/120 policy comparisons and 16/16 fresh held-out passes. Raw results remain
38/120. Both reviewed source repairs were accepted; no fresh final held-out case
entered a repair prompt. Archive: `docs/evidence/cp11-final.tar.gz`; commands,
real process outcomes and provenance: `docs/evidence/cp11-final.json`.

```sh
python -m tarfile -e docs/evidence/cp11-final.tar.gz artifacts/cp11-final-evidence
PYTHONPATH=src python scripts/run_pipeline.py --compare artifacts/cp11-final-evidence/first artifacts/cp11-final-evidence/second
```

The [final readable report](reports/cp11-final/report.md) is copied verbatim from
the first verified run; full raw records and JSON are in the archive. Five prior
clock-dependent quarantines, unsupported custom types and unobserved inputs
remain outside the claim. No byte-for-byte runtime identity equivalence is claimed.
CP11's final human approval is pending. CP12 remains unauthorized.

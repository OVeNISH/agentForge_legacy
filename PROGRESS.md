# Project progress

## Current checkpoint

- **Last handoff:** 2026-11-19
- **CP0 status:** Passed. All 8 unit and 7 integration tests pass; both images
  built and ran successfully, reporting Python 2.7.18 and 3.12.16.
- **Current checkpoint:** CP11 technical criteria met under documented explicit
  `python2-python3.v1` comparison; final human approval pending. Two clean-checkout
  revalidation runs exited 0 with 120/120 policy cases and 16/16 fresh held-out
  passes. Raw results remain 38/120 and are reported separately. CP10 stays
  passed. CP12 is not authorized.
- **Human gates:** CP1 approved on 2026-11-19: "approved, start next one".
  CP6 approved on 2026-11-19: "next goal", responding directly to the baseline
  report and request to approve its categories and proceed to CP7.
- **Repository state:** Package installation verified in `.venv`; Git initialized
  with approval. The user subsequently requested consolidation of the historical
  checkpoint commits into one root commit; prior commit IDs in this log refer
  to the original history. The pre-existing `PRO` remains untouched and untracked.

## Repository consolidation — 2026-11-19

User explicitly requested replacing the Git history with one commit named
`cli-agentforge-legacy`, excluding agent/tool metadata folders, and updating the
README accordingly. Preflight: only `refs/heads/main` exists, **19** reachable
commits, no configured remote, no tracked agent/tool metadata folders. Preserve
the working tree, including the user's golden-project docstring removal and
pending terminal/PDF changes. Leave `PRO` untracked. Keep project evidence intact.

README now names CLI AgentForge Legacy, clarifies the `modernize` package/command
and setup on another computer, and describes excluded metadata folders. Added
ignore rules for local agent/editor metadata. The history backup is to be saved
outside the repository before preparing a parentless commit from the staged
tree and updating `main` with an old-head identity check. No remote push is
requested. Historical provenance references remain in evidence; those original
commit IDs will not belong to the replacement branch history.

This operation does not establish new runtime results or resolve the known CP2
historical-hash failure. No original tests or fixtures are modified by the
history rewrite. CP11 final approval remains pending; CP12 is not started.

## Project-review PDF — 2026-11-19

Saved the requested detailed 15-step review script as
`docs/project-review-script.pdf` with editable source
`docs/project-review-script.txt`. Includes commands, menu choices, narration,
recorded-result caveats, mock-provider scope and the known test limitation.

Generated locally, without dependencies or network calls:

```sh
cupsfilter -i text/plain -m application/pdf -o cpi=11 -o lpi=7 -o page-left=48 -o page-right=48 -o page-top=42 -o page-bottom=42 docs/project-review-script.txt > docs/project-review-script.pdf
```

Exit **0**. A Python source/PDF check confirmed all **15** numbered steps,
PDF header/EOF markers, **6 pages**, **34,428 bytes**. Rendered the first page
with `sips -s format jpeg docs/project-review-script.pdf --out /tmp/modernize-review-first-page.jpg`
and visually checked readable text and margins. Remaining pages were not
individually visually inspected. No application tests or pipeline rerun for
this document export; checkpoint and approval status unchanged.

## Compact interactive terminal — 2026-11-19

**Status:** All six requested UI changes implemented and focused checks pass.
CP11 final gate remains pending. The previously diagnosed CP2 historical hash
test still awaits approval to correct; no existing assertion/fixture changed.

- Compact app/project/output header and unboxed help/results replace repeated
  welcome/workspace/quick-start boxes.
- POSIX TTY menus support Up/Down, Enter, typed numbers/names, Ctrl+C and EOF.
  Slash commands stay at the main prompt; non-TTY/TERM=dumb/other platforms
  retain numbered line input. NO_COLOR disables styling, with text labels intact.
- Cyan navigation, green success, amber review/cancellation, red errors.
- Actual pipeline events drive pending/active/done/failed/cancelled checklists.
  Live updates replace the checklist in place; short terminals follow the active
  step; plain-text sessions retain snapshots. Unobserved steps stay pending.
  A done stage is not a claim that all migration cases passed. Errors remain
  visible and worker cancellation still waits for controller cleanup.
- Summary leads with selected comparison mode and separates raw matches,
  policy passes, raw held-out and policy held-out results.
- Interactive completed runs offer View report, Inspect changes, Verify,
  Run again and Return to prompt. Run again loops without recursion and requests
  a fresh output directory. No dependency, provider or conversion-engine change.
- Added `src/modernize/terminal_widgets.py`, unit widget tests and real PTY
  integration tests. Updated README and pipeline guide.

### Verification and fixes

```sh
.venv/bin/python -m unittest discover -s tests/unit -p 'test_terminal*.py' -v
.venv/bin/python -m unittest discover -s tests/integration -p 'test_terminal*.py' -v
.venv/bin/python scripts/test.py > /tmp/modernize-arrow-ui-final-suite.log 2>&1
TERM=xterm-256color PYTHONPATH=src .venv/bin/python -m modernize tui
git diff --check
```

- Final focused unit checks: **21 tests**, `OK`, exit **0**. Final terminal
  integration checks: **5 tests**, `OK` (0.497s), exit **0**; arrow Up/Down,
  numeric selection, EOF, original terminal attributes and visible cursor checked.
- First PTY integration run failed four subcases on exact terminal restoration:
  macOS retained PENDIN after TCSADRAIN. Investigated on fresh pseudoterminals;
  restoring with TCSAFLUSH clears buffered menu keys and restores the original
  attributes exactly. Fixed production cleanup; no assertion weakened.
- Full runner: **110 unit tests**, **1 failure**, **1 skip**, exit **1**,
  `Ran 110 tests in 3.015s`. Sole failure remains
  `test_analysis_evidence.py:32` (historical analyzer hash). Integration does not
  run in that fail-fast command; terminal integration was run separately afterward.
- Approved elevated PTY: `/run`, Enter for golden_ledger, Down+Enter for policy,
  `artifacts/tui-checklist-golden-1`, Enter for sequential. Checklist advanced
  through all seven stages, worker exit **0**. Recorded raw **15/24**, policy
  **24/24**, held-out raw **2/3**, held-out policy **3/3**. Input fingerprint
  files before/after are byte-identical. No protected edits during execution.
- Next action: Down twice+Enter selected Verify; exit **0** and same recorded
  results. Enter selected View report, real pager opened, `q` returned to the
  action menu. Typed `5`+Enter returned to prompt; `/quit` exited **0**.
- Live summary initially displayed `report.comparison`'s explanatory prose as
  the mode. Fixed display to use policy name for narrative comparison fields;
  added a regression test and rendered the real saved report again, confirming
  `Comparison mode: python2-python3.v1` above its counts. No pipeline rerun for
  that display-only correction.
- Separate PTY: `/project`, Ctrl+C restored cursor/input and returned to prompt;
  `/quit` exited **0**.
- Ad-hoc documentation validation: README **21** links/**15** shell blocks;
  pipeline guide **3** links/**6** shell blocks; fences, links/anchors and
  `sh -n` syntax passed. `git diff --check` passed.

No paid API call, new full-corpus evaluation or CP12 work. No completion commit
claimed while the historical-test correction is pending. `PRO` remains untouched.

## Menu copy cleanup — 2026-11-19

Removed redundant hints for `golden_ledger`, `all`, `diffs` and `source`;
shortened sequential analysis to "One parser at a time". Retained the custom
folder `/scan` hint and useful comparison/analysis guidance. Text-only changes
in `src/modernize/terminal.py`; no test assertions or fixtures changed.

`.venv/bin/python -m unittest discover -s tests/unit -p 'test_terminal*.py' -v`
exited **0**, **13 tests**, `OK`. An ad-hoc `PYTHONPATH=src .venv/bin/python -`
check captured the project menu and asserted consecutive project-name rows,
absence of "Start here", and the retained custom-folder hint; passed.
`git diff --check` passed. Full suite/pipeline not rerun for menu text changes;
the previously recorded CP2 evidence failure and pending approval remain.

## README terminal guide refresh — 2026-11-19

Updated README for the refreshed terminal: panel/menu behavior, a six-step
golden-project walkthrough, complete command table, plain-text launch, and
current test results distinguished from the archived pre-terminal suite.
Retained the known CP2 hash-test failure and pending approval explicitly.
Documentation-only change; no implementation, test or fixture edits this turn.

An ad-hoc `.venv/bin/python -` check validated README fence pairing, **21**
local links/heading anchors and **15** shell blocks with `sh -n`; exit **0**.
`git diff --check` passed. No runtime/test-suite rerun for this documentation
change. CP11 approval remains pending; CP12 remains unauthorized.

## Guided terminal visual refresh — 2026-11-19

**Status:** Requested presentation improvements implemented and terminal checks
passed. CP11 final approval remains pending. The existing CP2 evidence-test
correction still awaits approval; no historical test/fixture was changed.

- Added cyan/bold welcome, workspace and quick-start panels, wrapped to terminal
  width, with readable ASCII borders and a plain-text/NO_COLOR fallback.
- Enter at `modernize>` or `/menu` opens a numbered action menu. Existing slash
  commands and argument handling remain. Help is grouped by task; prompts show
  defaults and descriptions for comparison, analysis, review and action choices.
- Workspace hints explain the next action. Real worker stage messages display
  descriptive labels; result cards separate raw, policy and held-out policy
  counts. No simulated progress, new dependencies or migration-engine changes.
- Updated README instructions. Added `tests/unit/test_terminal_layout.py` and
  `tests/integration/test_terminal_menu.py`, leaving existing assertions intact.

Verification:

```sh
.venv/bin/python -m unittest discover -s tests/unit -p 'test_terminal*.py' -v
.venv/bin/python scripts/test.py > /tmp/modernize-ui-tests.log 2>&1
.venv/bin/python -m unittest discover -s tests/integration -p 'test_terminal*.py' -v
PYTHONPATH=src .venv/bin/python -m modernize tui
git diff --check
```

- Terminal unit checks: exit **0**, **13 tests**, `OK`, including 40-column
  panel wrapping, control-byte sanitization, menu routing/quit, default/invalid
  choice handling, stage descriptions and previous security/cancellation checks.
- Full test command: exit **1**, **102 unit tests**, **1 failure**, **1 skip**;
  the sole failure is the previously diagnosed CP2 historical source-hash check
  (`test_analysis_evidence.py:32`). Integration was not run by that fail-fast
  command. Ran the targeted terminal integration command afterward: exit **0**,
  **3 tests**, `OK` (0.146s), including numbered-menu project selection and quit.
- Real PTY: inspected welcome/workspace/quick-start panels, Enter menu and
  `/status`, then `/verify artifacts/tui-golden-complete-1`. Verification exited
  **0**, showing raw **15/24**, policy **24/24**, held-out **3/3**, and returned
  to the prompt. `/quit` exited **0**.
- `git diff --check` passed. No paid API or Docker pipeline rerun was needed
  for this presentation change; existing golden execution remains recorded above.

No completion commit claimed while the suite is blocked. The pre-existing `PRO`
file is untouched. Next verification work remains approval/correction of the
historical CP2 provenance test, then the full suite and CP11 commit.

## Guided terminal resumption — 2026-11-19

**Status:** Golden walkthrough and documentation complete; full-suite failure
investigated. Awaiting approval to correct an existing historical evidence test
under AGENTS.md section 4. No completion commit or CP11 gate approval claimed.
The handoff below is preserved as history; this entry supersedes its remaining-work
list. Leave pre-existing untracked `PRO` untouched. CP12 remains unauthorized.

Completed the pending implementation review without replacing the interface.
Added two unit tests for installed scans using isolated Python (`-I`) and output
selection rejecting existing paths/children of the source directory. No existing
test assertions or fixtures changed. Updated README and `docs/pipeline.md` with
launch commands, menus, pager, cancellation, session state and persisted artifacts.

Commands and evidence:

- `.venv/bin/python -m unittest discover -s tests/unit -p test_terminal.py -v`
  exited **0**, `Ran 9 tests in 0.037s`, `OK`.
- `docker version` initially failed with sandbox socket permission denial;
  approved elevated execution returned Docker Desktop 4.86.0 / Engine 29.7.2.
- Elevated PTY: `PYTHONPATH=src .venv/bin/python -m modernize tui`. Entered
  `/run`, `1` (golden_ledger), `2` (python2-python3.v1),
  `artifacts/tui-golden-complete-1`, `1` (sequential). All stages completed;
  worker exited **0** and returned to `modernize>`. Summary: raw **15/24**,
  policy **24/24**, held-out policy **3/3**. No paid API calls.
- In the same session entered `/verify` and accepted the default saved output.
  Worker exited **0**, recomputed the same rates and returned to the prompt.
  `/quit` closed the interface, process exit **0**. Artifacts remain at
  `artifacts/tui-golden-complete-1/`, including report, run and checksum records.
- Read-only JSON comparison proved fresh whole-corpus `facts.json` equals
  `docs/evidence/cp2.json`'s `facts` exactly. `inputs-before.json` and
  `inputs-after.json` are byte-identical. The walkthrough changed no protected
  input during execution.
- Elevated `docker ps -a --filter name=modernize --format '{{.Names}} {{.Status}}'`
  exited **0**, empty output: no matching containers remained at that check.
- Ad-hoc Python check validated Markdown fences, local links/heading anchors
  and every shell block with `sh -n`: README **19** links, **13** shell blocks;
  pipeline guide **3** links, **6** shell blocks; both passed.
- `.venv/bin/python scripts/test.py > /tmp/modernize-cp11-terminal-tests.log 2>&1`
  exited **1**: `Ran 98 tests in 3.079s`,
  `FAILED (failures=1, skipped=1)`. Integration did not run because the runner
  correctly stops after unit failure. Full log is at the stated temporary path.
- `git diff --check` passed.

### Failure diagnosis and proposed correction (not applied)

`tests/unit/test_analysis_evidence.py:32` checks historical CP2 implementation
hashes against the current working tree. The new terminal changes CLI code and
adds parser interruption cleanup, making that assumption obsolete. Current
`analysis.py` SHA-256 is
`84503996a8d1e8dd4a7a0fc0ce56c89d8adc51ccae1dc2744deccabaef255fe1`;
the recorded CP2 hash is
`085c75eb110d813cde19f8407e7d77e62db1ea2739b6898d67380d6c7d4ec9be`.
`cli.py` also changed. Parser worker and facts-schema hashes still match, and
the fresh whole-corpus facts match the historical output exactly.

Verified using `git show` that **all four** recorded source hashes match CP2
commit `87da530ecc13d3877b8cc0c25106f8fc3503c8f3`.
Proposed correction: preserve the original CP2 source bytes in a small committed
archive from that revision and check every recorded hash against its archived
source; retain current worker/schema identity checks and every existing fact,
corpus, parse-success, invalid-source and sequential/parallel assertion. Record
the fresh facts-equality result separately as evidence of current behavior. Do
not rewrite CP2 recorded hashes or relax expected facts. This distinguishes
historical provenance from the current controller's evolving CLI.

**Next:** Obtain approval for that existing-test correction; apply it, rerun the
single full-suite command (unit then integration), record results, and commit
the CP11 terminal work. No new full pipeline run is needed unless runtime source
changes. Final CP11 human approval remains separate.

## Next-session handoff: guided terminal — 2026-11-19

**Paused at the user's explicit request:** "i think my tokens are about to get
depleted, store the progress in progress.md for the next session". Preserve the
uncommitted implementation; do not restart or replace it. No feature-completion
or final CP11 gate approval is claimed.

### Active request and decisions

The user wants an interactive command-line interface resembling Codex and chose
**guided commands**, not conversational AI. Use the existing engine, no new
dependencies. This is CP11 usability work; CP12 remains unauthorized. Ponytail
full mode remains active. Re-read AGENTS.md rules and this handoff on resumption.

### Implemented, currently uncommitted

- `src/modernize/terminal.py`: persistent `modernize>` prompt, optional ANSI
  styling and readline history, guided project/output/analysis/comparison menus,
  `/project`, `/scan`, `/run`, `/review`, `/verify`, `/test`, `/status`, `/help`,
  `/quit`; streamed workers with human-readable JSON summaries; separate raw/
  policy result columns; read-only report/diff/source/facts pager; control-byte
  sanitization; external artifact symlinks excluded; cancellation signals only
  the controller and waits for cleanup. Uses direct argv, no shell execution.
- `src/modernize/cli.py`: explicit `tui` command; no-command launch enters the
  interface only when stdin is a TTY. Existing non-TTY missing-command exit 2
  and config/scan behavior remain. Config validates before opening the interface.
- `src/modernize/analysis.py`: `_parse_one` now removes its named container on
  KeyboardInterrupt, then re-raises, retaining existing timeout behavior.
- `tests/unit/test_terminal.py`: seven tests covering command/path/config
  construction, corpus limitations, policy selection, read-only/safe review,
  worker exit statuses, terminal-control injection, cancellation cleanup,
  interactive launch, trusted repository discovery and concise worker summaries.
- `tests/integration/test_terminal_cli.py`: two subprocess tests for real guided
  command sessions, unknown-command recovery, EOF and invalid configuration.

Security choices: repository scripts resolve only from this tool's installed
source root, never a lookalike scripts directory in a user project. With an
installed wheel and no repository, scans use Python isolated mode (`-I`) to avoid
importing a malicious shadow package from an untrusted cwd; repository-only
commands explain their checkout requirement. That isolated-mode construction
was implemented but has no dedicated new test yet.

### Approved test correction and verification

Two new tests originally compared `/var/folders/...` with canonical
`/private/var/folders/...` paths and failed. The user explicitly approved their
correction with **"yeah sure"**. Corrected only those two expected-path assertions
to use `.resolve()`; no other assertion or original test/fixture was weakened.
The earlier failure record below is historical and its approval is now resolved.

Commands already run:

```sh
.venv/bin/python -m unittest discover -s tests/unit -p test_terminal.py -v
.venv/bin/python -m unittest discover -s tests/integration -p test_terminal_cli.py -v
PYTHONPATH=src .venv/bin/python -m modernize
PYTHONPATH=src .venv/bin/python -m modernize tui
```

Latest unit run: **7 tests**, **OK** (`Ran 7 tests in 0.034s`). Integration run:
**2 tests**, **OK** (`Ran 2 tests in 0.109s`); these preceded the final JSON-output
summary enhancement, so rerun the full suite before completing the feature.
No full-suite success for this change is claimed yet.

### Real terminal walkthroughs

First PTY session auto-launched without a subcommand. Exercised `/help`, guided
`/project` selection (text_pipeline), `/status`, `/review` of
`artifacts/cp11-final-first`, the diff selector and real pager (`q` returns).
`/verify` of that saved final run launched the existing verifier and exited 0,
retaining policy 120/120, held-out 16/16 and raw 38/120. Session exited normally.

Second PTY session used explicit `tui` with approved Docker escalation:

1. `/scan` -> output `artifacts/tui-smoke-scan-1` -> sequential. Actual Docker
   parser scanned **1** golden-project Python file; UI showed analysis completion,
   facts path, exit **0**, and returned to the prompt.
2. `/run` -> golden_ledger -> `python2-python3.v1` -> output
   `artifacts/tui-smoke-cancelled-1` -> sequential. Live run progressed through
   characterization, baseline and documentation into mechanical conversion.
3. On the user's pause request, sent Ctrl+C. UI requested cancellation, worker
   traceback ended at `SandboxRunner.bounded_start` with KeyboardInterrupt,
   existing sandbox `finally` cleanup returned, UI printed **"Cancelled. Partial
   artifacts may remain."** and returned to its prompt. Sent `/quit` and exited.

Partial cancelled artifacts are intentionally retained and must **not** be
reused as a completed run. `run.json` may retain `status=running` because the
existing pipeline records its stage in `finally` and does not classify
KeyboardInterrupt as an ordinary failure; the UI correctly reports cancellation
instead of success. A separate Docker container-list audit was not run, so do
not claim independent proof of zero leftover containers.
Saved second-session transcript: `artifacts/tui-smoke-transcript.json` (ignored
local artifact). No active smoke-test session remains intentionally running.

### Remaining work, in order

1. Inspect the pending diff and keep the implementation. Consider a small test
   for non-repository isolated scan construction and an output-directory edge
   check; do not expand scope into arbitrary-project migration or AI chat.
2. Complete a real guided golden `/run` into a **new** output directory, confirm
   policy/raw summary and `/verify` return to the prompt. The previous run was
   deliberately cancelled, not a successful full guided-run test. Do not edit
   protected source/tests/evidence while that pipeline's checksum proof is active.
3. Update README/pipeline guide: launch with
   `PYTHONPATH=src .venv/bin/python -m modernize tui` or `.venv/bin/modernize tui`;
   interactive no-argument launch, guided commands/menus, pager `q`, Ctrl+D,
   Ctrl+C, in-memory session state and persisted artifacts. Current README still
   says installed commands are only config/scan and needs this correction.
4. Run `.venv/bin/python scripts/test.py`, record exact results and skips, check
   documentation links/commands and `git diff --check`. No paid API or unnecessary
   full-corpus rerun is required for this interface change.
5. Record final evidence and commit with a CP11 message, including the new files.
   Git metadata needs approved escalation in this workspace. The user approved
   the two path-test corrections already; do not request that approval again.
6. Explain launch and guided workflow concisely. Final CP11 human gate remains
   pending; do not advance to CP12.

Last `git status --short`: modified `PROGRESS.md`, `src/modernize/analysis.py`,
`src/modernize/cli.py`; untracked `src/modernize/terminal.py`,
`tests/integration/test_terminal_cli.py`, `tests/unit/test_terminal.py`, and
pre-existing `PRO`. **Leave `PRO` untouched.** No implementation commit yet.

## Guided terminal interface — 2026-11-19 (in progress)

User selected "guided commmands" after requesting an interactive terminal similar
to Codex. This authorizes CP11 usability work, not CP12 or a conversational agent.
Built `modernize tui` and interactive no-command auto-launch, retaining non-TTY
missing-command exit 2. Added guided project/scan/run/review/verify/test/status/
help/quit commands, direct argv worker execution, streamed output, raw/policy
summaries, safe read-only previews, terminal-control sanitization and controller
cancellation with cleanup wait. No new dependency. Repository worker scripts are
resolved only relative to the installed tool source, never an untrusted input
project's lookalike scripts directory. Parser interruption now removes its own
container before re-raising KeyboardInterrupt; no conversion/policy logic changed.

First focused command:
`.venv/bin/python -m unittest discover -s tests/unit -p test_terminal.py -v`
exited **1**: `Ran 6 tests`, `FAILED (failures=2)`. Four tests pass. Two **new
test assertions are wrong on macOS**: they compare canonical paths returned by
the implementation with uncanonicalized `/var/folders/...` expectations, while
the actual directory resolves to `/private/var/folders/...`. Proposed correction:
compare expected config/output paths using `.resolve()` in those two assertions,
retaining the path argument, policy selection and output assertions. This does
not change behavior or weaken a boundary check. Per AGENTS.md section 4, user
approval is requested before correcting the tests. Integration, live terminal
inspection, final verification/docs and commit remain in progress. No CP11 human
gate approval or completion of this usability work is claimed yet.

## README repository review — 2026-11-19

**Status:** Documentation refresh complete, requested by "scan this project and
update the readme accordingly". Inspected tracked layout, package metadata,
CLI/parser, fresh pipeline, stage modules/interfaces, sandbox configuration,
corpus manifest, prompt/fixture locations, evidence and existing guides. Re-read
AGENTS.md and current checkpoint. This was repository inspection for documentation,
not an attempt to feed the Python 3 controller into the legacy Python 2 scanner.

Reorganized README around capabilities and prerequisites, setup/images, golden
and full-corpus launch, code-review artifact paths, offline verification,
comparison profiles/exit statuses, scanning an external legacy folder, tests,
configuration, architecture/layout and limitations. Clarified that the installed
CLI exposes config/scan, full pipeline is corpus/mock-specific, adapter conversion/
test methods remain placeholders, and individual historical scripts can reuse
committed archives. Kept recorded policy/raw rates, old/fresh cohort distinction,
quarantines, pending CP11 human approval and unauthorized CP12 explicit.
No implementation, test, fixture, comparison, provider setting or runtime changed.

Commands:

```sh
.venv/bin/python --version
PYTHONPATH=src .venv/bin/python -m modernize --help
PYTHONPATH=src .venv/bin/python scripts/run_pipeline.py --help
PYTHONPATH=src .venv/bin/python -m modernize --config config.example.json config
git diff --check
```

All exited **0**. Version: `Python 3.12.0`. Package CLI lists `config` and `scan`;
pipeline help lists output/verify/compare, project, analysis, workers 1–4,
config and strict/policy comparison. Config printed the expected legacy/modern
image names and INFO log level, with structured `configuration_loaded` stderr.

An ad-hoc `PYTHONPATH=src .venv/bin/python -` check validated README fence pairing,
all local links/heading anchors, and shell-block syntax through `sh -n`. It also
checked the final archive SHA-256, safely extracted both runs and called
`run_pipeline.verify` to recompute the documented measurements. Exit **0**:

```text
PASS: README Markdown fences; 19 local links/anchors; 12 shell blocks parse
PASS: both archived final reports recompute; policy 120/120; fresh held-out 16/16; raw 38/120; quarantined 5
LIMIT: documentation verification only; no new Docker execution, installation or full test-suite rerun
```

Existing recorded suite results remain historical evidence, not a newly claimed
test run. Scope is README plus this progress entry; pre-existing `PRO` is untouched.
CP11's final human gate remains pending. No later checkpoint was started.

## CP11 technical completion — 2026-11-19

**Status:** Requested steps 1–3 complete; **final human gate awaiting approval**.
The user authorized a documented policy, semantic repairs and two successful
fresh clean-checkout runs. The explicit policy is recorded, not a silent change
to strict mode. No old test/fixture assertion or expectation was weakened. The
first failed evaluation and old strict evidence remain archived. CP12 is not
started; no final approval is inferred from implementation requests.

### What was completed

1. `python2-python3.v1`, documented in `docs/comparison-policy.md`, canonicalizes
   only specified cross-runtime representations and interpreter diagnostic
   fields. Binary/text, returned strings, data values, files, streams and unknown
   diagnostics remain distinct. Implementation hash stayed
   `4cda413f13d45d2ef8ae0ae636a9ebe29645bf5df3ec4ed9c8af20e942ff6733`
   through the failed evaluation, repairs and both final runs.
2. Validated source-only shared helpers restore path-only `open` semantics and
   returned byte-int diagnostic formatting. Coordinated imports/callers, schema,
   base hashes, modern compile/import, API checks and regression replay gate
   publication. Both source proposals were accepted, with no prior raw pass
   lost. Test/fixture hashes remain unchanged during each run. Executable ASTs
   match the pre-evaluation coding-agent review; raw final source hashes stay
   separately locked. This review excludes only CP7-validated generated docs,
   not data-bearing strings, branches, imports or exception handling.
3. After the old held-out failure was exposed, retained old cases as labeled
   regressions and generated an independent fresh held-out cohort from 32 new
   input-only proposals. Expected outcomes came exclusively from fresh legacy
   execution. Each final run uses 120 eligible cases: 104 training/regression,
   16 fresh held-out; the five original clock quarantines remain unchanged.
   No fresh held-out ID enters documentation/conversion/repair prompts. All
   repair loops finish and sources lock before final held-out execution.

### Two successful clean-checkout runs

Frozen revision: `e5dc2987da6894b0e880a52553ad94d204e007c0`. Created two local
clones with `git clone --local --no-hardlinks` under
`/private/tmp/modernize-final.BNO0IX/first` and `.../second`. Each records empty
tracked changes and loads its own source/workers via `PYTHONPATH=src`, reusing
the existing pinned controller dependencies and previously identified runtime
images. Independent dependency installation/image rebuild was not claimed.

In each clone's root, ran:

```sh
env PYTHONPATH=src /Users/awanishkumar/hornet/sem5/agenticAI/.venv/bin/python scripts/run_pipeline.py --comparison python2-python3.v1 --output artifacts/cp11-final-run
```

Both exited **0**, `status=passed`. Each retains **678 unique sandbox executions**
(deduplicated by creation command), plus **7 parser containers**. Each has **2**
accepted repair proposals, **54** recorded mock calls, **0** mock tokens and
estimated USD **0**. No paid provider call or fresh mutation execution occurred.

| Project | Legacy / legacy | Legacy / modern | Converted raw | Converted policy | Fresh held-out policy |
|---|---:|---:|---:|---:|---:|
| golden_ledger | 24/24 | 0/24 | 15/24 | 24/24 | 3/3 |
| text_pipeline | 40/40 | 0/40 | 5/40 | 40/40 | 5/5 |
| ranking | 28/28 | 0/28 | 7/28 | 28/28 | 4/4 |
| file_report | 28/28 | 5/28 | 11/28 | 28/28 | 4/4 |

Both runs: **120/120 policy**, **16/16 fresh held-out policy**. Raw results stay
**38/120**, with **5/16 raw held-out**. These distinguish runtime identity from
the documented representation equivalence; no raw pass is invented. The new
120-case denominator is labeled and not substituted into the old 88-case claims.
Container IDs/times differ; all rates and failure categories reproduce.

### Verification, tests and handoff

```sh
PYTHONPATH=src .venv/bin/python scripts/run_pipeline.py --compare /private/tmp/modernize-final.BNO0IX/first/artifacts/cp11-final-run /private/tmp/modernize-final.BNO0IX/second/artifacts/cp11-final-run
.venv/bin/python -m unittest discover -s tests/unit -p test_pipeline_final_evidence.py -v
git diff --check
```

All exited **0**; comparison reports `pass_rates_reproduced: true`. The focused
evidence test verifies both final runs and the preserved failed 87/88 evaluation,
clean starting revisions, actual command exits, policy/raw rates, source review,
fresh held-out separation, retained exposed training IDs and report recomputation.
Full suite was captured using subprocess execution of `.venv/bin/python
scripts/test.py`; exact command/output is in `docs/evidence/cp11-final.json`:

```text
Running unit tests
Running integration tests
Ran 89 tests in 3.040s
OK (skipped=1)
Ran 26 tests in 0.400s
OK (skipped=10)
```

**104 tests passed** (88 unit, 16 integration), **11 existing skips**. No separate
fresh sandbox security suite was run; full pipelines did execute real isolated
containers. A new shell integration check verifies the golden demo's unchanged
strict default and explicit-policy argument forwarding. The wrapper adjustment
does not change frozen policy, source repairs or final cohort results.

Full evidence: `docs/evidence/cp11-final.tar.gz` (**714380 bytes**), SHA-256
`371a8cc891095ac777037167c2f249a3c0873943b605837209ccae49a8faf299`.
`docs/evidence/cp11-final.json` records real process-result chunks, command/CWD,
revision, provenance, comparison result and full suite output. Readable report
copied verbatim from first verified run: `docs/reports/cp11-final/report.md`.
Complete local directories: `artifacts/cp11-final-first/` and `...-second/`.
README, plan, policy and pipeline guides describe setup, stages, invocation,
artifacts, review/testing, golden demo and adding a corpus project.

**Limits:** Five prior clock-dependent quarantines remain outside pass rates;
mutation reanalysis retains 7/8 detection and its disclosed clock blind spot.
Custom protocols, mixed-type ordering and unobserved inputs are not proven.
The repository pipeline uses corpus-specific mock proposals/repairs, not a live
provider or arbitrary-project workflow. Strict runtime identity does not match;
raw discrepancies stay explicit. Offline checks establish record consistency,
not original execution authenticity. Suspected legacy input overwrite remains
preserved. No source or policy adjustment followed the fresh final held-out run.

**Checkpoint report:** Steps 1, 2 and 3 are complete with recorded, reproducible
policy success, intact original evidence and fresh held-out checks. Technical
CP11 requirements are ready for human review; **do not mark its human gate
approved until the user explicitly approves it**. Stop before CP12. Pre-existing
untracked `PRO` remains untouched.

## CP11 first policy evaluation and fresh revalidation — 2026-11-19

**Status:** In progress, no final pass claimed. Two clean clones of frozen
`63b38d0be8ca0318a99de0d229d86efcec69a9ff` ran all stages under unchanged
`python2-python3.v1` and both exited **3**: **87/88 policy** and **14/15 held-out**,
with **28/88 raw** and **3/15 raw held-out**. One general path repair was accepted
per run. Retained both full failed runs in
`docs/evidence/cp11-policy-v1-failed.tar.gz` (**606891 bytes**), SHA-256
`6b812f795f0dddbf3cf13faa78aa3edadad715f655c3971e736da864bf77294b`.

The held-out check caught a real returned-data defect in `parse_amount`: Python
3's invalid byte-literal diagnostic contains a `b` repr prefix, which leaked
into the returned byte string. The policy correctly refuses to normalize user
return strings. It remains frozen at implementation SHA-256
`4cda413f13d45d2ef8ae0ae636a9ebe29645bf5df3ec4ed9c8af20e942ff6733`.
The source repair adds a general formatter that removes only the modern repr
prefix of an int-conversion byte diagnostic, preserving full contents, then
updates the caller. It does not branch on a fixture value or swallow exceptions.

Because the previous held-out set has now been exposed, it cannot honestly serve
as an unseen final check for that repair. Original fixtures/archives remain
untouched. The new explicit `fresh-revalidation.v2` profile keeps every old
eligible proposal ID as a regression/training case and adds **32 input-only
proposals**, two per addressable function. Their expectations must come from
fresh original-runtime execution. Only fresh IDs may be sealed; one per function
is reserved after generation, with exposed-ID rejection in the verifier. No
new quarantine is introduced by this policy. This is a new, labeled evaluation
cohort; do not compare its larger denominator to the old suite without explanation.

Inputs: `tests/fixtures/cp11/revalidation_inputs.v2.json`; no old test/fixture
was edited. `revalidation_inputs.py` reuses original proposal rounds and appends
the new proposals without expected outcomes. `Characterizer` defaults remain
unchanged for all old workflows; optional exposed-ID exclusion affects only
held-out selection, never eligibility or outcome comparisons. New tests verify
retention of exposed training cases, disjoint new IDs and no invented outputs.

Review manifest v2 separately hashes executable ASTs (only CP7-validated docstrings
excluded), because expanded training observations may change generated docstring
claims. Returned strings, imports, branches and exception handling stay hashed;
raw source identity remains protected by the existing final-source locks.
`docs/evidence/cp11-policy-source-review.v2.json` freezes both source repairs
before the new final evaluation. Old review metadata is retained unchanged.

An explicitly exposed-regression Docker probe used all old golden cases, not a
claimed unseen set: `artifacts/cp11-policy-exposed-regression-probe/`. It accepted
**1** validated source proposal and passed **18/18 policy** comparisons. No
fresh held-out expectation or input was supplied to that repair. Full preflight
suite (captured at `artifacts/cp11-revalidation-preflight-tests.json`) exited **0**:
`Ran 88 tests in 2.488s`, `OK (skipped=1)`; `Ran 25 tests in 0.393s`,
`OK (skipped=10)`. Existing strict evidence continues to verify.

Next: commit these source/input changes and independently run the new cohort
twice from clean checkouts. Do not modify policy/source after that final held-out
evaluation. Final CP11 approval and CP12 remain pending.

## CP11 policy and repair resumption — 2026-11-19

**Status:** In progress; final human gate pending. The user asked "can't you
complete 1,2 & 3", referring to comparison-policy resolution, semantic repairs
and two new clean-checkout runs. This supersedes strict-only delivery scope and
authorizes the documented symmetric normalization allowed by AGENTS.md section 5.
It does not authorize fixture edits, hidden exclusions or final human approval.

Added explicit `--comparison python2-python3.v1`; `strict` remains the default.
`docs/comparison-policy.md` specifies and justifies every representation rule.
Raw observations, original expectations, old strict reports and strict test
assertions remain unchanged. The policy retains binary/text distinctions, numeric
and container types, file/stream/exit effects, exception classes, diagnostic fields
and unknown messages. Runtime names and known interpreter-generated diagnostic
rendering are canonicalized identically on each side. Policy and raw results
are separate. Implementation hash and source review hashes are locked per run.

Only previously available **training** fixtures were used to develop the policy
and fix. Offline training reassessment: golden **15/15**, text **25/25**, ranking
**16/16**, file-report **16/17**. The remaining issue is real: Python 3 accepts
integer paths as descriptors while Python 2 open rejects them. A source-only
repair proposes a shared path-validating `legacy_open` and updates all three I/O
call sites across package/storage modules. This is general type dispatch, not a
branch on fixture values; no exception is swallowed. Schema, base hashes,
modern compile/import, public API and candidate replay validate acceptance.
Repair candidates must improve policy results without losing any prior raw pass.

Training-only live probe command: `PYTHONPATH=src .venv/bin/python -` with a script
extracting CP5/CP8 to temporary storage, loading only
`file_report/training/file_report.json`, and calling `repair(...,
comparison=modernize.comparison.equal)` with `PolicyRepairClient` and the existing
modern sandbox. Retained `artifacts/cp11-policy-training-probe/` includes complete
initial/candidate runs, validation, patch reasons, source, call log and checksums.
It exited **0**, accepted **1** proposal, and passed **17/17 policy** cases,
retaining **6/17 raw** passes. No held-out data entered that repair. Final probe
source hashes equal the pre-evaluation coding-agent source-review manifest.

Because full policy training passes could indicate weak checks, reassessed the
eight archived CP5 mutations using the same policy: **7/8 detected**, retaining
the existing disclosed clock/quarantine blind spot. No new quarantine or relaxed
value comparison was introduced. These are reanalyses of recorded mutations,
not new mutation container executions. Added five tests covering preserved
binary/text and side-effect distinctions, exception class/message/arity/data/
offset differences, immutability and separation of raw versus policy pass flags.

`.venv/bin/python scripts/test.py` was executed via subprocess capture to
`artifacts/cp11-policy-preflight-tests.json`: exit **0**, `Ran 85 tests in 2.428s`,
`OK (skipped=1)`; `Ran 25 tests in 0.387s`, `OK (skipped=10)`. Existing strict
evidence tests still pass. Policy implementation, mutation checks, complete probe
report and suite output are retained in `docs/evidence/cp11-policy-preflight.json`.
Source review: `docs/evidence/cp11-policy-source-review.json` (coding agent,
general dispatch/encoding/division/sorting review, not final human approval).

Next: freeze/commit this policy and reviewed source repair, run every corpus
project twice in clean checkouts, and record both raw and policy results,
independent held-out evaluation, checksums and source-review matching. Do not
adjust this frozen policy/source after seeing final held-out results. CP12 has
not started; pre-existing `PRO` remains untouched.

## CP11 partial delivery — 2026-11-19

**Status:** Authorized orchestration work delivered; checkpoint **incomplete**.
The original exit criterion "Full pipeline succeeds on every corpus project"
is unmet: both full runs correctly return **3** for unresolved migrations. The
user explicitly chose this strict-failure implementation; no criterion, test,
fixture, comparison or quarantine policy was weakened. No final human approval
is claimed and CP12 remains unauthorized.

The implementation was committed as `3a844f5` before cloning. Created two fresh
local checkouts, each at full revision
`3a844f5af8c35a6ff1d1b9e1b5cd8ce1789589fe`, with empty recorded tracked changes.
Each clone used its own controller source/workers via `PYTHONPATH=src` and reused
the existing pinned virtual environment for controller dependencies; independent
dependency installation/image rebuild was not tested. Both runtimes match the
image identities recorded in the implementation section below.

### Clean-checkout commands and outcomes

```sh
mktemp -d /private/tmp/modernize-cp11.XXXXXX
git clone --local --no-hardlinks /Users/awanishkumar/hornet/sem5/agenticAI /private/tmp/modernize-cp11.uo34OG/first
git clone --local --no-hardlinks /Users/awanishkumar/hornet/sem5/agenticAI /private/tmp/modernize-cp11.uo34OG/second
```

`mktemp` returned `/private/tmp/modernize-cp11.uo34OG`. Clone commands exited **0**.
Ran the following command once in each clone's root (separate independent runs):

```sh
env PYTHONPATH=src /Users/awanishkumar/hornet/sem5/agenticAI/.venv/bin/python scripts/run_pipeline.py --output artifacts/cp11-run
```

Both completed all stages on all four projects, printed the saved report path,
and exited **3** with `status=needs_human_review`. Each recorded **471 unique
sandbox executions**, deduplicated by container creation command (initial/final
training files retain the same raw executions), plus **7 parser containers**.
No paid provider calls. All repairs finished and final source was locked before
the final held-out runs; verifier checks their recorded times and source locks.

| Project | Legacy / legacy, both runs | Legacy / modern, both runs | Converted / modern, both runs | Converted held-out, both runs |
|---|---:|---:|---:|---:|
| golden_ledger | 18/18 | 0/18 | 11/18 | 1/3 |
| text_pipeline | 30/30 | 0/30 | 5/30 | 0/5 |
| ranking | 20/20 | 0/20 | 5/20 | 1/4 |
| file_report | 20/20 | 3/20 | 7/20 | 1/3 |

Each run: **88/88**, **3/88**, **28/88** headline passes; **3/15** held-out;
**5** quarantines; **30** repair proposals, **0** accepted; **82** mock calls,
**0** mock-reported tokens/estimated USD. Differences in container IDs and times
are execution metadata; no pass-rate or failure-cause differences occurred.
This reproduces failures, not behavioral equivalence.

Verified both reports and compared all project rates and separate held-out
metrics from the repository root:

```sh
PYTHONPATH=src .venv/bin/python scripts/run_pipeline.py --compare /private/tmp/modernize-cp11.uo34OG/first/artifacts/cp11-run /private/tmp/modernize-cp11.uo34OG/second/artifacts/cp11-run
.venv/bin/python -m unittest discover -s tests/unit -p 'test_pipeline*.py' -v
git diff --check
```

All exited **0**. Comparison prints `pass_rates_reproduced: true`. Focused tests:
`Ran 4 tests in 0.391s`, `OK`. Final full suite ran via Python subprocess capture
of `.venv/bin/python scripts/test.py`; exact command and complete stdout/stderr
are retained in `docs/evidence/cp11.json` (`test_suite`) and
`artifacts/cp11-tests.json`. It exited **0**:

```text
Running unit tests
Running integration tests
Ran 80 tests in 2.469s
OK (skipped=1)
Ran 25 tests in 0.398s
OK (skipped=10)
```

**79 unit and 15 integration tests passed**. Existing Python-2 host-only and ten
opt-in security tests were skipped; no separate fresh security test run is
claimed. The two full pipeline runs did execute real isolated Docker programs.
The evidence test checks archive hash, clean-checkout metadata, real process
exits, strict raw comparisons, both reports and held-out ID absence from prompts.

### Artifacts and remaining gaps

Copied run directories to `artifacts/cp11-first/` and `artifacts/cp11-second/`,
including readable `report.md` and machine-readable `report.json`. Committed
both complete run directories as `docs/evidence/cp11.tar.gz` (**641767 bytes**),
SHA-256 `e8f21cbc0677ed72d5c7f4fe279b5a321bdcce5ecf972394c29f93d214a146d8`.
`docs/evidence/cp11.json` retains actual process-result chunks, exact commands,
provenance, reproduction outcome and full suite output. Extract the archive and
use `--verify`/`--compare` as documented in `docs/pipeline.md` for offline checks.

README and `docs/pipeline.md` explain setup, stage architecture, configuration,
artifacts, command exit statuses, reproducibility, limits and adding a corpus
project. `scripts/demo_golden.sh` invokes the same full pipeline for the golden
project and propagates its failing status; the live golden probe completed all
stages with exit **3** and its saved output verifies offline.

Remaining: **60 eligible migration failures**, including **12 held-out**;
strict cross-runtime type/exception identities and semantic differences remain.
The repository command is corpus/mock-specific; arbitrary-project and provider
pipeline support remain unimplemented. Mutation sanity checks are not rerun by
this command; existing CP5 evidence remains separate. Fresh automatic diff
review is heuristic and flags human review, not comprehensive anti-gaming proof.
Offline verification checks record consistency, not execution authenticity.

**Checkpoint report:** Single-command orchestration, failure reporting, docs,
golden demo and two clean-checkout reproducible strict runs are delivered under
the user's option 2. CP11 is **not passed** and its final human gate is **not
approved**. Stop here. Pre-existing untracked `PRO` remains untouched.

## CP11 implementation history — 2026-11-19

**Status:** In progress, incomplete under original exit criteria. User selected
"2" in response to the documented choice: build the pipeline with strict
comparisons and failing status for unresolved cases. This resolves the scope
question without changing tests, normalization, frozen fixtures or success claims.

Built `scripts/run_pipeline.py`, `scripts/demo_golden.sh`, three unit tests,
`docs/pipeline.md` and README usage. Fresh analysis, original snapshots, repeated
legacy characterization, modern baseline, training-only documentation/conversion/
repairs, all-project source locks then final held-out evaluation produce JSON and
Markdown reports. Reuses existing stage functions and recorded mock clients.
The corpus script accepts `--project <id>` or `all`, sequential/parallel analysis,
existing config, offline verification and comparison of two runs. It reads no
prior checkpoint archive to supply outcomes. Exit 3 records unresolved review;
exit 2 records execution errors; offline consistent evidence verifies with exit 0.

Scope limits are explicit: repository corpus/mock proposals only; no arbitrary
project/live-provider CLI integration, no mutation rerun, heuristic diff review
only. These remain CP11 gaps rather than silently weakened requirements. No
existing test was changed. A new-code syntax error (unmatched parenthesis) caused
the first focused import to fail; implementation was corrected, with assertions
unchanged. Focused rerun: `Ran 3 tests in 0.129s`, `OK`.

Commands so far:

```sh
docker image inspect modernize-legacy:cp0 modernize-modern:cp0 --format '{{.Id}}'
.venv/bin/python -m unittest discover -s tests/unit -p test_pipeline.py -v
.venv/bin/python scripts/run_pipeline.py --project golden_ledger --output artifacts/cp11-golden-probe
PYTHONPATH=src .venv/bin/python scripts/run_pipeline.py --verify artifacts/cp11-golden-probe
.venv/bin/python scripts/test.py
git diff --check
```

Docker required escalation after socket permission denial. Existing image IDs:
legacy `sha256:981bbf199b2a829c4cfceb54f1e75a1409d4dff7602b64a09c58f08a2fd4e5e5`;
modern `sha256:c05c4c189eda65dd7dd1d6767f5f9330033c93c81b7a10ba709d837f74b4562c`.
The golden probe ran every stage live, saved its report and exited **3** as
designed: legacy/legacy **18/18**, legacy/modern **0/18**, converted/modern
**11/18**, held-out converted **1/3**, **4** repair proposals, **0** accepted,
**13** mock calls, **0** mock tokens/estimated USD. Offline verification exited
**0**. Full default suite exited **0**, retaining its eleven existing environment
skips; no separate security suite or paid provider run is claimed.

Next: commit this implementation for clean-checkout execution, run the whole
corpus twice from local clean clones, verify/compare raw results, retain evidence
and record actual exit statuses. CP11 remains incomplete regardless of matching
rates while strict migrations fail. Pre-existing untracked `PRO` is untouched.

## CP11 requirements review — 2026-11-19

**Status:** Started, blocked; not passed. Authorized by "start next goal" after
CP10 completion. Re-read AGENTS.md, current progress, PROJECT_PLAN.md, existing
stage scripts, CLI, repair implementation and observation codec/harness. No code,
test, fixture or comparison changes were made in this review.

CP11 requires the full pipeline to succeed on every corpus project. The current
approved CLI contract returns nonzero for unresolved review, and CP10 reports
**60 unresolved eligible cases**, including **12 held-out failures**. Treating a
completed orchestration as successful behavior preservation would misrepresent
those results. Some mismatches cannot be repaired solely in project source under
the frozen observation contract: `sandbox_codec.outcome_value` accepts exact
built-in types and records their runtime names. Python 3 built-in text records
`type=str`, whereas the Python 2 oracle records `type=unicode`. A renamed subclass
is rejected by that codec, so source-level type impersonation is not a solution.
Exception module names and argument string representations also differ.

Concrete recorded example: text_pipeline case `726a9707f6b8681a538d`, target
`main.py::clean_names`, returns the same list of text contents `Ada` and `Lin`
in both runtimes, but expected elements have `type=unicode` and actual elements
have `type=str`. Raw replay reference:
`cp9.tar.gz!/text_pipeline/repair/training-final.json#726a9707f6b8681a538d`.
Golden-ledger case `2933d0e1a536a13e1c9b` reports the same ZeroDivisionError
message but different module (`exceptions`/`builtins`) and argument text encoding.
Other failures are semantic, including file_report's integer-path handling;
type-name normalization alone would not establish a successful migration.

Reverification command:

```sh
PYTHONPATH=src .venv/bin/python scripts/report_corpus.py --verify docs/reports/cp10
```

Exited **0** with report status `needs_human_review`; legacy/legacy **88/88**,
legacy/modern **3/88**, converted/modern **28/88**, converted held-out **3/15**.
These are recomputed existing observations, not new project executions.

AGENTS.md section 8 requires stopping if a checkpoint exit criterion cannot be
met as written; sections 2/5 prohibit quietly weakening comparisons or changing
frozen fixtures. Requested decision: either authorize a CP11 delivery that
completes orchestration and reports unresolved migrations with nonzero exit
(keeping CP11 incomplete under its current success criterion), or first approve
development of a documented cross-runtime comparison policy applied equally to
both observations, retaining the raw evidence and addressing real semantic
failures separately. No policy change, new quarantine, test edit, gate approval,
provider call or fresh Docker run is inferred from the request to start CP11.

## CP10 completion — 2026-11-19

**Status:** Passed. The user approved the documented new-test correction with
"yeah correct it". Changed only that assertion from zero to three baseline
passes; no existing test, frozen expectation, fixture or comparator was changed.
The preceding CP10 implementation history below retains the failed-test evidence.
CP11 has not started; stop at this checkpoint report.

Built `scripts/report_corpus.py`, three focused tests, `docs/reporting.md`, and
the committed JSON/Markdown reports in `docs/reports/cp10/`. README and plan now
identify CP11 as next. Uses existing CP5/CP6/CP9 verifiers, observation comparison,
documentation schemas/claim checks and call-log usage accounting. No dependency,
provider call, source execution or new container run was needed.

The aggregate report includes every CP10 exit item: three rates per project on
the same eligible cases, coverage and original targets, exclusions/quarantines
with reasons, separate held-out results, all final conversion diffs, per-function
repair counts/attempts, per-stage and total usage/cost, unresolved exact outcome
comparisons, source-grounded suspected legacy bugs, machine-tagged documentation
and architecture summaries. Archive hashes and archive/member/case references
trace the numbers to recorded runs. Verification rebuilds both report files and
rejects changed numbers, prose or raw replay results. Protected-output checks
and refusal to overwrite existing outputs are tested too.

### Recomputed results

| Project | Legacy / legacy | Legacy / modern | Converted / modern | Held-out converted |
|---|---:|---:|---:|---:|
| golden_ledger | 18/18 (100%) | 0/18 (0%) | 11/18 (61.11%) | 1/3 (33.33%) |
| text_pipeline | 30/30 (100%) | 0/30 (0%) | 5/30 (16.67%) | 0/5 (0%) |
| ranking | 20/20 (100%) | 0/20 (0%) | 5/20 (25%) | 1/4 (25%) |
| file_report | 20/20 (100%) | 3/20 (15%) | 7/20 (35%) | 1/3 (33.33%) |

Aggregate: **88/88**, **3/88**, **28/88** respectively; converted held-out
**3/15**; **60** eligible failures remain. **5** cases remain quarantined.
**30** repair proposals, **0** accepted repairs, **9** diff files. **82** logged
mock calls, **0** mock-reported tokens and estimated USD **0**. Usage covers only
successful retained CP5/CP7/CP8/CP9 corpus stages, excluding infrastructure tests,
failed/probe runs and coding-agent authoring. These are not live-provider cost
or repair-quality estimates. No comparison or quarantine policy was relaxed.

### Commands and evidence

```sh
.venv/bin/python -m unittest discover -s tests/unit -p test_reporting.py -v
PYTHONPATH=src .venv/bin/python scripts/report_corpus.py --output docs/reports/cp10
PYTHONPATH=src .venv/bin/python scripts/report_corpus.py --verify docs/reports/cp10
.venv/bin/python scripts/test.py
git diff --check
```

All commands exited **0**. Focused suite: `Ran 3 tests in 1.544s`, `OK`.
Full suite, unit before integration:

```text
Running unit tests
Ran 76 tests in 2.086s
OK (skipped=1)
Running integration tests
Ran 25 tests in 0.375s
OK (skipped=10)
```

**75 unit and 15 integration tests passed**. The existing Python-2 host-only test
and ten opt-in Docker security tests were skipped. No fresh security execution,
paid provider call or CP11 clean-checkout end-to-end run is claimed.

Reports: `docs/reports/cp10/report.json` (**252189 bytes**), SHA-256
`f87ae98e4d6e60797253b70bc8cb3ae56927789f6c941a46bb95dd607197243c`;
`docs/reports/cp10/report.md` (**181846 bytes**), SHA-256
`67f89f410f76b8770dc0712871719fc4719bb577272186af1de5bbbbaac64a24`.
Sizes and hashes were recomputed with Python pathlib/hashlib from these files.

**Limits:** Offline verification checks consistency of recorded evidence, not
original execution authenticity. Existing CP9 no-patch corpus evidence does not
demonstrate accepted provider repairs. Documentation prose and suspected bugs
remain source-grounded claims with explicit limitations. The report correctly
retains `needs_human_review` while CP10's reporting requirements pass.

**Checkpoint report:** CP10 is complete with verified aggregate evidence; CP11
is next. Pre-existing untracked `PRO` remains untouched.

## CP10 implementation history — 2026-11-19

**Status:** In progress. Read AGENTS.md, PROJECT_PLAN.md and current checkpoint;
CP9 is passed and CP10 reporting is authorized by "start the next goal".

Built `scripts/report_corpus.py` to derive JSON and Markdown from CP5–CP9
archives, reuse the CP5/CP6/CP9 verifiers, and recompute report contents offline.
Includes shared-denominator pass rates, separate held-out metrics, coverage,
quarantines, repair attempts, mock usage/cost provenance, unresolved comparisons,
source-grounded suspected bugs, documentation, diffs and archive/member references.
No original source, fixtures or existing tests were modified.

New `tests/unit/test_reporting.py` currently has an incorrect assertion:
`totals['legacy_on_modern']['passed'] == 0`. The recorded CP6 baseline (see the
CP6 table below) actually has **3** passes, all in file_report. The report correctly
recomputes **3**. This is a mistaken new test expectation, not an implementation
failure. Proposed correction: assert **3**, retaining exact comparison and every
other assertion. Under AGENTS.md section 4, approval is requested before editing
the incorrect test. No correction or checkpoint pass is claimed yet.

Command: `.venv/bin/python -m unittest discover -s tests/unit -p test_reporting.py -v`
exited **1**: `Ran 3 tests in 1.334s`, `FAILED (failures=1)`;
the report/Markdown tamper test and raw-observation tamper test passed, while the
required-evidence test stopped at `AssertionError: 3 != 0`.

CP11 has not started. Remaining: approved test correction, full suite, generated
report and independent verification, usage documentation, checkpoint evidence and
commit. The pre-existing untracked `PRO` file remains untouched.

While the correction request is pending, generated and verified a concrete report:

```sh
PYTHONPATH=src .venv/bin/python scripts/report_corpus.py --output artifacts/cp10-run1
PYTHONPATH=src .venv/bin/python scripts/report_corpus.py --verify artifacts/cp10-run1
wc -lc artifacts/cp10-run1/report.json artifacts/cp10-run1/report.md
```

Both report commands exited **0**, reporting `needs_human_review`. Recomputed
totals: legacy/legacy **88/88**, legacy/modern **3/88**, converted/modern **28/88**;
held-out converted **3/15**; **5** quarantines; **30** repair proposals and **0**
accepted repairs; **9** diff files; **82** mock calls with **0** mock tokens and
estimated USD **0**. JSON: **252189 bytes**, Markdown: **181846 bytes**. Report
verification does not resolve the incorrect test or pass CP10. Added
`docs/reporting.md` with commands, evidence scope and limitations. No full suite,
paid API call, fresh sandbox execution or commit has been performed in CP10.

## CP9 completion — 2026-11-19

**Status:** Passed. Authorized by "read program project report and agent, then
start the next goal completion". All four loops terminated, frozen inputs were
unchanged, held-out results are separate, and anti-gaming review is recorded.
Unresolved cases are explicitly `needs_human_review`, as CP9 requires. CP10 was
not started; CP11 approval remains pending.

Built `repair.py`, a diagnostic replay worker, versioned `repair.v1` prompt/schema,
`scripts/repair_corpus.py`, focused tests and offline archive verification.
Reuses CP3 isolation, CP4 schema/retry/logging/accounting and CP8 source patches,
hash validation, modern compile/import and public-signature validation. No new
dependency, image or framework. Source executes only in the modern sandbox.

Only training exports enter repairs. Prompts include current source/hashes,
failed inputs, exact expected-versus-actual diff, traceback frames and previous
rejection. The original CP5 harness/codec/comparator and expectations remain
unchanged. Per-function cap is two proposals; CP4's schema retry cap remains
separate. A candidate must compile/import, retain public API and improve the
visible suite without losing any prior pass. Failed candidates cannot publish.
Final source publishes as a complete directory after the loop.

### Recorded results

| Project | Training before/after (unchanged) | Held-out after loop | Proposals | Status |
|---|---:|---:|---:|---|
| golden_ledger | 10/15 (66.67%) | 1/3 (33.33%) | 4 | needs human review |
| text_pipeline | 5/25 (20%) | 0/5 (0%) | 10 | needs human review |
| ranking | 4/16 (25%) | 1/4 (25%) | 8 | needs human review |
| file_report | 6/17 (35.29%) | 1/3 (33.33%) | 8 | needs human review |

Training: **25/73 passed**, **48 unresolved**. Held-out: **3/15 passed**,
**12 unresolved**. Raw run comparisons, not manually assigned pass flags, produce
these counts. Each failing function reached its cap; retry counts and errors are
saved. The corpus run contains **88 live sandbox executions** (training once and
held-out once). No proposed source patch was accepted, so final source equals CP8
and no additional candidate compile/import runs were needed.

The corpus demonstration replays coding-LLM-authored **no-patch assessments** via
the deterministic mock: **30 calls, 0 mock-reported tokens, 0 mock estimated USD**.
It does not demonstrate autonomous provider repair quality or a live accepted
repair. Unit tests separately prove successful acceptance, rejection of invalid
source and regressions, retries, atomic publication and evidence tamper detection.

Many failures distinguish Python 2 `str`/`unicode` from Python 3 `bytes`/`str`,
including nested values, dictionary keys and instance state. Exceptions also
differ in module, argument types and messages. Other semantic mismatches remain,
including Python 3 treating an integer file path as a descriptor. No codec,
fixture or comparison was weakened to conceal them; no runtime identity was
impersonated. These are unresolved migrations, not suspected legacy bugs.
The already documented suspected legacy input overwrite remains preserved.

All projects finished repairs and locked source hashes before the controller
opened any held-out cases. Recorded held-out container start times follow all
repair calls. No held-out input/ID/outcome appears in a repair prompt. Checksum
manifests cover **38 protected files**, including tests/fixtures, corpus and
CP5–CP8 archives, with identical before/after hashes, checked in `finally`.
CP9 adds no quarantine; CP5's existing exclusions remain unchanged.

An AST scan covers mechanical-to-final semantic changes, flags new branches and
exception handlers for inspection, and checks fixture references/imports. Full
CP7-to-final diffs cover every conversion file, including helpers. Coding-agent
manual review of all saved conversion diffs found no fixture-valued branches,
new exception suppression, fixture access or comparison relaxation. Existing
type dispatch is general; `describe`'s type-name labels are public return values,
not rewrites of observation metadata. Automatic flags on numeric helper branches
were reviewed as general int/float division dispatch. Review is heuristic/manual,
not proof of comprehensive detection. Assessment: archive `cp9-review.json`.

### Commands, evidence and limits

```sh
docker image inspect modernize-modern:cp0 --format '{{.Id}}'
.venv/bin/python -m unittest discover -s tests/unit -p test_repair.py -v
PYTHONPATH=src .venv/bin/python scripts/repair_corpus.py --output artifacts/cp9-run1
.venv/bin/python -m unittest discover -s tests/unit -p 'test_repair*.py' -v
PYTHONPATH=src .venv/bin/python scripts/repair_corpus.py --verify docs/evidence/cp9.tar.gz
.venv/bin/python scripts/test.py
git diff --check
```

All final commands exited **0**. Initial unapproved Docker inspection failed with
socket permission denied; approved escalation succeeded. The live run used the
same modern image as CP3/CP8:
`sha256:c05c4c189eda65dd7dd1d6767f5f9330033c93c81b7a10ba709d837f74b4562c`.
A preliminary training-only probe in `artifacts/cp9-probe` recorded another 73
sandbox executions before repair implementation was finalized; those are not
included in the committed successful-run archive or its metrics.

Focused final checks: `Ran 7 tests`, `OK`. Full suite:

```text
Running unit tests
Ran 73 tests in 0.486s
OK (skipped=1)
Running integration tests
Ran 25 tests in 0.374s
OK (skipped=10)
```

**72 unit and 15 integration tests passed**. Existing Python-2 host-only and ten
opt-in CP3 live security tests were skipped. No separate security rerun or paid
API run is claimed. Seven new test methods were added; existing tests were not
changed or weakened. Offline verification recomputes comparisons, caps,
training-only contexts, source/image/request identities, held-out ordering,
source locks, diff scans and mock usage. Its rejected-candidate archive checks
are scoped to this run's no-patch responses; future rejected source patches need
their validation records checked too.

Successful directory: `artifacts/cp9-run1`. Committed evidence:
`docs/evidence/cp9.tar.gz` (**89123 bytes**), SHA-256
`500b3e25f1c1ec2f9377fb376ef77eac963f71275f00cc7766525aff110f8b62`.
README, plan and `docs/repair.md` document usage and limits.

**Checkpoint report:** CP9 verification/repair infrastructure and all required
evidence are complete. Behavior preservation remains unresolved and is reported
honestly. Stop here; CP10 aggregate reporting is next.

## CP8 completion — 2026-11-19

**Status:** Passed. Authorized by "next goal" following the CP7 report. CP9
characterization verification, repair and held-out evaluation were not started.

Built `transformation.py`, two sandbox workers, the versioned strict
`transformation.v1` schema/template, and `scripts/transform_corpus.py`.
Conversion starts from CP7's documented source copies, preserving original
corpus files. The mechanical worker parses with Python 2 before conversion and
uses an explicit list of lib2to3 fixers from the pinned legacy image. It handles
print/except syntax, dictionary methods and iterator materialization, stabilizing
within four passes or failing. Unicode literals and division are deferred to
the semantic layer. No new dependency, image or framework was introduced.

Semantic proposals pass through the existing `LLMRun` schema, retry, logging and
usage boundary. Change sets contain source paths, base hashes, full replacement
text, reasons, hazard labels and review flags. The controller rejects protected/
unsafe paths, duplicate patches, stale bases, invalid modern syntax and new helper
directories. It checks existing definition names, parameter names, default counts
and variadic names against CP2. Changed defaults' values and runtime equivalence
are not proven by this signature check.

Helpers, imports and affected callers are changed together: two division helpers
dispatch built-in integer versus float division; ranking uses cmp_to_key with a
shared comparator; text functions retain ASCII/UTF-8 boundaries and original type
labels; report writers explicitly use binary payloads and byte-valued keys.
The suspected input overwrite and time/randomness remain in source. Every
semantic patch has a recorded reason. No public definition was renamed.

Each complete candidate compiles and imports in the CP3 modern sandbox, which
also records refreshed definition/signature/import facts. Rejected candidates
receive the validation error on the next attempt, capped at two candidates per
project, with CP4's separate schema retry cap unchanged. A source directory is
published only after full project validation; failed candidates never publish.

### Recorded results

| Project | Files compiled/imported | Final diff files | Semantic patch files | Successful-run candidate attempts |
|---|---:|---:|---:|---:|
| golden_ledger | 2 | 2 | 2 | 1 |
| text_pipeline | 1 | 1 | 1 | 1 |
| ranking | 1 | 1 | 1 | 1 |
| file_report | 5 | 5 | 4 | 1 |

All **four projects / nine Python files** compile/import under the recorded
Python 3.12 image. Seven incoming files changed and two helper modules were
added. Diffs cover every final changed/new file, against incoming CP7 documented
source, with separate mechanical diffs. Original corpus remains unchanged.
Successful evidence contains **nine live sandbox runs**: one mechanical
self-check, four mechanical conversions and four modern compile/import runs.
This is **not a converted-behavior pass rate**; no frozen suite was run here.

Prompts receive CP2 project facts and CP5 training-only observed type/exception
summaries. Existing export/seal checks keep held-out outcomes and private oracle
logs out of conversion. Before/after checksums prove tests, fixtures, corpus and
CP5/CP6/CP7 evidence archives unchanged, including failure exits via `finally`.
No model receives write access to test/fixture stores, and all source execution
remains in the unchanged network-disabled sandbox with no writable host mounts.

The corpus demo uses coding-LLM-authored semantic edits from
`docs/evidence/cp8-proposals.json`, replayed through the deterministic mock.
Successful run: **4 mock calls, 0 mock-reported tokens, 0 mock estimated USD**.
The earlier failed corpus run made five additional mock calls, retained in
`artifacts/cp8-run5/*/llm/`; no paid provider calls were made in this session.
This does not verify autonomous provider conversion quality or estimate its cost.

### Commands and verification

```sh
docker image inspect modernize-legacy:cp0 modernize-modern:cp0 --format '{{.Id}}'
.venv/bin/python -m unittest discover -s tests/unit -p test_transformation.py -v
PYTHONPATH=src .venv/bin/python scripts/transform_corpus.py --output artifacts/cp8-run6
.venv/bin/python scripts/test.py
git diff --check
```

Final commands exited **0**, with approved Docker escalation. Image IDs match
CP3: legacy `sha256:981bbf199b2a829c4cfceb54f1e75a1409d4dff7602b64a09c58f08a2fd4e5e5`;
modern `sha256:c05c4c189eda65dd7dd1d6767f5f9330033c93c81b7a10ba709d837f74b4562c`.
Focused tests: `Ran 4 tests`, `OK`. Full suite:

```text
Running unit tests
Ran 66 tests in 0.280s
OK (skipped=1)
Running integration tests
Ran 25 tests in 0.372s
OK (skipped=10)
```

**65 unit and 15 integration tests passed**. Existing Python-2 host and ten
opt-in CP3 live security tests were skipped; no separate security rerun claimed.
Five new methods cover schema/retry behavior, safe paths, stale hashes, duplicate
patches, invalid syntax, public signature changes, error feedback with atomic
publication, and recomputation of the archived source/diffs/reasons/imports/
training context/checksum evidence. No existing tests were changed or weakened.

Failures retained: initial sandboxed Docker inspection and `cp8-run1` were denied
socket access. Approved `cp8-run2` through `run4` self-checks exposed non-idempotent
standard-library dict conversion (`iteritems` then `items` wrapping). Fixed by
bounded stabilization without removing the assertion; print conversion also
gets a future import. `cp8-run5` compiled the first three projects, but
file-report's future import appeared after an ordinary import. Both modern
attempts failed with SyntaxError; error feedback/cap were recorded and that
project published no candidate. The converter now places the future import
immediately after the module docstring, with a new self-check preserving ordinary
imports. All checks and projects passed in `cp8-run6`.

### Artifacts and limits

Successful directory: `artifacts/cp8-run6`; per project `mechanical/`,
`mechanical-diffs/`, `changes-0.json`, `validation-0.json`, `attempts.json`,
`source/`, `diffs/`, `report.json` and `llm/`. Complete committed archive:
`docs/evidence/cp8.tar.gz` (**49584 bytes**), SHA-256
`e49bb3b7a90e3d734676ad5553732b68dac9e586f41cd5deca61b742645097cd`.
The archive unit test reconstructs candidates from recorded bases/patches and
checks saved diffs, raw request/source/image identities and all result counts.
README, plan and `docs/transformation.md` document the interface and limits.

Custom __div__/__cmp__, heterogeneous comparison, long-result types, precise
Python 2 exception identity/messages, runtime byte/Unicode tags and non-ASCII
formatting remain explicit review risks. Successful clock-dependent paths are
still quarantined. CP9 must evaluate the frozen suite, cap repair attempts,
separately run held-out cases and review diffs for anti-gaming violations.
Compilation/import alone makes no behavioral preservation claim.

**Checkpoint report:** CP8 is complete with layered conversion, modern
compile/import proof, frozen-input checksums and saved diffs/reasons. Stop here;
CP9 verification and repair is next. CP11 human approval remains pending.

## CP7 completion — 2026-11-19

**Status:** Passed. CP6 approval recorded above; CP8 not started.

Built `documentation.py`, a versioned strict documentation schema/template, and
the trusted Python 2 `documentation_worker.py`. Generation visits known callees
before callers (cycles ordered deterministically), classes after methods,
modules after definitions, and package summaries last. Function prompts include
source, AST signatures, caller/callee facts, effects and training-only observed
return types/exception names. Existing CP5 training export excludes sealed cases
and private oracle logs from generation. All generated text is tagged.

`LLMRun.generate` now also accepts an explicit versioned `Prompt`, retaining its
named input-prompt interface, validation, retries and logs. The documentation
template/schema subdirectory is included in package data. No dependency, runtime
image, corpus, existing test or original fixture was changed. `PRO` is untouched.

The editor inserts string literals into a separate source copy. In CP3's legacy
sandbox it parses/compiles each result, checks inserted docstrings, and compares
ASTs with docstrings removed. No corpus module is imported/executed, and host
Python 3's AST is never used to parse original Python 2 files. The annotated copy
changes introspection/line numbers by design; it is not a characterization oracle.

### Recorded results

| Project | Function/method docs | Class docs | Module summaries | Package summaries | Omissions | Claim mismatches |
|---|---:|---:|---:|---:|---:|---:|
| golden_ledger | 3 | 0 | 1 | 1 | 0 | 0 |
| text_pipeline | 5 | 0 | 1 | 1 | 1 lambda | 0 |
| ranking | 4 | 1 | 1 | 1 | 0 | 0 |
| file_report | 4 | 0 | 4 | 1 | 0 | 0 |

All **16 named functions/methods**, **1 class**, **7 modules** and **4 packages**
have generated docs. The nested lambda has a logged reason: no docstring suite;
its enclosing helper documents it. Evidence tests reconcile these with CP2's
17 function facts including the lambda. All seven annotated files compile and
retain their executable AST. Five successful live sandbox runs were recorded:
one editor self-check and four project validations.

Cross-checks compare structured claimed return types/exception names with actual
CP5 training outcomes and retain mismatches. A calibration test deliberately
claims a floating return/TypeError and detects both false claims. **Prose is
source-based inference, not mechanically proven behavior.** Dynamic/callback
graph edges can remain unresolved. `build_report` success paths remain
quarantined; docs disclose this and flag its input overwrite as a suspected
legacy bug without changing it. No comparison normalization was added.

`scripts/document_corpus.py` replays coding-LLM-authored summaries from
`docs/evidence/cp7-proposals.json` through the deterministic mock; observed type
claims are populated directly from training outcomes. **28 mock calls**, **0 paid
provider calls**, **0 mock-reported tokens**, **0 mock estimated USD**. These do
not measure live-provider quality/cost. A provider-backed `LLMRun` can use the
same API. Docs-only prompt contracts are tested separately from input proposals.

### Commands and verification

```sh
.venv/bin/python -m unittest discover -s tests/unit -p test_documentation.py -v
PYTHONPATH=src .venv/bin/python scripts/document_corpus.py --output artifacts/cp7-run3
.venv/bin/python scripts/test.py
git diff --check
```

Final commands exited **0**. Focused tests: `Ran 3 tests`, `OK`. Full suite:

```text
Running unit tests
Ran 61 tests in 0.227s
OK (skipped=1)
Running integration tests
Ran 25 tests in 0.370s
OK (skipped=10)
```

**60 unit and 15 integration tests passed**. Existing Python-2 host and ten opt-in
CP3 live security tests were skipped; their unchanged isolation policy was used
for the new validation runs. No separate security-suite rerun is claimed.
The new archive test recomputes symbol coverage, structured claim checks, call
counts, saved source bytes, module/package artifacts and checksum proof.

Failures retained: sandboxed `artifacts/cp7-run1` was denied Docker access.
Approved `cp7-run2` self-check found Python 2 multiline strings report AST
positions differently from tokenizer starts (`StopIteration`). The editor now
matches a spanning token with the same literal value and logs ambiguous tokens
as omissions. The unchanged self-check then passed multiline signatures/comments,
existing multiline docs, class/decorator insertion, module docs, escaped quotes/
Unicode, inline omission and unknown-target rejection.

Successful run: `artifacts/cp7-run3`; per-project `source/`, `documentation.json`,
`modules/`, `architecture.md`, `validation-run.json`, `llm/`. Before/after
checksum manifests prove identical tests, fixtures, original corpus and CP5/CP6
archives. Extracted CP5 seals were verified before/after; held-out outcomes never
enter prompts. Documentation output paths cannot overwrite protected inputs.

Complete committed archive: `docs/evidence/cp7.tar.gz` (**44532 bytes**), SHA-256
`07b6aef479708034e7ea1a2a7c49bae814da4c1001a9d633b086d2a7cb26d65f`.
Contract/limits: `docs/documentation.md`. README and plan updated.

**Checkpoint report:** CP7 is complete with docstrings, module/package summaries,
observation cross-checks, explicit omissions and frozen-input proof. Stop here;
CP8 transformation is next. CP11 human approval remains pending.

## CP6 baseline — 2026-11-19

**Status:** Passed after the user's "next goal" approval on 2026-11-19.
The measurement session below originally stopped at the human gate; approval
and subsequent CP7 completion are recorded above.

Built `scripts/baseline_corpus.py` to replay unchanged corpus source in the
existing CP3 modern sandbox, group exact comparison failures, and independently
recompute the report from retained records. Two new unit tests cover category
selection, exact type/stream comparisons, archive recomputation, missing cases,
and tampered comparison flags. README and stale project-plan status updated.
No dependency, corpus, existing test, fixture, sandbox or prompt was changed.

### Recorded results

| Project | Legacy on Python 2.7 | Legacy on Python 3.12 | First observed failure groups |
|---|---:|---:|---|
| golden_ledger | 18/18 (100%) | 0/18 (0%) | 18 syntax errors |
| text_pipeline | 30/30 (100%) | 0/30 (0%) | 30 syntax errors |
| ranking | 20/20 (100%) | 0/20 (0%) | 20 syntax errors |
| file_report | 20/20 (100%) | 3/20 (15%) | 5 outcome mismatches; 6 AttributeError; 3 TypeError; 3 ValueError |

Legacy results reuse the **first independent CP5 repeat** for each case (repeat
index 1), not the original expectation-producing observation (index 0). All
88 modern outcomes are new container executions. Accepted fixtures include the
15 sealed cases for this baseline evaluation; repair still must use CP5's
training-only export. The five CP5 flaky cases remain quarantined. No expectations
were regenerated or comparisons normalized. Fixture seals and full corpus hashes
were checked before/after measurement and again by the offline verifier.

Syntax errors prevent importing all of the first three projects' tested modules
(including Python 2 print/except syntax). These are first blockers, so this
baseline does not expose their later division, iterator or sorting failures.
File-report tests import its package modules directly and reach runtime behaviour:

- `write_report`: removed `dict.iteritems` causes six AttributeErrors, including
  cases that previously raised Unicode encoding/decoding errors.
- `summarize`: four nonempty numeric cases change integer means to floats; the
  empty case also differs because dictionary keys change byte/text representation.
- `build_report`'s one eligible invalid-path case now reaches a binary-file
  string write and raises a different TypeError. Successful clock-dependent
  cases remain quarantined and are not evaluated here.
- Three `read_numbers` ValueErrors and two `summarize` TypeErrors remain errors
  in both runtimes, but their exact module, argument encoding and messages differ.

Categories labeled `runtime_exception:<name>` group the **actual** exception
when its outcome differs; they do not imply the original returned normally.
All original/actual values, exception details, streams and scratch files remain
in the raw records. Strict byte/text and exception comparison is intentionally
unchanged from CP5; future normalization would need equal application and a
written justification under AGENTS.md. No equivalence or repair claim is made.

### Commands and evidence

```sh
docker image inspect modernize-modern:cp0 --format '{{.Id}}'
PYTHONPATH=src .venv/bin/python scripts/baseline_corpus.py --output artifacts/cp6-run2
PYTHONPATH=src .venv/bin/python scripts/baseline_corpus.py --verify docs/evidence/cp6.tar.gz
.venv/bin/python scripts/test.py
```

All final commands exited **0**. Docker commands required approved escalation.
The initial sandboxed image inspection and baseline invocation to
`artifacts/cp6-run1` were denied Docker socket access; the failed baseline
produced no completed project records. The approved run used modern image
`sha256:c05c4c189eda65dd7dd1d6767f5f9330033c93c81b7a10ba709d837f74b4562c`.
The legacy records use image
`sha256:981bbf199b2a829c4cfceb54f1e75a1409d4dff7602b64a09c58f08a2fd4e5e5`.
Both match earlier CP3 runtime identities. No images rebuilt or provider calls made.

Run directory: `artifacts/cp6-run2`. Complete raw archive:
`docs/evidence/cp6.tar.gz` (**46596 bytes**), SHA-256
`aa3750c755fe285d75681dc0ebd12a62d3a67f69c61defc692d9a762f12ed4f7`.
It contains each project's 88 total legacy and 88 total modern records plus
`summary.json`. Verification also checks the committed CP5 archive and seals,
actual requests/source hashes, runtime identities, isolation, stopped containers
and cleanup flags. Counts and groups above are recomputed from those records.

Final suite output:

```text
Running unit tests
Ran 57 tests in 0.209s
OK (skipped=1)
Running integration tests
Ran 25 tests in 0.387s
OK (skipped=10)
```

**56 unit and 15 integration tests passed**. The existing Python-2 host test
and ten opt-in live CP3 tests were skipped; unchanged CP3 isolation was used for
the 88 new baseline runs, not retested as a separate security suite.

**Checkpoint report:** Baseline measurement is ready for human review. Approve
the failure categories above to pass CP6 and authorize CP7 documentation
generation. This stop is required by `AGENTS.md`, section 6, CP6: "Human reviews
that the failure categories make sense and approves proceeding."

## CP5 completion — 2026-11-19

**Status:** Passed. User authorized CP5 with "complete the next checkpoint".
No modern-runtime baseline, documentation generation, conversion or repair was
started. CP6 and CP11 human gates remain unapproved.

### Built and decisions

- `characterize.py`: bounded validated proposals, legacy-only oracle collection,
  exact replay comparison, flakiness quarantine, coverage feedback, deterministic
  held-out selection, read-only checksum seals and training-only export.
- `characterize_worker.py`: trusted Python 2/3 observation harness running only
  inside CP3's unchanged sandbox. Legacy `ast` supplies static denominators;
  `sys.settrace` measures unmodified function source. Captures return values,
  exceptions, instance state, streams and scratch files through CP3's codec.
- Added versioned `characterization_inputs.v1` prompt/schema with input-only
  scratch assets and method setup. Existing prompt contracts/callers are unchanged.
- `scripts/characterize_corpus.py` evaluates the four projects, replays eight
  disposable mutations against training fixtures and separately checks held-out
  fixtures. `scripts/verify_cp5.py` recomputes metrics from raw records.
- No dependency, image, agent framework or sandbox policy change. No corpus,
  existing test or original fixture was edited. Existing uncommitted handoff
  notes were preserved; `PRO` was not inspected or changed.
- No provider key is configured. This coding LLM authored the input-only
  proposal file; the corpus command replays it through the schema-validated
  deterministic mock. All 20 calls are labeled mock evidence, not autonomous
  live-provider input discovery. A provider-backed `LLMRun` can use the same
  `Characterizer` interface. Paid calls: **0**; mock usage/estimates: **0**.
- Wrote `artifacts/cp5-run2/plan.json` before oracle collection: 90% function
  statement-line and explicit-branch targets, three observations per case,
  at most two proposal rounds, at least 80% detection of eight mutations.

### Commands, failures and evidence

Focused verification:

```sh
.venv/bin/python -m unittest discover -s tests/unit -p test_characterize.py -v
```

Initial exit **1**: the flaky-case test found that a zero-accepted-case first
round stopped before coverage feedback. Removed that premature stop; kept the
test unchanged. Final focused command exited **0**, `Ran 5 tests`, `OK`.

The first sandboxed corpus invocation to `artifacts/cp5-run1` exited **1** because
Docker socket access was denied. It produced no oracle outcomes. Approved
Docker access verified the existing image, then the successful command was:

```sh
PYTHONPATH=src .venv/bin/python scripts/characterize_corpus.py --output artifacts/cp5-run2
```

Exit **0**. Recorded Python 2.7 image identity:
`sha256:981bbf199b2a829c4cfceb54f1e75a1409d4dff7602b64a09c58f08a2fd4e5e5`.
Observed summary, independently recomputed below:

| Project | Accepted cases | Repeat passes/comparisons | Eligible function lines | Explicit branches | Quarantined | Held-out passed |
|---|---:|---:|---:|---:|---:|---:|
| golden_ledger | 18 | 36/36 | 8/8 (100%) | 2/2 | 0 | 3/3 |
| text_pipeline | 30 | 60/60 | 8/8 (100%) | 0/0 | 0 | 5/5 |
| ranking | 20 | 40/40 | 9/9 (100%) | 2/2 | 0 | 4/4 |
| file_report | 20 | 40/40 | 9/16 (56.25%) | 4/4 | 5 | 3/3 |

**88 accepted cases**, **176/176 independent repeat comparisons (100%)**,
**73 training fixtures**, **15 held-out fixtures**, **5 quarantined cases**.
Eligible outcomes include 67 normal returns and 21 stable legacy exceptions.
Every accepted case ran three times; held-out cases ran once more separately.
There are **443 actual sandbox executions**: 283 inventory/oracle runs, 145
mutation comparisons and 15 held-out verification runs. Each raw record includes
image identity, actual isolation policy, source hashes and container cleanup.

Detected mutations: division, accumulation, integer parsing, empty-name
filtering, zip length, comparison sort direction and mean calculation. The
deliberate clock mutation survived: **7/8 (87.5%)**, exceeding the stated 80%
minimum while exposing the quarantined-function blind spot.

All three first projects finished in one proposal round. File-report's second
round added an empty summary input targeting its uncovered `if` branch. The
unaddressable text-cleaning lambda is explicitly logged and exercised through
`clean_names`; all 16 named functions/methods received proposals and eligible
cases. Zero-argument initialization has only two distinct applicable proposals.

Raw run directory: `artifacts/cp5-run2`. Committed complete evidence archive:
`docs/evidence/cp5.tar.gz` (**120716 bytes**), SHA-256:
`6488d6a708ef0cd9b0858b20d7e25af9341df7e44b10e0a9cd818f9d29f1b6a2`.
`docs/evidence/cp5.json` contains the recomputed summary and command identities.

```sh
PYTHONPATH=src .venv/bin/python scripts/verify_cp5.py artifacts/cp5-run2
PYTHONPATH=src .venv/bin/python scripts/verify_cp5.py docs/evidence/cp5.tar.gz
.venv/bin/python scripts/test.py
docker ps -a --filter name=modernize-run- --format '{{.ID}} {{.Names}}'
```

All final commands exited **0**. Both verifier commands printed the table's
counts, 176 repeat passes, 15 held-out passes, 20 mock calls and 87.5% mutation
detection. Docker cleanup check returned empty output after approved access;
its initial sandboxed check was denied and is not counted as cleanup evidence.
Full-suite output:

```text
Running unit tests
Ran 55 tests in 0.126s
OK (skipped=1)
Running integration tests
Ran 25 tests in 0.378s
OK (skipped=10)
```

**54 unit and 15 integration tests passed**. The existing Python-2-only host
test and ten opt-in CP3 live isolation tests were skipped; their earlier CP2/CP3
proof remains recorded and unchanged. CP5's 443 live runs are separate evidence,
not mislabeled as reruns of the skipped tests. Seven new unit methods include
raw archive recomputation, hand-checkable golden division calibration, validated
mock prompts/assets, exact stream comparisons, bounded flaky feedback, static
denominators and checksum/training-export tampering checks.

### Exit criteria and known gaps

- Legacy-on-legacy: **100%** of non-quarantined cases match across repeated
  fresh containers; every expectation comes from the first recorded execution.
- Coverage target and shortfall: recorded per project before/after collection.
  File-report misses 90% lines because all five successful `build_report` cases
  change timestamps (and unseeded randomness also changes). They are quarantined,
  without normalization or weaker comparisons. Its seven successful-body lines
  remain uncovered by eligible cases; its stable invalid-path case is eligible,
  but there is no held-out successful `build_report` case. The clock mutation
  confirms this limitation. No equivalence claim is made for these paths.
- Quarantine: every excluded input and its three raw outcomes/reason live in
  `file_report/private/file_report-quarantine.json` inside the archive. Other
  projects have explicit empty quarantine reports.
- Mutation threshold: 7/8 detected, with the survivor and its raw comparisons
  retained. Original source and fixtures are unchanged throughout mutation runs.
- Held-out subset: 15 cases selected after coverage feedback, stored separately,
  sealed with all fixture/log hashes and separately verified 15/15. Mutation
  stages use training fixtures only. `export_training` mechanically excludes
  held-out cases and private proposal/oracle logs; later repair must receive that
  exported view. Checksums detect edits, deletions and additions. Read-only file
  modes are additional protection, not encryption against the host account.

Explicit branch coverage excludes comprehensions, Boolean short-circuit and
implicit exception branches; module/main execution is outside function coverage.
No full bytecode-branch-coverage or live-provider-quality claim is made. There
is no clock, whitespace, path or byte/text normalization. Exception tracebacks
are diagnostic locations, excluded from comparison; type/args/message remain
exact. Unsupported external resources and construction requirements must be
flagged, and capture/infrastructure failures stop collection. Details and the
artifact/export contract are in `docs/characterization.md`.

**Checkpoint report:** CP5 is complete with recorded characterization, bounded
coverage feedback, explicit quarantine, mutation sensitivity and a sealed
held-out set. Stop here. CP6 baseline measurement is next.

## Next-session working preference — 2026-11-19

The user reported that individual checkpoints take too long. The assistant
identified avoidable overhead: broader implementation/tests than necessary,
extensive documentation, and repeated builds/checks while refining the work.
Dependency installation and permission requests also contributed to CP4 time.

For subsequent checkpoints:

- Implement the smallest complete scope that meets the current exit criteria.
- Reuse existing infrastructure; avoid extra features and unnecessary abstractions.
- Run focused checks during development, then required final verification once.
  Repeat only when a change, failure or unresolved concern justifies it.
- Keep progress updates and checkpoint reports concise. Record exact required
  evidence without duplicating long transcripts across documents.
- Preserve all required evidence, validation, security boundaries and human gates.

Resume at CP5; CP0–CP4 are passed. CP4 completion commit is `c6d0d04`.
Live API authentication/model behaviour remains unverified: CP4 used intercepted
SDK requests and no paid provider calls. This save does not start CP5 or approve
the CP6/CP11 human gates.

## CP4 completion — 2026-11-19

**Status:** Passed. User authorized this checkpoint with "next". No CP5 input
execution, characterization fixtures, coverage rounds or held-out selection
was implemented. No paid provider request was made.

### Built and decisions

- Extended `src/modernize/llm.py` without changing its existing mock callers:
  validated token usage and response metadata, provider error categories,
  optional schema/timeouts and scripted deterministic mock replies.
- `openai_client.py`: official OpenAI Responses SDK adapter behind that interface.
  Explicit model, JSON-schema requests, no tools, response storage disabled,
  output-token bound, per-attempt I/O timeout and disabled SDK automatic retries.
  Handles connection errors, timeouts, HTTP errors, rate-limit headers, refusals,
  incomplete responses and invalid token metadata.
- `llm_run.py`: deterministic capped retries, sanitized validation-error feedback,
  response/argument validation, private per-call JSONL logs, failure summaries,
  explicit dated Decimal rate cards and independently recomputable accounting.
  Missing usage/cost remains explicitly unknown. Mock usage cannot be labeled as
  provider usage.
- `llm_prompts.py` and `prompts/input_proposals.v1.{txt,schema.json}`: the first
  versioned input-only contract, Pydantic strict schemas, JSON/base64 validation,
  and forbidden expected-output fields. This defines a prompt, not the CP5
  characterization workflow; proposed inputs were not run on corpus code.
- Direct SDK and Pydantic are pinned controller dependencies: OpenAI **3.55.1**,
  Pydantic **2.14.3**; tested HTTPX2 **2.16.2**. No agent framework or new runtime
  image. Model and rates must be supplied explicitly to avoid stale defaults.
- `docs/llm-layer.md` documents setup, contracts, retries, rate accounting,
  secrets, provenance and limitations. No real key was needed or introduced.

### Commands and package evidence

```sh
.venv/bin/python -m pip install openai pydantic
.venv/bin/python -m pip install -e .
.venv/bin/python -m pip wheel --no-deps --wheel-dir artifacts/cp4-wheel .
.venv/bin/python -m pip check
```

Final commands exited **0**. Package downloads/build isolation used approved
network escalation. The initial sandboxed editable installation exited **1**
because setuptools-index DNS/network access was blocked; the approved retry
succeeded. Observed selected outputs:

```text
Successfully installed ... openai-3.55.1 pydantic-2.14.3 ... httpx2-2.16.2 ...
Successfully built legacy-modernize
Successfully installed legacy-modernize-0.1.0
No broken requirements found.
```

Wheel: `artifacts/cp4-wheel/legacy_modernize-0.1.0-py3-none-any.whl`, SHA-256
`245a0043920022f2f2b13cde6fa4f3f8007f34148dfcd369abde94f029dff4f7`.
Used an isolated import from the wheel, not the editable source:

```sh
.venv/bin/python -I - <<'PY'
import sys
from pathlib import Path
import zipfile
wheel = next(Path('artifacts/cp4-wheel').glob('*.whl')).resolve()
with zipfile.ZipFile(wheel) as archive:
    names = archive.namelist()
    assert 'modernize/prompts/input_proposals.v1.txt' in names
    assert 'modernize/prompts/input_proposals.v1.schema.json' in names
sys.path.insert(0, str(wheel))
import modernize
from modernize.llm_prompts import load_prompt
assert str(wheel) in modernize.__file__
assert load_prompt('input_proposals.v1').response_model.__name__ == 'InputProposals'
print('PASS: wheel includes and loads the versioned prompt and schema')
print('Wheel:', wheel.name)
PY
```

Exit **0**, printing the two PASS/wheel lines. Prompt/schema package data was
also verified before the final wheel rebuild; the resource contract is unchanged.

### Final tests and recorded failures/recovery

`.venv/bin/python scripts/test.py` exited **0**, unit suite before integration:

```text
Running unit tests
Ran 48 tests in 0.049s
OK (skipped=1)
Running integration tests
Ran 25 tests in 0.364s
OK (skipped=10)
```

**47 unit and 15 integration tests passed**. The historical host-only Python 2
AST skip remains covered by CP2's recorded worker run; CP3's ten live Docker
methods were not rerun because sandbox implementation/policy did not change.
Their opt-in skips are explicit, not new quarantine or claimed runtime evidence.
All eight new SDK HTTP-transport integration methods ran and passed. No test was
deleted or weakened, and all existing foundation tests remain unchanged.

Independent SDK-only verification also exited **0**:

```sh
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests/integration -p test_openai_sdk.py -v
```

Observed `Ran 8 tests in 0.067s`, `OK`. It uses the real installed SDK and an
intercepted HTTPX2 transport, with generated fake credentials retained only in
memory. Tests check actual Authorization construction, SDK timeout options,
JSON-schema/token/storage/tool options and one HTTP request per logged attempt
despite the injected SDK's default retry setting. DEBUG SDK logs and all run
artifacts are checked for credential leakage.

`docs/evidence/cp4.json` commits the redacted per-attempt SDK fixture records,
mock failure, usage reports, source hashes, dependency versions, wheel identity
and a credential-pattern scan. There are **8 recorded SDK scenarios**, **14
intercepted HTTP attempts**, and **3 deterministic mock failure attempts**.
These are simulated provider responses and tariffs, not live model measurements.

| SDK fixture scenario | Attempts | Known fixture tokens | Known synthetic USD estimate |
|---|---:|---:|---:|
| success | 1 | 120 | 0.00026 |
| malformed failure | 3 | 360 | 0.00078 |
| schema recovery | 2 | 240 | 0.00052 |
| timeout / 429 / success | 3 | 120 | 0.00026 |
| authentication failure | 1 | 0 known; 1 unknown-usage attempt | 0 known; incomplete |
| refusal | 1 | 120 | 0.00026 |
| incomplete response / recovery | 2 | 240 | 0.00052 |
| credential echo redaction | 1 | 120 | 0.00026 |

Totals recomputed from those records: **1320 known fixture tokens**, **0.00286
synthetic estimated USD**, with **3 unknown-usage attempts** (authentication,
timeout, rate limit). **Paid provider calls: 0**. No actual bill or zero-cost
claim is inferred from missing usage; fixture estimates are explicitly separate
from money spent. Failed validation/refusal/incomplete replies are included.

The SDK malformed-response case stops at three failed validations and logs the
error in subsequent prompts. The deterministic mock repeats the same malformed
response three times, produces a final failed summary, and raises cleanly.
Both demonstrate bounded logged failure, rather than accepting invalid output.

`test_llm_evidence.py`, included in the final suite, independently validates
accepted recorded responses and recomputes usage/cost from every attempt. A
masked credential-pattern scan of tracked/unignored repository files and CP4
artifacts found no credential-like values; only file counts, never secret
values, were printed. Known-secret and encoded-log redaction tests passed.

### Exit criteria and limits

| CP4 criterion | Evidence | Result |
|---|---|---|
| Every prompt has schema and mock tests | 1/1 versioned templates; schema equality and mock validation test | Passed |
| Malformed response retries then clean logged failure | Three-attempt mock and intercepted real-SDK failure records | Passed |
| Token and cost usage per run | JSONL-derived reports, dated Decimal rates, completeness flags and independent recomputation | Passed |
| No API key in repository/logs | In-memory fake keys, request/error/response/DEBUG-log tests and masked file scan | Passed |

No live authenticated provider call, current model-quality evaluation or paid
benchmark was run. Users must supply a supported model, credential and verified
tariff before live use. SDK timeouts constrain I/O phases; the retry window is
not a killable hard deadline for arbitrary custom transports. Nonzero cache-write
usage lacks a separate tariff and is reported as unknown cost. Attempt/token
bounds are not a hard prepaid USD cap. No CP5 characterization/coverage or later
stage code generation was performed.

**Checkpoint report:** CP4 is complete with direct provider integration,
versioned/validated prompts, bounded failure handling and traceable accounting.
Stop here; CP5 is next. CP6 and CP11 human gates remain unapproved.

## CP3 completion — 2026-11-19

**Status:** Passed. User authorized the next checkpoint with "next". Stopped at
CP3; no CP4 provider, prompt or test-generation work was performed.

### Built and decisions

- `src/modernize/sandbox.py`: `SandboxRunner.run` for scripts/functions and
  `run_tests` for supplied test scripts, using either configured runtime image.
  Validated resource limits, immutable source/asset snapshots, pinned image
  identities, bounded Docker streams, strict result validation, actual Docker
  state/configuration records and removal on success/failure.
- `sandbox_worker.py`: Python 2/3 supervisor and separate target child. CPU,
  address-space and file-size limits; wall-clock kill; stdout/stderr bytes;
  typed values/exceptions/tracebacks; new/modified scratch files and symlinks.
- `sandbox_codec.py`: explicit input transport and output types. Retains byte
  strings versus text, integer types, list/tuple distinctions and exact streams.
  Canonical mapping/set wire ordering is documented and applied equally to
  both runtimes. Unsupported/cyclic values fail capture, never silently pass.
- No new dependency or image required. Only trusted harness code is bind-mounted,
  read-only; source bytes travel over stdin to disposable tmpfs, never execute
  on the host, and have no writable host mount. Declared image volumes are
  rejected. Docker logging is disabled to avoid container output host log files.
- Non-root UID/GID 65534, all capabilities dropped, no-new-privileges, no external
  network, read-only root, 32-PID bound, one CPU, hard memory/no-extra-swap limits,
  child CPU/address-space limits, 32 MiB scratch and an outer controller deadline.
- Exposed the runner as a Python API; kept the existing analysis CLI and CP2
  evidence unchanged. No full-pipeline command was introduced ahead of CP11.
- `docs/sandbox.md` documents the API, exact schemas, type handling, limits,
  opt-in live tests, capture failures and known boundaries.

### Failure investigated before completion

The initial live suite exited **1**, with four failing Python 2 subtests:
deterministic execution, filesystem, network and timeout. Captured exceptions
identified imported modules such as `os` and `socket` becoming `None` after
Python 2 `runpy` temporary-module teardown. These were harness failures, not
successful isolation evidence. Initial records were retained at
`artifacts/cp3-live-initial-failure.json`.

Fixed the shared function loader to use persistent imports, including package
relative imports, and a retained module for extensionless/pyw inputs. Kept all
original assertions unchanged; added package-import and missing-outcome checks.
Reran live tests after the fix and after disabling Docker logging. No test was
deleted, weakened, quarantined or excluded to make the checkpoint pass.

### Final commands and output

```sh
env MODERNIZE_DOCKER_TESTS=1 python3 scripts/test.py
```

Exited **0**, unit tests before integration tests. Summary (per-test lines and
separators omitted):

```text
Running unit tests
Ran 38 tests in 0.046s
OK (skipped=1)
Running integration tests
Ran 17 tests in 10.792s
OK
```

**37 unit tests and all 17 integration tests passed**, including all ten live
sandbox test methods over both runtimes. The one host skip remains the CP2
Python 2 AST-specific test, already executed successfully in the recorded CP2
legacy worker run. No live sandbox test was skipped in this final command.
Without `MODERNIZE_DOCKER_TESTS=1`, the ten live methods are explicitly skipped;
that default development run is not counted as isolation evidence.

The final live integration tests generated `artifacts/cp3-live.json`; its complete
records are committed in `docs/evidence/cp3.json`. There are **26 actual container
executions**, 13 per runtime. Exact `docker create` arguments, actual limits and
mount write flags, original source hashes, requests, target outcomes, supervisor
errors and container state/removal are recorded for every execution. Images:

- Python 2.7.18: `sha256:981bbf199b2a829c4cfceb54f1e75a1409d4dff7602b64a09c58f08a2fd4e5e5`
- Python 3.12.16: `sha256:c05c4c189eda65dd7dd1d6767f5f9330033c93c81b7a10ba709d837f74b4562c`

These are the images already runtime-verified at CP0. The trusted controller
used approved Docker access; all target execution used the recorded policy.

### Observed security and capture evidence

Every row below was exercised on **both** images; these are controlled sandbox
probes, not characterization tests or modernization pass rates.

| Probe | Recorded result |
|---|---|
| External socket connection to numeric `198.51.100.1:9` | Structured socket/OSError exception, errno 101; actual NetworkMode `none` |
| Infinite CPU loop | Child killed by signal 9 under one-second hard CPU limit; `resource_limit` |
| Sleeping child with 0.2-second wall deadline | `timeout`, child exit -9; partial stdout and pre-timeout file retained |
| 512 MiB allocation under 64 MiB memory/address-space bounds | Structured `MemoryError`; no allocation allowed to succeed |
| Writes to `/outside-cp3`, `/tmp/outside-cp3`, trusted read-only harness mount | All three return errno 30 (`EROFS`) |
| Write to `/scratch/allowed.bin`, then fresh container | Created bytes captured; next run returns typed boolean false for existence |
| Symlink to `/etc/passwd` | Symlink target captured without following it |
| Deterministic callable run twice | Complete result objects identical for each image: typed value, raw streams, files, status and target exit |
| Explicit ValueError | Class/module/typed args/message/traceback captured |
| Unsupported object return | Explicit `capture_error`, never a completed capture |
| Child exits without writing outcome | Protocol failure, result null, supervisor exit 1, container removed |
| Package-relative callable and supplied unittest script | Complete captures under each runtime |

The deterministic probe includes NUL and non-UTF-8 bytes, Unicode text, a tuple,
a dictionary, stderr and a generated binary file. No whitespace, encoding or
type comparison was loosened. Mapping/set canonicalization is described in
`docs/sandbox.md`, with iteration-order observations retained via sequences or
raw output. Docker inspection confirmed memory/no-extra-swap, CPU and PID bounds,
non-root user, no-new-privileges, read-only binds/root and logging driver `none`.

`docker ps -a --filter name=modernize-run- --format '{{.ID}} {{.Names}}'` exited
**0** with empty output at the cleanup recheck. Each final record also confirms
stopped state and successful container removal. No original source changed.

The committed evidence is independently checked without rerunning Docker:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests/unit -p test_sandbox_evidence.py -v
```

It validates capture schemas, source identity, actual isolation fields,
deterministic pair equality and all critical recorded outcomes. This test was
also included in the successful final full-suite command.

### Exit criteria and known limits

| CP3 criterion | Evidence | Result |
|---|---|---|
| Network, runaway loop, memory and filesystem protections proven | Real live tests and Docker inspection on both images | Passed |
| Structured return/exception/stdout/stderr/created files | Codec/worker/validator, binary replay and exception/file probes | Passed |
| Identical captured output for repeated deterministic input | Two complete identical result captures per runtime | Passed |

The runner handles small snapshots (4 MiB), limited captures (1 MiB per stream,
1 MiB aggregate files, 128 file records) and nesting to depth 30. Unsupported,
unreadable or oversized captures are explicit failures; empty directories and
deleted files are not exported. Docker's private loopback/device mounts remain
isolated and ephemeral. This proves the stated probes/policy, not immunity to
all kernel vulnerabilities. Target code shares the supervisor's non-root UID
and may sabotage its own harness; protocol failures never count as valid captures.
Projects shadowing harness-preloaded standard modules require explicit evaluation.

**Checkpoint report:** CP3 is complete with recorded isolation and capture proofs
for both runtimes. Stop here. CP4 is next; no further human gate has been approved.

## CP2 completion — 2026-11-19

**Status:** Passed. User authorization: "approved, start next one" approved CP1
and authorized CP2. No later checkpoint started. No input source, existing test,
fixture or corpus record was changed by CP2.

### Built and decisions

- `src/modernize/analyzer_worker.py`: Python 2.7-compatible, deterministic
  `ast`/`tokenize` extraction of functions (including lambdas), classes,
  signatures, existing docstrings/comments, imports, calls, scoped bindings and
  references, and global-state candidates. It never imports or executes input.
- `src/modernize/analysis.py`: immutable source-byte inventory, a language
  adapter protocol and Python 2 implementation, isolated parser invocation,
  sequential/bounded parallel parsing, import/call graphs, lexical symbol
  merging, alias/shadowing resolution and all seven required side-effect kinds.
  Conversion and execution methods explicitly remain unimplemented for their
  later checkpoints.
- `src/modernize/facts_schema.py`: exact structural schemas and recursive type
  checks, position/enum validation, plus source-path/hash reconciliation at the
  worker boundary. The schema is documented in `docs/analysis-schema.md`.
- CLI `modernize scan`: validated facts and separate run metadata; new output
  directories outside input; explicit parse errors with a saved failure record.
- Standard library only. Kept the existing legacy image, pinned its actual ID
  before each scan, and mounted only trusted parser code read-only. Source bytes
  travel over stdin; project code has no runtime mount and never executes.
- Parallel mode uses at most four containers (128 MiB and one CPU each); output
  ordering is stable. No LLM client/provider is used or imported by analysis.
- Added worker/fact/schema/inventory/scope/CLI/failure/evidence tests. Kept actual
  Python 2 syntax tests compatible with that runtime instead of attempting to
  parse Python 2-only syntax using the controller's Python 3 AST.

### Recorded commands and runtime evidence

Both commands exited **0**:

```sh
.venv/bin/modernize scan corpus --analysis sequential --output artifacts/cp2-final-sequential
.venv/bin/modernize scan corpus --analysis parallel --workers 2 --output artifacts/cp2-final-parallel
```

Configuration and completion events were JSON on stderr. Stdout respectively:

```json
{"files": 7, "output": "/Users/awanishkumar/hornet/sem5/agenticAI/artifacts/cp2-final-sequential/facts.json"}
{"files": 7, "output": "/Users/awanishkumar/hornet/sem5/agenticAI/artifacts/cp2-final-parallel/facts.json"}
```

Each run records seven exit-0 parser invocations and this actual legacy image:
`sha256:981bbf199b2a829c4cfceb54f1e75a1409d4dff7602b64a09c58f08a2fd4e5e5`.
The image's Python 2.7.18 identity was established at CP0 and reused at CP1.
All Docker calls used approved escalation. Early exploratory scans also
succeeded in `artifacts/cp2-sequential` and `artifacts/cp2-parallel`; final
evidence uses only the final runs above, after scope/marker refinements.

`docs/evidence/cp2.json` commits both complete fact sets, both actual run records,
the deliberate syntax-failure record, analyzer hashes and original source
hashes. `artifacts/` contains the original per-command files and remains ignored
by Git. Corpus parsing counts derived from the stored records:

| Project | Parsed / source files |
|---|---|
| golden_ledger | 1 / 1 |
| text_pipeline | 1 / 1 |
| ranking | 1 / 1 |
| file_report | 4 / 4 |
| Total | 7 / 7 (100%) |

Recorded facts contain **17 functions** (including one lambda), **1 class**,
and **75 call sites**, with **20** targets resolved to corpus definitions.
External and dynamic calls remain explicitly unresolved. The complete
sequential and parallel fact objects compare equal, including diagnostics;
only their separate execution records differ. Canonical fact SHA-256:
`17053e9013dde8a61abffcfdf6f0bf6a6af7fb4777b02956abe77546358945f2`.

The following assertion command recomputes the stored schema, source hashes,
all-file inclusion and mode equivalence without invoking Docker:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests/unit -p test_analysis_evidence.py -v
```

It is also included in the complete test command recorded below. The evidence
test additionally checks both run records' successful per-file statuses and
the hashes of the analyzer implementation used to create them.

### Python 2 fact tests and rejection evidence

Executed the worker tests in the real legacy runtime:

```sh
docker run --rm --network none --read-only --user 65534:65534 --cap-drop ALL --security-opt no-new-privileges --memory 128m --cpus 1 --pids-limit 32 --ulimit cpu=10:10 --tmpfs /tmp:rw,nosuid,nodev,size=16m --mount type=bind,source=/Users/awanishkumar/hornet/sem5/agenticAI/src,target=/tool,readonly --mount type=bind,source=/Users/awanishkumar/hornet/sem5/agenticAI/tests/unit/test_analysis_worker.py,target=/tests/test_analysis_worker.py,readonly --env PYTHONPATH=/tool --entrypoint python modernize-legacy:cp0 -B /tests/test_analysis_worker.py
```

Exit **0**:

```text
test_comments_and_encoding ... ok
test_functions_classes_signatures_and_docstrings ... ok
test_global_mutable_markers ... ok
test_imports_calls_scopes_and_references ... ok
test_invalid_source_is_not_skipped ... ok
test_lambda_parameters_have_a_separate_scope ... ok
test_parsing_does_not_execute_code ... ok
test_python2_specific_nodes ... ok
Ran 8 tests in 0.010s
OK
```

Class qualifiers/separators omitted. Fixtures cover encoded comments, tuple
parameters, old exception syntax, signatures, nested definitions, lambda scopes
and a top-level `raise` that parses successfully without execution.

A temporary input `broken.py` contained exactly `def broken(:\n`. Ran:

```sh
.venv/bin/modernize scan /var/folders/27/3g20dbhs1v790k413_hms7p80000gn/T/modernize-cp2-invalid-pbjyowa4 --output artifacts/cp2-invalid
```

Exit **2**, identifying `broken.py`, line 1, and `SyntaxError: invalid syntax`.
`run.json` records the failed parser command and traceback; no partial facts
file was published. This deliberate rejection was investigated and expected;
no corpus file failed parsing or was skipped.

### Full suite

`python3 scripts/test.py` exited **0**, unit tests before integration tests:

```text
Running unit tests
Ran 31 tests in 0.014s
OK (skipped=1)
Running integration tests
Ran 7 tests in 0.293s
OK
```

Thus **30 host unit tests and 7 integration tests passed**. The single host
skip is `test_python2_specific_nodes`: it requires the Python 2 AST and was
executed successfully in the eight-test legacy run above. This is a runtime
placement decision, not a quarantined corpus case. Schema rejection, all fact
types, all side-effect kinds, scopes/shadowing, relative/re-export imports,
sequential/parallel equality, timeout cleanup, and output protection are tested.

### Exit criteria and known limits

| CP2 exit criterion | Evidence | Result |
|---|---|---|
| 100% of corpus files parse; failures investigated | 7/7 in both real Docker scans; explicit malformed-file rejection | Passed |
| Documented schema, automatically validated | `facts_schema.py`, `docs/analysis-schema.md`, response and merged-fact checks | Passed |
| Unit tests for every fact type | Worker and controller tests; eight worker tests also pass in Python 2.7 | Passed |
| No LLM in the stage | Pure AST/tokenize worker, deterministic controller, no AI dependency/calls | Passed |

Call targets and side-effect markers are approximate; reflective code, wildcard
imports, receiver types, arbitrary alias mutation and external consumers remain
unresolved. Unsupported assets and exclusions are reported; symlinks are rejected.
The 16 MiB snapshot bound and four-worker bound are documented. Parsing smoke
isolation does not establish CP3's runtime-capture or adversarial isolation
requirements. No modernization or behavioural-equivalence result is claimed.

**Checkpoint report:** CP2 is complete with committed facts, reproducible schema
and hash checks, and actual Python 2 parsing evidence. Stop at CP2. CP3 is next;
CP6 and CP11 human gates remain unapproved.

## CP1 approval — 2026-11-19

The user explicitly approved corpus commit `a34ea73`: "approved, start next one".
All CP1 technical exit criteria were already recorded below; CP1 is now passed.
This supersedes its pending-approval status. CP2 is authorized; later human gates
remain unapproved.

## CP1 corpus ready for approval — 2026-11-19

**Status:** Awaiting human approval. All technical exit criteria are met; the
required corpus approval is outstanding. This entry supersedes earlier notes
that CP1 has not started. CP0 remains passed (commit `9c4c66d`).

### Built and decisions

- Four original Python 2.7 projects, seven Python source files, under `corpus/`:
  `golden_ledger`, `text_pipeline`, `ranking`, and the multi-module `file_report`.
- `corpus/LICENSE` grants MIT permission for all four projects;
  `corpus/manifest.json` records each project's source provenance, license,
  entry point, golden status, and migration hazards. No upstream downloads or
  dependencies were needed.
- `corpus/README.md` contains the required hazard matrix, golden-project hand
  review, reproduction command, and limitations. Original projects were chosen
  to keep licensing explicit and review manageable, as CP1 permits.
- `corpus/evidence/cp1-runs.json` preserves actual run output, exit codes, exact
  Docker commands, source SHA-256 hashes, and image identity. These records are
  smoke evidence, not CP5 characterization fixtures or CP6 baseline metrics.
- Two new corpus unit checks verify inventory/provenance/hazard metadata and
  that every project's successful execution record matches its current source
  hashes. Existing source, tests, and fixtures were not weakened or changed.
- Used the existing CP0 image with read-only source, no network, non-root UID,
  resource limits, and disposable `/tmp`; no legacy code executed on the host.
  No reusable CP3 runner or later-checkpoint functionality was implemented.

### Commands and results

Executed the following command separately for each project, with `PROJECT`
replaced by its directory name. The four exact expanded commands and outputs
are saved in `corpus/evidence/cp1-runs.json`:

```sh
docker run --rm --network none --read-only --cap-drop ALL --security-opt no-new-privileges --memory 128m --cpus 1 --pids-limit 64 --ulimit cpu=10:10 --tmpfs /tmp:rw,nosuid,nodev,size=16m --mount type=bind,source=/Users/awanishkumar/hornet/sem5/agenticAI/corpus,target=/corpus,readonly --workdir /tmp --entrypoint python modernize-legacy:cp0 -B /corpus/PROJECT/main.py
```

Every project exited **0**. Captured output:

```text
golden_ledger:
split: 3 -4
total: 5
empty: 0
parsed: 12
bad: invalid: invalid literal for int() with base 10: 'bad'

text_pipeline:
names: [u'Ada', u'Lin']
pairs: (2, [(0, u'Ada'), (1, u'Lin')])
empty: (0, [])
encoded: 'caf\xc3\xa9'
decoded: u'caf\xe9'
types: ('str', 'unicode', 5, 4)

ranking:
empty: []
ranked: [('ada', 7), ('Bob', 7), ('Lin', 3)]
equal: 0

file_report:
{'count': 3, 'ticket': 391, 'created_at': 1795086746.297066, 'mean': 1}
```

`docker image inspect --format '{{.Id}} {{.Os}}/{{.Architecture}} user={{.Config.User}}' modernize-legacy:cp0`
exited **0**:

```text
sha256:981bbf199b2a829c4cfceb54f1e75a1409d4dff7602b64a09c58f08a2fd4e5e5 linux/arm64 user=65534:65534
```

This is the Python 2.7.18 image verified at CP0. Approved Docker escalation was
used for the four runs and image inspection.

`python3 scripts/test.py` exited **0**, unit suite before integration suite:

```text
Running unit tests
Ran 10 tests in 0.004s
OK
Running integration tests
Ran 7 tests in 0.254s
OK
```

Summary omits per-test lines. Both new checks passed:
`test_inventory_has_provenance_and_all_required_hazards` and
`test_every_project_has_successful_evidence_for_current_sources`.
The suite reads corpus bytes and JSON only; Python 2 source is not imported or
parsed by the host Python 3 interpreter.

### Exit criteria and known gaps

| CP1 exit criterion | Evidence | Status |
|---|---|---|
| Every project runs under Python 2.7 | Four exit-0 records with source hashes and CP0 image ID | Met |
| Coverage matrix for all migration hazards | `corpus/README.md`, with matching manifest hazard identifiers | Met |
| Small hand-checkable golden project | `golden_ledger/main.py` and observed output/explanation | Met |
| Human approves corpus | No approval received yet | Pending |

The corpus is synthetic; smoke runs do not establish branch coverage or
general migration quality. `file_report` deliberately uses wall-clock time;
its default seed also permits randomness. Normalization/quarantine belongs to
CP5 and is not silently applied here. No held-out set, mutation results,
modern-runtime baseline, or full sandbox-isolation proof is claimed.

**Checkpoint report:** CP1 is ready for review and committed for inspection;
it remains incomplete until the user approves this specific corpus. Stop here
under the CP1 human gate; do not begin CP2.

## CP0 completion — 2026-11-19

**Status:** Passed; stop at this checkpoint. This entry supersedes historical
Docker/Git blockers, pending test-boundary questions, and missing-suite notes
below. Existing tests were neither edited nor weakened. No CP1 work performed.

### Built and decisions

- Existing package/CLI, strict JSON configuration, structured stderr logging,
  LLM protocol and deterministic mock, both Dockerfiles, smoke script, and
  unit-before-integration test runner satisfy the CP0 scope without source changes.
- Installed the package in a project-local virtual environment, keeping the
  controller's global Python environment unchanged. Only the setuptools build
  dependency was required; there are no runtime dependencies.
- Updated README setup/status and the project-plan status. No agent framework,
  provider integration, analyzer, or corpus added.
- Sandbox denied Docker socket access, network access for pip, and `.git`
  creation. Used explicit approved escalation for those operations. Image builds
  download base images; container execution uses no network or host mounts.

### Exact commands and observed evidence

`python3 scripts/test.py` exited **0**, running unit tests first:

```text
Running unit tests
test_defaults (test_foundation.ConfigurationTests.test_defaults) ... ok
test_invalid_documents_are_rejected (test_foundation.ConfigurationTests.test_invalid_documents_are_rejected) ... ok
test_missing_file_is_rejected (test_foundation.ConfigurationTests.test_missing_file_is_rejected) ... ok
test_overrides_preserve_other_defaults (test_foundation.ConfigurationTests.test_overrides_preserve_other_defaults) ... ok
test_configuration_filters_level_and_does_not_duplicate_events (test_foundation.LoggingTests.test_configuration_filters_level_and_does_not_duplicate_events) ... ok
test_formatter_preserves_message_as_json (test_foundation.LoggingTests.test_formatter_preserves_message_as_json) ... ok
test_custom_response (test_foundation.MockClientTests.test_custom_response) ... ok
test_interface_returns_deterministic_response (test_foundation.MockClientTests.test_interface_returns_deterministic_response) ... ok
Ran 8 tests in 0.003s
OK
Running integration tests
test_config_stdout_and_structured_stderr (test_cli.CLITests.test_config_stdout_and_structured_stderr) ... ok
test_help_and_version (test_cli.CLITests.test_help_and_version) ... ok
test_invalid_config_and_missing_command (test_cli.CLITests.test_invalid_config_and_missing_command) ... ok
test_actual_integration_failure_returns_nonzero (test_runner.RunnerTests.test_actual_integration_failure_returns_nonzero) ... ok
test_actual_unit_failure_stops_integration (test_runner.RunnerTests.test_actual_unit_failure_stops_integration) ... ok
test_empty_suite_is_not_success (test_runner.RunnerTests.test_empty_suite_is_not_success) ... ok
test_runs_unit_before_integration (test_runner.RunnerTests.test_runs_unit_before_integration) ... ok
Ran 7 tests in 0.247s
OK
```

Blank separators omitted. Runner integration tests execute actual failing probe
tests in temporary copies, assert exit **1** and `FAILED (failures=1)`, and prove
unit failure prevents integration execution; empty-suite rejection asserts exit
**2**. Mock interface and repeated deterministic responses are covered in
`tests/unit/test_foundation.py`.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/modernize --version
.venv/bin/modernize --config config.example.json config
.venv/bin/python -m pip check
```

All final commands exited **0**. Initial sandboxed pip attempt exited **1** with
DNS/network errors fetching setuptools; approved retry succeeded. Selected pip
output:

```text
Successfully built legacy-modernize
Successfully installed legacy-modernize-0.1.0
```

Installed version output: `modernize 0.1.0`. Configuration stdout:

```json
{"legacy_image": "modernize-legacy:cp0", "log_level": "INFO", "modern_image": "modernize-modern:cp0"}
```

Configuration stderr:

```json
{"timestamp": "2026-11-19T11:08:48.273242+00:00", "level": "INFO", "logger": "modernize", "message": "configuration_loaded"}
```

`pip check` printed `No broken requirements found.` plus a sandbox cache warning;
it required no escalation.

```sh
docker build -f containers/legacy.Dockerfile -t modernize-legacy:cp0 .
docker build -f containers/modern.Dockerfile -t modernize-modern:cp0 .
```

Both exited **0**. Build output ended with image naming/unpacking and `DONE`.
Resolved base image manifest digests recorded in build output:

- `python:2.7.18-slim@sha256:6c1ffdff499e29ea663e6e67c9b6b9a3b401d554d2c9f061f9a45344e3992363`
- `python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b`

```sh
docker run --rm --network none --read-only --cap-drop ALL --security-opt no-new-privileges --memory 128m --cpus 1 --pids-limit 64 --tmpfs /tmp modernize-legacy:cp0
docker run --rm --network none --read-only --cap-drop ALL --security-opt no-new-privileges --memory 128m --cpus 1 --pids-limit 64 --tmpfs /tmp modernize-modern:cp0
```

Both exited **0**, with the respective stdout:

```json
{"message": "runtime ready", "python": "2.7.18 (default, Apr 20 2020, 19:49:40) \n[GCC 8.3.0]"}
{"message": "runtime ready", "python": "3.12.16 (main, Nov  5 2026, 08:06:14) [GCC 14.2.0]"}
```

```sh
docker image inspect --format '{{.RepoTags}} {{.Id}} {{.Os}}/{{.Architecture}} user={{.Config.User}}' modernize-legacy:cp0 modernize-modern:cp0
```

Exited **0**:

```text
[modernize-legacy:cp0] sha256:981bbf199b2a829c4cfceb54f1e75a1409d4dff7602b64a09c58f08a2fd4e5e5 linux/arm64 user=65534:65534
[modernize-modern:cp0] sha256:c05c4c189eda65dd7dd1d6767f5f9330033c93c81b7a10ba709d837f74b4562c linux/arm64 user=65534:65534
```

`git status --short` initially exited **128** (not a Git repository).
`git init` initially exited **1** (`Operation not permitted`); approved retry
exited **0** and printed `Initialized empty Git repository in
/Users/awanishkumar/hornet/sem5/agenticAI/.git/`. Subsequent `git status --short`
exited **0**, listing the existing project files as untracked.

### Exit-criteria reconciliation and limits

| CP0 criterion | Evidence | Result |
|---|---|---|
| Both containers start and execute a trivial script with versions | Smoke runs above: Python 2.7.18 / 3.12.16, exit 0 | Passed |
| LLM interface, mock, and unit test | `src/modernize/llm.py`; both MockClientTests pass | Passed |
| One command runs all tests and exits nonzero on failure | `python3 scripts/test.py`; runner tests prove failure propagation | Passed |
| PROGRESS.md records CP0 | This dated entry and prior implementation evidence | Passed |

Package installation and structured CLI output are also verified. Runtime image
tags remain mutable; exact identities above describe this run, not future pulls.
Smoke checks do not prove CP3 isolation requirements. The language adapter,
artifact persistence, and real provider remain scheduled for their relevant
later stages; no defaults are replaced. GSD supplemental workflows still lack
their planning-phase prerequisites and are not claimed as run or passed.

**Checkpoint report:** CP0 foundation is complete with recorded runtime and test
evidence. CP1 is next and requires corpus approval; no human gate is approved.

## CP0 Docker access recheck — 2026-11-19

- User reported Docker running and requested completion of pending CP0 work.
- Re-read checkpoint rules, current progress, package metadata, README, and image
  definitions. No source or test changes required by this recheck.
- `docker version` exited **1**. Client version `29.7.2`, API `1.55`,
  context `desktop-linux`; server could not be queried:

  ```text
  permission denied while trying to connect to the docker API at unix:///Users/awanishkumar/.docker/run/docker.sock
  ```

- This supersedes the previous missing-socket observation. Docker may be running;
  the active execution environment cannot connect to its socket. No container
  build, container run, or image identity is claimed.
- `git status --short` exited **128**:

  ```text
  fatal: not a git repository (or any of the parent directories): .git
  ```

- Current workspace policy prevents writing `.git` and disallows sandbox
  escalation. No alternate endpoint, permission change, or sandbox bypass was
  attempted. Package installation and container versions remain unverified;
  tests were not rerun because no implementation changed.
- **Next:** Resume CP0 in an execution environment permitted to access Docker's
  socket and write Git metadata. Build/run both images using the README commands,
  record actual Python versions and image identities, verify package installation,
  and create the CP0 commit. Keep CP0 incomplete until runtime evidence exists.
  CP1 has not started; no human gate is approved.

## CP0 autonomous continuation — 2026-11-19

- **Status:** In progress; CP1 not started. Container version evidence is still
  missing, so CP0 has not passed.
- **Authorization:** User asked to proceed independently after being told the
  outstanding CP0 work. This resolves the previous routine test-boundary pause;
  it does not approve any later human gate. Earlier pending-approval entries
  below are historical.
- **Built:** `tests/unit/test_foundation.py` covers configuration defaults,
  overrides, malformed inputs and missing files, the deterministic mock through
  the LLM client interface, JSON formatting, log filtering and repeated setup.
  `tests/integration/test_cli.py` exercises the CLI in subprocesses.
  `tests/integration/test_runner.py` copies the runner into temporary directories
  and proves unit-before-integration order, unit fail-fast behavior, actual
  integration failure exit status, and empty-suite rejection. Intentionally
  failing probe tests exist only in temporary directories; no project test was
  weakened or removed. Updated README test instructions.
- **Decision:** Use standard-library unittest and subprocesses; no new dependency,
  production-source change, later-stage feature, or external service required.

### Recorded commands and results

`python3 scripts/test.py` exited **0**:

```text
Running unit tests
test_defaults ... ok
test_invalid_documents_are_rejected ... ok
test_missing_file_is_rejected ... ok
test_overrides_preserve_other_defaults ... ok
test_configuration_filters_level_and_does_not_duplicate_events ... ok
test_formatter_preserves_message_as_json ... ok
test_custom_response ... ok
test_interface_returns_deterministic_response ... ok
Ran 8 tests in 0.003s
OK
Running integration tests
test_config_stdout_and_structured_stderr ... ok
test_help_and_version ... ok
test_invalid_config_and_missing_command ... ok
test_actual_integration_failure_returns_nonzero ... ok
test_actual_unit_failure_stops_integration ... ok
test_empty_suite_is_not_success ... ok
test_runs_unit_before_integration ... ok
Ran 7 tests in 0.251s
OK
```

Above, unittest class/module qualifiers and separator lines are omitted for
readability. Passing runner checks assert exit 1 and `FAILED (failures=1)` from
actual failing probes; the unit failure check also asserts integration did not
start. Empty-suite check asserts exit 2.

`docker version` exited **1**; client version `29.7.2`, context `desktop-linux`:

```text
failed to connect to the docker API at unix:///Users/awanishkumar/.docker/run/docker.sock; check if the path is correct and if the daemon is running: dial unix /Users/awanishkumar/.docker/run/docker.sock: connect: no such file or directory
```

`git status --short` exited **128**:

```text
fatal: not a git repository (or any of the parent directories): .git
```

`git init` exited **1**:

```text
/Users/awanishkumar/hornet/sem5/agenticAI/.git: Operation not permitted
```

`python3 -m pip --version` exited **0**:

```text
pip 26.0.1 from /Users/awanishkumar/.pyenv/versions/3.12.0/lib/python3.12/site-packages/pip (python 3.12)
```

`python3 -c 'import setuptools; print(setuptools.__version__)'` exited **1**
with `ModuleNotFoundError: No module named 'setuptools'`. Package installation
is unverified; no packages installed or downloaded.

### CP0 exit-criteria review and next action

- LLM interface, deterministic mock, and a unit test using it: satisfied.
- One command runs both suites and propagates actual test failure: satisfied.
- Progress record: satisfied.
- Both containers start and print Python 2.7/3.12 versions: **not satisfied**.
- Git checkpoint commit: blocked by filesystem permissions.

Start Docker Desktop and make its daemon reachable, then build and run the two
images with the README commands and record their actual version output and image
identities. Verify package installation when build dependencies are available.
Initialize Git in a writable environment for the required CP0 commit. Reconcile
all CP0 criteria and issue its checkpoint report before starting CP1. No human
checkpoint gate has been approved by this continuation.

## CP0 continuation check — 2026-11-19

- Read `AGENTS.md`, this progress log, `PROJECT_PLAN.md`, all existing CP0
  source files, the test runner, package metadata, image definitions, and README.
  No file named `PROGRESS_PLAN` was found; `PROJECT_PLAN.md` is the existing plan.
- CP0 remains the next checkpoint. No later checkpoint was started.
- The previously invoked TDD skill explicitly requires confirmed public test
  boundaries. Requested confirmation for configuration validation, deterministic
  LLM mock responses, JSON logging, CLI subprocess behavior, and runner failure
  exits. Confirmation is pending; no test files were written.
- `docker version` exited 1: client `29.7.2`, context `desktop-linux`, missing
  `/Users/awanishkumar/.docker/run/docker.sock`. Requested that the user start
  Docker Desktop; neither image was built or run.
- `python3 --version` exited 0: `Python 3.12.0`.
- `python3 -m compileall -q src scripts containers` exited 0 with no output.
- `PYTHONPATH=src python3 -m modernize --config config.example.json config`
  exited 0, printed the expected three configuration fields, and emitted a JSON
  `configuration_loaded` event. This is a manual preflight, not a test suite.
- `python3 scripts/test.py` exited 2:
  `Missing unit suite: /Users/awanishkumar/hornet/sem5/agenticAI/tests/unit`.
  No passing tests or actual failing-test propagation are claimed.
- `git status --short` exited 128: `fatal: not a git repository (or any of the
  parent directories): .git`. No commit could be created.
- **Next:** With boundary confirmation, implement unit tests before integration
  tests and prove actual test-failure exit propagation. Verify both runtime
  images once Docker is available. CP0 remains incomplete.

## Latest save — 2026-11-19

- Saved at the user's request after the CP0 resumption below. This save changes
  only `PROGRESS.md`; no implementation, tests, or container runs were performed.
- CP0 remains incomplete. The request to save progress does not approve test
  boundaries or any human checkpoint gate.
- Resume with configuration, mock LLM, JSON logging, CLI subprocess, and runner
  failure-status tests once their pending boundary confirmation is resolved.
- Docker remains unavailable from the last check; verify daemon access before
  building and running both images. Package installation remains unverified.
- Preserve all previous evidence below. Do not start CP1 until CP0 passes.

## CP0 resumption — 2026-11-19

- **Status:** In progress; no checkpoint passed and no later checkpoint started.
- Read the rules, handoff, source, runner, package metadata, and image definitions.
  No implementation or test files changed in this resumption.
- Requested confirmation of public test boundaries: configuration loading,
  deterministic LLM mock, JSON logging, CLI subprocess behavior, and test-runner
  failure status. The prior TDD approval remains unresolved; a fresh asynchronous
  question was sent. No tests were written while that question was pending.
- `python3 --version` returned `Python 3.12.0`.
- `git status --short` again failed with `fatal: not a git repository (or any of
  the parent directories): .git`; no commit could be made.
- `docker version` returned client `29.7.2`, context `desktop-linux`, then failed
  because `/Users/awanishkumar/.docker/run/docker.sock` does not exist.
  `docker context ls` lists `default` and `desktop-linux`; this does not establish
  a working daemon. Neither image was built or run.
- `docker desktop status` could not create its log file under
  `~/Library/Containers/com.docker.docker/Data/log/host` (`operation not permitted`)
  and did not return promptly. Docker Desktop status was not established.
- `PYTHONPATH=src python3 -m modernize --config config.example.json config`
  exited 0, printed the three expected configuration fields and emitted the JSON
  `configuration_loaded` event. This remains a manual preflight, not a test suite.
- `python3 scripts/test.py` exited 2 with
  `Missing unit suite: /Users/awanishkumar/hornet/sem5/agenticAI/tests/unit`.
  This is not evidence of failure propagation from an actual failing test.
- `python3 -m pip --version` returned `pip 26.0.1` for Python 3.12.
  `python3 -c 'import setuptools; print(setuptools.__version__)'` exited 1 with
  `ModuleNotFoundError: No module named 'setuptools'`. Package installation is
  still unverified; no package downloads or host environment changes attempted.
- **Next:** Obtain test-boundary confirmation and implement/run CP0 tests in
  unit-before-integration order. Docker Desktop must be running and accessible
  before the required two-runtime evidence can be collected. GSD completed-phase
  workflows remain inapplicable without their phase artifacts; none fabricated.

## Requested architecture documentation

**Status:** LaTeX source complete; source checks passed; PDF rendering unverified.

Created `docs/project-architecture.tex` in response to the user's explicit request
for diagrams of the entire planned architecture and explanations understandable
to a nontechnical reader. This is design documentation, not implementation of
CP7's documentation-generation stage. No pipeline implementation was started.

The self-contained document contains nine sections and six TikZ diagrams:

1. End-to-end project workflow.
2. Components, orchestration, and shared services.
3. Plain-language component guide.
4. Original, baseline, and converted execution evidence.
5. Sandbox boundaries and the separate AI provider connection.
6. AI validation, bounded repair, checksums, and sealed held-out tests.
7. CP0–CP12 roadmap and human approval gates.
8. An explicitly illustrative division example and glossary.
9. Build instructions, reading guide, scope, and design choices still open.

### Decisions and limits

- Treat all architecture components as planned because no implementation exists.
- Use standard LaTeX/TikZ without external assets; no new toolchain was installed.
- Document Python 2.7 to Python 3.12 only; Java/PHP remain future adapters and
  CP12 remains optional after CP11 approval.
- Keep the execution sandbox's network ban distinct from the trusted AI client's
  provider connection. Only the trusted controller writes collected artifacts.
- Explain that matching recorded tests does not prove equivalence for all inputs.
- No measurements, runtime proofs, pass rates, or checkpoint passes are claimed.
- No commit was possible because this directory is not a Git repository.

### Verification evidence

Environment commands:

```sh
python3 --version
command -v pdflatex
command -v tectonic
command -v latexmk
command -v lualatex
```

Observed: `Python 3.12.0`; none of the four compiler commands returned a path.
The LaTeX source has **not** been compiled or visually inspected as a PDF.

Source-check command (run from the repository root):

```sh
python3 - <<'PY'
from pathlib import Path
import re
source = Path('docs/project-architecture.tex')
text = source.read_text()
assert text.isascii(), 'Keep source portable with ASCII text and LaTeX escapes'
clean = re.sub(r'(?<!\\)%[^\n]*', '', text)
environments = []
for match in re.finditer(r'\\(begin|end)\{([^}]+)\}', clean):
    kind, name = match.groups()
    if kind == 'begin':
        environments.append(name)
    else:
        assert environments and environments.pop() == name, f'Environment mismatch: {name}'
assert not environments, environments
braces = []
for match in re.finditer(r'(?<!\\)[{}]', clean):
    if match.group() == '{':
        braces.append(match.start())
    else:
        assert braces, f'Unmatched closing brace at {match.start()}'
        braces.pop()
assert not braces, 'Unclosed braces'
headings = re.findall(r'\\pageheading\{([^}]+)\}', text)
assert len(headings) == 9, headings
assert len(re.findall(r'\\newpage\b', text)) == 8
assert len(re.findall(r'\\begin\{tikzpicture\}', text)) == 6
for cp in range(13):
    assert re.search(rf'\bCP{cp}\b', text), f'Missing CP{cp}'
assert not re.search(r'\\(?:includegraphics|input|include)\s*\{', text)
for picture in re.findall(r'\\begin\{tikzpicture\}(.*?)\\end\{tikzpicture\}', text, re.S):
    names = re.findall(r'\\node(?:\[[^\]]*\])?\s*\(([^)]+)\)', picture)
    assert len(names) == len(set(names)), 'Duplicate diagram node name'
print(f'PASS: {source} ({len(text.splitlines())} lines)')
print('PASS: balanced braces and matching LaTeX environments')
print('PASS: 9 sections, 8 explicit page breaks, 6 TikZ diagrams')
print('PASS: CP0-CP12 covered; diagram node names unique; no external assets')
print('LIMIT: source checks only; PDF compilation and visual layout not verified')
PY
```

Output:

```text
PASS: docs/project-architecture.tex (547 lines)
PASS: balanced braces and matching LaTeX environments
PASS: 9 sections, 8 explicit page breaks, 6 TikZ diagrams
PASS: CP0-CP12 covered; diagram node names unique; no external assets
LIMIT: source checks only; PDF compilation and visual layout not verified
```

To render with a LaTeX installation, run twice:

```sh
pdflatex -halt-on-error -output-directory=docs docs/project-architecture.tex
```

Expected PDF path: `docs/project-architecture.pdf`. This path is an intended
build output, not an existing artifact.

## CLI approach and implementation plan

- **Date:** 2026-11-18
- **Status:** Documentation complete; CP0 remains not started.
- **Artifact:** `PROJECT_PLAN.md`.
- **Scope:** Whole-codebase inventory; sequential and bounded parallel analysis;
  shared dependency/symbol facts; coordinated source generation and changes
  across files; CLI examples; stack options; CP0–CP11 implementation roadmap.
- **Decision:** Keep migration repairs behaviour-preserving. Document the user's
  requested existing-bug correction as a separate post-foundation extension
  using specified intended behaviour and independent regression tests. Preserve
  original fixtures and report intentional baseline differences explicitly.
- **Decision:** LangGraph remains proposed and LangChain optional; adopting them
  requires a written justification against the direct-SDK default. No framework
  was installed or selected by this documentation task.
- **Limits:** No CLI, parser, parallel worker, converter, or repair behaviour was
  implemented or benchmarked. Dynamic references and external callers remain
  explicit limitations. No checkpoint passed and no human gate was advanced.
- **Commit:** Unavailable; the workspace is not a Git repository.

Verification command:

````sh
python3 - <<'PY'
from pathlib import Path
import re
p = Path('PROJECT_PLAN.md')
s = p.read_text()
assert s.count('```') == 4, 'Unbalanced Markdown fences'
assert len(re.findall(r'^\| CP\d+:', s, re.M)) == 12
for term in ('sequential', 'parallel', 'CLI', 'scoped symbol', 'shared variable', 'working copy', 'checksum', 'held-out', 'corrective', 'not implemented yet'):
    assert term in s, term
for target in re.findall(r'\]\(([^)]+)\)', s):
    assert (p.parent / target).is_file(), target
assert Path('AGENTS.md').is_file()
print('PASS: PROJECT_PLAN.md; required topics present; CP0-CP11 rows present')
print('PASS: Markdown fences balanced; local document links resolve')
print('LIMIT: documentation checks only; proposed commands are not implemented')
PY
````

Output:

```text
PASS: PROJECT_PLAN.md; required topics present; CP0-CP11 rows present
PASS: Markdown fences balanced; local document links resolve
LIMIT: documentation checks only; proposed commands are not implemented
```

## CP0 implementation session

- **Date:** 2026-11-18
- **Status:** In progress; exit criteria not met. CP1 not started.
- **Built:** `pyproject.toml` package and console entry point; `src/modernize/`
  CLI, strict JSON configuration, structured logging, AI client protocol and
  deterministic mock; both Dockerfiles and compatible smoke script;
  `scripts/test.py` with unit-before-integration order, fail-fast behaviour,
  and nonzero empty-suite exit; example configuration; setup README.
- **Decisions:** Standard-library runtime dependencies for CP0. Direct SDK
  default retained; no agent framework installed. No later-stage implementation.
  No source from an input legacy project is executed on the host.
- **Tests:** No test files written or passing tests claimed. Matt Pocock TDD
  requires confirmation of public testing boundaries before writing tests;
  an asynchronous approval request is pending. GSD add-tests requires a completed
  phase and its SUMMARY; these prerequisites do not exist yet. It has not been
  represented as executed. Use its classification/test-plan approvals when the
  completed-phase workflow becomes applicable.
- **Proposed boundaries:** configuration loading, deterministic AI mock, JSON
  log formatter (unit), CLI subprocess behaviour (integration), then real Docker
  runtime smoke checks. No browser tests for the CLI.
- **GSD UAT:** `gsd-sdk query audit-uat --raw` exited 1:
  `Error: No phases directory found in planning directory`. This is a blocked
  audit, not evidence that UAT has passed. No GSD workflow artifacts fabricated.
- **Docker:** `docker version` showed client 29.7.2, API 1.55, darwin/arm64,
  context desktop-linux, then failed to connect to
  `unix:///Users/awanishkumar/.docker/run/docker.sock` because the socket does
  not exist. Neither image has been built or started. CP0 cannot pass until
  actual Python 2.7 and 3.12 output is recorded from the containers.
- **Git:** `git status --short` returned `fatal: not a git repository (or any
of the parent directories): .git`; no commit created.

Manual preflight commands (not a unit/integration test suite):

```sh
python3 -m compileall -q src scripts containers
PYTHONPATH=src python3 -m modernize --config config.example.json config
PYTHONPATH=src python3 -m modernize --help
python3 scripts/test.py
```

Observed: compilation emitted no errors; configuration printed
`{"legacy_image": "modernize-legacy:cp0", "log_level": "INFO", "modern_image": "modernize-modern:cp0"}`
and a JSON `configuration_loaded` event on stderr. Help listed `config`,
`--config`, `--version`, and `--help`. The suite command exited 2 with
`Missing unit suite: /Users/awanishkumar/hornet/sem5/agenticAI/tests/unit`.
The runner therefore does not claim success when tests have not been written.

Remaining: approved test boundaries, unit tests followed by CLI integration
tests, verified nonzero test-failure propagation, actual container build/run
evidence, completed-phase GSD supplemental test workflow and UAT audit.

## Next-session handoff — 2026-11-19

### Current state

CP0 is partially implemented. No required checkpoint has passed; CP1–CP11 have
not started. The CLI foundation is not an end-to-end modernization prototype.
The user requested this handoff; no additional coding was requested this turn.

Existing implementation:

- `src/modernize/cli.py`, `__main__.py`, and `__init__.py`: CLI entry points,
  help, version, and configuration command.
- `src/modernize/config.py`: strict JSON configuration loading and validation.
- `src/modernize/logging.py`: structured JSON logging.
- `src/modernize/llm.py`: client interface and deterministic mock; no real provider.
- `pyproject.toml`, `config.example.json`, and `README.md`: package setup,
  settings example, and local usage instructions.
- `containers/legacy.Dockerfile`, `containers/modern.Dockerfile`, and
  `containers/smoke.py`: environment definitions only; build/run unverified.
- `scripts/test.py`: unit-before-integration runner; no test suites exist yet.
- `PROJECT_PLAN.md` and `docs/project-architecture.tex`: design documents.
  LaTeX source checks passed previously; no PDF compilation was performed.

Whole-codebase scanning, sequential/parallel analysis, dependency resolution,
safe execution runner, characterization, conversion, coordinated cross-file
repairs, and generated evidence reports remain unimplemented. LangChain and
LangGraph were discussed as options, not installed or adopted.

### User requirements to carry forward

- CLI only; scan the entire input codebase, with sequential and bounded parallel
  analysis modes and a shared project-wide dependency/symbol map.
- Coordinate changes across definitions, imports, callers, variable references,
  and affected logic. Resolve symbols by scope; avoid global text replacement.
- Generate source repairs and needed helper code in a working copy.
- Preserve behaviour in modernization. The requested existing-bug correction
  extension is separately documented in `PROJECT_PLAN.md`; retain original
  baselines and label intended behaviour changes explicitly.
- Run unit tests first, integration tests afterward. User invoked Ponytail,
  Matt Pocock skills, `gsd-add-tests`, and `gsd-audit-uat`.

### Open prerequisites and resumption order

1. Re-read `AGENTS.md`, this handoff, and the current implementation.
2. Resolve the still-unanswered testing-boundary confirmation required by the
   Matt Pocock TDD skill. Proposed unit boundaries: configuration loader, mock
   AI client, JSON log formatter. Integration boundary: CLI subprocess behaviour.
   Later status questions and this save request did not approve these boundaries.
3. Write meaningful tests at the confirmed boundaries. Run unit tests, then CLI
   integration tests; demonstrate that actual failing tests propagate nonzero
   exit status. Record exact commands and outputs; do not claim empty-suite
   failure as proof of failure propagation from an actual test.
4. Recheck Docker availability. Last check on 2026-11-18 found the client but no
   daemon socket. Build and run both images, recording actual Python versions.
5. Reconcile CP0 against every exit criterion before marking it passed. Record
   remaining gaps honestly, including package installation verification if needed.
6. Apply GSD workflows when prerequisites exist: `gsd-add-tests` requires a
   completed phase and SUMMARY; the UAT audit requires planning phase records.
   Do not manufacture completion artifacts to bypass these requirements.
7. End CP0 with its checkpoint report. Start CP1 only after CP0 passes; corpus
   approval at CP1 is a separate human gate.

Last environment observations: no Git repository was present, no Docker daemon
was reachable, and no LaTeX compiler was available. Recheck before treating those
as current blockers. The file `PRO` exists but its purpose has not been inspected;
leave it intact.

### Handoff evidence

On 2026-11-19, read `AGENTS.md` and `PROGRESS.md`, then ran:

```sh
rg --files --hidden -g '!.git/**' -g '!**/__pycache__/**'
```

Observed the source, container definitions, runner, and documents listed above;
no `tests/` or `.planning/` files appeared. This handoff changes only
`PROGRESS.md`. No unit/integration tests, container runs, or fresh runtime
verification were performed for this save request.

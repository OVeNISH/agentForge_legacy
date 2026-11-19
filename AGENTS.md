AGENTS.md — Legacy Code Modernization Agent

You are building a tool that takes a small legacy codebase, documents it, pins down its current behaviour with tests, converts it to a modern version, and proves the behaviour did not change. Read this whole file before doing anything. Re-read the "Rules" and the current checkpoint at the start of every work session.

1. Goal

Input: a small legacy codebase. Foundation target is Python 2.7 to Python 3.12. Java and PHP are future work; design for them, do not build them.

The tool must:

Parse every file into an AST and extract structured facts.
Generate docstrings and a module-level architecture summary.
Generate characterization tests that record the legacy code's actual behaviour.
Convert the code to the modern version.
Run the tests against the converted code and confirm behaviour is unchanged.
Report pass rates before and after.

Optional extension (only after all required checkpoints pass): dependency upgrade report.

2. Non-negotiable principles
   The legacy code is the oracle. Expected outputs in tests come from executing the original code in a sandbox, never from an LLM's guess. The LLM proposes inputs only.
   Tests are read-only during conversion and repair. No stage that edits source may edit tests or fixtures. Enforce this mechanically (checksums), not by promise.
   Deterministic code controls the flow. The orchestrator decides what runs next. The LLM does thinking inside a stage and nothing else.
   Never trust LLM output unvalidated. Every LLM response is parsed against a schema and checked (does it parse, compile, run) before use. On failure, retry with the error, up to a cap.
   Every claim in the final report must be backed by a recorded run. No hand-entered numbers.
   Python 3's own ast module cannot parse Python 2 files. Use a Python 2-capable parser or run the analysis inside the legacy container. Do not "fix" this by converting first.
   No network and no host filesystem writes while executing legacy or converted code.
   Do not game the metrics. See section 5.
3. Defaults you may change only with a written justification
   Two container images: legacy runtime (Python 2.7) and modern runtime (Python 3.12).
   A language adapter interface (parse, list entry points, convert, run tests) with Python 2 as the only implementation.
   An LLM client interface with at least two implementations: a real provider and a deterministic mock used in tests.
   A shared artifact store (a workspace directory layout or a small database) holding AST facts, docs, fixtures, run results, diffs, and LLM call logs.
   Prefer the provider SDK directly over agent frameworks.
4. Working protocol
   Work one checkpoint at a time, in order. Do not start work belonging to a later checkpoint.
   Keep a file named PROGRESS.md at the repo root. For each checkpoint record: status, date, what was built, evidence (exact commands run and their outputs, counts, file paths), known gaps, decisions made and why.
   A checkpoint is passed only when every exit criterion is met and the evidence is recorded. "Looks right" is not evidence.
   At the end of each checkpoint, write a short checkpoint report and stop. Checkpoints marked [HUMAN GATE] require explicit human approval before you continue. For the others, continue only if all criteria are met; otherwise stop and report.
   If blocked, or if a requirement conflicts with another, stop and ask. Do not silently pick a workaround that weakens a principle.
   Commit small, with messages that name the checkpoint.
   Never delete or weaken a test to make a checkpoint pass. If a test is wrong, explain why in PROGRESS.md and get approval.
5. Anti-gaming rules
   Do not special-case test inputs in converted code (no branches keyed on fixture values).
   Do not catch and swallow exceptions to make tests pass unless the legacy code did the same.
   Do not loosen comparisons (for example ignoring whitespace or type differences) unless the normalization rule is documented, justified, and applied equally to both runs.
   Do not quarantine a test without logging the reason and including it in the report.
   Preserve legacy bugs. If preserving behaviour means preserving a bug, flag it as a "suspected legacy bug" in the report instead of fixing it.
   Keep a held-out set of tests that the repair stage never sees; use it as a final check.
6. Checkpoints
   CP0 — Scaffolding and environments

Build: repo layout, package setup, both container images, a single command that runs the whole test suite, configuration handling, structured logging. Exit criteria:

Legacy and modern containers both start and run a trivial script, shown with version output.
The LLM client interface exists with the mock implementation, and a unit test uses it.
One command runs all tests and exits non-zero on failure.
PROGRESS.md exists and records CP0.
CP1 — Evaluation corpus [HUMAN GATE]

Build: a corpus of 4 to 6 small Python 2 projects (permissively licensed, or written by you), each with a recorded license and source. Together they must cover: print statements, except syntax, dict iteration methods, integer division, str versus bytes and unicode, map and filter and zip usage, sorting with comparison functions, relative imports, file I/O, and at least one use of time or randomness. Exit criteria:

Every project runs under the Python 2.7 container.
A coverage matrix shows which migration hazards each project exercises.
At least one project is small enough to verify by hand, designated the "golden" project.
Human approves the corpus.
CP2 — Static analyzer

Build: a deterministic analyzer producing structured facts per file: functions, classes, signatures, existing comments, import graph, approximate call graph, and side-effect markers (file I/O, network, database, environment variables, time, randomness, global mutable state). Exit criteria:

100% of corpus files parse. Any failure is investigated, not skipped.
Output conforms to a documented schema, validated automatically.
Unit tests cover each fact type using small fixtures.
No LLM is used in this stage.
CP3 — Sandbox runner

Build: a runner that executes code and tests in either container with no network, CPU and memory limits, wall-clock timeouts, and a scratch filesystem. Exit criteria:

Tests prove that: a network call fails, a runaway loop is killed, an excessive memory request is stopped, and writes outside scratch space are impossible or discarded.
Results (return values, exceptions, stdout, stderr, files created) are captured in a structured form.
The same input run twice produces identical captured output for deterministic code.
CP4 — LLM layer

Build: the real provider implementation behind the client interface, prompt templates as separate versioned files, schema validation of every response, bounded retries that feed back the validation error, per-call logging (prompt, response, model, token counts, validation result), timeouts, and rate-limit handling. Exit criteria:

Every prompt template has a schema and tests using the mock.
A malformed response triggers a retry and eventually a clean, logged failure, demonstrated by test.
Cost and token usage per run are reported.
No API key appears in the repo or in logs.
CP5 — Characterization test generation

Build: for each function, the LLM proposes inputs (typical, edge, empty, boundary, unicode and bytes). The harness runs them in the legacy container and records outcomes as fixtures. Coverage measurement drives a bounded number of follow-up rounds targeting uncovered branches. Flakiness detection reruns each test several times. Time, randomness, and paths are normalized or the test is quarantined with a logged reason. Untestable code (needs a database, sockets, specific files) is mocked, skipped, or flagged, per a documented policy. Exit criteria:

Legacy code on the legacy runtime passes 100% of non-quarantined tests, across repeated runs.
Coverage per project is recorded, with a target stated up front and any shortfall explained.
A quarantine report lists every excluded test and why.
Mutation sanity check: deliberately break the legacy code in several ways and show the suite catches a stated minimum fraction of the breaks.
A held-out test subset is set aside and sealed from later stages.
CP6 — Baseline measurement [HUMAN GATE]

Build: run the characterization suite against the unmodified legacy code on the modern runtime. Exit criteria:

Baseline numbers recorded for every project: pass rate of legacy-on-legacy and legacy-on-modern, with failures grouped by cause.
Human reviews that the failure categories make sense and approves proceeding.
CP7 — Documentation generation

Build: docstrings generated bottom-up (functions first, with AST facts and callers and callees as context), then module summaries, then a package-level architecture summary. Generated text is tagged as machine-written. Exit criteria:

Every function and class has a docstring or a logged reason it does not.
A cross-check compares docstring claims against recorded behaviour (for example, stated return types versus observed), and mismatches are listed.
Module and package summaries exist for every corpus project and are written to the artifact store.
Docs generation never modifies tests or fixtures.
CP8 — Transformation

Build: a layered conversion. First a deterministic rule-based pass for mechanical changes. Then LLM-assisted handling of semantic issues the rules cannot decide (str versus bytes, division intent, sorting, iterator-returning builtins). Exit criteria:

Converted files compile and import under the modern runtime.
Test and fixture checksums are unchanged before and after the stage, proven by recorded comparison.
A diff of every changed file is saved.
Each LLM-made change is logged with its reason.
CP9 — Verify and repair loop

Build: run the suite on converted code; for each failure give the LLM the expected-versus-actual diff, the relevant code, and the traceback; retry with a cap per function; escalate unresolved cases as "needs human review". Exit criteria:

The loop terminates on every corpus project, with retry counts recorded.
No test or fixture was modified (checksum proof).
Held-out tests are run after the loop and results are reported separately.
A review step scans diffs for anti-gaming violations (section 5), and the result is recorded.
CP10 — Reporting

Build: an aggregate report generated entirely from run records. Exit criteria — the report contains:

Three pass rates per project: legacy on legacy, legacy on modern, converted on modern.
Coverage achieved, quarantined tests, held-out results.
Files changed with diffs, repair rounds used, token and cost totals.
Unresolved failures and suspected legacy bugs.
The generated architecture summary and docs.
Every number traceable to a run record, verified by a script that recomputes them.
CP11 — End-to-end run and hand-off [HUMAN GATE]

Build: one command that runs the full pipeline on a project from scratch. Exit criteria:

Full pipeline succeeds on every corpus project from a clean checkout.
A second full run reproduces the same pass rates (differences explained).
A README explains setup, usage, architecture, known limitations, and how to add a new corpus project.
A short demo script walks through the golden project start to finish.
CP12 — Optional: dependency upgrade report

Only start after CP11 is approved. Exit criteria:

Requirements files and imports are parsed; each package is checked for modern-runtime support and the newest compatible version; abandoned or replaced packages are flagged.
The upgraded set is trial-installed in the modern container and breakage is reported.
The report recommends changes but never applies them. 7. Definition of done

All required checkpoints (CP0 to CP11) passed with evidence in PROGRESS.md, all human gates approved, a clean-checkout end-to-end run reproducible, and a report whose numbers a script can recompute from raw run records.

8. When to stop and ask
   A principle in section 2 would have to be bent.
   A checkpoint's exit criteria cannot be met as written.
   Results look too good (for example 100% on converted code on the first try). Treat that as a signal to check for weak tests or leakage before celebrating.
   You are about to spend significantly more LLM budget than recorded estimates.

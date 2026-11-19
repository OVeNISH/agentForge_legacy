# Documentation generation (CP7)

`modernize.documentation.generate` accepts CP2 facts, CP5 **training-only**
fixtures, an `LLMRun`, the legacy sandbox runner and an artifact directory.
It visits known callees before callers, marks cycles visited deterministically,
then generates class, module and package text. Unresolved callback/dynamic edges
remain approximate. Source, signatures, effects and caller/callee facts accompany
function prompts; observations supply return-type and exception-name sets.
Held-out outcomes never enter generation prompts or generated docs.

The versioned `prompts/documentation/documentation.v1` template has a strict
Pydantic/JSON schema. `LLMRun` accepts existing input-prompt names or an explicit
`Prompt`, sharing capped retries, validation, redaction and usage logs.
The corpus demo replays coding-LLM-authored summaries through the deterministic
mock; type claims come directly from training observations. This does not verify
live-provider documentation quality. No paid API calls are required.

Artifacts per project:

- `documentation.json`: tagged text, structured claims, cross-checks and omissions.
- `source/`: separate legacy source copy with function, class and module docstrings.
- `modules/*.md` and `architecture.md`: tagged module/package descriptions.
- `validation-run.json` and `llm/`: sandbox validation and per-call logs.

The trusted editor inserts string literals, never model-supplied code. Inside the
Python 2 sandbox it parses and compiles the result, verifies inserted docstrings,
and compares ASTs with docstrings removed. Inline suites and ambiguous existing
string tokens receive logged omissions instead of source restructuring. Lambdas
have no docstring suite and are covered by enclosing-function docs. Introspection
sees the new docstrings and traceback lines may move; no source is imported or
executed during this validation.

Cross-checks compare structured return types/exception names with training
outcomes and retain every mismatch. Prose is source-based inference, not
mechanically proven behavior. A deliberately false-claim unit test calibrates
the checker. Successful `build_report` paths remain quarantined; docs disclose
that limit and flag input overwrite as a suspected legacy bug without changing it.

The corpus command hashes original corpus, tests, fixtures and CP5/CP6 archives
before/after generation, verifies CP5 seals, and refuses protected output paths.
It emits checksum proof and a summary. The committed CP7 archive contains the
successful run and is checked offline by the unit suite.

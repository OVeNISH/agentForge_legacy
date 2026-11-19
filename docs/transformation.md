# Transformation (CP8)

Run `PYTHONPATH=src python scripts/transform_corpus.py --output artifacts/cp8-new`
with both existing images available. The output must be new and outside protected
inputs. The corpus demonstration consumes CP7's annotated source copies, the
original CP2 facts and **training-only** observed type/exception summaries.
Held-out expectations and baseline case outcomes never enter conversion prompts.

`modernize.transformation.transform` first calls the trusted Python 2 converter
inside the legacy sandbox. It parses the original before conversion and uses
the image's standard-library lib2to3 with an explicit fixer list for mechanical
syntax, dictionary and iterator changes. Unicode literals and division decisions
are deferred. The pass stabilizes within four iterations or fails; a correctly
placed future print import prevents repeated print-statement conversion. The
legacy image identity pins this obsolete tooling; unsupported syntax fails.

The second layer uses a strict versioned `transformation.v1` prompt/schema and
the existing `LLMRun` validation, retry and usage boundary. Each response gives
whole-file replacements or new helper files, base hashes, migration hazards,
reasons and unsupported cases. The corpus command replays coding-LLM-authored
semantic edits through the deterministic mock. It makes no paid provider calls
and does not measure autonomous provider conversion quality.

The controller rejects unsafe/protected paths, stale hashes, duplicate patches,
invalid modern syntax and new helpers outside existing source directories.
Public definition names, argument names, default counts and variadic argument
names are checked against CP2. The comparison does not prove default-expression
or runtime behavior equivalence. Helpers and their imports/callers are changed
together. The modern sandbox compiles every source file and imports every module;
its record includes refreshed definition/signature/import facts. At most two
semantic candidates are accepted/rejected with error feedback. Source is
published as a whole directory only after successful validation.

Artifacts include `mechanical/`, `mechanical-diffs/`, `changes-N.json`,
`validation-N.json`, `attempts.json`, final `source/`, per-file `diffs/` and
`report.json`, plus LLM call logs. Diffs compare incoming CP7 documented source
with converted source and include new helpers. Before/after checksums cover the
original corpus, tests, fixtures and CP5/CP6/CP7 evidence; CP5 seals are checked.
Models never receive write access to tests or fixture stores.

Semantic decisions cover built-in integer/float division, cmp-to-key sorting,
list-returning builtins and byte/text boundaries. They preserve the input-file
overwrite and leave time/randomness untouched. Custom `__div__`, heterogeneous
comparison/custom `__cmp__`, exact Python 2 exception identities/messages and
runtime byte/Unicode tags remain explicit review risks. Characterization tests,
repair, held-out evaluation and anti-gaming review are **CP9 work**. Passing
compilation/import does not imply behavioral equivalence.

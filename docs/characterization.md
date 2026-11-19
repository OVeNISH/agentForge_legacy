# CP5 characterization

Run from the repository root with the existing images available:

```sh
PYTHONPATH=src .venv/bin/python scripts/characterize_corpus.py --output artifacts/cp5-new
PYTHONPATH=src .venv/bin/python scripts/verify_cp5.py artifacts/cp5-new
```

The destination must not exist. Failed runs retain their evidence. This command
implements CP5 only; it does not measure the modern-runtime baseline or convert
source. Docker access is required. No package installation or paid call is needed.

`Characterizer` accepts the existing `SandboxRunner` and `LLMRun`. A provider-backed
`LLMRun` can be passed through the same API. The corpus command instead replays
input proposals authored by the coding LLM in
`tests/fixtures/cp5/input_proposals.json` through a deterministic mock. Logs label
this as mock evidence. It establishes execution, validation and replay behaviour,
not live-provider proposal quality. Mock token/cost values are synthetic zeros;
there were no paid provider calls. No model, credential or provider tariff is
silently selected.

## Observation policy

Every case runs three times in fresh Python 2.7 containers using CP3's existing
network, filesystem and resource restrictions. The original source snapshot is
unchanged; only the trusted observation harness is added. Methods use fresh
zero-argument instances, optional input-only setup calls and captured instance
state. `__init__` is called once. Scratch assets are input proposals too; paths
and base64 are validated. The only expected results are observations of the
original code, never values supplied by a proposal.

Return values and instance state retain CP3's exact type encoding. Comparisons
include exception module/name/arguments/message, all stdout/stderr bytes, target
exit code and every captured file. Traceback locations are excluded from the
behaviour contract because source locations change during conversion. There is
no whitespace, exception-type, byte/text, clock, random-value or path
normalization. CP3's canonical mapping/set ordering applies equally to all runs.

Different repeated observations quarantine the entire case with its input,
reason and run references. Quarantine is excluded from both pass-rate and eligible
coverage numerators; counts remain visible. Infrastructure, protocol and capture
failures stop the run rather than becoming passing exceptions or quarantine.
Bad user inputs that raise stable legacy exceptions remain eligible cases.

External resources must be supplied as explicit scratch-file assets. Database,
socket and unsupported construction requirements must be flagged for review; the
harness does not silently mock them or execute them on the host. Corpus methods
need only zero-argument construction. Nested callables such as the text-cleaning
lambda are covered through their enclosing function and logged as not separately
addressable. Non-UTF-8 source context, complex object inputs and non-zero-argument
class construction need additional input contracts before use on other projects.

## Coverage and bounds

The pre-run targets are 90% function statement-line coverage, 90% explicit
`if`/`for`/`while` branch coverage and at least 80% detection of eight specified
mutations. The legacy interpreter's `ast` builds the denominator without executing
source; `sys.settrace` observes lines and branch arcs on the unchanged source.
Module initialization and CLI/main blocks, definitions and docstrings are outside
the function-line denominator. Comprehension, Boolean short-circuit, implicit
exception and bytecode branches are not counted as explicit branches. A project
with zero explicit branches reports 100% by convention, with its zero denominator
retained. This is not a claim of full bytecode branch coverage.

There are at most two proposal rounds, 32 cases per response and three attempts
per LLM call through CP4. Uncovered static lines and arcs feed the second round;
duplicate inputs are not rerun. File-report's second round adds its missing empty
summary case. Successful completion does not require hiding a target shortfall:
file-report's eligible line coverage is 9/16 (56.25%) because five unstable
`build_report` cases are quarantined. Its remaining eligible `build_report` case
checks a stable invalid-path exception. Seven successful-body lines therefore
remain outside eligible coverage, and that function has no held-out case.

The eight isolated source mutations run only against training fixtures. Seven
are detected (87.5%); a deliberate change to the quarantined clock behaviour
survives. That is a recorded test gap, not evidence of equivalence. All mutation
copies are disposable; neither corpus nor fixture contents are edited.

## Artifacts and stage boundary

Each project has `training/`, `sealed/` and `private/` directories. One accepted
case per target with at least two distinct eligible cases is selected by smallest
SHA-256 input ID after all coverage feedback ends. The corpus yields 73 training
and 15 held-out cases. The split is deterministic, not a statistical estimate of
generalization. Held-out cases receive a separate final replay after mutations.

`private/` contains proposal logs, all raw sandbox records, quarantine and coverage
reports. `seal.json` hashes every file under these three directories. Sealed files
are read-only, and checksum verification detects changes, removals and additions.
`export_training` verifies the seal and copies **only** training fixtures into a
separate stage directory. Tests prove that held-out cases and proposal/oracle
logs are excluded. Later repair stages must use that exported view as their only
fixture context; private and sealed directories are controller-owned. This is a
mechanical export/checksum boundary, not encryption against the host account.

`docs/evidence/cp5.tar.gz` preserves the complete successful run, including raw
records; `scripts/verify_cp5.py` recomputes its metrics without Docker or an LLM.
Its checks include source identity, oracle/replay equality, static coverage
denominators, quarantine differences, split disjointness, mutation source hashes,
held-out outcomes, schema validation and mock usage provenance.

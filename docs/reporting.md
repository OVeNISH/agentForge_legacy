# Recorded corpus reporting

Generate CP10's aggregate report without Docker, network access or provider calls:

```sh
PYTHONPATH=src .venv/bin/python scripts/report_corpus.py --output artifacts/cp10-new
PYTHONPATH=src .venv/bin/python scripts/report_corpus.py --verify artifacts/cp10-new
PYTHONPATH=src .venv/bin/python scripts/report_corpus.py --verify docs/reports/cp10
```

The committed [report](reports/cp10/report.md) and [JSON](reports/cp10/report.json)
contain the completed CP10 output.

The output directory must be new and outside protected inputs. `report.md`
contains the readable report, including documentation and diffs; `report.json`
contains exact values and evidence references. Verification rebuilds both from
the committed CP5–CP9 archives and rejects changed report contents. It reuses
the characterization, baseline and repair evidence verifiers, including their
source, raw-observation, frozen-input and held-out checks. No project code runs.

All three headline rates use the same eligible cases: training plus held-out,
excluding quarantined cases. Held-out results are also shown separately. Exact
comparisons retain runtime type identities, exception details, streams and files.
Coverage describes eligible legacy observations; it does not prove converted
coverage or successful execution of quarantined paths. Coverage targets and
shortfalls, each quarantine and its reason, mutation checks, repair attempts,
unresolved expected/actual comparisons, review flags, docs and diffs are included.

`cp9.tar.gz!/project/heldout.json#case-id`, for example, identifies an archived
raw replay. The report includes archive SHA-256 hashes and member references for
each section. It recomputes usage from call logs rather than copying usage totals.
Reported token/cost totals cover only successful retained corpus stage runs
(CP5, CP7, CP8, CP9). Mock provenance is explicit; zero mock usage does not
estimate live provider cost or include coding-agent authoring, probes, failed
runs, or infrastructure checks.

Suspected legacy bugs are copied from recorded, source-grounded documentation
and kept distinct from unresolved migration failures. Documentation's structured
claims are checked against training observations; its prose is not mechanically
proven. The existing manual and heuristic anti-gaming reviews are included with
their limitations. An offline verifier checks evidence consistency, not the
authenticity of the original execution environment.

Generation and verification exit zero when the report matches the evidence,
including evidence of unresolved migrations. The report's `needs_human_review`
status remains explicit; a successful report command does not certify behavioral
equivalence or complete CP11's end-to-end pipeline.

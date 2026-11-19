# CP1 evaluation corpus

Status: CP1 approved by the user on 2026-11-19. These are four small,
original Python 2.7 projects authored in this repository on 2026-11-19, each
licensed under the [MIT license](LICENSE). There is no downloaded upstream code
or third-party runtime dependency. Per-project provenance, entry points, licenses,
and hazard identifiers are recorded in [manifest.json](manifest.json).

| Project | Purpose | License | Source |
|---|---|---|---|
| `golden_ledger` | Hand-checkable bill splitting and balances; golden project | MIT | Original; `golden_ledger/main.py` |
| `text_pipeline` | List-producing builtins and UTF-8 boundaries | MIT | Original; `text_pipeline/main.py` |
| `ranking` | Mutable scoreboard, descending scores and name tie-breaks | MIT | Original; `ranking/main.py` |
| `file_report` | Multi-module package, numeric files, timestamp and ticket | MIT | Original; `file_report/` |

## Migration hazard coverage matrix

This matrix describes source constructs, not measured branch or test coverage.

| Required hazard | golden_ledger | text_pipeline | ranking | file_report |
|---|---|---|---|---|
| Print statements | `main.py` | `main.py` | `main.py` | `main.py` |
| Old exception syntax | `parse_amount` | — | — | — |
| Dict iteration methods | `summarize`: `iteritems` | — | `ranked`: `iteritems` | `storage.write_report`: `iteritems` |
| Integer division | `split_bill`, positive and negative | — | — | `summary.summarize`: mean |
| str / bytes / unicode | — | UTF-8 encode/decode, type and length observations | — | Binary file streams |
| map, filter, zip | — | `clean_names`, `pair_names` | — | — |
| Comparison-function sorting | — | — | `rows.sort(cmp=compare_scores)` | — |
| Relative imports | — | — | — | `reportkit/__init__.py`: `.storage`, `.summary` |
| File I/O | — | — | — | `build_report`, `read_numbers`, `write_report` |
| Time or randomness | — | — | — | `time.time`, `random.Random(seed).randint` |

## Golden project review

`golden_ledger/main.py` contains three short functions and no imports or external
state. Its actual Python 2.7 smoke output was:

```text
split: 3 -4
total: 5
empty: 0
parsed: 12
bad: invalid: invalid literal for int() with base 10: 'bad'
```

For hand review: Python 2 integer division floors `7 / 2` to `3` and `-7 / 2`
to `-4`; the balances sum to `5`; an empty sum is `0`; valid decimal text gives
`12`, and invalid text returns the caught exception message. This explanation
accompanies observed output; it is not a generated characterization suite.

## Reproduce the CP1 runtime checks

Build the CP0 legacy image as described in the root README. From the repository
root, run the following command once for each project, replacing `PROJECT` with
`golden_ledger`, `text_pipeline`, `ranking`, or `file_report`:

```sh
docker run --rm --network none --read-only --cap-drop ALL --security-opt no-new-privileges --memory 128m --cpus 1 --pids-limit 64 --ulimit cpu=10:10 --tmpfs /tmp:rw,nosuid,nodev,size=16m --mount "type=bind,source=$PWD/corpus,target=/corpus,readonly" --workdir /tmp --entrypoint python modernize-legacy:cp0 -B /corpus/PROJECT/main.py
```

The existing image runs as UID/GID 65534. Only `/tmp` is writable; it is an
ephemeral container tmpfs. Source is mounted read-only; `-B` prevents bytecode
writes. The file-report smoke creates `sample.txt` and `report.txt` in scratch;
both disappear with the container. No legacy code executes on the host.

[evidence/cp1-runs.json](evidence/cp1-runs.json) records exact commands, captured
output, exit status, source SHA-256 hashes, and image identity. This is CP1 smoke
evidence, not CP5 fixtures or CP6 baseline pass rates. Unit tests verify evidence
matches current sources and that all required hazard metadata is present.

## Known limits for later stages

- This original corpus exercises the required hazards but is synthetic and small;
  it does not establish performance on real third-party applications.
- The file report intentionally retains the current time. Its ticket is seeded
  in the smoke entry point; calls with the default seed can vary. CP5 must detect
  and document normalization or quarantine; CP1 does neither.
- Dictionary representation order and exact exception messages are observations
  from the recorded runtime. No comparison normalization has been introduced.
- Smoke paths exercise representative inputs, not every function branch or
  argument type. No characterization coverage or held-out results are claimed.

The user approved corpus commit `a34ea73`; approval is recorded in PROGRESS.md.

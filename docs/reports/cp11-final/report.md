# Recorded modernization report

**Status: passed**

Fresh sandbox executions using recorded corpus mock proposals. No prior run archive supplies outcomes. Mock tokens/costs do not estimate provider use. Raw stage records are retained under this run directory.

Exact frozen comparisons; all headline rates use training plus held-out cases. Held-out cases run only after every repair has finished. No normalization or new exclusions. Versioned policy results are separate; raw rates above remain exact. Policy status requires every eligible case and the independently recorded source review to match. Prior exposed cases are retained as training regressions; final held-out results use fresh inputs only.

See report.json for exact values, raw-record references, archive hashes and all report fields.

| Project | Legacy / legacy | Legacy / modern | Converted / modern | Held-out converted |
|---|---:|---:|---:|---:|
| golden_ledger | 24/24 (100.00%) | 0/24 (0.00%) | 15/24 (62.50%) | 2/3 (66.67%) |
| text_pipeline | 40/40 (100.00%) | 0/40 (0.00%) | 5/40 (12.50%) | 0/5 (0.00%) |
| ranking | 28/28 (100.00%) | 0/28 (0.00%) | 7/28 (25.00%) | 1/4 (25.00%) |
| file_report | 28/28 (100.00%) | 5/28 (17.86%) | 11/28 (39.29%) | 2/4 (50.00%) |

## Totals and usage

```json
{
  "accepted_repairs": 2,
  "converted_on_modern": {
    "pass_rate_percent": 31.666666666666668,
    "passed": 38,
    "tests": 120
  },
  "heldout_passed": 5,
  "heldout_tests": 16,
  "legacy_on_legacy": {
    "pass_rate_percent": 100.0,
    "passed": 120,
    "tests": 120
  },
  "legacy_on_modern": {
    "pass_rate_percent": 4.166666666666667,
    "passed": 5,
    "tests": 120
  },
  "quarantined": 5,
  "repair_proposals": 2,
  "usage": {
    "attempts": 54,
    "cost_complete": true,
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  }
}
```

## Characterization plan and sanity checks

```json
{
  "branch_target": 90,
  "limitation": "CP5 mutation sanity evidence remains separately archived; mutations are not rerun by this pipeline.",
  "line_target": 90,
  "max_rounds": 2,
  "repeats": 3
}
```

## Recorded anti-gaming review

```json
{
  "automatic": {
    "file_report": {
      "findings": [
        {
          "path": "reportkit/_legacy_compat.py",
          "rule": "changed_branch_count"
        }
      ],
      "limitation": "Heuristic only; inspect all saved diffs for fixture branches, swallowed exceptions and changed comparisons.",
      "status": "needs_human_review"
    },
    "golden_ledger": {
      "findings": [
        {
          "path": "_legacy_compat.py",
          "rule": "changed_branch_count"
        }
      ],
      "limitation": "Heuristic only; inspect all saved diffs for fixture branches, swallowed exceptions and changed comparisons.",
      "status": "needs_human_review"
    },
    "ranking": {
      "findings": [],
      "limitation": "Heuristic only; inspect all saved diffs for fixture branches, swallowed exceptions and changed comparisons.",
      "status": "no_automatic_flags"
    },
    "text_pipeline": {
      "findings": [],
      "limitation": "Heuristic only; inspect all saved diffs for fixture branches, swallowed exceptions and changed comparisons.",
      "status": "no_automatic_flags"
    }
  },
  "limitation": "Heuristic scan only; fresh diffs require human review.",
  "source_review": {
    "limitations": "Supports recorded primitive inputs only; custom numeric protocols, mixed-type ordering, dynamic behavior and quarantined clock paths remain outside the evidence.",
    "projects": {
      "file_report": {
        "assessment": "Reviewed general numeric/type/encoding/sorting compatibility and unchanged public API; file_report adds shared path-only open validation. No fixture-valued branches, exception suppression, test access or observation mutation. Golden ledger additionally formats byte-literal diagnostics returned as data, preserving bytes and full error contents with only the Python 3 repr prefix removed. No normalization of returned data.",
        "executable_sha256": {
          "main.py": "373c81a3ff018329c3b93466283356ce299de1f969c14b6f7cf52c72f5960558",
          "reportkit/__init__.py": "cbb1c4d9ebdc95978e6fe61c8202d92cdfe5ba6214cef90eaf9d103e893e1f56",
          "reportkit/_legacy_compat.py": "903d3832ddf8efe0f4ea9a8ebc5629a8839686d5aad467b920943fa3fca773fe",
          "reportkit/storage.py": "8c8799daac525165924b42aea7d958a9e92e7e7816f46c40bc48916006298f40",
          "reportkit/summary.py": "4cd231b0e64d0e3c2c4427d0c7e554a8ae310cd38b14a7a0fb12a268c004f096"
        }
      },
      "golden_ledger": {
        "assessment": "Reviewed general numeric/type/encoding/sorting compatibility and unchanged public API; file_report adds shared path-only open validation. No fixture-valued branches, exception suppression, test access or observation mutation. Golden ledger additionally formats byte-literal diagnostics returned as data, preserving bytes and full error contents with only the Python 3 repr prefix removed. No normalization of returned data.",
        "executable_sha256": {
          "_legacy_compat.py": "cc7e31251af6b879fa2e46c1fc92f0738755b68b63a752c1f3e206045df065a5",
          "main.py": "250620f60855b0ea542e0aad73baa908fe0863dce3dc875c56492071d6930816"
        }
      },
      "ranking": {
        "assessment": "Reviewed general numeric/type/encoding/sorting compatibility and unchanged public API; file_report adds shared path-only open validation. No fixture-valued branches, exception suppression, test access or observation mutation. Golden ledger additionally formats byte-literal diagnostics returned as data, preserving bytes and full error contents with only the Python 3 repr prefix removed. No normalization of returned data.",
        "executable_sha256": {
          "main.py": "e875cf78421fdf2b582a2c0e94ac6247408c0fa1bd4a9d435bc2095b1107534a"
        }
      },
      "text_pipeline": {
        "assessment": "Reviewed general numeric/type/encoding/sorting compatibility and unchanged public API; file_report adds shared path-only open validation. No fixture-valued branches, exception suppression, test access or observation mutation. Golden ledger additionally formats byte-literal diagnostics returned as data, preserving bytes and full error contents with only the Python 3 repr prefix removed. No normalization of returned data.",
        "executable_sha256": {
          "main.py": "a1c94b0819c03160b0c28fae1ad903e1038f34c4f85f890fd9dbd4a977f33ed3"
        }
      }
    },
    "reviewer": "Coding agent",
    "scope": "Pre-evaluation review of executable ASTs, excluding only CP7-validated generated docstrings. Raw final source hashes remain locked separately; payload strings, branches, imports and exception handling must match reviewed code."
  },
  "status": "recorded_source_review_matches"
}
```

## Cross-runtime policy (raw rates above are unchanged)

```json
{
  "heldout_passed": 16,
  "heldout_tests": 16,
  "implementation_sha256": "4cda413f13d45d2ef8ae0ae636a9ebe29645bf5df3ec4ed9c8af20e942ff6733",
  "name": "python2-python3.v1",
  "pass_rate_percent": 100.0,
  "passed": 120,
  "source_review": {
    "limitations": "Supports recorded primitive inputs only; custom numeric protocols, mixed-type ordering, dynamic behavior and quarantined clock paths remain outside the evidence.",
    "projects": {
      "file_report": {
        "assessment": "Reviewed general numeric/type/encoding/sorting compatibility and unchanged public API; file_report adds shared path-only open validation. No fixture-valued branches, exception suppression, test access or observation mutation. Golden ledger additionally formats byte-literal diagnostics returned as data, preserving bytes and full error contents with only the Python 3 repr prefix removed. No normalization of returned data.",
        "executable_sha256": {
          "main.py": "373c81a3ff018329c3b93466283356ce299de1f969c14b6f7cf52c72f5960558",
          "reportkit/__init__.py": "cbb1c4d9ebdc95978e6fe61c8202d92cdfe5ba6214cef90eaf9d103e893e1f56",
          "reportkit/_legacy_compat.py": "903d3832ddf8efe0f4ea9a8ebc5629a8839686d5aad467b920943fa3fca773fe",
          "reportkit/storage.py": "8c8799daac525165924b42aea7d958a9e92e7e7816f46c40bc48916006298f40",
          "reportkit/summary.py": "4cd231b0e64d0e3c2c4427d0c7e554a8ae310cd38b14a7a0fb12a268c004f096"
        }
      },
      "golden_ledger": {
        "assessment": "Reviewed general numeric/type/encoding/sorting compatibility and unchanged public API; file_report adds shared path-only open validation. No fixture-valued branches, exception suppression, test access or observation mutation. Golden ledger additionally formats byte-literal diagnostics returned as data, preserving bytes and full error contents with only the Python 3 repr prefix removed. No normalization of returned data.",
        "executable_sha256": {
          "_legacy_compat.py": "cc7e31251af6b879fa2e46c1fc92f0738755b68b63a752c1f3e206045df065a5",
          "main.py": "250620f60855b0ea542e0aad73baa908fe0863dce3dc875c56492071d6930816"
        }
      },
      "ranking": {
        "assessment": "Reviewed general numeric/type/encoding/sorting compatibility and unchanged public API; file_report adds shared path-only open validation. No fixture-valued branches, exception suppression, test access or observation mutation. Golden ledger additionally formats byte-literal diagnostics returned as data, preserving bytes and full error contents with only the Python 3 repr prefix removed. No normalization of returned data.",
        "executable_sha256": {
          "main.py": "e875cf78421fdf2b582a2c0e94ac6247408c0fa1bd4a9d435bc2095b1107534a"
        }
      },
      "text_pipeline": {
        "assessment": "Reviewed general numeric/type/encoding/sorting compatibility and unchanged public API; file_report adds shared path-only open validation. No fixture-valued branches, exception suppression, test access or observation mutation. Golden ledger additionally formats byte-literal diagnostics returned as data, preserving bytes and full error contents with only the Python 3 repr prefix removed. No normalization of returned data.",
        "executable_sha256": {
          "main.py": "a1c94b0819c03160b0c28fae1ad903e1038f34c4f85f890fd9dbd4a977f33ed3"
        }
      }
    },
    "reviewer": "Coding agent",
    "scope": "Pre-evaluation review of executable ASTs, excluding only CP7-validated generated docstrings. Raw final source hashes remain locked separately; payload strings, branches, imports and exception handling must match reviewed code."
  },
  "source_review_sha256": "13b317841a7547a077a4a3bd11edb420e54a34983feaf1dd89aecaae2fc89f09",
  "tests": 120
}
```

## Evaluation profile and exposed-case disposition

```json
{
  "disposition": "All previously exposed proposal IDs remain eligible regression/training cases; only fresh IDs may be sealed.",
  "fresh_inputs_sha256": "ba7ce99a9481e4fcb528a4ae78c5ce2ef8c4684b9ed7c1482941c4ee9e3d555a",
  "name": "fresh-revalidation.v2"
}
```

## Policy results: golden_ledger

```json
{
  "failures": [],
  "heldout": {
    "pass_rate_percent": 100.0,
    "passed": 3,
    "tests": 3,
    "unresolved": []
  },
  "pass_rate_percent": 100.0,
  "passed": 24,
  "source_review_matches": true,
  "tests": 24,
  "training": {
    "pass_rate_percent": 100.0,
    "passed": 21,
    "tests": 21,
    "unresolved": []
  },
  "unresolved": []
}
```

## golden_ledger

### Evidence references

```json
{
  "baseline": "golden_ledger/baseline-modern.json",
  "characterization": "golden_ledger/characterization/private/runs.jsonl",
  "diffs": "golden_ledger/diffs/",
  "documentation": "golden_ledger/documentation/documentation.json",
  "heldout": "golden_ledger/heldout.json",
  "repair": "golden_ledger/repair/attempts.json",
  "training": "golden_ledger/repair/training-final.json"
}
```

### Coverage, exclusions and quarantines

```json
{
  "coverage": {
    "branches": {
      "covered": [
        "main.py:10:11",
        "main.py:10:12"
      ],
      "missing": [],
      "percent": 100.0,
      "possible": [
        "main.py:10:11",
        "main.py:10:12"
      ]
    },
    "lines": {
      "covered": [
        "main.py:10",
        "main.py:11",
        "main.py:12",
        "main.py:16",
        "main.py:17",
        "main.py:19",
        "main.py:5",
        "main.py:9"
      ],
      "missing": [],
      "percent": 100.0,
      "possible": [
        "main.py:10",
        "main.py:11",
        "main.py:12",
        "main.py:16",
        "main.py:17",
        "main.py:19",
        "main.py:5",
        "main.py:9"
      ]
    }
  },
  "coverage_targets": {
    "branches": 90,
    "lines": 90
  },
  "inventory_exclusions": [],
  "quarantine": []
}
```

### Repair attempts and usage

```json
{
  "attempts": [
    {
      "accepted": true,
      "error": null,
      "function": [
        "main.py",
        "parse_amount"
      ],
      "function_attempt": 1,
      "index": 0
    }
  ],
  "max_attempts_per_function": 2,
  "retry_counts": {
    "main.py::parse_amount": 1
  }
}
```


```json
{
  "characterization": {
    "attempts": 3,
    "cost_complete": true,
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "conversion": {
    "attempts": 1,
    "cost_complete": true,
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "documentation": {
    "attempts": 5,
    "cost_complete": true,
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "repair": {
    "attempts": 1,
    "cost_complete": true,
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  }
}
```

### Unresolved failures

```json
[
  {
    "actual": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "integer division or modulo by zero"
            }
          ],
          "type": "tuple"
        },
        "message": "integer division or modulo by zero",
        "module": "builtins",
        "name": "ZeroDivisionError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[7, 0]",
      "category": "boundary",
      "files_json": "{}",
      "id": "2933d0e1a536a13e1c9b",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: boundary input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "split_bill"
    },
    "expected": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "aW50ZWdlciBkaXZpc2lvbiBvciBtb2R1bG8gYnkgemVybw==",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "integer division or modulo by zero",
        "module": "exceptions",
        "name": "ZeroDivisionError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "2933d0e1a536a13e1c9b",
    "run": "golden_ledger/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "unsupported operand type(s) for /: 'str' and 'int'"
            }
          ],
          "type": "tuple"
        },
        "message": "unsupported operand type(s) for /: 'str' and 'int'",
        "module": "builtins",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[\"\\u00e9\", 2]",
      "category": "unicode",
      "files_json": "{}",
      "id": "ae99ca04829212e8d066",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: unicode input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "split_bill"
    },
    "expected": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "dW5zdXBwb3J0ZWQgb3BlcmFuZCB0eXBlKHMpIGZvciAvOiAndW5pY29kZScgYW5kICdpbnQn",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "unsupported operand type(s) for /: 'unicode' and 'int'",
        "module": "exceptions",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "ae99ca04829212e8d066",
    "run": "golden_ledger/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "unsupported operand type(s) for /: 'bytes' and 'int'"
            }
          ],
          "type": "tuple"
        },
        "message": "unsupported operand type(s) for /: 'bytes' and 'int'",
        "module": "builtins",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"Nw==\"}, 2]",
      "category": "bytes",
      "files_json": "{}",
      "id": "1ce3d591a6fab727dea2",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: bytes input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "split_bill"
    },
    "expected": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "dW5zdXBwb3J0ZWQgb3BlcmFuZCB0eXBlKHMpIGZvciAvOiAnc3RyJyBhbmQgJ2ludCc=",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "unsupported operand type(s) for /: 'str' and 'int'",
        "module": "exceptions",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "1ce3d591a6fab727dea2",
    "run": "golden_ledger/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "unsupported operand type(s) for +=: 'int' and 'bytes'"
            }
          ],
          "type": "tuple"
        },
        "message": "unsupported operand type(s) for +=: 'int' and 'bytes'",
        "module": "builtins",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"x\": {\"$bytes\": \"Nw==\"}}]",
      "category": "bytes",
      "files_json": "{}",
      "id": "0b3592f5255fad064b80",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: bytes input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "summarize"
    },
    "expected": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "dW5zdXBwb3J0ZWQgb3BlcmFuZCB0eXBlKHMpIGZvciArPTogJ2ludCcgYW5kICdzdHIn",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "unsupported operand type(s) for +=: 'int' and 'str'",
        "module": "exceptions",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "0b3592f5255fad064b80",
    "run": "golden_ledger/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "aW52YWxpZDogaW52YWxpZCBsaXRlcmFsIGZvciBpbnQoKSB3aXRoIGJhc2UgMTA6ICdiYWQn",
          "type": "bytes"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[\"bad\"]",
      "category": "edge",
      "files_json": "{}",
      "id": "3de50b5084cce723213b",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: edge input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "parse_amount"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "aW52YWxpZDogaW52YWxpZCBsaXRlcmFsIGZvciBpbnQoKSB3aXRoIGJhc2UgMTA6ICdiYWQn",
          "type": "str"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "3de50b5084cce723213b",
    "run": "golden_ledger/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "aW52YWxpZDogaW52YWxpZCBsaXRlcmFsIGZvciBpbnQoKSB3aXRoIGJhc2UgMTA6ICcn",
          "type": "bytes"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[\"\"]",
      "category": "empty",
      "files_json": "{}",
      "id": "d45c541e84e5ce2da0b7",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: empty input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "parse_amount"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "aW52YWxpZDogaW52YWxpZCBsaXRlcmFsIGZvciBpbnQoKSB3aXRoIGJhc2UgMTA6ICcn",
          "type": "str"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "d45c541e84e5ce2da0b7",
    "run": "golden_ledger/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "aW52YWxpZDogaW52YWxpZCBsaXRlcmFsIGZvciBpbnQoKSB3aXRoIGJhc2UgMTA6ICdceGZmJw==",
          "type": "bytes"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"/w==\"}]",
      "category": "bytes",
      "files_json": "{}",
      "id": "38e1023d868eec42b03b",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: bytes input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "parse_amount"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "aW52YWxpZDogaW52YWxpZCBsaXRlcmFsIGZvciBpbnQoKSB3aXRoIGJhc2UgMTA6ICdceGZmJw==",
          "type": "str"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "38e1023d868eec42b03b",
    "run": "golden_ledger/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "aW52YWxpZDogaW52YWxpZCBsaXRlcmFsIGZvciBpbnQoKSB3aXRoIGJhc2UgMTA6ICdiYWQtaW5wdXQtYmV0YSc=",
          "type": "bytes"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"YmFkLWlucHV0LWJldGE=\"}]",
      "category": "edge",
      "files_json": "{}",
      "id": "d845edd81d00753db703",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[]",
      "target": "parse_amount"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "aW52YWxpZDogaW52YWxpZCBsaXRlcmFsIGZvciBpbnQoKSB3aXRoIGJhc2UgMTA6ICdiYWQtaW5wdXQtYmV0YSc=",
          "type": "str"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "d845edd81d00753db703",
    "run": "golden_ledger/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "aW52YWxpZDogaW52YWxpZCBsaXRlcmFsIGZvciBpbnQoKSB3aXRoIGJhc2UgMTA6ICdiYWQtaW5wdXQtYWxwaGEn",
          "type": "bytes"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"YmFkLWlucHV0LWFscGhh\"}]",
      "category": "typical",
      "files_json": "{}",
      "id": "514ed5abfba49fd40ddc",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[]",
      "target": "parse_amount"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "aW52YWxpZDogaW52YWxpZCBsaXRlcmFsIGZvciBpbnQoKSB3aXRoIGJhc2UgMTA6ICdiYWQtaW5wdXQtYWxwaGEn",
          "type": "str"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "514ed5abfba49fd40ddc",
    "run": "golden_ledger/heldout.json"
  }
]
```

### Review flags and suspected legacy bugs

```json
[
  "Python 2 exception identity, messages and byte-string runtime tags still need CP9 evaluation.",
  "Custom __div__ and Python 2 long result types are outside this numeric helper's support."
]
```


```json
[]
```

### Documentation omissions and claim mismatches

```json
{
  "mismatches": [],
  "omitted": []
}
```

### function: golden_ledger/main.py::parse_amount

[Machine-generated]
Parse an integer and turn ValueError into an invalid-prefix message. Other exceptions propagate, including invalid input types.

Observed return types: int, str
Observed exceptions: 
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### function: golden_ledger/main.py::split_bill

[Machine-generated]
Divide the amount among people using Python 2 division. Integer inputs round toward negative infinity; zero divisors raise an error.

Observed return types: int
Observed exceptions: exceptions.TypeError, exceptions.ZeroDivisionError
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### function: golden_ledger/main.py::summarize

[Machine-generated]
Accumulate amounts from the balances mapping using iteritems. An empty mapping leaves the total at zero.

Observed return types: int
Observed exceptions: exceptions.TypeError
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### module: golden_ledger/main.py

[Machine-generated]
A small ledger module with bill division, mapping accumulation and integer parsing. Its main block prints examples. Integer division and legacy exception syntax require migration care.

Observed return types: 
Observed exceptions: 
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### package: golden_ledger

[Machine-generated]
The ledger is one module with three independent helpers and a demonstration main block. There are no project-local import dependencies. Rounding and error behavior follow the original Python 2 implementation.

Observed return types: 
Observed exceptions: 
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### Diff: _legacy_compat.py.diff

```diff
--- /dev/null
+++ b/_legacy_compat.py
@@ -0,0 +1,18 @@
+"""[Machine-generated] Compatibility for built-in numeric division."""
+
+
+def legacy_divide(left, right):
+    """[Machine-generated] Floor integer quotients; divide other numbers normally."""
+    # shortcut: custom Python 2 __div__ protocols are unsupported; review user-defined numeric types.
+    if isinstance(left, int) and isinstance(right, int):
+        return left // right
+    return left / right
+
+
+def legacy_int_error(error, value):
+    """[Machine-generated] Preserve byte-literal diagnostic rendering returned by the legacy API."""
+    message = str(error)
+    prefix = 'invalid literal for int() with base 10: '
+    if isinstance(value, bytes) and message.startswith(prefix + 'b'):
+        message = prefix + message[len(prefix) + 1:]
+    return message.encode('ascii')

```

### Diff: main.py.diff

```diff
--- a/main.py
+++ b/main.py
@@ -1,15 +1,19 @@
 u'[Machine-generated]\nA small ledger module with bill division, mapping accumulation and integer parsing. Its main block prints examples. Integer division and legacy exception syntax require migration care.\n\nObserved return types: \nObserved exceptions: \nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
+from __future__ import print_function
+
+
+from _legacy_compat import legacy_divide, legacy_int_error
 
 
 def split_bill(amount, people):
     u'[Machine-generated]\nDivide the amount among people using Python 2 division. Integer inputs round toward negative infinity; zero divisors raise an error.\n\nObserved return types: int\nObserved exceptions: exceptions.TypeError, exceptions.ZeroDivisionError\nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
-    return amount / people
+    return legacy_divide(amount, people)
 
 
 def summarize(balances):
     u'[Machine-generated]\nAccumulate amounts from the balances mapping using iteritems. An empty mapping leaves the total at zero.\n\nObserved return types: int\nObserved exceptions: exceptions.TypeError\nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
     total = 0
-    for name, amount in balances.iteritems():
+    for name, amount in list(balances.items()):
         total += amount
     return total
 
@@ -18,13 +22,13 @@
     u'[Machine-generated]\nParse an integer and turn ValueError into an invalid-prefix message. Other exceptions propagate, including invalid input types.\n\nObserved return types: int, str\nObserved exceptions: \nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
     try:
         return int(text)
-    except ValueError, error:
-        return 'invalid: ' + str(error)
+    except ValueError as error:
+        return b'invalid: ' + legacy_int_error(error, text)
 
 
 if __name__ == '__main__':
-    print 'split:', split_bill(7, 2), split_bill(-7, 2)
-    print 'total:', summarize({'Ada': 7, 'Lin': -2})
-    print 'empty:', summarize({})
-    print 'parsed:', parse_amount('12')
-    print 'bad:', parse_amount('bad')
+    print('split:', split_bill(7, 2), split_bill(-7, 2))
+    print('total:', summarize({'Ada': 7, 'Lin': -2}))
+    print('empty:', summarize({}))
+    print('parsed:', parse_amount('12'))
+    print('bad:', parse_amount('bad'))

```

## Policy results: text_pipeline

```json
{
  "failures": [],
  "heldout": {
    "pass_rate_percent": 100.0,
    "passed": 5,
    "tests": 5,
    "unresolved": []
  },
  "pass_rate_percent": 100.0,
  "passed": 40,
  "source_review_matches": true,
  "tests": 40,
  "training": {
    "pass_rate_percent": 100.0,
    "passed": 35,
    "tests": 35,
    "unresolved": []
  },
  "unresolved": []
}
```

## text_pipeline

### Evidence references

```json
{
  "baseline": "text_pipeline/baseline-modern.json",
  "characterization": "text_pipeline/characterization/private/runs.jsonl",
  "diffs": "text_pipeline/diffs/",
  "documentation": "text_pipeline/documentation/documentation.json",
  "heldout": "text_pipeline/heldout.json",
  "repair": "text_pipeline/repair/attempts.json",
  "training": "text_pipeline/repair/training-final.json"
}
```

### Coverage, exclusions and quarantines

```json
{
  "coverage": {
    "branches": {
      "covered": [],
      "missing": [],
      "percent": 100.0,
      "possible": []
    },
    "lines": {
      "covered": [
        "main.py:10",
        "main.py:11",
        "main.py:15",
        "main.py:19",
        "main.py:23",
        "main.py:24",
        "main.py:5",
        "main.py:6"
      ],
      "missing": [],
      "percent": 100.0,
      "possible": [
        "main.py:10",
        "main.py:11",
        "main.py:15",
        "main.py:19",
        "main.py:23",
        "main.py:24",
        "main.py:5",
        "main.py:6"
      ]
    }
  },
  "coverage_targets": {
    "branches": 90,
    "lines": 90
  },
  "inventory_exclusions": [
    {
      "line": 5,
      "path": "main.py",
      "reason": "nested callable exercised through enclosing function; not independently addressable"
    }
  ],
  "quarantine": []
}
```

### Repair attempts and usage

```json
{
  "attempts": [],
  "max_attempts_per_function": 2,
  "retry_counts": {}
}
```


```json
{
  "characterization": {
    "attempts": 5,
    "cost_complete": true,
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "conversion": {
    "attempts": 1,
    "cost_complete": true,
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "documentation": {
    "attempts": 7,
    "cost_complete": true,
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "repair": {
    "attempts": 0,
    "cost_complete": true,
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  }
}
```

### Unresolved failures

```json
[
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "type": "str",
              "value": "Ada"
            },
            {
              "type": "str",
              "value": "Lin"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[\" Ada \", \"\", \" Lin \"]]",
      "category": "typical",
      "files_json": "{}",
      "id": "726a9707f6b8681a538d",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: typical input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "clean_names"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "type": "unicode",
              "value": "Ada"
            },
            {
              "type": "unicode",
              "value": "Lin"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "726a9707f6b8681a538d",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "'NoneType' object has no attribute 'strip'"
            }
          ],
          "type": "tuple"
        },
        "message": "'NoneType' object has no attribute 'strip'",
        "module": "builtins",
        "name": "AttributeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[null]]",
      "category": "boundary",
      "files_json": "{}",
      "id": "11a4d8c58484fe3274dd",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: boundary input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "clean_names"
    },
    "expected": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "J05vbmVUeXBlJyBvYmplY3QgaGFzIG5vIGF0dHJpYnV0ZSAnc3RyaXAn",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "'NoneType' object has no attribute 'strip'",
        "module": "exceptions",
        "name": "AttributeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "11a4d8c58484fe3274dd",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "type": "str",
              "value": "caf\u00e9"
            },
            {
              "type": "str",
              "value": "\u96ea"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[\" caf\\u00e9 \", \"\\u96ea\"]]",
      "category": "unicode",
      "files_json": "{}",
      "id": "ab63227f76f8d0efd3ef",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: unicode input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "clean_names"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "type": "unicode",
              "value": "caf\u00e9"
            },
            {
              "type": "unicode",
              "value": "\u96ea"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "ab63227f76f8d0efd3ef",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "base64": "QQ==",
              "type": "bytes"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[{\"$bytes\": \"IEEg\"}, {\"$bytes\": \"\"}]]",
      "category": "bytes",
      "files_json": "{}",
      "id": "6c672f24c270e03d2a02",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: bytes input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "clean_names"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "base64": "QQ==",
              "type": "str"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "6c672f24c270e03d2a02",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "type": "str",
              "value": "\u03a9"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[\" \\u03a9 \", \"\"]]",
      "category": "edge",
      "files_json": "{}",
      "id": "c9f52cb8756079cab087",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[]",
      "target": "clean_names"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "type": "unicode",
              "value": "\u03a9"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "c9f52cb8756079cab087",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "type": "int",
              "value": "2"
            },
            {
              "items": [
                {
                  "items": [
                    {
                      "type": "int",
                      "value": "0"
                    },
                    {
                      "type": "str",
                      "value": "A"
                    }
                  ],
                  "type": "tuple"
                },
                {
                  "items": [
                    {
                      "type": "int",
                      "value": "1"
                    },
                    {
                      "type": "str",
                      "value": "B"
                    }
                  ],
                  "type": "tuple"
                }
              ],
              "type": "list"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[\"A\", \"B\"]]",
      "category": "typical",
      "files_json": "{}",
      "id": "56373a722e78d01fa485",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: typical input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "pair_names"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "type": "int",
              "value": "2"
            },
            {
              "items": [
                {
                  "items": [
                    {
                      "type": "int",
                      "value": "0"
                    },
                    {
                      "type": "unicode",
                      "value": "A"
                    }
                  ],
                  "type": "tuple"
                },
                {
                  "items": [
                    {
                      "type": "int",
                      "value": "1"
                    },
                    {
                      "type": "unicode",
                      "value": "B"
                    }
                  ],
                  "type": "tuple"
                }
              ],
              "type": "list"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "56373a722e78d01fa485",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "type": "int",
              "value": "2"
            },
            {
              "items": [
                {
                  "items": [
                    {
                      "type": "int",
                      "value": "0"
                    },
                    {
                      "type": "str",
                      "value": "\u00e9"
                    }
                  ],
                  "type": "tuple"
                },
                {
                  "items": [
                    {
                      "type": "int",
                      "value": "1"
                    },
                    {
                      "type": "str",
                      "value": "\u96ea"
                    }
                  ],
                  "type": "tuple"
                }
              ],
              "type": "list"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[\"\\u00e9\", \"\\u96ea\"]]",
      "category": "unicode",
      "files_json": "{}",
      "id": "01d3efe461a877d3b62a",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: unicode input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "pair_names"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "type": "int",
              "value": "2"
            },
            {
              "items": [
                {
                  "items": [
                    {
                      "type": "int",
                      "value": "0"
                    },
                    {
                      "type": "unicode",
                      "value": "\u00e9"
                    }
                  ],
                  "type": "tuple"
                },
                {
                  "items": [
                    {
                      "type": "int",
                      "value": "1"
                    },
                    {
                      "type": "unicode",
                      "value": "\u96ea"
                    }
                  ],
                  "type": "tuple"
                }
              ],
              "type": "list"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "01d3efe461a877d3b62a",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "type": "int",
              "value": "1"
            },
            {
              "items": [
                {
                  "items": [
                    {
                      "type": "int",
                      "value": "0"
                    },
                    {
                      "base64": "/w==",
                      "type": "bytes"
                    }
                  ],
                  "type": "tuple"
                }
              ],
              "type": "list"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[{\"$bytes\": \"/w==\"}]]",
      "category": "bytes",
      "files_json": "{}",
      "id": "b6384cd6d19716efb5d7",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: bytes input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "pair_names"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "type": "int",
              "value": "1"
            },
            {
              "items": [
                {
                  "items": [
                    {
                      "type": "int",
                      "value": "0"
                    },
                    {
                      "base64": "/w==",
                      "type": "str"
                    }
                  ],
                  "type": "tuple"
                }
              ],
              "type": "list"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "b6384cd6d19716efb5d7",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "type": "int",
              "value": "3"
            },
            {
              "items": [
                {
                  "items": [
                    {
                      "type": "int",
                      "value": "0"
                    },
                    {
                      "type": "str",
                      "value": "Solo"
                    }
                  ],
                  "type": "tuple"
                },
                {
                  "items": [
                    {
                      "type": "int",
                      "value": "1"
                    },
                    {
                      "type": "str",
                      "value": "Pair"
                    }
                  ],
                  "type": "tuple"
                },
                {
                  "items": [
                    {
                      "type": "int",
                      "value": "2"
                    },
                    {
                      "type": "str",
                      "value": "Third"
                    }
                  ],
                  "type": "tuple"
                }
              ],
              "type": "list"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[\"Solo\", \"Pair\", \"Third\"]]",
      "category": "typical",
      "files_json": "{}",
      "id": "4f30ef80e0425cb406e4",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[]",
      "target": "pair_names"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "type": "int",
              "value": "3"
            },
            {
              "items": [
                {
                  "items": [
                    {
                      "type": "int",
                      "value": "0"
                    },
                    {
                      "type": "unicode",
                      "value": "Solo"
                    }
                  ],
                  "type": "tuple"
                },
                {
                  "items": [
                    {
                      "type": "int",
                      "value": "1"
                    },
                    {
                      "type": "unicode",
                      "value": "Pair"
                    }
                  ],
                  "type": "tuple"
                },
                {
                  "items": [
                    {
                      "type": "int",
                      "value": "2"
                    },
                    {
                      "type": "unicode",
                      "value": "Third"
                    }
                  ],
                  "type": "tuple"
                }
              ],
              "type": "list"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "4f30ef80e0425cb406e4",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "YWJj",
          "type": "bytes"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[\"abc\"]",
      "category": "typical",
      "files_json": "{}",
      "id": "fddd3749f79f7ff16e94",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: typical input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "encode_label"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "YWJj",
          "type": "str"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "fddd3749f79f7ff16e94",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "'NoneType' object has no attribute 'encode'"
            }
          ],
          "type": "tuple"
        },
        "message": "'NoneType' object has no attribute 'encode'",
        "module": "builtins",
        "name": "AttributeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[null]",
      "category": "edge",
      "files_json": "{}",
      "id": "0fef156a3f6a59aa53a8",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: edge input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "encode_label"
    },
    "expected": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "J05vbmVUeXBlJyBvYmplY3QgaGFzIG5vIGF0dHJpYnV0ZSAnZW5jb2RlJw==",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "'NoneType' object has no attribute 'encode'",
        "module": "exceptions",
        "name": "AttributeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "0fef156a3f6a59aa53a8",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "",
          "type": "bytes"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[\"\"]",
      "category": "empty",
      "files_json": "{}",
      "id": "2d3ddf46fe4eef997dd2",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: empty input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "encode_label"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "",
          "type": "str"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "2d3ddf46fe4eef997dd2",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "AA==",
          "type": "bytes"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[\"\\u0000\"]",
      "category": "boundary",
      "files_json": "{}",
      "id": "5f2b1c611a9f837afaa0",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: boundary input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "encode_label"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "AA==",
          "type": "str"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "5f2b1c611a9f837afaa0",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "Y2Fmw6k=",
          "type": "bytes"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[\"caf\\u00e9\"]",
      "category": "unicode",
      "files_json": "{}",
      "id": "4d4aa3e3875bc16f4f64",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: unicode input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "encode_label"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "Y2Fmw6k=",
          "type": "str"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "4d4aa3e3875bc16f4f64",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "ascii"
            },
            {
              "base64": "/w==",
              "type": "bytes"
            },
            {
              "type": "int",
              "value": "0"
            },
            {
              "type": "int",
              "value": "1"
            },
            {
              "type": "str",
              "value": "ordinal not in range(128)"
            }
          ],
          "type": "tuple"
        },
        "message": "'ascii' codec can't decode byte 0xff in position 0: ordinal not in range(128)",
        "module": "builtins",
        "name": "UnicodeDecodeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"/w==\"}]",
      "category": "bytes",
      "files_json": "{}",
      "id": "6741ce7d68a4f00fe686",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: bytes input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "encode_label"
    },
    "expected": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "YXNjaWk=",
              "type": "str"
            },
            {
              "base64": "/w==",
              "type": "str"
            },
            {
              "type": "int",
              "value": "0"
            },
            {
              "type": "int",
              "value": "1"
            },
            {
              "base64": "b3JkaW5hbCBub3QgaW4gcmFuZ2UoMTI4KQ==",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "'ascii' codec can't decode byte 0xff in position 0: ordinal not in range(128)",
        "module": "exceptions",
        "name": "UnicodeDecodeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "6741ce7d68a4f00fe686",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "bmV3IHNub3cg6Zuq",
          "type": "bytes"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[\"new snow \\u96ea\"]",
      "category": "typical",
      "files_json": "{}",
      "id": "5742c42cdbf3aa960e4b",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[]",
      "target": "encode_label"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "bmV3IHNub3cg6Zuq",
          "type": "str"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "5742c42cdbf3aa960e4b",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "type": "str",
          "value": "abc"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"YWJj\"}]",
      "category": "typical",
      "files_json": "{}",
      "id": "0c4db0f662d8a9bafdd5",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: typical input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "decode_label"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "type": "unicode",
          "value": "abc"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "0c4db0f662d8a9bafdd5",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "utf-8"
            },
            {
              "base64": "/w==",
              "type": "bytes"
            },
            {
              "type": "int",
              "value": "0"
            },
            {
              "type": "int",
              "value": "1"
            },
            {
              "type": "str",
              "value": "invalid start byte"
            }
          ],
          "type": "tuple"
        },
        "message": "'utf-8' codec can't decode byte 0xff in position 0: invalid start byte",
        "module": "builtins",
        "name": "UnicodeDecodeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"/w==\"}]",
      "category": "edge",
      "files_json": "{}",
      "id": "c78c9c114ae67a202efd",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: edge input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "decode_label"
    },
    "expected": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "dXRmOA==",
              "type": "str"
            },
            {
              "base64": "/w==",
              "type": "str"
            },
            {
              "type": "int",
              "value": "0"
            },
            {
              "type": "int",
              "value": "1"
            },
            {
              "base64": "aW52YWxpZCBzdGFydCBieXRl",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "'utf8' codec can't decode byte 0xff in position 0: invalid start byte",
        "module": "exceptions",
        "name": "UnicodeDecodeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "c78c9c114ae67a202efd",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "type": "str",
          "value": ""
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"\"}]",
      "category": "empty",
      "files_json": "{}",
      "id": "1da4ece3f3dc25151a35",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: empty input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "decode_label"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "type": "unicode",
          "value": ""
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "1da4ece3f3dc25151a35",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "type": "str",
          "value": "\u0000"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"AA==\"}]",
      "category": "boundary",
      "files_json": "{}",
      "id": "21f941606c7c635eaf9b",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: boundary input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "decode_label"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "type": "unicode",
          "value": "\u0000"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "21f941606c7c635eaf9b",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "type": "str",
          "value": "caf\u00e9"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"Y2Fmw6k=\"}]",
      "category": "unicode",
      "files_json": "{}",
      "id": "2b14ad1e199ea9f019f2",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: unicode input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "decode_label"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "type": "unicode",
          "value": "caf\u00e9"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "2b14ad1e199ea9f019f2",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "ascii"
            },
            {
              "type": "str",
              "value": "\u00e9"
            },
            {
              "type": "int",
              "value": "0"
            },
            {
              "type": "int",
              "value": "1"
            },
            {
              "type": "str",
              "value": "ordinal not in range(128)"
            }
          ],
          "type": "tuple"
        },
        "message": "'ascii' codec can't encode character '\\xe9' in position 0: ordinal not in range(128)",
        "module": "builtins",
        "name": "UnicodeEncodeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[\"\\u00e9\"]",
      "category": "bytes",
      "files_json": "{}",
      "id": "269244e7fba00e42e183",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: bytes input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "decode_label"
    },
    "expected": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "YXNjaWk=",
              "type": "str"
            },
            {
              "type": "unicode",
              "value": "\u00e9"
            },
            {
              "type": "int",
              "value": "0"
            },
            {
              "type": "int",
              "value": "1"
            },
            {
              "base64": "b3JkaW5hbCBub3QgaW4gcmFuZ2UoMTI4KQ==",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "'ascii' codec can't encode character u'\\xe9' in position 0: ordinal not in range(128)",
        "module": "exceptions",
        "name": "UnicodeEncodeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "269244e7fba00e42e183",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "type": "str",
          "value": "new snow \u96ea"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"bmV3IHNub3cg6Zuq\"}]",
      "category": "typical",
      "files_json": "{}",
      "id": "8d429cba48aa6b9f5b89",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[]",
      "target": "decode_label"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "type": "unicode",
          "value": "new snow \u96ea"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "8d429cba48aa6b9f5b89",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "base64": "c3Ry",
              "type": "bytes"
            },
            {
              "base64": "dW5pY29kZQ==",
              "type": "bytes"
            },
            {
              "type": "int",
              "value": "3"
            },
            {
              "type": "int",
              "value": "3"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"YWJj\"}]",
      "category": "typical",
      "files_json": "{}",
      "id": "5c25be3b3eed8b4d6998",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: typical input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "describe"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "base64": "c3Ry",
              "type": "str"
            },
            {
              "base64": "dW5pY29kZQ==",
              "type": "str"
            },
            {
              "type": "int",
              "value": "3"
            },
            {
              "type": "int",
              "value": "3"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "5c25be3b3eed8b4d6998",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "utf-8"
            },
            {
              "base64": "/w==",
              "type": "bytes"
            },
            {
              "type": "int",
              "value": "0"
            },
            {
              "type": "int",
              "value": "1"
            },
            {
              "type": "str",
              "value": "invalid start byte"
            }
          ],
          "type": "tuple"
        },
        "message": "'utf-8' codec can't decode byte 0xff in position 0: invalid start byte",
        "module": "builtins",
        "name": "UnicodeDecodeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"/w==\"}]",
      "category": "edge",
      "files_json": "{}",
      "id": "5a45c6834552576fa83f",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: edge input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "describe"
    },
    "expected": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "dXRmOA==",
              "type": "str"
            },
            {
              "base64": "/w==",
              "type": "str"
            },
            {
              "type": "int",
              "value": "0"
            },
            {
              "type": "int",
              "value": "1"
            },
            {
              "base64": "aW52YWxpZCBzdGFydCBieXRl",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "'utf8' codec can't decode byte 0xff in position 0: invalid start byte",
        "module": "exceptions",
        "name": "UnicodeDecodeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "5a45c6834552576fa83f",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "base64": "c3Ry",
              "type": "bytes"
            },
            {
              "base64": "dW5pY29kZQ==",
              "type": "bytes"
            },
            {
              "type": "int",
              "value": "0"
            },
            {
              "type": "int",
              "value": "0"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"\"}]",
      "category": "empty",
      "files_json": "{}",
      "id": "6ec197437cb261363926",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: empty input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "describe"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "base64": "c3Ry",
              "type": "str"
            },
            {
              "base64": "dW5pY29kZQ==",
              "type": "str"
            },
            {
              "type": "int",
              "value": "0"
            },
            {
              "type": "int",
              "value": "0"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "6ec197437cb261363926",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "base64": "c3Ry",
              "type": "bytes"
            },
            {
              "base64": "dW5pY29kZQ==",
              "type": "bytes"
            },
            {
              "type": "int",
              "value": "1"
            },
            {
              "type": "int",
              "value": "1"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"AA==\"}]",
      "category": "boundary",
      "files_json": "{}",
      "id": "13a56036a6b33739aeef",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: boundary input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "describe"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "base64": "c3Ry",
              "type": "str"
            },
            {
              "base64": "dW5pY29kZQ==",
              "type": "str"
            },
            {
              "type": "int",
              "value": "1"
            },
            {
              "type": "int",
              "value": "1"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "13a56036a6b33739aeef",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "base64": "c3Ry",
              "type": "bytes"
            },
            {
              "base64": "dW5pY29kZQ==",
              "type": "bytes"
            },
            {
              "type": "int",
              "value": "5"
            },
            {
              "type": "int",
              "value": "4"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"Y2Fmw6k=\"}]",
      "category": "unicode",
      "files_json": "{}",
      "id": "2fb20be9aac20aadfc7d",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: unicode input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "describe"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "base64": "c3Ry",
              "type": "str"
            },
            {
              "base64": "dW5pY29kZQ==",
              "type": "str"
            },
            {
              "type": "int",
              "value": "5"
            },
            {
              "type": "int",
              "value": "4"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "2fb20be9aac20aadfc7d",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "ascii"
            },
            {
              "type": "str",
              "value": "\u00e9"
            },
            {
              "type": "int",
              "value": "0"
            },
            {
              "type": "int",
              "value": "1"
            },
            {
              "type": "str",
              "value": "ordinal not in range(128)"
            }
          ],
          "type": "tuple"
        },
        "message": "'ascii' codec can't encode character '\\xe9' in position 0: ordinal not in range(128)",
        "module": "builtins",
        "name": "UnicodeEncodeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[\"\\u00e9\"]",
      "category": "bytes",
      "files_json": "{}",
      "id": "42feeb19a65990275c63",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: bytes input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "describe"
    },
    "expected": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "YXNjaWk=",
              "type": "str"
            },
            {
              "type": "unicode",
              "value": "\u00e9"
            },
            {
              "type": "int",
              "value": "0"
            },
            {
              "type": "int",
              "value": "1"
            },
            {
              "base64": "b3JkaW5hbCBub3QgaW4gcmFuZ2UoMTI4KQ==",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "'ascii' codec can't encode character u'\\xe9' in position 0: ordinal not in range(128)",
        "module": "exceptions",
        "name": "UnicodeEncodeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "42feeb19a65990275c63",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "base64": "c3Ry",
              "type": "bytes"
            },
            {
              "base64": "dW5pY29kZQ==",
              "type": "bytes"
            },
            {
              "type": "int",
              "value": "12"
            },
            {
              "type": "int",
              "value": "11"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"bmV3IGJ5dGVzIMOp\"}]",
      "category": "typical",
      "files_json": "{}",
      "id": "aebb18292b9abf354ad4",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[]",
      "target": "describe"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "base64": "c3Ry",
              "type": "str"
            },
            {
              "base64": "dW5pY29kZQ==",
              "type": "str"
            },
            {
              "type": "int",
              "value": "12"
            },
            {
              "type": "int",
              "value": "11"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "aebb18292b9abf354ad4",
    "run": "text_pipeline/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "type": "str",
              "value": "New Name"
            },
            {
              "type": "str",
              "value": "C"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[\"  New Name  \", \" \", \" C \"]]",
      "category": "typical",
      "files_json": "{}",
      "id": "42b89a699ab83b5f3856",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[]",
      "target": "clean_names"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "type": "unicode",
              "value": "New Name"
            },
            {
              "type": "unicode",
              "value": "C"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "42b89a699ab83b5f3856",
    "run": "text_pipeline/heldout.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "type": "int",
              "value": "2"
            },
            {
              "items": [
                {
                  "items": [
                    {
                      "type": "int",
                      "value": "0"
                    },
                    {
                      "base64": "WA==",
                      "type": "bytes"
                    }
                  ],
                  "type": "tuple"
                },
                {
                  "items": [
                    {
                      "type": "int",
                      "value": "1"
                    },
                    {
                      "base64": "WQ==",
                      "type": "bytes"
                    }
                  ],
                  "type": "tuple"
                }
              ],
              "type": "list"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[{\"$bytes\": \"WA==\"}, {\"$bytes\": \"WQ==\"}]]",
      "category": "edge",
      "files_json": "{}",
      "id": "33b228c4e42487c9a63d",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[]",
      "target": "pair_names"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "type": "int",
              "value": "2"
            },
            {
              "items": [
                {
                  "items": [
                    {
                      "type": "int",
                      "value": "0"
                    },
                    {
                      "base64": "WA==",
                      "type": "str"
                    }
                  ],
                  "type": "tuple"
                },
                {
                  "items": [
                    {
                      "type": "int",
                      "value": "1"
                    },
                    {
                      "base64": "WQ==",
                      "type": "str"
                    }
                  ],
                  "type": "tuple"
                }
              ],
              "type": "list"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "33b228c4e42487c9a63d",
    "run": "text_pipeline/heldout.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "QVNDSUktbmV3",
          "type": "bytes"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"QVNDSUktbmV3\"}]",
      "category": "edge",
      "files_json": "{}",
      "id": "446fb20edf5d6a3deb0f",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[]",
      "target": "encode_label"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "QVNDSUktbmV3",
          "type": "str"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "446fb20edf5d6a3deb0f",
    "run": "text_pipeline/heldout.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "type": "str",
          "value": "ASCII-new-two"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"QVNDSUktbmV3LXR3bw==\"}]",
      "category": "edge",
      "files_json": "{}",
      "id": "595090ca9a685ee0cd7c",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[]",
      "target": "decode_label"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "type": "unicode",
          "value": "ASCII-new-two"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "595090ca9a685ee0cd7c",
    "run": "text_pipeline/heldout.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "base64": "c3Ry",
              "type": "bytes"
            },
            {
              "base64": "dW5pY29kZQ==",
              "type": "bytes"
            },
            {
              "type": "int",
              "value": "9"
            },
            {
              "type": "int",
              "value": "9"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"bmV3LWFzY2lp\"}]",
      "category": "edge",
      "files_json": "{}",
      "id": "66930f8150d68ee345ce",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[]",
      "target": "describe"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            {
              "base64": "c3Ry",
              "type": "str"
            },
            {
              "base64": "dW5pY29kZQ==",
              "type": "str"
            },
            {
              "type": "int",
              "value": "9"
            },
            {
              "type": "int",
              "value": "9"
            }
          ],
          "type": "tuple"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "66930f8150d68ee345ce",
    "run": "text_pipeline/heldout.json"
  }
]
```

### Review flags and suspected legacy bugs

```json
[
  "List materialization is supplied by deterministic map/filter/zip fixers and requires CP9 behavioral verification.",
  "Unicode/byte runtime return tags and precise exception records remain unverified until CP9."
]
```


```json
[]
```

### Documentation omissions and claim mismatches

```json
{
  "mismatches": [],
  "omitted": [
    {
      "key": "text_pipeline/main.py::clean_names.<lambda@5:19>",
      "reason": "lambda expressions have no writable docstring suite; documented by enclosing function"
    }
  ]
}
```

### function: text_pipeline/main.py::clean_names

[Machine-generated]
Strip each supplied name, then remove false-valued results. Python 2 map and filter materialize lists. The nested lambda belongs to this helper.

Observed return types: list
Observed exceptions: exceptions.AttributeError
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### function: text_pipeline/main.py::decode_label

[Machine-generated]
Call the supplied value's UTF-8 decode method. Byte strings can produce Unicode text or raise decoding errors.

Observed return types: unicode
Observed exceptions: exceptions.UnicodeDecodeError, exceptions.UnicodeEncodeError
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### function: text_pipeline/main.py::describe

[Machine-generated]
Decode the supplied value through decode_label, then return original and decoded type names and their lengths. Byte length and Unicode character count can differ.

Observed return types: tuple
Observed exceptions: exceptions.UnicodeDecodeError, exceptions.UnicodeEncodeError
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### function: text_pipeline/main.py::encode_label

[Machine-generated]
Call the label's UTF-8 encode method. In Python 2 encoding Unicode text produces a byte string; inputs that cannot be encoded retain their legacy exceptions.

Observed return types: str
Observed exceptions: exceptions.AttributeError, exceptions.UnicodeDecodeError
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### function: text_pipeline/main.py::pair_names

[Machine-generated]
Pair zero-based positions with names and return the pair count together with the pairs. Python 2 zip produces a list.

Observed return types: tuple
Observed exceptions: 
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### module: text_pipeline/main.py

[Machine-generated]
Text helpers strip/filter names, attach positions, encode and decode UTF-8, and describe lengths and types. describe calls decode_label. The main block prints examples using Python 2 print syntax.

Observed return types: 
Observed exceptions: 
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### package: text_pipeline

[Machine-generated]
One module implements a text-processing demonstration. Name cleaning and pairing use list-returning Python 2 builtins; UTF-8 helpers expose byte versus Unicode behavior. These distinctions must survive modernization.

Observed return types: 
Observed exceptions: 
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### Diff: main.py.diff

```diff
--- a/main.py
+++ b/main.py
@@ -1,40 +1,46 @@
 u'[Machine-generated]\nText helpers strip/filter names, attach positions, encode and decode UTF-8, and describe lengths and types. describe calls decode_label. The main block prints examples using Python 2 print syntax.\n\nObserved return types: \nObserved exceptions: \nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
+from __future__ import print_function
 
 
 def clean_names(names):
     u'[Machine-generated]\nStrip each supplied name, then remove false-valued results. Python 2 map and filter materialize lists. The nested lambda belongs to this helper.\n\nObserved return types: list\nObserved exceptions: exceptions.AttributeError\nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
-    stripped = map(lambda name: name.strip(), names)
-    return filter(None, stripped)
+    stripped = [name.strip() for name in names]
+    return [_f for _f in stripped if _f]
 
 
 def pair_names(names):
     u'[Machine-generated]\nPair zero-based positions with names and return the pair count together with the pairs. Python 2 zip produces a list.\n\nObserved return types: tuple\nObserved exceptions: \nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
-    pairs = zip(range(len(names)), names)
+    pairs = list(zip(list(range(len(names))), names))
     return len(pairs), pairs
 
 
 def encode_label(label):
     u"[Machine-generated]\nCall the label's UTF-8 encode method. In Python 2 encoding Unicode text produces a byte string; inputs that cannot be encoded retain their legacy exceptions.\n\nObserved return types: str\nObserved exceptions: exceptions.AttributeError, exceptions.UnicodeDecodeError\nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven."
-    return label.encode('utf-8')
+    return label.decode('ascii').encode('utf-8') if isinstance(label, bytes) else label.encode('utf-8')
 
 
 def decode_label(raw):
     u"[Machine-generated]\nCall the supplied value's UTF-8 decode method. Byte strings can produce Unicode text or raise decoding errors.\n\nObserved return types: unicode\nObserved exceptions: exceptions.UnicodeDecodeError, exceptions.UnicodeEncodeError\nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven."
-    return raw.decode('utf-8')
+    return raw.encode('ascii').decode('utf-8') if isinstance(raw, str) else raw.decode('utf-8')
+
+
+def _legacy_type_name(value):
+    """[Machine-generated] Report built-in text type names using the original byte labels."""
+    return {bytes: b'str', str: b'unicode'}.get(type(value), type(value).__name__.encode('ascii'))
 
 
 def describe(raw):
     u'[Machine-generated]\nDecode the supplied value through decode_label, then return original and decoded type names and their lengths. Byte length and Unicode character count can differ.\n\nObserved return types: tuple\nObserved exceptions: exceptions.UnicodeDecodeError, exceptions.UnicodeEncodeError\nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
     text = decode_label(raw)
-    return type(raw).__name__, type(text).__name__, len(raw), len(text)
+    return _legacy_type_name(raw), _legacy_type_name(text), len(raw), len(text)
 
 
 if __name__ == '__main__':
     names = clean_names([u' Ada ', u'', u' Lin '])
-    print 'names:', repr(names)
-    print 'pairs:', repr(pair_names(names))
-    print 'empty:', repr(pair_names(clean_names([])))
+    print('names:', repr(names))
+    print('pairs:', repr(pair_names(names)))
+    print('empty:', repr(pair_names(clean_names([]))))
     raw = encode_label(u'caf\u00e9')
-    print 'encoded:', repr(raw)
-    print 'decoded:', repr(decode_label(raw))
-    print 'types:', repr(describe(raw))
+    print('encoded:', repr(raw))
+    print('decoded:', repr(decode_label(raw)))
+    print('types:', repr(describe(raw)))

```

## Policy results: ranking

```json
{
  "failures": [],
  "heldout": {
    "pass_rate_percent": 100.0,
    "passed": 4,
    "tests": 4,
    "unresolved": []
  },
  "pass_rate_percent": 100.0,
  "passed": 28,
  "source_review_matches": true,
  "tests": 28,
  "training": {
    "pass_rate_percent": 100.0,
    "passed": 24,
    "tests": 24,
    "unresolved": []
  },
  "unresolved": []
}
```

## ranking

### Evidence references

```json
{
  "baseline": "ranking/baseline-modern.json",
  "characterization": "ranking/characterization/private/runs.jsonl",
  "diffs": "ranking/diffs/",
  "documentation": "ranking/documentation/documentation.json",
  "heldout": "ranking/heldout.json",
  "repair": "ranking/repair/attempts.json",
  "training": "ranking/repair/training-final.json"
}
```

### Coverage, exclusions and quarantines

```json
{
  "coverage": {
    "branches": {
      "covered": [
        "main.py:6:7",
        "main.py:6:8"
      ],
      "missing": [],
      "percent": 100.0,
      "possible": [
        "main.py:6:7",
        "main.py:6:8"
      ]
    },
    "lines": {
      "covered": [
        "main.py:13",
        "main.py:16",
        "main.py:19",
        "main.py:20",
        "main.py:21",
        "main.py:5",
        "main.py:6",
        "main.py:7",
        "main.py:8"
      ],
      "missing": [],
      "percent": 100.0,
      "possible": [
        "main.py:13",
        "main.py:16",
        "main.py:19",
        "main.py:20",
        "main.py:21",
        "main.py:5",
        "main.py:6",
        "main.py:7",
        "main.py:8"
      ]
    }
  },
  "coverage_targets": {
    "branches": 90,
    "lines": 90
  },
  "inventory_exclusions": [],
  "quarantine": []
}
```

### Repair attempts and usage

```json
{
  "attempts": [],
  "max_attempts_per_function": 2,
  "retry_counts": {}
}
```


```json
{
  "characterization": {
    "attempts": 4,
    "cost_complete": true,
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "conversion": {
    "attempts": 1,
    "cost_complete": true,
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "documentation": {
    "attempts": 7,
    "cost_complete": true,
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "repair": {
    "attempts": 0,
    "cost_complete": true,
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  }
}
```

### Unresolved failures

```json
[
  {
    "actual": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "list index out of range"
            }
          ],
          "type": "tuple"
        },
        "message": "list index out of range",
        "module": "builtins",
        "name": "IndexError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[], []]",
      "category": "empty",
      "files_json": "{}",
      "id": "de9cc2d30b487c37f8cd",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: empty input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "compare_scores"
    },
    "expected": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "bGlzdCBpbmRleCBvdXQgb2YgcmFuZ2U=",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "list index out of range",
        "module": "exceptions",
        "name": "IndexError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "de9cc2d30b487c37f8cd",
    "run": "ranking/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "type": "str",
                "value": "scores"
              },
              {
                "items": [],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "type": "NoneType"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[]",
      "category": "typical",
      "files_json": "{}",
      "id": "46b4ec53acffc20e3556",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: typical input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "Scoreboard.__init__"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "base64": "c2NvcmVz",
                "type": "str"
              },
              {
                "items": [],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "type": "NoneType"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "46b4ec53acffc20e3556",
    "run": "ranking/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "Scoreboard.__init__() takes 1 positional argument but 2 were given"
            }
          ],
          "type": "tuple"
        },
        "message": "Scoreboard.__init__() takes 1 positional argument but 2 were given",
        "module": "builtins",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[0]",
      "category": "edge",
      "files_json": "{}",
      "id": "48b0a70fa1e90a5ce78a",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: edge input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "Scoreboard.__init__"
    },
    "expected": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "X19pbml0X18oKSB0YWtlcyBleGFjdGx5IDEgYXJndW1lbnQgKDIgZ2l2ZW4p",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "__init__() takes exactly 1 argument (2 given)",
        "module": "exceptions",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "48b0a70fa1e90a5ce78a",
    "run": "ranking/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "Scoreboard.__init__() takes 1 positional argument but 4 were given"
            }
          ],
          "type": "tuple"
        },
        "message": "Scoreboard.__init__() takes 1 positional argument but 4 were given",
        "module": "builtins",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[1, 2, 3]",
      "category": "edge",
      "files_json": "{}",
      "id": "cc4f6371ad98c1e86af9",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[]",
      "target": "Scoreboard.__init__"
    },
    "expected": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "X19pbml0X18oKSB0YWtlcyBleGFjdGx5IDEgYXJndW1lbnQgKDQgZ2l2ZW4p",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "__init__() takes exactly 1 argument (4 given)",
        "module": "exceptions",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "cc4f6371ad98c1e86af9",
    "run": "ranking/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "type": "str",
                "value": "scores"
              },
              {
                "items": [
                  [
                    {
                      "type": "str",
                      "value": "Ada"
                    },
                    {
                      "type": "int",
                      "value": "7"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "type": "NoneType"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[\"Ada\", 7]",
      "category": "typical",
      "files_json": "{}",
      "id": "802d468fafe139f8574a",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: typical input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "Scoreboard.add"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "base64": "c2NvcmVz",
                "type": "str"
              },
              {
                "items": [
                  [
                    {
                      "type": "unicode",
                      "value": "Ada"
                    },
                    {
                      "type": "int",
                      "value": "7"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "type": "NoneType"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "802d468fafe139f8574a",
    "run": "ranking/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "type": "str",
                "value": "scores"
              },
              {
                "items": [
                  [
                    {
                      "type": "str",
                      "value": "Ada"
                    },
                    {
                      "type": "int",
                      "value": "2"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "type": "NoneType"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[\"Ada\", -2]",
      "category": "edge",
      "files_json": "{}",
      "id": "1fc9a907d97efcc99436",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: edge input; observe legacy outcome only.",
      "setup_json": "[{\"method\": \"add\", \"args\": [\"Ada\", 4], \"kwargs\": {}}]",
      "target": "Scoreboard.add"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "base64": "c2NvcmVz",
                "type": "str"
              },
              {
                "items": [
                  [
                    {
                      "type": "unicode",
                      "value": "Ada"
                    },
                    {
                      "type": "int",
                      "value": "2"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "type": "NoneType"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "1fc9a907d97efcc99436",
    "run": "ranking/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "type": "str",
                "value": "scores"
              },
              {
                "items": [
                  [
                    {
                      "type": "str",
                      "value": ""
                    },
                    {
                      "type": "int",
                      "value": "0"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "type": "NoneType"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[\"\", 0]",
      "category": "empty",
      "files_json": "{}",
      "id": "caf3b9ff00e0c8db5c45",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: empty input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "Scoreboard.add"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "base64": "c2NvcmVz",
                "type": "str"
              },
              {
                "items": [
                  [
                    {
                      "type": "unicode",
                      "value": ""
                    },
                    {
                      "type": "int",
                      "value": "0"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "type": "NoneType"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "caf3b9ff00e0c8db5c45",
    "run": "ranking/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "type": "str",
                "value": "scores"
              },
              {
                "items": [
                  [
                    {
                      "type": "str",
                      "value": "Ada"
                    },
                    {
                      "type": "int",
                      "value": "0"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "type": "NoneType"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[\"Ada\", 0]",
      "category": "boundary",
      "files_json": "{}",
      "id": "9dfaa77b8cd1ae7f6062",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: boundary input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "Scoreboard.add"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "base64": "c2NvcmVz",
                "type": "str"
              },
              {
                "items": [
                  [
                    {
                      "type": "unicode",
                      "value": "Ada"
                    },
                    {
                      "type": "int",
                      "value": "0"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "type": "NoneType"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "9dfaa77b8cd1ae7f6062",
    "run": "ranking/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "type": "str",
                "value": "scores"
              },
              {
                "items": [
                  [
                    {
                      "type": "str",
                      "value": "\u00e9"
                    },
                    {
                      "type": "int",
                      "value": "5"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "type": "NoneType"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[\"\\u00e9\", 5]",
      "category": "unicode",
      "files_json": "{}",
      "id": "f51a64f2ccc20ad6cd59",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: unicode input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "Scoreboard.add"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "base64": "c2NvcmVz",
                "type": "str"
              },
              {
                "items": [
                  [
                    {
                      "type": "unicode",
                      "value": "\u00e9"
                    },
                    {
                      "type": "int",
                      "value": "5"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "type": "NoneType"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "f51a64f2ccc20ad6cd59",
    "run": "ranking/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "type": "str",
                "value": "scores"
              },
              {
                "items": [
                  [
                    {
                      "base64": "/w==",
                      "type": "bytes"
                    },
                    {
                      "type": "int",
                      "value": "1"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "type": "NoneType"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"/w==\"}, 1]",
      "category": "bytes",
      "files_json": "{}",
      "id": "be9ef3d6da9141b3433d",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: bytes input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "Scoreboard.add"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "base64": "c2NvcmVz",
                "type": "str"
              },
              {
                "items": [
                  [
                    {
                      "base64": "/w==",
                      "type": "str"
                    },
                    {
                      "type": "int",
                      "value": "1"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "type": "NoneType"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "be9ef3d6da9141b3433d",
    "run": "ranking/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "type": "str",
                "value": "scores"
              },
              {
                "items": [
                  [
                    {
                      "base64": "TmV3Qg==",
                      "type": "bytes"
                    },
                    {
                      "type": "int",
                      "value": "17"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "type": "NoneType"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"TmV3Qg==\"}, 17]",
      "category": "edge",
      "files_json": "{}",
      "id": "50e5bc897f8bd5d0f3bb",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[]",
      "target": "Scoreboard.add"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "base64": "c2NvcmVz",
                "type": "str"
              },
              {
                "items": [
                  [
                    {
                      "base64": "TmV3Qg==",
                      "type": "str"
                    },
                    {
                      "type": "int",
                      "value": "17"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "type": "NoneType"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "50e5bc897f8bd5d0f3bb",
    "run": "ranking/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "type": "str",
                "value": "scores"
              },
              {
                "items": [
                  [
                    {
                      "type": "str",
                      "value": "Ada"
                    },
                    {
                      "type": "int",
                      "value": "7"
                    }
                  ],
                  [
                    {
                      "type": "str",
                      "value": "Lin"
                    },
                    {
                      "type": "int",
                      "value": "4"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "items": [
            {
              "items": [
                {
                  "type": "str",
                  "value": "Ada"
                },
                {
                  "type": "int",
                  "value": "7"
                }
              ],
              "type": "tuple"
            },
            {
              "items": [
                {
                  "type": "str",
                  "value": "Lin"
                },
                {
                  "type": "int",
                  "value": "4"
                }
              ],
              "type": "tuple"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[]",
      "category": "typical",
      "files_json": "{}",
      "id": "e14fba78f97e7c5681d8",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: typical input; observe legacy outcome only.",
      "setup_json": "[{\"method\": \"add\", \"args\": [\"Ada\", 7], \"kwargs\": {}}, {\"method\": \"add\", \"args\": [\"Lin\", 4], \"kwargs\": {}}]",
      "target": "Scoreboard.ranked"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "base64": "c2NvcmVz",
                "type": "str"
              },
              {
                "items": [
                  [
                    {
                      "type": "unicode",
                      "value": "Ada"
                    },
                    {
                      "type": "int",
                      "value": "7"
                    }
                  ],
                  [
                    {
                      "type": "unicode",
                      "value": "Lin"
                    },
                    {
                      "type": "int",
                      "value": "4"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "items": [
            {
              "items": [
                {
                  "type": "unicode",
                  "value": "Ada"
                },
                {
                  "type": "int",
                  "value": "7"
                }
              ],
              "type": "tuple"
            },
            {
              "items": [
                {
                  "type": "unicode",
                  "value": "Lin"
                },
                {
                  "type": "int",
                  "value": "4"
                }
              ],
              "type": "tuple"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "e14fba78f97e7c5681d8",
    "run": "ranking/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "type": "str",
                "value": "scores"
              },
              {
                "items": [
                  [
                    {
                      "type": "str",
                      "value": "Bob"
                    },
                    {
                      "type": "int",
                      "value": "7"
                    }
                  ],
                  [
                    {
                      "type": "str",
                      "value": "ada"
                    },
                    {
                      "type": "int",
                      "value": "7"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "items": [
            {
              "items": [
                {
                  "type": "str",
                  "value": "ada"
                },
                {
                  "type": "int",
                  "value": "7"
                }
              ],
              "type": "tuple"
            },
            {
              "items": [
                {
                  "type": "str",
                  "value": "Bob"
                },
                {
                  "type": "int",
                  "value": "7"
                }
              ],
              "type": "tuple"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[]",
      "category": "edge",
      "files_json": "{}",
      "id": "4b2402edf0cf8c4c3f54",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: edge input; observe legacy outcome only.",
      "setup_json": "[{\"method\": \"add\", \"args\": [\"Bob\", 7], \"kwargs\": {}}, {\"method\": \"add\", \"args\": [\"ada\", 7], \"kwargs\": {}}]",
      "target": "Scoreboard.ranked"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "base64": "c2NvcmVz",
                "type": "str"
              },
              {
                "items": [
                  [
                    {
                      "type": "unicode",
                      "value": "Bob"
                    },
                    {
                      "type": "int",
                      "value": "7"
                    }
                  ],
                  [
                    {
                      "type": "unicode",
                      "value": "ada"
                    },
                    {
                      "type": "int",
                      "value": "7"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "items": [
            {
              "items": [
                {
                  "type": "unicode",
                  "value": "ada"
                },
                {
                  "type": "int",
                  "value": "7"
                }
              ],
              "type": "tuple"
            },
            {
              "items": [
                {
                  "type": "unicode",
                  "value": "Bob"
                },
                {
                  "type": "int",
                  "value": "7"
                }
              ],
              "type": "tuple"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "4b2402edf0cf8c4c3f54",
    "run": "ranking/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "type": "str",
                "value": "scores"
              },
              {
                "items": [],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "items": [],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[]",
      "category": "empty",
      "files_json": "{}",
      "id": "52d2dbb5c21652fa43ba",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: empty input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "Scoreboard.ranked"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "base64": "c2NvcmVz",
                "type": "str"
              },
              {
                "items": [],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "items": [],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "52d2dbb5c21652fa43ba",
    "run": "ranking/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "type": "str",
                "value": "scores"
              },
              {
                "items": [
                  [
                    {
                      "type": "str",
                      "value": "A"
                    },
                    {
                      "type": "int",
                      "value": "0"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "items": [
            {
              "items": [
                {
                  "type": "str",
                  "value": "A"
                },
                {
                  "type": "int",
                  "value": "0"
                }
              ],
              "type": "tuple"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[]",
      "category": "boundary",
      "files_json": "{}",
      "id": "7fb896b5f23e0f1df46b",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: boundary input; observe legacy outcome only.",
      "setup_json": "[{\"method\": \"add\", \"args\": [\"A\", 0], \"kwargs\": {}}]",
      "target": "Scoreboard.ranked"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "base64": "c2NvcmVz",
                "type": "str"
              },
              {
                "items": [
                  [
                    {
                      "type": "unicode",
                      "value": "A"
                    },
                    {
                      "type": "int",
                      "value": "0"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "items": [
            {
              "items": [
                {
                  "type": "unicode",
                  "value": "A"
                },
                {
                  "type": "int",
                  "value": "0"
                }
              ],
              "type": "tuple"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "7fb896b5f23e0f1df46b",
    "run": "ranking/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "type": "str",
                "value": "scores"
              },
              {
                "items": [
                  [
                    {
                      "type": "str",
                      "value": "\u00e9"
                    },
                    {
                      "type": "int",
                      "value": "2"
                    }
                  ],
                  [
                    {
                      "type": "str",
                      "value": "\u96ea"
                    },
                    {
                      "type": "int",
                      "value": "1"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "items": [
            {
              "items": [
                {
                  "type": "str",
                  "value": "\u00e9"
                },
                {
                  "type": "int",
                  "value": "2"
                }
              ],
              "type": "tuple"
            },
            {
              "items": [
                {
                  "type": "str",
                  "value": "\u96ea"
                },
                {
                  "type": "int",
                  "value": "1"
                }
              ],
              "type": "tuple"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[]",
      "category": "unicode",
      "files_json": "{}",
      "id": "361aab45580a01185bcd",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: unicode input; observe legacy outcome only.",
      "setup_json": "[{\"method\": \"add\", \"args\": [\"\\u00e9\", 2], \"kwargs\": {}}, {\"method\": \"add\", \"args\": [\"\\u96ea\", 1], \"kwargs\": {}}]",
      "target": "Scoreboard.ranked"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "base64": "c2NvcmVz",
                "type": "str"
              },
              {
                "items": [
                  [
                    {
                      "type": "unicode",
                      "value": "\u00e9"
                    },
                    {
                      "type": "int",
                      "value": "2"
                    }
                  ],
                  [
                    {
                      "type": "unicode",
                      "value": "\u96ea"
                    },
                    {
                      "type": "int",
                      "value": "1"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "items": [
            {
              "items": [
                {
                  "type": "unicode",
                  "value": "\u00e9"
                },
                {
                  "type": "int",
                  "value": "2"
                }
              ],
              "type": "tuple"
            },
            {
              "items": [
                {
                  "type": "unicode",
                  "value": "\u96ea"
                },
                {
                  "type": "int",
                  "value": "1"
                }
              ],
              "type": "tuple"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "361aab45580a01185bcd",
    "run": "ranking/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "type": "str",
                "value": "scores"
              },
              {
                "items": [
                  [
                    {
                      "base64": "QQ==",
                      "type": "bytes"
                    },
                    {
                      "type": "int",
                      "value": "3"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "items": [
            {
              "items": [
                {
                  "base64": "QQ==",
                  "type": "bytes"
                },
                {
                  "type": "int",
                  "value": "3"
                }
              ],
              "type": "tuple"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[]",
      "category": "bytes",
      "files_json": "{}",
      "id": "f96e5a01843f84546806",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Coding LLM proposal: bytes input; observe legacy outcome only.",
      "setup_json": "[{\"method\": \"add\", \"args\": [{\"$bytes\": \"QQ==\"}, 3], \"kwargs\": {}}]",
      "target": "Scoreboard.ranked"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "base64": "c2NvcmVz",
                "type": "str"
              },
              {
                "items": [
                  [
                    {
                      "base64": "QQ==",
                      "type": "str"
                    },
                    {
                      "type": "int",
                      "value": "3"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "items": [
            {
              "items": [
                {
                  "base64": "QQ==",
                  "type": "str"
                },
                {
                  "type": "int",
                  "value": "3"
                }
              ],
              "type": "tuple"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "f96e5a01843f84546806",
    "run": "ranking/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "type": "str",
                "value": "scores"
              },
              {
                "items": [
                  [
                    {
                      "type": "str",
                      "value": "NewA"
                    },
                    {
                      "type": "int",
                      "value": "17"
                    }
                  ],
                  [
                    {
                      "type": "str",
                      "value": "NewB"
                    },
                    {
                      "type": "int",
                      "value": "19"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "items": [
            {
              "items": [
                {
                  "type": "str",
                  "value": "NewB"
                },
                {
                  "type": "int",
                  "value": "19"
                }
              ],
              "type": "tuple"
            },
            {
              "items": [
                {
                  "type": "str",
                  "value": "NewA"
                },
                {
                  "type": "int",
                  "value": "17"
                }
              ],
              "type": "tuple"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[]",
      "category": "typical",
      "files_json": "{}",
      "id": "ad7df8853af92065aca2",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[{\"method\": \"add\", \"args\": [\"NewA\", 17], \"kwargs\": {}}, {\"method\": \"add\", \"args\": [\"NewB\", 19], \"kwargs\": {}}]",
      "target": "Scoreboard.ranked"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "base64": "c2NvcmVz",
                "type": "str"
              },
              {
                "items": [
                  [
                    {
                      "type": "unicode",
                      "value": "NewA"
                    },
                    {
                      "type": "int",
                      "value": "17"
                    }
                  ],
                  [
                    {
                      "type": "unicode",
                      "value": "NewB"
                    },
                    {
                      "type": "int",
                      "value": "19"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "items": [
            {
              "items": [
                {
                  "type": "unicode",
                  "value": "NewB"
                },
                {
                  "type": "int",
                  "value": "19"
                }
              ],
              "type": "tuple"
            },
            {
              "items": [
                {
                  "type": "unicode",
                  "value": "NewA"
                },
                {
                  "type": "int",
                  "value": "17"
                }
              ],
              "type": "tuple"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "ad7df8853af92065aca2",
    "run": "ranking/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "Scoreboard.__init__() takes 1 positional argument but 3 were given"
            }
          ],
          "type": "tuple"
        },
        "message": "Scoreboard.__init__() takes 1 positional argument but 3 were given",
        "module": "builtins",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[1, 2]",
      "category": "typical",
      "files_json": "{}",
      "id": "45244655d18a1e3c6b00",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[]",
      "target": "Scoreboard.__init__"
    },
    "expected": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "X19pbml0X18oKSB0YWtlcyBleGFjdGx5IDEgYXJndW1lbnQgKDMgZ2l2ZW4p",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "__init__() takes exactly 1 argument (3 given)",
        "module": "exceptions",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "45244655d18a1e3c6b00",
    "run": "ranking/heldout.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "type": "str",
                "value": "scores"
              },
              {
                "items": [
                  [
                    {
                      "type": "str",
                      "value": "NewA"
                    },
                    {
                      "type": "int",
                      "value": "9"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "type": "NoneType"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[\"NewA\", 9]",
      "category": "typical",
      "files_json": "{}",
      "id": "47ae97fb631c75721b86",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[]",
      "target": "Scoreboard.add"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "base64": "c2NvcmVz",
                "type": "str"
              },
              {
                "items": [
                  [
                    {
                      "type": "unicode",
                      "value": "NewA"
                    },
                    {
                      "type": "int",
                      "value": "9"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "type": "NoneType"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "47ae97fb631c75721b86",
    "run": "ranking/heldout.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "type": "str",
                "value": "scores"
              },
              {
                "items": [
                  [
                    {
                      "type": "str",
                      "value": "NewC"
                    },
                    {
                      "type": "int",
                      "value": "23"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "items": [
            {
              "items": [
                {
                  "type": "str",
                  "value": "NewC"
                },
                {
                  "type": "int",
                  "value": "23"
                }
              ],
              "type": "tuple"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[]",
      "category": "edge",
      "files_json": "{}",
      "id": "3f170dcbe7970fe682de",
      "kwargs_json": "{}",
      "path": "main.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[{\"method\": \"add\", \"args\": [\"NewC\", 23], \"kwargs\": {}}]",
      "target": "Scoreboard.ranked"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": {
          "items": [
            [
              {
                "base64": "c2NvcmVz",
                "type": "str"
              },
              {
                "items": [
                  [
                    {
                      "type": "unicode",
                      "value": "NewC"
                    },
                    {
                      "type": "int",
                      "value": "23"
                    }
                  ]
                ],
                "type": "dict"
              }
            ]
          ],
          "type": "dict"
        },
        "status": "completed",
        "value": {
          "items": [
            {
              "items": [
                {
                  "type": "unicode",
                  "value": "NewC"
                },
                {
                  "type": "int",
                  "value": "23"
                }
              ],
              "type": "tuple"
            }
          ],
          "type": "list"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "3f170dcbe7970fe682de",
    "run": "ranking/heldout.json"
  }
]
```

### Review flags and suspected legacy bugs

```json
[
  "Mixed incomparable types, NaN ordering and user-defined __cmp__ may differ; CP9 must report unresolved cases."
]
```


```json
[]
```

### Documentation omissions and claim mismatches

```json
{
  "mismatches": [],
  "omitted": []
}
```

### function: ranking/main.py::Scoreboard.__init__

[Machine-generated]
Initialize an empty scores dictionary on the instance. Construction returns None from initialization; the harness also records instance state.

Observed return types: NoneType
Observed exceptions: exceptions.TypeError
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### function: ranking/main.py::Scoreboard.add

[Machine-generated]
Add points to the named score, starting from zero when the name is absent. This mutates the scores dictionary and returns None.

Observed return types: NoneType
Observed exceptions: 
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### function: ranking/main.py::Scoreboard.ranked

[Machine-generated]
Copy the scores mapping entries into a list and sort them using compare_scores as the comparison function. The original mapping remains in place.

Observed return types: list
Observed exceptions: 
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### function: ranking/main.py::compare_scores

[Machine-generated]
Compare score pairs for descending numeric score, then compare lowercased names for ties using cmp. Equal scores and case-insensitive equal names compare equal.

Observed return types: int
Observed exceptions: exceptions.IndexError
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### class: ranking/main.py::Scoreboard

[Machine-generated]
Hold a mutable scores dictionary, accumulate points through add, and expose sorted score rows through ranked. Ranking uses the module comparison helper.

Observed return types: 
Observed exceptions: 
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### module: ranking/main.py

[Machine-generated]
A stateful Scoreboard and comparison helper implement score accumulation and ranking. ranked uses iteritems and a cmp sort argument. The approximate call graph may not resolve the callback edge passed to sort.

Observed return types: 
Observed exceptions: 
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### package: ranking

[Machine-generated]
The ranking project has one module. Scoreboard owns mutable state; compare_scores defines score/name ordering used by ranked. Preserving accumulated state, tie behavior and comparison sorting is necessary for migration.

Observed return types: 
Observed exceptions: 
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### Diff: main.py.diff

```diff
--- a/main.py
+++ b/main.py
@@ -1,12 +1,22 @@
 u'[Machine-generated]\nA stateful Scoreboard and comparison helper implement score accumulation and ranking. ranked uses iteritems and a cmp sort argument. The approximate call graph may not resolve the callback edge passed to sort.\n\nObserved return types: \nObserved exceptions: \nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
+from __future__ import print_function
+
+
+from functools import cmp_to_key
+
+
+def _compare_values(left, right):
+    """[Machine-generated] Three-way comparison for mutually orderable values."""
+    # shortcut: Python 2 heterogeneous ordering/custom __cmp__ is unsupported; review such inputs.
+    return (left > right) - (left < right)
 
 
 def compare_scores(left, right):
     u'[Machine-generated]\nCompare score pairs for descending numeric score, then compare lowercased names for ties using cmp. Equal scores and case-insensitive equal names compare equal.\n\nObserved return types: int\nObserved exceptions: exceptions.IndexError\nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
-    score_order = cmp(right[1], left[1])
+    score_order = _compare_values(right[1], left[1])
     if score_order:
         return score_order
-    return cmp(left[0].lower(), right[0].lower())
+    return _compare_values(left[0].lower(), right[0].lower())
 
 
 class Scoreboard(object):
@@ -21,17 +31,17 @@
 
     def ranked(self):
         u'[Machine-generated]\nCopy the scores mapping entries into a list and sort them using compare_scores as the comparison function. The original mapping remains in place.\n\nObserved return types: list\nObserved exceptions: \nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
-        rows = list(self.scores.iteritems())
-        rows.sort(cmp=compare_scores)
+        rows = list(self.scores.items())
+        rows.sort(key=cmp_to_key(compare_scores))
         return rows
 
 
 if __name__ == '__main__':
     board = Scoreboard()
-    print 'empty:', repr(board.ranked())
+    print('empty:', repr(board.ranked()))
     board.add('Lin', 4)
     board.add('ada', 7)
     board.add('Bob', 7)
     board.add('Lin', -1)
-    print 'ranked:', repr(board.ranked())
-    print 'equal:', compare_scores(('Ada', 7), ('Ada', 7))
+    print('ranked:', repr(board.ranked()))
+    print('equal:', compare_scores(('Ada', 7), ('Ada', 7)))

```

## Policy results: file_report

```json
{
  "failures": [],
  "heldout": {
    "pass_rate_percent": 100.0,
    "passed": 4,
    "tests": 4,
    "unresolved": []
  },
  "pass_rate_percent": 100.0,
  "passed": 28,
  "source_review_matches": true,
  "tests": 28,
  "training": {
    "pass_rate_percent": 100.0,
    "passed": 24,
    "tests": 24,
    "unresolved": []
  },
  "unresolved": []
}
```

## file_report

### Evidence references

```json
{
  "baseline": "file_report/baseline-modern.json",
  "characterization": "file_report/characterization/private/runs.jsonl",
  "diffs": "file_report/diffs/",
  "documentation": "file_report/documentation/documentation.json",
  "heldout": "file_report/heldout.json",
  "repair": "file_report/repair/attempts.json",
  "training": "file_report/repair/training-final.json"
}
```

### Coverage, exclusions and quarantines

```json
{
  "coverage": {
    "branches": {
      "covered": [
        "reportkit/storage.py:11:-9",
        "reportkit/storage.py:11:12",
        "reportkit/summary.py:5:6",
        "reportkit/summary.py:5:7"
      ],
      "missing": [],
      "percent": 100.0,
      "possible": [
        "reportkit/storage.py:11:-9",
        "reportkit/storage.py:11:12",
        "reportkit/summary.py:5:6",
        "reportkit/summary.py:5:7"
      ]
    },
    "lines": {
      "covered": [
        "reportkit/__init__.py:11",
        "reportkit/storage.py:10",
        "reportkit/storage.py:11",
        "reportkit/storage.py:12",
        "reportkit/storage.py:5",
        "reportkit/storage.py:6",
        "reportkit/summary.py:5",
        "reportkit/summary.py:6",
        "reportkit/summary.py:7"
      ],
      "missing": [
        "reportkit/__init__.py:12",
        "reportkit/__init__.py:13",
        "reportkit/__init__.py:14",
        "reportkit/__init__.py:15",
        "reportkit/__init__.py:16",
        "reportkit/__init__.py:17",
        "reportkit/__init__.py:18"
      ],
      "percent": 56.25,
      "possible": [
        "reportkit/__init__.py:11",
        "reportkit/__init__.py:12",
        "reportkit/__init__.py:13",
        "reportkit/__init__.py:14",
        "reportkit/__init__.py:15",
        "reportkit/__init__.py:16",
        "reportkit/__init__.py:17",
        "reportkit/__init__.py:18",
        "reportkit/storage.py:10",
        "reportkit/storage.py:11",
        "reportkit/storage.py:12",
        "reportkit/storage.py:5",
        "reportkit/storage.py:6",
        "reportkit/summary.py:5",
        "reportkit/summary.py:6",
        "reportkit/summary.py:7"
      ]
    }
  },
  "coverage_targets": {
    "branches": 90,
    "lines": 90
  },
  "inventory_exclusions": [],
  "quarantine": [
    {
      "case": {
        "args_json": "[\"in.txt\", \"out.txt\", 7]",
        "category": "typical",
        "files_json": "{}",
        "id": "06a017e027038e98eb8a",
        "kwargs_json": "{}",
        "path": "reportkit/__init__.py",
        "reason": "Coding LLM proposal: typical input; observe legacy outcome only.",
        "setup_json": "[]",
        "target": "build_report"
      },
      "reason": "nonidentical repeated legacy observations",
      "run_labels": [
        "file_report:06a017e027038e98eb8a:0",
        "file_report:06a017e027038e98eb8a:1",
        "file_report:06a017e027038e98eb8a:2"
      ]
    },
    {
      "case": {
        "args_json": "[\"in.txt\", \"out.txt\", null]",
        "category": "edge",
        "files_json": "{}",
        "id": "72e15e21c69710d58817",
        "kwargs_json": "{}",
        "path": "reportkit/__init__.py",
        "reason": "Coding LLM proposal: edge input; observe legacy outcome only.",
        "setup_json": "[]",
        "target": "build_report"
      },
      "reason": "nonidentical repeated legacy observations",
      "run_labels": [
        "file_report:72e15e21c69710d58817:0",
        "file_report:72e15e21c69710d58817:1",
        "file_report:72e15e21c69710d58817:2"
      ]
    },
    {
      "case": {
        "args_json": "[\"in.txt\", \"out.txt\", 0]",
        "category": "empty",
        "files_json": "{}",
        "id": "75fdea77383d6bf9edb1",
        "kwargs_json": "{}",
        "path": "reportkit/__init__.py",
        "reason": "Coding LLM proposal: empty input; observe legacy outcome only.",
        "setup_json": "[]",
        "target": "build_report"
      },
      "reason": "nonidentical repeated legacy observations",
      "run_labels": [
        "file_report:75fdea77383d6bf9edb1:0",
        "file_report:75fdea77383d6bf9edb1:1",
        "file_report:75fdea77383d6bf9edb1:2"
      ]
    },
    {
      "case": {
        "args_json": "[\"entr\\u00e9e.txt\", \"r\\u00e9sum\\u00e9.txt\", 9]",
        "category": "unicode",
        "files_json": "{}",
        "id": "37fdb1dd1d1fa62c04a4",
        "kwargs_json": "{}",
        "path": "reportkit/__init__.py",
        "reason": "Coding LLM proposal: unicode input; observe legacy outcome only.",
        "setup_json": "[]",
        "target": "build_report"
      },
      "reason": "nonidentical repeated legacy observations",
      "run_labels": [
        "file_report:37fdb1dd1d1fa62c04a4:0",
        "file_report:37fdb1dd1d1fa62c04a4:1",
        "file_report:37fdb1dd1d1fa62c04a4:2"
      ]
    },
    {
      "case": {
        "args_json": "[{\"$bytes\": \"aW4udHh0\"}, {\"$bytes\": \"b3V0LnR4dA==\"}, 8]",
        "category": "bytes",
        "files_json": "{}",
        "id": "ef4a4675cfe5e256258c",
        "kwargs_json": "{}",
        "path": "reportkit/__init__.py",
        "reason": "Coding LLM proposal: bytes input; observe legacy outcome only.",
        "setup_json": "[]",
        "target": "build_report"
      },
      "reason": "nonidentical repeated legacy observations",
      "run_labels": [
        "file_report:ef4a4675cfe5e256258c:0",
        "file_report:ef4a4675cfe5e256258c:1",
        "file_report:ef4a4675cfe5e256258c:2"
      ]
    }
  ]
}
```

### Repair attempts and usage

```json
{
  "attempts": [
    {
      "accepted": true,
      "error": null,
      "function": [
        "reportkit/__init__.py",
        "build_report"
      ],
      "function_attempt": 1,
      "index": 0
    }
  ],
  "max_attempts_per_function": 2,
  "retry_counts": {
    "reportkit/__init__.py::build_report": 1
  }
}
```


```json
{
  "characterization": {
    "attempts": 8,
    "cost_complete": true,
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "conversion": {
    "attempts": 1,
    "cost_complete": true,
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "documentation": {
    "attempts": 9,
    "cost_complete": true,
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "repair": {
    "attempts": 1,
    "cost_complete": true,
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  }
}
```

### Unresolved failures

```json
[
  {
    "actual": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "coercing to Unicode: need string or buffer, int found"
            }
          ],
          "type": "tuple"
        },
        "message": "coercing to Unicode: need string or buffer, int found",
        "module": "builtins",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[0, \"out.txt\", 7]",
      "category": "boundary",
      "files_json": "{}",
      "id": "e665e1c7d0504c7b33c6",
      "kwargs_json": "{}",
      "path": "reportkit/__init__.py",
      "reason": "Coding LLM proposal: boundary input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "build_report"
    },
    "expected": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "Y29lcmNpbmcgdG8gVW5pY29kZTogbmVlZCBzdHJpbmcgb3IgYnVmZmVyLCBpbnQgZm91bmQ=",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "coercing to Unicode: need string or buffer, int found",
        "module": "exceptions",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "e665e1c7d0504c7b33c6",
    "run": "file_report/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "coercing to Unicode: need string or buffer, NoneType found"
            }
          ],
          "type": "tuple"
        },
        "message": "coercing to Unicode: need string or buffer, NoneType found",
        "module": "builtins",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[null, \"out-alt.txt\", null]",
      "category": "edge",
      "files_json": "{}",
      "id": "d2324fe595ea2cba2fb9",
      "kwargs_json": "{}",
      "path": "reportkit/__init__.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[]",
      "target": "build_report"
    },
    "expected": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "Y29lcmNpbmcgdG8gVW5pY29kZTogbmVlZCBzdHJpbmcgb3IgYnVmZmVyLCBOb25lVHlwZSBmb3VuZA==",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "coercing to Unicode: need string or buffer, NoneType found",
        "module": "exceptions",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "d2324fe595ea2cba2fb9",
    "run": "file_report/repair/training-final.json"
  },
  {
    "actual": {
      "files": [
        {
          "base64": "YmFkCg==",
          "kind": "file",
          "path": "work/numbers.txt",
          "sha256": "1d7a363ce12430881ec56c9cf1409c49c491043618e598c356e2959040872f5a"
        }
      ],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "invalid literal for int() with base 10: b'bad'"
            }
          ],
          "type": "tuple"
        },
        "message": "invalid literal for int() with base 10: b'bad'",
        "module": "builtins",
        "name": "ValueError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[\"numbers.txt\"]",
      "category": "edge",
      "files_json": "{\"numbers.txt\": \"YmFkCg==\"}",
      "id": "9bd5e615de8ece947f1d",
      "kwargs_json": "{}",
      "path": "reportkit/storage.py",
      "reason": "Coding LLM proposal: edge input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "read_numbers"
    },
    "expected": {
      "files": [
        {
          "base64": "YmFkCg==",
          "kind": "file",
          "path": "work/numbers.txt",
          "sha256": "1d7a363ce12430881ec56c9cf1409c49c491043618e598c356e2959040872f5a"
        }
      ],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "aW52YWxpZCBsaXRlcmFsIGZvciBpbnQoKSB3aXRoIGJhc2UgMTA6ICdiYWQn",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "invalid literal for int() with base 10: 'bad'",
        "module": "exceptions",
        "name": "ValueError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "9bd5e615de8ece947f1d",
    "run": "file_report/repair/training-final.json"
  },
  {
    "actual": {
      "files": [
        {
          "base64": "77yR77ySCg==",
          "kind": "file",
          "path": "work/numbers.txt",
          "sha256": "a52f5b83591b4dff640614b87bc3c1ad1773d998625af883d7f3edec83f617c3"
        }
      ],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "invalid literal for int() with base 10: b'\\xef\\xbc\\x91\\xef\\xbc\\x92'"
            }
          ],
          "type": "tuple"
        },
        "message": "invalid literal for int() with base 10: b'\\xef\\xbc\\x91\\xef\\xbc\\x92'",
        "module": "builtins",
        "name": "ValueError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[\"numbers.txt\"]",
      "category": "unicode",
      "files_json": "{\"numbers.txt\": \"77yR77ySCg==\"}",
      "id": "d5290c50168b68963fdc",
      "kwargs_json": "{}",
      "path": "reportkit/storage.py",
      "reason": "Coding LLM proposal: unicode input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "read_numbers"
    },
    "expected": {
      "files": [
        {
          "base64": "77yR77ySCg==",
          "kind": "file",
          "path": "work/numbers.txt",
          "sha256": "a52f5b83591b4dff640614b87bc3c1ad1773d998625af883d7f3edec83f617c3"
        }
      ],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "aW52YWxpZCBsaXRlcmFsIGZvciBpbnQoKSB3aXRoIGJhc2UgMTA6ICdceGVmXHhiY1x4OTFceGVmXHhiY1x4OTIn",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "invalid literal for int() with base 10: '\\xef\\xbc\\x91\\xef\\xbc\\x92'",
        "module": "exceptions",
        "name": "ValueError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "d5290c50168b68963fdc",
    "run": "file_report/repair/training-final.json"
  },
  {
    "actual": {
      "files": [
        {
          "base64": "/wo=",
          "kind": "file",
          "path": "work/numbers.txt",
          "sha256": "e4688624e5f1ad0629505e6768e3bb36244f2f3e33e751215afa820334a76ed3"
        }
      ],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "invalid literal for int() with base 10: b'\\xff'"
            }
          ],
          "type": "tuple"
        },
        "message": "invalid literal for int() with base 10: b'\\xff'",
        "module": "builtins",
        "name": "ValueError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[\"numbers.txt\"]",
      "category": "bytes",
      "files_json": "{\"numbers.txt\": \"/wo=\"}",
      "id": "6860a61cb6e5525bea67",
      "kwargs_json": "{}",
      "path": "reportkit/storage.py",
      "reason": "Coding LLM proposal: bytes input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "read_numbers"
    },
    "expected": {
      "files": [
        {
          "base64": "/wo=",
          "kind": "file",
          "path": "work/numbers.txt",
          "sha256": "e4688624e5f1ad0629505e6768e3bb36244f2f3e33e751215afa820334a76ed3"
        }
      ],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "aW52YWxpZCBsaXRlcmFsIGZvciBpbnQoKSB3aXRoIGJhc2UgMTA6ICdceGZmJw==",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "invalid literal for int() with base 10: '\\xff'",
        "module": "exceptions",
        "name": "ValueError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "6860a61cb6e5525bea67",
    "run": "file_report/repair/training-final.json"
  },
  {
    "actual": {
      "files": [
        {
          "base64": "",
          "kind": "file",
          "path": "work/out.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        }
      ],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "ascii"
            },
            {
              "type": "str",
              "value": "\u00e9=\u96ea\n"
            },
            {
              "type": "int",
              "value": "0"
            },
            {
              "type": "int",
              "value": "1"
            },
            {
              "type": "str",
              "value": "ordinal not in range(128)"
            }
          ],
          "type": "tuple"
        },
        "message": "'ascii' codec can't encode character '\\xe9' in position 0: ordinal not in range(128)",
        "module": "builtins",
        "name": "UnicodeEncodeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[\"out.txt\", {\"\\u00e9\": \"\\u96ea\"}]",
      "category": "unicode",
      "files_json": "{}",
      "id": "14a86d2c5e895a90a6cb",
      "kwargs_json": "{}",
      "path": "reportkit/storage.py",
      "reason": "Coding LLM proposal: unicode input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "write_report"
    },
    "expected": {
      "files": [
        {
          "base64": "",
          "kind": "file",
          "path": "work/out.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        }
      ],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "YXNjaWk=",
              "type": "str"
            },
            {
              "type": "unicode",
              "value": "\u00e9=\u96ea\n"
            },
            {
              "type": "int",
              "value": "0"
            },
            {
              "type": "int",
              "value": "1"
            },
            {
              "base64": "b3JkaW5hbCBub3QgaW4gcmFuZ2UoMTI4KQ==",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "'ascii' codec can't encode character u'\\xe9' in position 0: ordinal not in range(128)",
        "module": "exceptions",
        "name": "UnicodeEncodeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "14a86d2c5e895a90a6cb",
    "run": "file_report/repair/training-final.json"
  },
  {
    "actual": {
      "files": [
        {
          "base64": "",
          "kind": "file",
          "path": "work/out.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        }
      ],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "ascii"
            },
            {
              "base64": "/w==",
              "type": "bytes"
            },
            {
              "type": "int",
              "value": "0"
            },
            {
              "type": "int",
              "value": "1"
            },
            {
              "type": "str",
              "value": "ordinal not in range(128)"
            }
          ],
          "type": "tuple"
        },
        "message": "'ascii' codec can't decode byte 0xff in position 0: ordinal not in range(128)",
        "module": "builtins",
        "name": "UnicodeDecodeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[{\"$bytes\": \"b3V0LnR4dA==\"}, {\"a\": {\"$bytes\": \"/w==\"}}]",
      "category": "bytes",
      "files_json": "{}",
      "id": "5c6691a653902c4bcbda",
      "kwargs_json": "{}",
      "path": "reportkit/storage.py",
      "reason": "Coding LLM proposal: bytes input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "write_report"
    },
    "expected": {
      "files": [
        {
          "base64": "",
          "kind": "file",
          "path": "work/out.txt",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        }
      ],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "YXNjaWk=",
              "type": "str"
            },
            {
              "base64": "/w==",
              "type": "str"
            },
            {
              "type": "int",
              "value": "0"
            },
            {
              "type": "int",
              "value": "1"
            },
            {
              "base64": "b3JkaW5hbCBub3QgaW4gcmFuZ2UoMTI4KQ==",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "'ascii' codec can't decode byte 0xff in position 0: ordinal not in range(128)",
        "module": "exceptions",
        "name": "UnicodeDecodeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "5c6691a653902c4bcbda",
    "run": "file_report/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            [
              {
                "base64": "Y291bnQ=",
                "type": "bytes"
              },
              {
                "type": "int",
                "value": "3"
              }
            ],
            [
              {
                "base64": "bWVhbg==",
                "type": "bytes"
              },
              {
                "type": "int",
                "value": "1"
              }
            ]
          ],
          "type": "dict"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[7, -2, 0]]",
      "category": "typical",
      "files_json": "{}",
      "id": "25a9132e4eb2071add56",
      "kwargs_json": "{}",
      "path": "reportkit/summary.py",
      "reason": "Coding LLM proposal: typical input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "summarize"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            [
              {
                "base64": "Y291bnQ=",
                "type": "str"
              },
              {
                "type": "int",
                "value": "3"
              }
            ],
            [
              {
                "base64": "bWVhbg==",
                "type": "str"
              },
              {
                "type": "int",
                "value": "1"
              }
            ]
          ],
          "type": "dict"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "25a9132e4eb2071add56",
    "run": "file_report/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            [
              {
                "base64": "Y291bnQ=",
                "type": "bytes"
              },
              {
                "type": "int",
                "value": "2"
              }
            ],
            [
              {
                "base64": "bWVhbg==",
                "type": "bytes"
              },
              {
                "type": "int",
                "value": "-3"
              }
            ]
          ],
          "type": "dict"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[-7, 2]]",
      "category": "edge",
      "files_json": "{}",
      "id": "dbcef5cdcb7fa78412ac",
      "kwargs_json": "{}",
      "path": "reportkit/summary.py",
      "reason": "Coding LLM proposal: edge input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "summarize"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            [
              {
                "base64": "Y291bnQ=",
                "type": "str"
              },
              {
                "type": "int",
                "value": "2"
              }
            ],
            [
              {
                "base64": "bWVhbg==",
                "type": "str"
              },
              {
                "type": "int",
                "value": "-3"
              }
            ]
          ],
          "type": "dict"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "dbcef5cdcb7fa78412ac",
    "run": "file_report/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            [
              {
                "base64": "Y291bnQ=",
                "type": "bytes"
              },
              {
                "type": "int",
                "value": "1"
              }
            ],
            [
              {
                "base64": "bWVhbg==",
                "type": "bytes"
              },
              {
                "type": "int",
                "value": "0"
              }
            ]
          ],
          "type": "dict"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[0]]",
      "category": "empty",
      "files_json": "{}",
      "id": "981e41f6e4e76360f5a2",
      "kwargs_json": "{}",
      "path": "reportkit/summary.py",
      "reason": "Coding LLM proposal: empty input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "summarize"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            [
              {
                "base64": "Y291bnQ=",
                "type": "str"
              },
              {
                "type": "int",
                "value": "1"
              }
            ],
            [
              {
                "base64": "bWVhbg==",
                "type": "str"
              },
              {
                "type": "int",
                "value": "0"
              }
            ]
          ],
          "type": "dict"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "981e41f6e4e76360f5a2",
    "run": "file_report/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            [
              {
                "base64": "Y291bnQ=",
                "type": "bytes"
              },
              {
                "type": "int",
                "value": "2"
              }
            ],
            [
              {
                "base64": "bWVhbg==",
                "type": "bytes"
              },
              {
                "type": "int",
                "value": "1"
              }
            ]
          ],
          "type": "dict"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[1, 2]]",
      "category": "boundary",
      "files_json": "{}",
      "id": "6a64b8ae60bf34fb3a82",
      "kwargs_json": "{}",
      "path": "reportkit/summary.py",
      "reason": "Coding LLM proposal: boundary input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "summarize"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            [
              {
                "base64": "Y291bnQ=",
                "type": "str"
              },
              {
                "type": "int",
                "value": "2"
              }
            ],
            [
              {
                "base64": "bWVhbg==",
                "type": "str"
              },
              {
                "type": "int",
                "value": "1"
              }
            ]
          ],
          "type": "dict"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "6a64b8ae60bf34fb3a82",
    "run": "file_report/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "unsupported operand type(s) for +: 'int' and 'str'"
            }
          ],
          "type": "tuple"
        },
        "message": "unsupported operand type(s) for +: 'int' and 'str'",
        "module": "builtins",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[\"\\u00e9\"]]",
      "category": "unicode",
      "files_json": "{}",
      "id": "deb9759c28f1d6e10620",
      "kwargs_json": "{}",
      "path": "reportkit/summary.py",
      "reason": "Coding LLM proposal: unicode input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "summarize"
    },
    "expected": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "dW5zdXBwb3J0ZWQgb3BlcmFuZCB0eXBlKHMpIGZvciArOiAnaW50JyBhbmQgJ3VuaWNvZGUn",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "unsupported operand type(s) for +: 'int' and 'unicode'",
        "module": "exceptions",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "deb9759c28f1d6e10620",
    "run": "file_report/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "unsupported operand type(s) for +: 'int' and 'bytes'"
            }
          ],
          "type": "tuple"
        },
        "message": "unsupported operand type(s) for +: 'int' and 'bytes'",
        "module": "builtins",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[{\"$bytes\": \"Nw==\"}]]",
      "category": "bytes",
      "files_json": "{}",
      "id": "60b44226959740392362",
      "kwargs_json": "{}",
      "path": "reportkit/summary.py",
      "reason": "Coding LLM proposal: bytes input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "summarize"
    },
    "expected": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "dW5zdXBwb3J0ZWQgb3BlcmFuZCB0eXBlKHMpIGZvciArOiAnaW50JyBhbmQgJ3N0cic=",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "unsupported operand type(s) for +: 'int' and 'str'",
        "module": "exceptions",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "60b44226959740392362",
    "run": "file_report/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            [
              {
                "base64": "Y291bnQ=",
                "type": "bytes"
              },
              {
                "type": "int",
                "value": "3"
              }
            ],
            [
              {
                "base64": "bWVhbg==",
                "type": "bytes"
              },
              {
                "type": "int",
                "value": "39"
              }
            ]
          ],
          "type": "dict"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[113, 7, -3]]",
      "category": "typical",
      "files_json": "{}",
      "id": "fe23c0367ad7a38cc26b",
      "kwargs_json": "{}",
      "path": "reportkit/summary.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[]",
      "target": "summarize"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            [
              {
                "base64": "Y291bnQ=",
                "type": "str"
              },
              {
                "type": "int",
                "value": "3"
              }
            ],
            [
              {
                "base64": "bWVhbg==",
                "type": "str"
              },
              {
                "type": "int",
                "value": "39"
              }
            ]
          ],
          "type": "dict"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "fe23c0367ad7a38cc26b",
    "run": "file_report/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            [
              {
                "base64": "Y291bnQ=",
                "type": "bytes"
              },
              {
                "type": "int",
                "value": "0"
              }
            ],
            [
              {
                "base64": "bWVhbg==",
                "type": "bytes"
              },
              {
                "type": "NoneType"
              }
            ]
          ],
          "type": "dict"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[]]",
      "category": "typical",
      "files_json": "{}",
      "id": "26f0affcae44a95ee5d7",
      "kwargs_json": "{}",
      "path": "reportkit/summary.py",
      "reason": "Coding LLM proposal: typical input; observe legacy outcome only.",
      "setup_json": "[]",
      "target": "summarize"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            [
              {
                "base64": "Y291bnQ=",
                "type": "str"
              },
              {
                "type": "int",
                "value": "0"
              }
            ],
            [
              {
                "base64": "bWVhbg==",
                "type": "str"
              },
              {
                "type": "NoneType"
              }
            ]
          ],
          "type": "dict"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "26f0affcae44a95ee5d7",
    "run": "file_report/repair/training-final.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "type": "str",
              "value": "coercing to Unicode: need string or buffer, int found"
            }
          ],
          "type": "tuple"
        },
        "message": "coercing to Unicode: need string or buffer, int found",
        "module": "builtins",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[13, \"out-new.txt\", 7]",
      "category": "typical",
      "files_json": "{}",
      "id": "6afcfe311a226520ecf3",
      "kwargs_json": "{}",
      "path": "reportkit/__init__.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[]",
      "target": "build_report"
    },
    "expected": {
      "files": [],
      "outcome": {
        "args": {
          "items": [
            {
              "base64": "Y29lcmNpbmcgdG8gVW5pY29kZTogbmVlZCBzdHJpbmcgb3IgYnVmZmVyLCBpbnQgZm91bmQ=",
              "type": "str"
            }
          ],
          "type": "tuple"
        },
        "message": "coercing to Unicode: need string or buffer, int found",
        "module": "exceptions",
        "name": "TypeError",
        "status": "exception"
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "6afcfe311a226520ecf3",
    "run": "file_report/heldout.json"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            [
              {
                "base64": "Y291bnQ=",
                "type": "bytes"
              },
              {
                "type": "int",
                "value": "2"
              }
            ],
            [
              {
                "base64": "bWVhbg==",
                "type": "bytes"
              },
              {
                "type": "int",
                "value": "35"
              }
            ]
          ],
          "type": "dict"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "case": {
      "args_json": "[[29, 41]]",
      "category": "edge",
      "files_json": "{}",
      "id": "aed05690e55bf8588e2a",
      "kwargs_json": "{}",
      "path": "reportkit/summary.py",
      "reason": "Fresh input-only proposal for independent revalidation; outcome comes only from legacy execution.",
      "setup_json": "[]",
      "target": "summarize"
    },
    "expected": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "items": [
            [
              {
                "base64": "Y291bnQ=",
                "type": "str"
              },
              {
                "type": "int",
                "value": "2"
              }
            ],
            [
              {
                "base64": "bWVhbg==",
                "type": "str"
              },
              {
                "type": "int",
                "value": "35"
              }
            ]
          ],
          "type": "dict"
        }
      },
      "stderr_base64": "",
      "stdout_base64": "",
      "target_exit_code": 0
    },
    "id": "aed05690e55bf8588e2a",
    "run": "file_report/heldout.json"
  }
]
```

### Review flags and suspected legacy bugs

```json
[
  "Successful clock/randomness paths remain quarantined; conversion cannot claim equivalence for them.",
  "Precise exception records, non-ASCII byte formatting and arbitrary custom numeric objects need CP9 evaluation."
]
```


```json
[
  {
    "key": "file_report/reportkit/__init__.py::build_report",
    "text": "Create or overwrite the input file with fixed numeric sample data, read it, compute a summary, add a pseudo-random ticket and current timestamp, then write and return the report. This describes source structure: successful training outcomes are unavailable because clock-dependent cases were quarantined. Suspected legacy bug: the supplied input path is overwritten before being read."
  },
  {
    "key": "file_report",
    "text": "The main module calls reportkit.build_report. The package imports storage.read_numbers, storage.write_report and summary.summarize through relative imports. Execution combines file writes, integer averaging, randomness and wall-clock time. Suspected legacy bug: build_report overwrites its input with sample data. Quarantined success paths limit behavioral evidence."
  }
]
```

### Documentation omissions and claim mismatches

```json
{
  "mismatches": [],
  "omitted": []
}
```

### function: file_report/reportkit/storage.py::read_numbers

[Machine-generated]
Read a file in binary mode, skip blank stripped lines, and parse the remaining lines as integers. Invalid numeric bytes propagate parsing errors.

Observed return types: list
Observed exceptions: exceptions.ValueError
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### function: file_report/reportkit/summary.py::summarize

[Machine-generated]
Return count and mean for numbers. Empty input produces count zero and a None mean; nonempty integer input uses Python 2 integer division. Unsupported element types retain their errors.

Observed return types: dict
Observed exceptions: exceptions.TypeError
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### function: file_report/reportkit/storage.py::write_report

[Machine-generated]
Open a report file in binary write mode and serialize sorted mapping entries as key=value lines using iteritems. Opening truncates an existing file before iteration; formatting can expose Python 2 Unicode encoding errors.

Observed return types: NoneType
Observed exceptions: exceptions.UnicodeDecodeError, exceptions.UnicodeEncodeError
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### function: file_report/reportkit/__init__.py::build_report

[Machine-generated]
Create or overwrite the input file with fixed numeric sample data, read it, compute a summary, add a pseudo-random ticket and current timestamp, then write and return the report. This describes source structure: successful training outcomes are unavailable because clock-dependent cases were quarantined. Suspected legacy bug: the supplied input path is overwritten before being read.

Observed return types: 
Observed exceptions: exceptions.TypeError
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### module: file_report/main.py

[Machine-generated]
The demonstration entry module imports build_report from reportkit and prints its result with sample file paths when run as main. It retains Python 2 print syntax.

Observed return types: 
Observed exceptions: 
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### module: file_report/reportkit/__init__.py

[Machine-generated]
The reportkit package coordinates storage and summary through explicit relative imports. build_report overwrites sample input, uses randomness and time, and writes a report. Successful clock-dependent behavior is quarantined, so the source description is not a verified success claim.

Observed return types: 
Observed exceptions: 
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### module: file_report/reportkit/storage.py

[Machine-generated]
Storage helpers read binary numeric files and write sorted report lines. Both operate on supplied paths; errors propagate. Python 2 byte formatting and mapping iteration are migration hazards.

Observed return types: 
Observed exceptions: 
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### module: file_report/reportkit/summary.py

[Machine-generated]
A pure summary helper computes count and an integer-rounded mean, with an explicit empty-input result. No project-local dependencies are imported.

Observed return types: 
Observed exceptions: 
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### package: file_report

[Machine-generated]
The main module calls reportkit.build_report. The package imports storage.read_numbers, storage.write_report and summary.summarize through relative imports. Execution combines file writes, integer averaging, randomness and wall-clock time. Suspected legacy bug: build_report overwrites its input with sample data. Quarantined success paths limit behavioral evidence.

Observed return types: 
Observed exceptions: 
Limitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.

### Diff: main.py.diff

```diff
--- a/main.py
+++ b/main.py
@@ -1,7 +1,8 @@
 u'[Machine-generated]\nThe demonstration entry module imports build_report from reportkit and prints its result with sample file paths when run as main. It retains Python 2 print syntax.\n\nObserved return types: \nObserved exceptions: \nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
+from __future__ import print_function
 
 from reportkit import build_report
 
 
 if __name__ == '__main__':
-    print repr(build_report('sample.txt', 'report.txt', seed=7))
+    print(repr(build_report('sample.txt', 'report.txt', seed=7)))

```

### Diff: reportkit/__init__.py.diff

```diff
--- a/reportkit/__init__.py
+++ b/reportkit/__init__.py
@@ -7,13 +7,16 @@
 from .summary import summarize
 
 
+from ._legacy_compat import legacy_open
+
+
 def build_report(input_path, output_path, seed=None):
     u'[Machine-generated]\nCreate or overwrite the input file with fixed numeric sample data, read it, compute a summary, add a pseudo-random ticket and current timestamp, then write and return the report. This describes source structure: successful training outcomes are unavailable because clock-dependent cases were quarantined. Suspected legacy bug: the supplied input path is overwritten before being read.\n\nObserved return types: \nObserved exceptions: exceptions.TypeError\nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
-    with open(input_path, 'wb') as stream:
-        stream.write('7\n-2\n0\n')
+    with legacy_open(input_path, 'wb') as stream:
+        stream.write(b'7\n-2\n0\n')
     numbers = read_numbers(input_path)
     report = summarize(numbers)
-    report['ticket'] = random.Random(seed).randint(100, 999)
-    report['created_at'] = time.time()
+    report[b'ticket'] = random.Random(seed).randint(100, 999)
+    report[b'created_at'] = time.time()
     write_report(output_path, report)
     return report

```

### Diff: reportkit/_legacy_compat.py.diff

```diff
--- /dev/null
+++ b/reportkit/_legacy_compat.py
@@ -0,0 +1,16 @@
+"""[Machine-generated] Compatibility for built-in numeric division."""
+
+
+def legacy_divide(left, right):
+    """[Machine-generated] Floor integer quotients; divide other numbers normally."""
+    # shortcut: custom Python 2 __div__ protocols are unsupported; review user-defined numeric types.
+    if isinstance(left, int) and isinstance(right, int):
+        return left // right
+    return left / right
+
+
+def legacy_open(path, mode):
+    """[Machine-generated] Reject descriptors as Python 2's path-based open did."""
+    if not isinstance(path, (str, bytes)):
+        raise TypeError('coercing to Unicode: need string or buffer, %s found' % type(path).__name__)
+    return open(path, mode)

```

### Diff: reportkit/storage.py.diff

```diff
--- a/reportkit/storage.py
+++ b/reportkit/storage.py
@@ -1,14 +1,19 @@
 u'[Machine-generated]\nStorage helpers read binary numeric files and write sorted report lines. Both operate on supplied paths; errors propagate. Python 2 byte formatting and mapping iteration are migration hazards.\n\nObserved return types: \nObserved exceptions: \nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
+
+
+from ._legacy_compat import legacy_open
 
 
 def read_numbers(path):
     u'[Machine-generated]\nRead a file in binary mode, skip blank stripped lines, and parse the remaining lines as integers. Invalid numeric bytes propagate parsing errors.\n\nObserved return types: list\nObserved exceptions: exceptions.ValueError\nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
-    with open(path, 'rb') as stream:
+    with legacy_open(path, 'rb') as stream:
         return [int(line.strip()) for line in stream if line.strip()]
 
 
 def write_report(path, report):
     u'[Machine-generated]\nOpen a report file in binary write mode and serialize sorted mapping entries as key=value lines using iteritems. Opening truncates an existing file before iteration; formatting can expose Python 2 Unicode encoding errors.\n\nObserved return types: NoneType\nObserved exceptions: exceptions.UnicodeDecodeError, exceptions.UnicodeEncodeError\nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
-    with open(path, 'wb') as stream:
-        for key, value in sorted(report.iteritems()):
-            stream.write('%s=%s\n' % (key, value))
+    with legacy_open(path, 'wb') as stream:
+        for key, value in sorted(report.items()):
+            key_text = key.decode('ascii') if isinstance(key, bytes) else key
+            value_text = value.decode('ascii') if isinstance(value, bytes) else value
+            stream.write(('%s=%s\n' % (key_text, value_text)).encode('ascii'))

```

### Diff: reportkit/summary.py.diff

```diff
--- a/reportkit/summary.py
+++ b/reportkit/summary.py
@@ -1,8 +1,11 @@
 u'[Machine-generated]\nA pure summary helper computes count and an integer-rounded mean, with an explicit empty-input result. No project-local dependencies are imported.\n\nObserved return types: \nObserved exceptions: \nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
+
+
+from ._legacy_compat import legacy_divide
 
 
 def summarize(numbers):
     u'[Machine-generated]\nReturn count and mean for numbers. Empty input produces count zero and a None mean; nonempty integer input uses Python 2 integer division. Unsupported element types retain their errors.\n\nObserved return types: dict\nObserved exceptions: exceptions.TypeError\nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
     if not numbers:
-        return {'count': 0, 'mean': None}
-    return {'count': len(numbers), 'mean': sum(numbers) / len(numbers)}
+        return {b'count': 0, b'mean': None}
+    return {b'count': len(numbers), b'mean': legacy_divide(sum(numbers), len(numbers))}

```


# Recorded modernization report

**Status: needs_human_review**

Committed successful corpus runs only: characterization, documentation, transformation and repair. Excludes infrastructure checks, failed/probe runs and coding-agent authoring costs. Mock token/cost totals are not estimates of live provider use. No new sandbox execution.

Exact CP5 comparison, including types, exceptions, streams and files. All three headline rates use the same non-quarantined training plus held-out cases. Coverage includes eligible legacy observations only; dynamic/time paths may be absent. Failure causes show the first differing component. Suspected bugs are source-grounded, not proven.

See report.json for exact values, raw-record references, archive hashes and all report fields.

| Project | Legacy / legacy | Legacy / modern | Converted / modern | Held-out converted |
|---|---:|---:|---:|---:|
| golden_ledger | 18/18 (100.00%) | 0/18 (0.00%) | 11/18 (61.11%) | 1/3 (33.33%) |
| text_pipeline | 30/30 (100.00%) | 0/30 (0.00%) | 5/30 (16.67%) | 0/5 (0.00%) |
| ranking | 20/20 (100.00%) | 0/20 (0.00%) | 5/20 (25.00%) | 1/4 (25.00%) |
| file_report | 20/20 (100.00%) | 3/20 (15.00%) | 7/20 (35.00%) | 1/3 (33.33%) |

## Totals and usage

```json
{
  "accepted_repairs": 0,
  "changed_files": 9,
  "converted_on_modern": {
    "pass_rate_percent": 31.818181818181817,
    "passed": 28,
    "tests": 88
  },
  "heldout_passed": 3,
  "heldout_tests": 15,
  "legacy_on_legacy": {
    "pass_rate_percent": 100.0,
    "passed": 88,
    "tests": 88
  },
  "legacy_on_modern": {
    "pass_rate_percent": 3.409090909090909,
    "passed": 3,
    "tests": 88
  },
  "quarantined": 5,
  "repair_proposals": 30,
  "usage": {
    "attempts": 82,
    "cost_complete": true,
    "evidence_kinds": {
      "mock": 82
    },
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
  "plan": {
    "explicit_branch_target": 90,
    "line_target": 90,
    "max_rounds": 2,
    "minimum_mutation_detection_percent": 80,
    "proposal_provenance": "Coding LLM authored input-only proposals, deterministic mock replay; no provider calls",
    "proposal_sha256": "9e178e62de933015a004c317f93053b7fc54af3dff168fb06a5e15042b3d5a5d",
    "repeats": 3
  },
  "verification": {
    "heldout_passes": 15,
    "mutation_detection_percent": 87.5,
    "mutations_detected": 7,
    "mutations_total": 8,
    "projects": [
      {
        "accepted": 18,
        "comparisons": 36,
        "coverage": {
          "branches": 100.0,
          "lines": 100.0
        },
        "heldout": 3,
        "passes": 36,
        "project": "golden_ledger",
        "quarantined": 0
      },
      {
        "accepted": 30,
        "comparisons": 60,
        "coverage": {
          "branches": 100.0,
          "lines": 100.0
        },
        "heldout": 5,
        "passes": 60,
        "project": "text_pipeline",
        "quarantined": 0
      },
      {
        "accepted": 20,
        "comparisons": 40,
        "coverage": {
          "branches": 100.0,
          "lines": 100.0
        },
        "heldout": 4,
        "passes": 40,
        "project": "ranking",
        "quarantined": 0
      },
      {
        "accepted": 20,
        "comparisons": 40,
        "coverage": {
          "branches": 100.0,
          "lines": 56.25
        },
        "heldout": 3,
        "passes": 40,
        "project": "file_report",
        "quarantined": 5
      }
    ],
    "totals": {
      "accepted": 88,
      "comparisons": 176,
      "heldout": 15,
      "heldout_container_runs": 15,
      "mock_calls": 20,
      "mutation_container_runs": 145,
      "oracle_container_runs": 283,
      "passes": 176,
      "quarantined": 5,
      "training": 73
    }
  }
}
```

## Recorded anti-gaming review

```json
{
  "limitation": "Manual source review and heuristic scan are not a proof of equivalence or comprehensive detection of deceptive code.",
  "projects": [
    {
      "assessment": "Integer-type division dispatch is general. Existing ValueError handling is retained. No fixture-valued branch, new exception suppression or comparison relaxation found.",
      "files": [
        "_legacy_compat.py",
        "main.py"
      ],
      "project": "golden_ledger",
      "repair": "No CP9 source patches accepted; final source equals CP8 input."
    },
    {
      "assessment": "Encoding dispatch uses runtime types, not fixture values. The type-name helper preserves labels returned by the public describe function; it does not alter the observation codec. No test access or comparison relaxation found.",
      "files": [
        "main.py"
      ],
      "project": "text_pipeline",
      "repair": "No CP9 source patches accepted; final source equals CP8 input."
    },
    {
      "assessment": "cmp_to_key uses the shared comparator for all rows. No fixture-keyed ordering, new exception suppression or test access found. Runtime state/type mismatches remain reported.",
      "files": [
        "main.py"
      ],
      "project": "ranking",
      "repair": "No CP9 source patches accepted; final source equals CP8 input."
    },
    {
      "assessment": "Binary payloads, keys and encoding dispatch are general changes. The input overwrite, randomness and clock calls remain. No quarantine, suppression or comparison changes were introduced; mismatches remain visible.",
      "files": [
        "main.py",
        "reportkit/__init__.py",
        "reportkit/_legacy_compat.py",
        "reportkit/storage.py",
        "reportkit/summary.py"
      ],
      "project": "file_report",
      "repair": "No CP9 source patches accepted; final source equals CP8 input."
    }
  ],
  "reviewer": "Coding agent; manual review of full saved CP7-to-CP8 diffs and CP9 source identity",
  "status": "No anti-gaming violation found; behavioral mismatches require human review"
}
```

## golden_ledger

### Evidence references

```json
{
  "baseline": "cp6.tar.gz!/golden_ledger.json",
  "coverage": "cp5.tar.gz!/golden_ledger/private/golden_ledger-report.json",
  "diffs": "cp9.tar.gz!/golden_ledger/full-diffs/",
  "documentation": "cp7.tar.gz!/golden_ledger/documentation.json",
  "heldout": "cp9.tar.gz!/golden_ledger/heldout.json",
  "quarantine": "cp5.tar.gz!/golden_ledger/private/golden_ledger-quarantine.json",
  "repairs": "cp9.tar.gz!/golden_ledger/repair/attempts.json",
  "training": "cp9.tar.gz!/golden_ledger/repair/training-final.json"
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
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "parse_amount"
      ],
      "function_attempt": 1,
      "index": 0
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "parse_amount"
      ],
      "function_attempt": 2,
      "index": 1
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "split_bill"
      ],
      "function_attempt": 1,
      "index": 2
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "split_bill"
      ],
      "function_attempt": 2,
      "index": 3
    }
  ],
  "max_attempts_per_function": 2,
  "retry_counts": {
    "main.py::parse_amount": 2,
    "main.py::split_bill": 2
  }
}
```


```json
{
  "cp5": {
    "attempts": 3,
    "cost_complete": true,
    "evidence_kinds": {
      "mock": 3
    },
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "record": "cp5.tar.gz!/golden_ledger/private/llm/calls.jsonl",
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "cp7": {
    "attempts": 5,
    "cost_complete": true,
    "evidence_kinds": {
      "mock": 5
    },
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "record": "cp7.tar.gz!/golden_ledger/llm/calls.jsonl",
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "cp8": {
    "attempts": 1,
    "cost_complete": true,
    "evidence_kinds": {
      "mock": 1
    },
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "record": "cp8.tar.gz!/golden_ledger/llm/calls.jsonl",
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "cp9": {
    "attempts": 4,
    "cost_complete": true,
    "evidence_kinds": {
      "mock": 4
    },
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "record": "cp9.tar.gz!/golden_ledger/llm/calls.jsonl",
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
    "category": "runtime_exception:ZeroDivisionError",
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
    "run": "cp9.tar.gz!/golden_ledger/repair/training-final.json#2933d0e1a536a13e1c9b",
    "split": "training"
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
    "category": "runtime_exception:TypeError",
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
    "run": "cp9.tar.gz!/golden_ledger/repair/training-final.json#ae99ca04829212e8d066",
    "split": "training"
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
    "category": "runtime_exception:TypeError",
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
    "run": "cp9.tar.gz!/golden_ledger/repair/training-final.json#1ce3d591a6fab727dea2",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/golden_ledger/repair/training-final.json#3de50b5084cce723213b",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/golden_ledger/repair/training-final.json#d45c541e84e5ce2da0b7",
    "split": "training"
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
    "category": "runtime_exception:TypeError",
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
    "run": "cp9.tar.gz!/golden_ledger/heldout.json#0b3592f5255fad064b80",
    "split": "heldout"
  },
  {
    "actual": {
      "files": [],
      "outcome": {
        "state": null,
        "status": "completed",
        "value": {
          "base64": "aW52YWxpZDogaW52YWxpZCBsaXRlcmFsIGZvciBpbnQoKSB3aXRoIGJhc2UgMTA6IGInXHhmZic=",
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/golden_ledger/heldout.json#38e1023d868eec42b03b",
    "split": "heldout"
  }
]
```

### Review flags and suspected legacy bugs

```json
[
  "Frozen CP5 observations distinguish Python 2 str/unicode, exception modules and argument types from Python 3 bytes/str/builtins. Source-only changes cannot reproduce those built-in runtime identities. No safe patch is proposed; comparisons and fixtures stay unchanged. Review remaining semantic differences too."
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
Observed exceptions: 
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
@@ -0,0 +1,9 @@
+"""[Machine-generated] Compatibility for built-in numeric division."""
+
+
+def legacy_divide(left, right):
+    """[Machine-generated] Floor integer quotients; divide other numbers normally."""
+    # shortcut: custom Python 2 __div__ protocols are unsupported; review user-defined numeric types.
+    if isinstance(left, int) and isinstance(right, int):
+        return left // right
+    return left / right

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
+from _legacy_compat import legacy_divide
 
 
 def split_bill(amount, people):
     u'[Machine-generated]\nDivide the amount among people using Python 2 division. Integer inputs round toward negative infinity; zero divisors raise an error.\n\nObserved return types: int\nObserved exceptions: exceptions.TypeError, exceptions.ZeroDivisionError\nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
-    return amount / people
+    return legacy_divide(amount, people)
 
 
 def summarize(balances):
     u'[Machine-generated]\nAccumulate amounts from the balances mapping using iteritems. An empty mapping leaves the total at zero.\n\nObserved return types: int\nObserved exceptions: \nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
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
+        return b'invalid: ' + str(error).encode('ascii')
 
 
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

## text_pipeline

### Evidence references

```json
{
  "baseline": "cp6.tar.gz!/text_pipeline.json",
  "coverage": "cp5.tar.gz!/text_pipeline/private/text_pipeline-report.json",
  "diffs": "cp9.tar.gz!/text_pipeline/full-diffs/",
  "documentation": "cp7.tar.gz!/text_pipeline/documentation.json",
  "heldout": "cp9.tar.gz!/text_pipeline/heldout.json",
  "quarantine": "cp5.tar.gz!/text_pipeline/private/text_pipeline-quarantine.json",
  "repairs": "cp9.tar.gz!/text_pipeline/repair/attempts.json",
  "training": "cp9.tar.gz!/text_pipeline/repair/training-final.json"
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
  "attempts": [
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "clean_names"
      ],
      "function_attempt": 1,
      "index": 0
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "clean_names"
      ],
      "function_attempt": 2,
      "index": 1
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "decode_label"
      ],
      "function_attempt": 1,
      "index": 2
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "decode_label"
      ],
      "function_attempt": 2,
      "index": 3
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "describe"
      ],
      "function_attempt": 1,
      "index": 4
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "describe"
      ],
      "function_attempt": 2,
      "index": 5
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "encode_label"
      ],
      "function_attempt": 1,
      "index": 6
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "encode_label"
      ],
      "function_attempt": 2,
      "index": 7
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "pair_names"
      ],
      "function_attempt": 1,
      "index": 8
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "pair_names"
      ],
      "function_attempt": 2,
      "index": 9
    }
  ],
  "max_attempts_per_function": 2,
  "retry_counts": {
    "main.py::clean_names": 2,
    "main.py::decode_label": 2,
    "main.py::describe": 2,
    "main.py::encode_label": 2,
    "main.py::pair_names": 2
  }
}
```


```json
{
  "cp5": {
    "attempts": 5,
    "cost_complete": true,
    "evidence_kinds": {
      "mock": 5
    },
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "record": "cp5.tar.gz!/text_pipeline/private/llm/calls.jsonl",
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "cp7": {
    "attempts": 7,
    "cost_complete": true,
    "evidence_kinds": {
      "mock": 7
    },
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "record": "cp7.tar.gz!/text_pipeline/llm/calls.jsonl",
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "cp8": {
    "attempts": 1,
    "cost_complete": true,
    "evidence_kinds": {
      "mock": 1
    },
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "record": "cp8.tar.gz!/text_pipeline/llm/calls.jsonl",
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "cp9": {
    "attempts": 10,
    "cost_complete": true,
    "evidence_kinds": {
      "mock": 10
    },
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "record": "cp9.tar.gz!/text_pipeline/llm/calls.jsonl",
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/text_pipeline/repair/training-final.json#726a9707f6b8681a538d",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/text_pipeline/repair/training-final.json#ab63227f76f8d0efd3ef",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/text_pipeline/repair/training-final.json#6c672f24c270e03d2a02",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/text_pipeline/repair/training-final.json#56373a722e78d01fa485",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/text_pipeline/repair/training-final.json#b6384cd6d19716efb5d7",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/text_pipeline/repair/training-final.json#fddd3749f79f7ff16e94",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/text_pipeline/repair/training-final.json#2d3ddf46fe4eef997dd2",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/text_pipeline/repair/training-final.json#5f2b1c611a9f837afaa0",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/text_pipeline/repair/training-final.json#4d4aa3e3875bc16f4f64",
    "split": "training"
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
    "category": "runtime_exception:UnicodeDecodeError",
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
    "run": "cp9.tar.gz!/text_pipeline/repair/training-final.json#6741ce7d68a4f00fe686",
    "split": "training"
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
    "category": "runtime_exception:UnicodeDecodeError",
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
    "run": "cp9.tar.gz!/text_pipeline/repair/training-final.json#c78c9c114ae67a202efd",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/text_pipeline/repair/training-final.json#1da4ece3f3dc25151a35",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/text_pipeline/repair/training-final.json#21f941606c7c635eaf9b",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/text_pipeline/repair/training-final.json#2b14ad1e199ea9f019f2",
    "split": "training"
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
    "category": "runtime_exception:UnicodeEncodeError",
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
    "run": "cp9.tar.gz!/text_pipeline/repair/training-final.json#269244e7fba00e42e183",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/text_pipeline/repair/training-final.json#5c25be3b3eed8b4d6998",
    "split": "training"
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
    "category": "runtime_exception:UnicodeDecodeError",
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
    "run": "cp9.tar.gz!/text_pipeline/repair/training-final.json#5a45c6834552576fa83f",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/text_pipeline/repair/training-final.json#6ec197437cb261363926",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/text_pipeline/repair/training-final.json#2fb20be9aac20aadfc7d",
    "split": "training"
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
    "category": "runtime_exception:UnicodeEncodeError",
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
    "run": "cp9.tar.gz!/text_pipeline/repair/training-final.json#42feeb19a65990275c63",
    "split": "training"
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
    "category": "runtime_exception:AttributeError",
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
    "run": "cp9.tar.gz!/text_pipeline/heldout.json#11a4d8c58484fe3274dd",
    "split": "heldout"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/text_pipeline/heldout.json#01d3efe461a877d3b62a",
    "split": "heldout"
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
    "category": "runtime_exception:AttributeError",
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
    "run": "cp9.tar.gz!/text_pipeline/heldout.json#0fef156a3f6a59aa53a8",
    "split": "heldout"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/text_pipeline/heldout.json#0c4db0f662d8a9bafdd5",
    "split": "heldout"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/text_pipeline/heldout.json#13a56036a6b33739aeef",
    "split": "heldout"
  }
]
```

### Review flags and suspected legacy bugs

```json
[
  "Frozen CP5 observations distinguish Python 2 str/unicode, exception modules and argument types from Python 3 bytes/str/builtins. Source-only changes cannot reproduce those built-in runtime identities. No safe patch is proposed; comparisons and fixtures stay unchanged. Review remaining semantic differences too."
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
Observed exceptions: 
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
Observed exceptions: exceptions.UnicodeDecodeError
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
     u'[Machine-generated]\nStrip each supplied name, then remove false-valued results. Python 2 map and filter materialize lists. The nested lambda belongs to this helper.\n\nObserved return types: list\nObserved exceptions: \nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
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
     u"[Machine-generated]\nCall the label's UTF-8 encode method. In Python 2 encoding Unicode text produces a byte string; inputs that cannot be encoded retain their legacy exceptions.\n\nObserved return types: str\nObserved exceptions: exceptions.UnicodeDecodeError\nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven."
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

## ranking

### Evidence references

```json
{
  "baseline": "cp6.tar.gz!/ranking.json",
  "coverage": "cp5.tar.gz!/ranking/private/ranking-report.json",
  "diffs": "cp9.tar.gz!/ranking/full-diffs/",
  "documentation": "cp7.tar.gz!/ranking/documentation.json",
  "heldout": "cp9.tar.gz!/ranking/heldout.json",
  "quarantine": "cp5.tar.gz!/ranking/private/ranking-quarantine.json",
  "repairs": "cp9.tar.gz!/ranking/repair/attempts.json",
  "training": "cp9.tar.gz!/ranking/repair/training-final.json"
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
  "attempts": [
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "Scoreboard.__init__"
      ],
      "function_attempt": 1,
      "index": 0
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "Scoreboard.__init__"
      ],
      "function_attempt": 2,
      "index": 1
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "Scoreboard.add"
      ],
      "function_attempt": 1,
      "index": 2
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "Scoreboard.add"
      ],
      "function_attempt": 2,
      "index": 3
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "Scoreboard.ranked"
      ],
      "function_attempt": 1,
      "index": 4
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "Scoreboard.ranked"
      ],
      "function_attempt": 2,
      "index": 5
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "compare_scores"
      ],
      "function_attempt": 1,
      "index": 6
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "main.py",
        "compare_scores"
      ],
      "function_attempt": 2,
      "index": 7
    }
  ],
  "max_attempts_per_function": 2,
  "retry_counts": {
    "main.py::Scoreboard.__init__": 2,
    "main.py::Scoreboard.add": 2,
    "main.py::Scoreboard.ranked": 2,
    "main.py::compare_scores": 2
  }
}
```


```json
{
  "cp5": {
    "attempts": 4,
    "cost_complete": true,
    "evidence_kinds": {
      "mock": 4
    },
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "record": "cp5.tar.gz!/ranking/private/llm/calls.jsonl",
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "cp7": {
    "attempts": 7,
    "cost_complete": true,
    "evidence_kinds": {
      "mock": 7
    },
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "record": "cp7.tar.gz!/ranking/llm/calls.jsonl",
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "cp8": {
    "attempts": 1,
    "cost_complete": true,
    "evidence_kinds": {
      "mock": 1
    },
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "record": "cp8.tar.gz!/ranking/llm/calls.jsonl",
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "cp9": {
    "attempts": 8,
    "cost_complete": true,
    "evidence_kinds": {
      "mock": 8
    },
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "record": "cp9.tar.gz!/ranking/llm/calls.jsonl",
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
    "category": "runtime_exception:IndexError",
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
    "run": "cp9.tar.gz!/ranking/repair/training-final.json#de9cc2d30b487c37f8cd",
    "split": "training"
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
    "category": "runtime_exception:TypeError",
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
    "run": "cp9.tar.gz!/ranking/repair/training-final.json#48b0a70fa1e90a5ce78a",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/ranking/repair/training-final.json#802d468fafe139f8574a",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/ranking/repair/training-final.json#caf3b9ff00e0c8db5c45",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/ranking/repair/training-final.json#9dfaa77b8cd1ae7f6062",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/ranking/repair/training-final.json#f51a64f2ccc20ad6cd59",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/ranking/repair/training-final.json#be9ef3d6da9141b3433d",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/ranking/repair/training-final.json#e14fba78f97e7c5681d8",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/ranking/repair/training-final.json#4b2402edf0cf8c4c3f54",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/ranking/repair/training-final.json#52d2dbb5c21652fa43ba",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/ranking/repair/training-final.json#7fb896b5f23e0f1df46b",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/ranking/repair/training-final.json#f96e5a01843f84546806",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/ranking/heldout.json#46b4ec53acffc20e3556",
    "split": "heldout"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/ranking/heldout.json#1fc9a907d97efcc99436",
    "split": "heldout"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/ranking/heldout.json#361aab45580a01185bcd",
    "split": "heldout"
  }
]
```

### Review flags and suspected legacy bugs

```json
[
  "Frozen CP5 observations distinguish Python 2 str/unicode, exception modules and argument types from Python 3 bytes/str/builtins. Source-only changes cannot reproduce those built-in runtime identities. No safe patch is proposed; comparisons and fixtures stay unchanged. Review remaining semantic differences too."
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

Observed return types: 
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

## file_report

### Evidence references

```json
{
  "baseline": "cp6.tar.gz!/file_report.json",
  "coverage": "cp5.tar.gz!/file_report/private/file_report-report.json",
  "diffs": "cp9.tar.gz!/file_report/full-diffs/",
  "documentation": "cp7.tar.gz!/file_report/documentation.json",
  "heldout": "cp9.tar.gz!/file_report/heldout.json",
  "quarantine": "cp5.tar.gz!/file_report/private/file_report-quarantine.json",
  "repairs": "cp9.tar.gz!/file_report/repair/attempts.json",
  "training": "cp9.tar.gz!/file_report/repair/training-final.json"
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
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "reportkit/__init__.py",
        "build_report"
      ],
      "function_attempt": 1,
      "index": 0
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "reportkit/__init__.py",
        "build_report"
      ],
      "function_attempt": 2,
      "index": 1
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "reportkit/storage.py",
        "read_numbers"
      ],
      "function_attempt": 1,
      "index": 2
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "reportkit/storage.py",
        "read_numbers"
      ],
      "function_attempt": 2,
      "index": 3
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "reportkit/storage.py",
        "write_report"
      ],
      "function_attempt": 1,
      "index": 4
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "reportkit/storage.py",
        "write_report"
      ],
      "function_attempt": 2,
      "index": 5
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "reportkit/summary.py",
        "summarize"
      ],
      "function_attempt": 1,
      "index": 6
    },
    {
      "accepted": false,
      "error": "no source patch proposed; needs human review",
      "function": [
        "reportkit/summary.py",
        "summarize"
      ],
      "function_attempt": 2,
      "index": 7
    }
  ],
  "max_attempts_per_function": 2,
  "retry_counts": {
    "reportkit/__init__.py::build_report": 2,
    "reportkit/storage.py::read_numbers": 2,
    "reportkit/storage.py::write_report": 2,
    "reportkit/summary.py::summarize": 2
  }
}
```


```json
{
  "cp5": {
    "attempts": 8,
    "cost_complete": true,
    "evidence_kinds": {
      "mock": 8
    },
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "record": "cp5.tar.gz!/file_report/private/llm/calls.jsonl",
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "cp7": {
    "attempts": 9,
    "cost_complete": true,
    "evidence_kinds": {
      "mock": 9
    },
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "record": "cp7.tar.gz!/file_report/llm/calls.jsonl",
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "cp8": {
    "attempts": 1,
    "cost_complete": true,
    "evidence_kinds": {
      "mock": 1
    },
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "record": "cp8.tar.gz!/file_report/llm/calls.jsonl",
    "unknown_cost_attempts": 0,
    "unknown_usage_attempts": 0,
    "usage_complete": true
  },
  "cp9": {
    "attempts": 8,
    "cost_complete": true,
    "evidence_kinds": {
      "mock": 8
    },
    "known_estimated_usd": "0",
    "known_tokens": {
      "cache_write_tokens": 0,
      "cached_input_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    },
    "known_total_tokens": 0,
    "record": "cp9.tar.gz!/file_report/llm/calls.jsonl",
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
              "type": "int",
              "value": "9"
            },
            {
              "type": "str",
              "value": "Bad file descriptor"
            }
          ],
          "type": "tuple"
        },
        "message": "[Errno 9] Bad file descriptor",
        "module": "builtins",
        "name": "OSError",
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
    "category": "runtime_exception:OSError",
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
    "run": "cp9.tar.gz!/file_report/repair/training-final.json#e665e1c7d0504c7b33c6",
    "split": "training"
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
    "category": "runtime_exception:ValueError",
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
    "run": "cp9.tar.gz!/file_report/repair/training-final.json#9bd5e615de8ece947f1d",
    "split": "training"
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
    "category": "runtime_exception:ValueError",
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
    "run": "cp9.tar.gz!/file_report/repair/training-final.json#d5290c50168b68963fdc",
    "split": "training"
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
    "category": "runtime_exception:ValueError",
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
    "run": "cp9.tar.gz!/file_report/repair/training-final.json#6860a61cb6e5525bea67",
    "split": "training"
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
    "category": "runtime_exception:UnicodeDecodeError",
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
    "run": "cp9.tar.gz!/file_report/repair/training-final.json#5c6691a653902c4bcbda",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/file_report/repair/training-final.json#dbcef5cdcb7fa78412ac",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/file_report/repair/training-final.json#981e41f6e4e76360f5a2",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/file_report/repair/training-final.json#6a64b8ae60bf34fb3a82",
    "split": "training"
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
    "category": "runtime_exception:TypeError",
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
    "run": "cp9.tar.gz!/file_report/repair/training-final.json#deb9759c28f1d6e10620",
    "split": "training"
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
    "category": "runtime_exception:TypeError",
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
    "run": "cp9.tar.gz!/file_report/repair/training-final.json#60b44226959740392362",
    "split": "training"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/file_report/repair/training-final.json#26f0affcae44a95ee5d7",
    "split": "training"
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
    "category": "runtime_exception:UnicodeEncodeError",
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
    "run": "cp9.tar.gz!/file_report/heldout.json#14a86d2c5e895a90a6cb",
    "split": "heldout"
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
    "category": "outcome_mismatch",
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
    "run": "cp9.tar.gz!/file_report/heldout.json#25a9132e4eb2071add56",
    "split": "heldout"
  }
]
```

### Review flags and suspected legacy bugs

```json
[
  "Frozen CP5 observations distinguish Python 2 str/unicode, exception modules and argument types from Python 3 bytes/str/builtins. Source-only changes cannot reproduce those built-in runtime identities. No safe patch is proposed; comparisons and fixtures stay unchanged. Review remaining semantic differences too."
]
```


```json
[
  {
    "key": "file_report/reportkit/__init__.py::build_report",
    "record": "cp7.tar.gz!/file_report/documentation.json",
    "text": "Create or overwrite the input file with fixed numeric sample data, read it, compute a summary, add a pseudo-random ticket and current timestamp, then write and return the report. This describes source structure: successful training outcomes are unavailable because clock-dependent cases were quarantined. Suspected legacy bug: the supplied input path is overwritten before being read."
  },
  {
    "key": "file_report",
    "record": "cp7.tar.gz!/file_report/documentation.json",
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
Observed exceptions: exceptions.UnicodeDecodeError
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
@@ -10,10 +10,10 @@
 def build_report(input_path, output_path, seed=None):
     u'[Machine-generated]\nCreate or overwrite the input file with fixed numeric sample data, read it, compute a summary, add a pseudo-random ticket and current timestamp, then write and return the report. This describes source structure: successful training outcomes are unavailable because clock-dependent cases were quarantined. Suspected legacy bug: the supplied input path is overwritten before being read.\n\nObserved return types: \nObserved exceptions: exceptions.TypeError\nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
     with open(input_path, 'wb') as stream:
-        stream.write('7\n-2\n0\n')
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
@@ -0,0 +1,9 @@
+"""[Machine-generated] Compatibility for built-in numeric division."""
+
+
+def legacy_divide(left, right):
+    """[Machine-generated] Floor integer quotients; divide other numbers normally."""
+    # shortcut: custom Python 2 __div__ protocols are unsupported; review user-defined numeric types.
+    if isinstance(left, int) and isinstance(right, int):
+        return left // right
+    return left / right

```

### Diff: reportkit/storage.py.diff

```diff
--- a/reportkit/storage.py
+++ b/reportkit/storage.py
@@ -10,5 +10,7 @@
 def write_report(path, report):
     u'[Machine-generated]\nOpen a report file in binary write mode and serialize sorted mapping entries as key=value lines using iteritems. Opening truncates an existing file before iteration; formatting can expose Python 2 Unicode encoding errors.\n\nObserved return types: NoneType\nObserved exceptions: exceptions.UnicodeDecodeError\nLimitations: Source-based description. Claims cover training observations only; untested inputs, dynamic calls and quarantined behavior are not proven.'
     with open(path, 'wb') as stream:
-        for key, value in sorted(report.iteritems()):
-            stream.write('%s=%s\n' % (key, value))
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


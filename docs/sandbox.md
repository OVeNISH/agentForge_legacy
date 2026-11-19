# CP3 sandbox execution

The Python API runs an input snapshot in either existing runtime image. It does
not generate tests or perform conversion. Example, from the repository root:

```python
from modernize.config import Config
from modernize.sandbox import Limits, SandboxRunner

runner = SandboxRunner(Config().legacy_image, Limits(timeout_seconds=3))
record = runner.run('corpus/golden_ledger', 'main.py', 'split_bill', args=(7, 2))
# Scripts and supplied test suites use the same policy:
script_record = runner.run_tests('corpus/golden_ledger', 'main.py')
```

Use `Config().modern_image` to select Python 3.12. `function=None` executes the
script as `__main__`; a dotted function identifier imports the selected module
and invokes the function. Package-relative imports are supported. Arguments and
keyword arguments are explicitly transported, not interpolated into code.
The controller never imports or executes input modules. Source assets are
included, with the CP2 cache/VCS directory exclusions; symlinks and non-regular
input files are rejected. The snapshot is limited to 4 MiB and 8 MiB of request
JSON. Original source bytes and SHA-256 identities stay on the host unchanged.

## Isolation policy

- Linux Docker containers, pinned to the inspected image ID. Images declaring
  volumes are rejected, preventing implicit writable host-backed volumes.
- No project or fixture bind mounts. Only the two trusted harness files are
  mounted, both read-only; the root filesystem is read-only.
- Docker logging is disabled; captures travel over the attached pipe, avoiding
  a host log file for container output.
- No external network (`--network none`). Docker's private loopback interface
  remains available within the container; there is no host networking/socket.
- UID/GID 65534, all Linux capabilities dropped, no-new-privileges, 32-PID limit,
  64-descriptor limit, core dumps disabled, one CPU, bounded memory and no extra
  swap. The actual Docker configuration is recorded after execution.
- `/scratch` is a 32 MiB tmpfs. It holds the disposable source copy, supervisor
  control files and `/scratch/work`, the target's current directory. Writes to
  this copy are discarded when the container is removed. Docker's isolated
  device filesystems are also ephemeral. No legacy writes reach a host mount.
- The child has hard CPU-time, address-space and file-size limits. Defaults:
  two CPU seconds, 128 MiB address space/container memory, and a three-second
  wall-clock deadline. `Limits` validates supported bounds.
- The supervisor kills a timed-out child, stops other container processes,
  captures remaining output and files, and exits. The controller has a second
  deadline (target deadline plus ten seconds); if that expires, it kills the
  container. Cleanup always attempts `docker rm -f`; failure raises an error.

CPU limit and memory exceptions are observed outcomes, not repaired or swallowed
source errors. A negative target exit code records its signal. `resource_limit`
denotes signal termination under the policy; the code alone cannot distinguish
a resource signal from a target deliberately signaling itself. The controlled
CPU probe proves hard CPU termination. The memory probe proves a 512 MiB request
is refused under a 64 MiB address-space/container bound, via `MemoryError`.

## Result schema

The returned record separates execution metadata from observable results:

| Field | Meaning |
|---|---|
| `image_id`, `create_command` | Actual pinned runtime and exact container policy |
| `source_sha256`, `request`, `limits` | Immutable input identities and invocation |
| `isolation` | Actual Docker configuration, including mount types and write flags |
| `container_state`, `docker_exit_code` | Supervisor state/exit and OOM information |
| `protocol_error`, `supervisor_stderr_base64` | Harness/Docker failures, separate from target stderr |
| `container_removed` | True only after successful removal |
| `result` | Validated capture object, or null on protocol/infrastructure failure |

The capture object has exactly `status`, `value`, `exception`, `target_exit_code`,
`stdout_base64`, `stderr_base64`, `files`, and `capture_error`. Statuses:
`completed`, `exception`, `timeout`, `resource_limit`, `capture_error`,
`infrastructure_error`. A completed supervisor does not imply the target passed:
captured target exceptions normally leave the supervisor exit code at zero.
Callers must check protocol errors and the capture status. Nonzero supervisor
exit, OOM, malformed/missing results or host deadlines cannot produce an accepted
completed capture. Unsupported values are explicit capture errors.

Return values and exception arguments retain runtime type names: for example,
Python 2 byte strings are `str` with `base64`, while Python 3 bytes are `bytes`;
Python 2 text is `unicode`, Python 3 text is `str` with `value`. No type differences
are erased. Scalars carry their type and value, integer values are decimal
strings, floats use `hex`, and lists/tuples/sets/dicts retain distinct tags.
Unsupported objects and nesting beyond 30 levels fail capture rather than use
unstable `repr` fallbacks. Exceptions preserve module, class, typed arguments,
message and structured traceback frames, including file/line/function.

For a stable wire representation, dict entries are sorted by their encoded key
and set members by their encoded value. This treats them as unordered values
and is applied equally to both runtimes; all key/value types remain intact.
When iteration order is observable, capture an explicit list of items or its
stdout; those sequences/bytes are not sorted or normalized. Whitespace, byte
strings, text, numbers, exceptions and file contents are never loosened.

`files` records scratch-relative paths for newly created or modified regular
files, their bytes (base64) and SHA-256. Unchanged input copies and reserved root
control/log files are excluded. Symlinks record their targets without following
them. Empty directories and deletions are not represented. Streams are capped at
1 MiB each; captured file content totals at most 1 MiB and 128 records. Filesize
and scratch limits bound writes. Unsupported files, unreadable files and capture
overflow produce explicit capture errors, with no successful partial comparison.
Host Docker streams are independently capped at 8 MiB each.

## Verification and boundaries

Run all unit tests followed by integration tests, including both live runtimes:

```sh
MODERNIZE_DOCKER_TESTS=1 python3 scripts/test.py
```

This needs Docker access. Without that variable, live tests are explicitly
skipped, not counted as runtime evidence. `artifacts/cp3-live.json` is generated
from the live tests. [Committed run records](evidence/cp3.json) contain every
execution, input hashes, observed limits, outcomes and cleanup state. The evidence
unit test recomputes the isolation/replay assertions without requiring Docker.

The proofs cover the stated Linux Docker policy and probes, not all possible
kernel vulnerabilities. Target code shares a non-root UID with its in-container
supervisor and can sabotage that harness; malformed outcomes fail capture. The
harness is not a tamper-proof oracle for deliberately hostile colluding code.
Imports needed by the harness can affect modules already present in `sys.modules`;
projects that shadow standard-library names need explicit evaluation. Host
environment variables and Docker sockets are not forwarded; explicit project
assets are part of the supplied snapshot. External databases are unavailable.
Characterization coverage, normalizing time/randomness and held-out tests belong
to CP5; CP3 does not claim behaviour-preserving conversion.

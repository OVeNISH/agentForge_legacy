# CP2 static analysis contract, version 1

`modernize scan PROJECT --output NEW_DIRECTORY` inventories an immutable in-memory
snapshot and parses it with Python 2.7's `ast` and `tokenize` in Docker. No input
module is imported, executed, or converted. This stage has no LLM dependency.
The controller alone writes artifacts. The source bytes sent to a worker are
base64-encoded JSON, preserving Python 2 source encodings and hashes.

## Artifacts and structural schema

`facts.json` follows the exact structural schema in
[`facts_schema.py`](../src/modernize/facts_schema.py), checked automatically after
each parser response and after the project merge. Unknown/missing keys and wrong
types are rejected; booleans are not accepted as integers. Positions and marker
kinds are also checked. File paths, counts and SHA-256 hashes must exactly match
the controller's snapshot. There is no silent parse-failure skip.

| Top-level field | Type / meaning |
|---|---|
| `schema_version` | Integer, currently `1` |
| `files` | File records in stable relative path order |
| `index` | Merged modules, imports, calls, lexical symbols and references |
| `inventory` | `excluded` directory paths and `unsupported` asset/file paths |
| `entry_points` | Candidate top-level named functions, `path::qualname`; no claim of runtime callability |

Each file record has exactly these fields:

| Field | Type / contents |
|---|---|
| `path`, `sha256` | Relative POSIX path and original byte SHA-256 |
| `docstring` | Existing module docstring, string or null |
| `functions` | Named defs and lambdas: `name`, `qualname`, enclosing `scope`, `line`, `signature`, `decorators`, `docstring` |
| `classes` | `name`, `qualname`, enclosing `scope`, `line`, `bases`, `docstring` |
| `comments` | Tokenized comments: `line`, `column`, original `text` |
| `imports` | `scope`, `line`, `module`, imported `name` or null, bound `alias`, relative `level` |
| `calls` | Syntactic call sites: `scope`, `line`, `callee` expression |
| `symbols` | Binding occurrences: `scope`, `line`, `name`, `kind`, `target` or null |
| `references` | Name/attribute occurrences: `scope`, `line`, `column`, `name`, `context` |
| `side_effects` | Potential effects: `scope`, `line`, `kind`, `detail` |

All collections above are arrays of objects. Names, scopes and expression
representations are strings. Lines are positive integers and columns are
nonnegative integers. `<module>` denotes module scope; nested qualified names
use dots. Lambda names are `<lambda@LINE:COLUMN>` and have independent parameter
scopes. Signatures contain `parameters` (string array), trailing `defaults`
(expression string array), `vararg` and `kwarg` (strings or null). Python 2 tuple
parameters are represented as AST expressions; all bound names are recorded.
Decorators and bases are expression string arrays. Simple names/attributes retain
their spelling; other expressions use Python 2 `ast.dump`, without evaluation.

Symbol kinds are `function`, `class`, `parameter`, `variable`, `import`, `global`.
Reference contexts are `Load`, `Store`, `Del`. Import levels are nonnegative;
zero means a plain import, positive values count leading dots.

## Project graph schema and resolution

- `modules`: object mapping dotted inventory module names to source paths.
- `imports`: file import records plus `source` path and `target` path or null.
- `calls`: file call records plus `path`, `resolved_name` or null, and `target`
  definition ID or null. A definition ID is `path::qualname`. Null explicitly
  means unresolved, dynamic, or external; it does not mean an absent call.
- `symbols`: unique lexical bindings with `id`, `path`, `scope`, `name`, `kinds`
  (string array) and occurrence `lines` (integer array). IDs use
  `path::scope::name`; multiple possible bindings are retained.
- `references`: file reference records plus `path` and lexical `binding` ID or null.

Resolution handles explicit relative imports, Python 2 implicit sibling imports,
`absolute_import`, import aliases, package re-exports, nested functions, parameter
shadowing, `global` declarations and the distinction between class and function
lexical scope. Cyclic re-exports and conflicting import bindings terminate with
unresolved targets. Instance receiver types and dynamic dispatch are not inferred.

## Side-effect markers

Markers are conservative syntax-based candidates, including effects in uncalled
functions; they are not proof of execution. Import aliases and local shadowing
are considered before classifying calls and environment accesses.

| Kind | Representative recognized constructs |
|---|---|
| `file_io` | builtin `open`/`file`, `io.open`, selected `os` file operations |
| `network` | `socket`, `urllib`/`urllib2`, `httplib`, `requests`, `http` calls |
| `database` | `sqlite3`, `psycopg2`, `MySQLdb`, `pymysql`, `sqlalchemy` calls |
| `environment` | `os.getenv`/`putenv`/`unsetenv`, `os.environ` accesses |
| `time` | `time`, `datetime` calls |
| `randomness` | `random`, `secrets`, `os.urandom` calls |
| `global_mutable` | Module mutable literals/comprehensions, constructor/call results, attribute/subscript assignments; explicit `global` declarations |

Global call results are marked as potentially mutable even if their runtime
value turns out immutable. Conversely, arbitrary mutation through aliases,
extension modules, reflective code, wildcard imports, monkey-patching and
dynamic imports cannot be resolved fully. Generator/comprehension scoping and
data flow are approximate. These facts cannot authorize a later source rewrite
by themselves; unresolved impact needs review. Additional APIs can escape this
finite marker list; absence of a marker is not a safety guarantee.

## Inventory, execution modes, and run records

`.py`, `.pyw`, and extensionless files with a Python shebang are supported.
`.git`, `.venv`, `__pycache__`, and `.pytest_cache` directories are explicitly
excluded and reported. Other assets are reported as unsupported. Symlinks,
non-regular files, ambiguous module names, empty projects and source snapshots
over 16 MiB cause explicit failure.

Sequential mode parses files in sorted order. Parallel mode uses a bounded
controller thread pool with 1–4 workers. Each worker starts one parser container
with the same pinned image identity, no network, no project mount, a read-only
trusted parser mount, a non-root user, 128 MiB memory, one CPU, CPU limit,
PID limit, tmpfs and a 30-second timeout. Aggregate bounds are at most four CPUs
and 512 MiB of container memory; controller/Docker overhead is additional.
On timeout the controller attempts container removal. Source writes never occur.

Facts are merged in the same stable order in both modes. Execution metadata is
kept separately in `run.json`: mode, worker bound, status, image identity, each
parse command, return code and stderr; failures also have an error string.
Output directories must be new and outside the input project. On parse failure
the CLI exits 2 and keeps `run.json`, without publishing a partial `facts.json`.

`LanguageAdapter` defines parse, entry-point listing, conversion and execution
boundaries. `Python2Adapter` implements only CP2 operations; conversion and test
execution explicitly raise `NotImplementedError` until their checkpoints.
These parser restrictions do not constitute CP3's execution sandbox proof.

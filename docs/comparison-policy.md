# Python 2/Python 3 comparison policy v1

The user requested completing the comparison-policy, semantic-repair and repeat-run
work after the strict pipeline delivery. This authorizes a documented policy under
AGENTS.md section 5; raw fixtures, observations and strict results remain unchanged.
Policy identifier: `python2-python3.v1`. It is an explicit alternative to `strict`.

The same pure transformation is applied to each recorded expectation and actual
observation. It has no access to fixture IDs, input values, project names, source
or pass/fail goals. Policy identity and implementation hash must be recorded.

- Python 2 byte `str` and Python 3 `bytes` map to binary; Python 2 `unicode` and
  Python 3 text `str` map to text. Binary and text remain unequal, including ASCII.
  All bytes and Unicode code points remain exact. `long`/`int` map to integer;
  integer, float, boolean and container types remain distinct.
- Dictionary/set representations are sorted again after type canonicalization.
  List/tuple ordering is retained. Only top-level instance `__dict__` attribute
  names are treated as identifiers; nested user dictionary keys retain their types.
- Built-in exception modules `exceptions` and `builtins` have one identity. The
  exception class name stays exact. Custom exception modules stay distinct.
- Built-in one-message exceptions use that same message as structured diagnostic
  text instead of comparing Python 2 ASCII diagnostic bytes to Python 3 text.
  Unknown messages stay exact. Complete recognized TypeError grammars preserve
  operator, operand types, invalid int argument type, or called function name and
  arity; Python-version phrasing/qualification is canonicalized. AttributeError
  preserves object type and missing attribute. Invalid-int ValueError diagnostic
  repr prefixes `b`/`u` are canonicalized; the literal contents/base stay exact.
- Unicode encode/decode errors preserve encoding (using codec aliases), payload,
  start/end offsets and reason. Their redundant runtime-generated sentence is
  represented by those same structured fields; the payload still distinguishes
  binary from text. Changed payload, offset, encoding or reason fails comparison.

No user return strings are parsed or rewritten. Exception-message normalization
does not affect strings returned by code. File bytes/paths, stdout, stderr, exit
codes, exception classes, unknown diagnostics, whitespace and real value changes
remain exact. Integer file descriptors accepted only in Python 3 are a behavior
bug to fix in source, not a normalization rule. No additional quarantine is allowed
to conceal a failure. Original quarantines and coverage limitations stay visible.

Structured interpreter diagnostics are an explicit boundary: their wording and
runtime type names may change while their semantic fields must match. This does
not claim byte-for-byte exception rendering compatibility. Both raw and policy
rates must be shown, including separate held-out rates. Existing strict evidence
continues to verify as before. A policy pass is never relabeled as a raw pass.

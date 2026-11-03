"""Run the shared conformance vectors against this binding.

The vectors are written once, in wmoop.doc (``external/wmoop.doc/conformance/``; the format is its
README.md), and every binding runs them. This runner reads the bundle ``suite.json`` and drives the
generated classes through their model ids (``WM_ID``) and the model's member names. The hand-written
behaviour in ``wmoop_ext`` is what the ``behaviour`` cases check. Exit code is non-zero when an
active case fails, so CI can gate on it.

    python conformance.py                    # every case
    python conformance.py conf.transport     # only the cases whose id starts with a prefix
"""
from __future__ import annotations

import datetime
import importlib
import inspect
import json
import os
import sys
from collections.abc import Callable
from enum import Enum
from typing import Any

# The generated wmoop.* modules live in generated/; wmoop_ext and wmoop.patterns next to this file.
_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(_ROOT, "generated"), _ROOT]

from wmoop.core import ConceptId, Entity, Many, Quantity, Role, WmoopError  # noqa: E402

SUITE = os.path.join(_ROOT, "external", "wmoop.doc", "conformance", "suite.json")
FORMAT = 1


class Mismatch(Exception):
    """The binding did not do what the case says."""


class LanguageRule(Exception):
    """A rule Python enforces before any binding code runs, reported with the model's code."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


Names = dict[str, Any]


# ------------------------------------------------------------------ model types and members
def model_type(type_id: str) -> type:
    """The generated class whose WM_ID is ``type_id``: resolved through metadata, not a naming rule."""
    module = importlib.import_module(type_id.partition("/")[0])
    for value in vars(module).values():
        if isinstance(value, type) and vars(value).get("WM_ID") == type_id:
            return value
    raise Mismatch(f"no generated class has WM_ID {type_id}")


def _key(name: str) -> str:
    return name.replace("_", "").lower()


def member(obj: object, model_name: str) -> str:
    """The attribute of ``obj`` that is the model member ``model_name``: equal ignoring case and underscores."""
    want = _key(model_name)
    found = {n for k in type(obj).__mro__ for n in vars(k) if not n.startswith("_") and _key(n) == want}
    if len(found) != 1:
        raise Mismatch(f"{type(obj).__name__} has {'no' if not found else 'several'} member(s) for '{model_name}'")
    return found.pop()


# ------------------------------------------------------------------ values
def value(v: Any, names: Names) -> Any:
    """A value of the vectors' encoding, as this binding's own type."""
    if isinstance(v, list):
        return [value(item, names) for item in v]
    if isinstance(v, dict):
        if "ref" in v:
            return names[v["ref"]]
        if "date" in v:
            return datetime.date.fromisoformat(v["date"])
        if "unit" in v:
            return Quantity(v["value"], v["unit"])
        if "id" in v:
            return ConceptId(v["id"])
    return v  # a scalar; an enumeration value stays its model id, which the generated code converts


def plain(v: Any, names: Names) -> Any:
    """A result in the vectors' encoding, so it can be compared with ``equals``."""
    if isinstance(v, Enum):
        return v.value
    if v is None or isinstance(v, (bool, int, float, str)):
        return v
    if isinstance(v, datetime.date):
        return {"date": v.isoformat()}
    if isinstance(v, Quantity):
        return {"value": v.value, "unit": v.unit}
    if isinstance(v, ConceptId):
        return {"id": v.value}
    if isinstance(v, (Entity, Role)):
        for name, obj in names.items():
            if obj is v:
                return {"ref": name}
        raise Mismatch(f"a query returned {v}, which no step bound")
    if hasattr(v, "__iter__"):
        return [plain(item, names) for item in v]
    raise Mismatch(f"cannot compare a {type(v).__name__}")


def same(a: Any, b: Any) -> bool:
    """Equality of two plain values: numbers by value, but a boolean is never a number."""
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a == b
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    return type(a) is type(b) and a == b


# ------------------------------------------------------------------ steps
def arguments(cls: type, given: dict[str, Any], names: Names) -> dict[str, Any]:
    """Keyword arguments for ``cls`` from the case's model properties."""
    params = {p.name: p for p in inspect.signature(cls.__init__).parameters.values() if p.kind is p.KEYWORD_ONLY}
    by_key = {_key(name): name for name in params}
    kwargs = {}
    for model_name, v in given.items():
        if _key(model_name) not in by_key:
            raise Mismatch(f"{cls.__name__} takes no argument for '{model_name}'")
        kwargs[by_key[_key(model_name)]] = value(v, names)
    missing = [n for n, p in params.items() if p.default is p.empty and n not in kwargs]
    if missing:  # Python refuses the call itself: a keyword-only argument without a default
        raise LanguageRule("WM-REQUIRED-MISSING", f"{cls.__name__} requires {', '.join(missing)}")
    return kwargs


def construct(a: dict, names: Names) -> None:
    cls = model_type(a["type"])
    kwargs = arguments(cls, a.get("with", {}), names)
    if issubclass(cls, Role):
        obj = cls(**kwargs)
    else:
        default = a.get("bind") or a["type"].rsplit("/", 1)[1]
        obj = cls(a.get("id", f"conformance/{default}"), a.get("name", default), **kwargs)
    if "bind" in a:
        names[a["bind"]] = obj


def attach_role(a: dict, names: Names) -> None:
    if "ref" in a:
        role = names[a["ref"]]
    else:
        cls = model_type(a["role"])
        role = cls(**arguments(cls, a.get("with", {}), names))
        if "bind" in a:
            names[a["bind"]] = role
    names[a["to"]].add_role(role)


def _end(obj: object, relation: str) -> tuple[str, bool]:
    """The attribute of a relation end, and whether it is to-many."""
    attr = member(obj, relation)
    return attr, isinstance(inspect.getattr_static(type(obj), attr), Many)


def link(a: dict, names: Names) -> None:
    obj, target = names[a["subject"]], names[a["to"]]
    attr, many = _end(obj, a["relation"])
    if many:
        getattr(obj, attr).add(target)
    else:
        setattr(obj, attr, target)


def unlink(a: dict, names: Names) -> None:
    obj, target = names[a["subject"]], names[a["from"]]
    attr, many = _end(obj, a["relation"])
    if many:
        getattr(obj, attr).remove(target)
    elif getattr(obj, attr) is target:
        setattr(obj, attr, None)


def assert_(a: dict, names: Names) -> None:
    check(a, names, "assert")


# ------------------------------------------------------------------ queries
def _text(q: dict, names: Names) -> str:
    if "value" in q:
        return str(value(q["value"], names))
    obj = names[q["subject"]]
    return str(getattr(obj, member(obj, q["property"])) if "property" in q else obj)


def _same_value(q: list, names: Names) -> bool:
    a, b = (value(v, names) for v in q)
    return a == b and hash(a) == hash(b)


def _call(q: dict, names: Names) -> Any:
    obj = names[q["subject"]]
    return getattr(obj, member(obj, q["operation"]))(*(value(v, names) for v in q.get("args", [])))


def _unsupported(query: str) -> Callable[[Any, Names], Any]:
    def run(q: Any, names: Names) -> Any:
        raise Mismatch(f"this binding does not support {query} yet")

    return run


QUERIES: dict[str, Callable[[Any, Names], Any]] = {
    "type_chain": lambda q, n: [vars(k)["WM_ID"] for k in type(n[q["subject"]]).__mro__ if vars(k).get("WM_ID")],
    "is_a": lambda q, n: n[q["subject"]].is_a(q["type"]),
    "get": lambda q, n: getattr(n[q["subject"]], member(n[q["subject"]], q["property"])),
    "call": _call,
    "text": _text,
    "roles": lambda q, n: [r.role_type.value for r in n[q["subject"]].roles],
    "has_role": lambda q, n: n[q["subject"]].has_role(model_type(q["role"])),
    "get_role": lambda q, n: n[q["subject"]].get_role(model_type(q["role"])),
    "role_subject": lambda q, n: n[q["role"]].subject,
    "same_value": _same_value,
    "has_capability": _unsupported("has_capability"),
    "canonical_json": _unsupported("canonical_json"),
}
STEPS: dict[str, Callable[[dict, Names], None]] = {
    "construct": construct, "attach_role": attach_role, "link": link, "unlink": unlink, "assert": assert_,
}


def check(assertion: dict, names: Names, where: str) -> None:
    (query,) = (k for k in assertion if k != "equals")
    got = plain(QUERIES[query](assertion[query], names), names)
    if not same(got, assertion["equals"]):
        raise Mismatch(f"{where}: {query} returned {json.dumps(got)}, expected {json.dumps(assertion['equals'])}")


# ------------------------------------------------------------------ cases
def run(case: dict) -> None:
    """Run one case; raises Mismatch when the binding does not do what it says."""
    names: Names = {}
    steps, expect = case.get("given", []), case["expect"]
    fails = expect["error_code"] if isinstance(expect, dict) else None
    for i, step in enumerate(steps, 1):
        ((kind, args),) = step.items()
        try:
            STEPS[kind](args, names)
        except (WmoopError, LanguageRule) as exc:
            if fails and i == len(steps):
                if exc.code != fails:
                    raise Mismatch(f"given[{i}].{kind} failed with {exc.code}, expected {fails}: {exc}") from None
                return
            raise Mismatch(f"given[{i}].{kind} failed with {exc.code}: {exc}") from None
        except Mismatch as exc:
            raise Mismatch(f"given[{i}].{kind}: {exc}") from None
        except Exception as exc:  # noqa: BLE001 - an error without a code never matches a vector
            raise Mismatch(f"given[{i}].{kind} raised {type(exc).__name__} without an error code: {exc}") from None
    if fails:
        raise Mismatch(f"every step succeeded, expected {fails}")
    for j, assertion in enumerate(expect, 1):
        check(assertion, names, f"expect[{j}]")


def main(prefixes: list[str]) -> int:
    with open(SUITE, encoding="utf-8") as fh:
        suite = json.load(fh)
    if suite.get("format") != FORMAT:
        print(f"{SUITE} has format {suite.get('format')}; this runner reads format {FORMAT}")
        return 2
    passed = failed = pending = 0
    for case in suite["cases"]:
        if prefixes and not any(case["id"].startswith(p) for p in prefixes):
            continue
        try:
            run(case)
            problem = None
        except Exception as exc:  # noqa: BLE001 - a crash in one case must not hide the others
            problem = str(exc) if isinstance(exc, Mismatch) else f"{type(exc).__name__}: {exc}"
        if case.get("status") == "pending":
            pending += 1
            note = "passes now: make it active in wmoop.doc" if problem is None else case["reason"]
            print(f"[PENDING] {case['id']}: {note}")
        elif problem is None:
            passed += 1
            print(f"[PASS] {case['id']}")
        else:
            failed += 1
            print(f"[FAIL] {case['id']}: {problem}")
    print(f"\n{passed} passed, {failed} failed, {pending} pending.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

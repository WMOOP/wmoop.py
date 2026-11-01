"""Dependency-free checks of the GENERATED binding in generated/wmoop_model.

The same flagship cases as tests.py, run against the classes wmoop.tools generates from the
pinned wmoop.doc model, so CI proves the generated binding works, not only that it is up to date.
Exit code is non-zero on failure.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated"))

from wmoop_model._runtime import ConceptId, Quantity  # noqa: E402
from wmoop_model.nature import Person  # noqa: E402
from wmoop_model.transport import Driver, Owner  # noqa: E402

_fail = 0
_total = 0


def check(label: str, ok: bool) -> None:
    global _fail, _total
    _total += 1
    print(f"[{'PASS' if ok else 'FAIL'}] {label}")
    if not ok:
        _fail += 1


def raises(exc, fn) -> bool:
    try:
        fn()
        return False
    except exc:
        return True


check("ConceptId rejects blank", raises(ValueError, lambda: ConceptId("   ")))
check("Quantity requires a unit", raises(ValueError, lambda: Quantity(1.0, "")))
check("A Driver is NOT a subclass of Person (role, not inheritance)", not issubclass(Driver, Person))

person = Person("wm:nature/person/x", "X")
person.add_role(Driver(licenceNumber="L1"))
person.add_role(Owner())
check("Person can hold Driver and Owner at once", person.has_role(Driver) and person.has_role(Owner))
check("AddRole binds the role's Subject back to the person", person.get_role(Driver).subject is person)
check("GetRole returns None when absent", Person("wm:nature/person/y", "Y").get_role(Driver) is None)

shared = Driver(licenceNumber="L3")
Person("wm:nature/person/a", "A").add_role(shared)
check("A role cannot be attached to two subjects",
      raises(RuntimeError, lambda: Person("wm:nature/person/b", "B").add_role(shared)))

print(f"\n{_total - _fail} passed, {_fail} failed.")
sys.exit(0 if _fail == 0 else 1)

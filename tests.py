"""Dependency-free conformance checks — the Python twin of wmoop.net's Wmoop.Tests.

Mirrors the same 13 checks so the two bindings demonstrably agree. Exit code is
non-zero on failure, so CI can gate on it.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import date  # noqa: E402

from wmoop.core import ConceptId, Quantity  # noqa: E402
from wmoop.nature import Person  # noqa: E402
from wmoop.transport import DriverRole, Moped, Motorcycle, OwnerRole, Vehicle  # noqa: E402

_fail = 0


def check(label: str, ok: bool) -> None:
    global _fail
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
check("ConceptId equality is by value",
      ConceptId("wm:x") == ConceptId("wm:x") and hash(ConceptId("wm:x")) == hash(ConceptId("wm:x")))
check("Quantity requires a unit", raises(ValueError, lambda: Quantity(1.0, "")))
check("Quantity renders value and unit", str(Quantity(45, "km/h")) == "45 km/h")

moped = Moped("wm:transport/moped/x", "X", Quantity(45, "km/h"), Quantity(49, "cc"))
check("Moped is-a Vehicle (polymorphism)", isinstance(moped, Vehicle))
check("Classification overrides down the chain",
      moped.classification == "moped"
      and Motorcycle("wm:transport/mc", "MC", Quantity(100, "km/h")).classification == "motorcycle")

person = Person("wm:nature/person/x", "X", 1990)
check("Person is-a Animal with 2 legs", person.leg_count == 2 and person.taxon == "Homo sapiens")
check("Person starts with no roles", len(person.roles) == 0)

person.add_role(DriverRole("L", ["AM"], date(2020, 1, 1), date(2030, 1, 1)))
person.add_role(OwnerRole(moped, date(2021, 1, 1)))
check("Person can hold Driver and Owner at once",
      person.has_role(DriverRole) and person.has_role(OwnerRole) and len(person.roles) == 2)

check("AddRole binds the role's Subject back to the person",
      person.get_role(DriverRole).subject is person)

other = Person("wm:nature/person/y", "Y", 1991)
check("GetRole returns None when absent", other.get_role(DriverRole) is None)

licence = DriverRole("L2", ["AM", "B"], date(2018, 6, 1), date(2028, 6, 1))
on = date(2026, 10, 16)
check("DriverRole validity window and category are honoured",
      licence.can_drive("AM", on)
      and not licence.can_drive("C", on)
      and not licence.can_drive("AM", date(2030, 1, 1)))

shared = DriverRole("L3", ["B"], date(2020, 1, 1), date(2030, 1, 1))
pa = Person("wm:nature/person/a", "A", 1990)
pb = Person("wm:nature/person/b", "B", 1990)
pa.add_role(shared)
check("A role cannot be attached to two subjects", raises(RuntimeError, lambda: pb.add_role(shared)))

print(f"\n{13 - _fail} passed, {_fail} failed.")
sys.exit(0 if _fail == 0 else 1)

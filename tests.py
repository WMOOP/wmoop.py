"""Dependency-free conformance checks — the Python twin of wmoop.net's Wmoop.Tests.

Mirrors the same 16 checks so the two bindings demonstrably agree. The classes under test
are generated from the WML model; the behaviour (classification, can_drive, total_population)
comes from the wmoop_ext mixins. Exit code is non-zero on failure, so CI can gate on it.
"""
import os
import sys

# The generated wmoop.* modules live in generated/; wmoop_ext and wmoop.patterns next to this file.
_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(_ROOT, "generated"), _ROOT]

from collections.abc import Callable  # noqa: E402
from datetime import date  # noqa: E402

from wmoop.core import ConceptId, Quantity  # noqa: E402
from wmoop.geography import City, Country, County  # noqa: E402
from wmoop.nature import Animal, Person  # noqa: E402
from wmoop.transport import (  # noqa: E402
    Driver, LicenceCategory, Moped, Motorcycle, Owner, RoadVehicle, Vehicle,
)

_passed = 0
_failed = 0
on = date(2026, 1, 1)


def check(name: str, body: Callable[[], bool]) -> None:
    """Run one check; a check that raises counts as failed, like [THREW] in Wmoop.Tests."""
    global _passed, _failed
    try:
        ok = body()
    except Exception as exc:  # noqa: BLE001 - any crash is reported as a failed check
        ok = False
        print(f"[THREW] {name}: {type(exc).__name__}: {exc}")
    if ok:
        _passed += 1
        print(f"[PASS] {name}")
    else:
        _failed += 1
        print(f"[FAIL] {name}")


def raises(exc: type[Exception], fn: Callable[[], object]) -> bool:
    try:
        fn()
        return False
    except exc:
        return True


def new_moped() -> Moped:
    return Moped("wmoop.transport/moped/x", "X", wheel_count=2,
                 max_speed=Quantity(45, "km/h"), engine_displacement=Quantity(49, "cm3"))


def new_person(id: str) -> Person:
    return Person(id, id, full_name=id)


def new_driver(*categories: LicenceCategory) -> Driver:
    return Driver(licence_number="L1", licence_categories=categories, licence_expiry=date(2030, 1, 1))


# ---- Kernel value types -------------------------------------------------------------
check("ConceptId rejects blank", lambda: raises(ValueError, lambda: ConceptId("   ")))
check("ConceptId equality is by value",
      lambda: ConceptId("wmoop.x/y") == ConceptId("wmoop.x/y")
      and hash(ConceptId("wmoop.x/y")) == hash(ConceptId("wmoop.x/y")))
check("Quantity requires a unit", lambda: raises(ValueError, lambda: Quantity(1, "")))
check("Quantity renders value and unit", lambda: str(Quantity(49, "cm3")) == "49 cm3")

# ---- Inheritance (shallow, honest) --------------------------------------------------
check("Moped is-a Vehicle (polymorphism)",
      lambda: all(isinstance(new_moped(), kind) for kind in (Motorcycle, RoadVehicle, Vehicle)))
check("Classification overrides down the chain",
      lambda: new_moped().classification == "moped"
      and Motorcycle("wmoop.transport/mc", "MC", wheel_count=2,
                     engine_displacement=Quantity(600, "cm3")).classification == "motorcycle")
check("Person is-a Animal with 2 legs",
      lambda: isinstance(p := Person("wmoop.nature/person/p", "P", full_name="P", leg_count=2), Animal)
      and p.leg_count == 2 and p.is_a("wmoop.nature/Human"))

# ---- Roles over composition (the cross-domain crux) ---------------------------------
check("Person starts with no roles", lambda: len(new_person("p").roles) == 0)


def holds_driver_and_owner() -> bool:
    p = new_person("p")
    p.add_role(new_driver(LicenceCategory.AM))
    p.add_role(Owner(owned_since=date(2021, 1, 1)))
    return p.has_role(Driver) and p.has_role(Owner) and len(p.roles) == 2


check("Person can hold Driver and Owner at once", holds_driver_and_owner)


def binds_subject() -> bool:
    p = new_person("p")
    role = p.add_role(new_driver(LicenceCategory.B))
    return role.subject is p


check("AddRole binds the role's Subject back to the person", binds_subject)
check("GetRole returns None when absent", lambda: new_person("p").get_role(Driver) is None)


def honours_categories_and_expiry() -> bool:
    d = new_driver(LicenceCategory.AM, LicenceCategory.B)
    return (d.can_drive(LicenceCategory.AM, on)                 # category held, in date
            and not d.can_drive(LicenceCategory.A, on)          # category not held
            and not d.can_drive(LicenceCategory.B, date(2031, 1, 1)))  # expired


check("Driver categories and expiry are honoured", honours_categories_and_expiry)


def one_subject_per_role() -> bool:
    role = new_driver(LicenceCategory.B)
    new_person("p1").add_role(role)
    return raises(RuntimeError, lambda: new_person("p2").add_role(role))


check("A role cannot be attached to two subjects", one_subject_per_role)
check("A role refuses a subject that is not its played_by type (Driver on a Moped)",
      lambda: raises(TypeError, lambda: new_moped().add_role(new_driver(LicenceCategory.B))))


# ---- Generated relations ------------------------------------------------------------
def owns_and_owned_by_in_step() -> bool:
    owner = new_person("p").add_role(Owner())
    moped = new_moped()
    owner.owns.add(moped)
    linked = owner in moped.owned_by
    moped.owned_by.remove(owner)
    return linked and len(owner.owns) == 0


check("Owner.owns and Vehicle.owned_by stay in step", owns_and_owned_by_in_step)


def composite_move() -> bool:
    country = Country("wmoop.geography/c", "C")
    county = County("wmoop.geography/k", "K")
    county.part_of = country
    city = City("wmoop.geography/x", "X", resident_population=10)
    city.part_of = country
    city.part_of = county
    return len(country.contains) == 1 and city in county.contains and country.total_population == 10


check("Composite: moving a city updates both parents", composite_move)

print(f"\n{_passed} passed, {_failed} failed.")
sys.exit(0 if _failed == 0 else 1)

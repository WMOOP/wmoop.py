"""Design-patterns showcase — the Python twin of wmoop.net's Wmoop.Patterns.Demo."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import date  # noqa: E402

from wmoop.core import Quantity  # noqa: E402
from wmoop.nature import Person  # noqa: E402
from wmoop.transport import DriverRole, Moped  # noqa: E402
from wmoop.geography import City, Country, County  # noqa: E402
from wmoop.patterns import (  # noqa: E402
    ActiveDriverSpecification, CensusAreaFormat, CompactAreaFormat, ConceptRegistry,
    PersonBuilder, PopulationSumVisitor, PrettyPrintVisitor,
)

_fail = 0


def check(label: str, ok: bool) -> None:
    global _fail
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    if not ok:
        _fail += 1


def raises(exc, fn) -> bool:
    try:
        fn()
        return False
    except exc:
        return True


print("=== WMOOP (.py) design-patterns showcase ===\n")

print("-- Composite: administrative containment (part_of, NOT inheritance) --")
cluj = City("wm:geography/city/cluj-napoca", "Cluj-Napoca", 286_598)
turda = City("wm:geography/city/turda", "Turda", 43_319)
bucharest = City("wm:geography/city/bucharest", "Bucharest", 1_716_961)
cluj_county = County("wm:geography/county/cluj", "Cluj")
cluj_county.add(cluj)
cluj_county.add(turda)
ilfov = County("wm:geography/county/ilfov", "Ilfov")
ilfov.add(bucharest)
romania = Country("wm:geography/country/romania", "Romania")
romania.add(cluj_county)
romania.add(ilfov)
check("A city is a leaf (add is rejected)", raises(RuntimeError, lambda: cluj.add(turda)))
check("Composite sums population recursively", romania.total_population == 286_598 + 43_319 + 1_716_961)

print("\n-- Visitor: operations over the model --")
printer = PrettyPrintVisitor()
romania.accept(printer)
print(printer.result, end="")
census = PopulationSumVisitor()
romania.accept(census)
check("Visitor computes the same total, independently", census.total == romania.total_population)
check("Visitor counts 3 cities", census.city_count == 3)

print("\n-- Builder: fluent construction of a Person with roles --")
moped = Moped("wm:transport/moped/ciao", "Piaggio Ciao", Quantity(45, "km/h"), Quantity(49, "cc"))
ada = (
    PersonBuilder()
    .with_id("wm:nature/person/ada")
    .named("Ada")
    .born_in(1990)
    .with_driver_licence("RO-AB-123456", ["AM", "A1", "B"], date(2018, 6, 1), date(2028, 6, 1))
    .with_ownership(moped, date(2022, 3, 15))
    .build()
)
check("Builder attached 2 roles", len(ada.roles) == 2)
check("Builder's person is a driver (has_role)", ada.has_role(DriverRole))

print("\n-- Specification: composable rules (&, |, ~) --")
on = date(2026, 10, 16)
can_am = ActiveDriverSpecification("AM", on)
can_c = ActiveDriverSpecification("C", on)
check("Ada satisfies 'can ride a moped (AM)'", can_am.is_satisfied_by(ada))
check("Ada does NOT satisfy 'can drive a truck (C)'", not can_c.is_satisfied_by(ada))
check("AM and not C holds", (can_am & ~can_c).is_satisfied_by(ada))
check("C or AM holds", (can_c | can_am).is_satisfied_by(ada))

print("\n-- Strategy: swappable area formatting --")
compact = CompactAreaFormat()
detailed = CensusAreaFormat()
print("  compact:  " + compact.format(romania))
print("  detailed: " + detailed.format(romania))
check("Two strategies produce different output", compact.format(romania) != detailed.format(romania))

print("\n-- Registry + Flyweight --")
registry = ConceptRegistry()
check("Interned ids compare equal", registry.intern("wm:nature/Person") == registry.intern("wm:nature/Person"))
registry.register(ada)
registry.register(romania)
check("Registry resolves a registered entity", isinstance(registry.resolve("wm:nature/person/ada"), Person))
check("Registry holds 2 entities", registry.count == 2)

print(f"\n=== {'all checks passed' if _fail == 0 else str(_fail) + ' check(s) FAILED'} ===")
sys.exit(0 if _fail == 0 else 1)

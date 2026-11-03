"""Design-patterns showcase — the Python twin of wmoop.net's Wmoop.Patterns.Demo.

Each section demonstrates one named pattern on the generated WMOOP model and self-checks
(non-zero exit on failure, so CI can gate on it). Deterministic: fixed dates, no randomness.
"""
import os
import sys

# The generated wmoop.* modules live in generated/; wmoop_ext and wmoop.patterns next to this file.
_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(_ROOT, "generated"), _ROOT]

from datetime import date  # noqa: E402

from wmoop.core import Quantity  # noqa: E402
from wmoop.geography import City, Country, County  # noqa: E402
from wmoop.nature import Person  # noqa: E402
from wmoop.patterns import (  # noqa: E402
    ActiveDriverSpecification, CensusAreaFormat, CompactAreaFormat, ConceptRegistry,
    PersonBuilder, PopulationSumVisitor, PrettyPrintVisitor,
)
from wmoop.transport import Driver, LicenceCategory, Moped  # noqa: E402

_fail = 0


def check(label: str, ok: bool) -> None:
    global _fail
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    if not ok:
        _fail += 1


print("=== WMOOP (.py) design-patterns showcase ===\n")

print("-- Composite: administrative containment (part_of, NOT inheritance) --")
cluj = City("wmoop.geography/city/cluj-napoca", "Cluj-Napoca", resident_population=286_598)
turda = City("wmoop.geography/city/turda", "Turda", resident_population=43_319)
bucharest = City("wmoop.geography/city/bucharest", "Bucharest", resident_population=1_716_961)

cluj_county = County("wmoop.geography/county/cluj", "Cluj")
cluj_county.contains.add(cluj)
turda.part_of = cluj_county  # either end of the relation can be used

romania = Country("wmoop.geography/country/romania", "Romania")
romania.contains.add(cluj_county)
romania.contains.add(bucharest)  # a municipality at county level, not part of a county

check("The inverse end follows: a city knows its county (part_of)", cluj.part_of is cluj_county)
check("Composite sums population recursively", romania.total_population == 286_598 + 43_319 + 1_716_961)

print("\n-- Visitor: operations over the model (double dispatch) --")
printer = PrettyPrintVisitor()
romania.accept(printer)
print(printer.result, end="")
census = PopulationSumVisitor()
romania.accept(census)
check("Visitor computes the same total, independently", census.total == romania.total_population)
check("Visitor counts 3 cities", census.city_count == 3)

print("\n-- Builder: fluent construction of a Person with roles --")
moped = Moped("wmoop.transport/moped/ciao", "Piaggio Ciao", wheel_count=2,
              max_speed=Quantity(45, "km/h"), engine_displacement=Quantity(49, "cm3"))
ada = (
    PersonBuilder()
    .with_id("wmoop.nature/person/ada")
    .named("Ada", "Ada Lovelace")
    .born_on(date(1990, 1, 1))
    .with_driver_licence("RO-AB-123456", [LicenceCategory.AM, LicenceCategory.A1, LicenceCategory.B],
                         date(2028, 6, 1))
    .with_ownership(date(2022, 3, 15), moped)
    .build()
)
check("Builder attached 2 roles", len(ada.roles) == 2)
check("Builder's person is a driver (has_role)", ada.has_role(Driver))
check("The moped knows its owner (owned_by)", [o.subject for o in moped.owned_by] == [ada])

print("\n-- Specification: composable rules (&, |, ~) --")
on = date(2026, 10, 16)
can_ride_moped = ActiveDriverSpecification(LicenceCategory.AM, on)
can_ride_any_motorcycle = ActiveDriverSpecification(LicenceCategory.A, on)
check("Ada satisfies 'can ride a moped (AM)'", can_ride_moped.is_satisfied_by(ada))
check("Ada does NOT satisfy 'can ride an unrestricted motorcycle (A)'",
      not can_ride_any_motorcycle.is_satisfied_by(ada))
check("AM and not A holds", (can_ride_moped & ~can_ride_any_motorcycle).is_satisfied_by(ada))
check("A or AM holds", (can_ride_any_motorcycle | can_ride_moped).is_satisfied_by(ada))

print("\n-- Strategy: swappable area formatting --")
compact = CompactAreaFormat()
detailed = CensusAreaFormat()
print("  compact:  " + compact.format(romania))
print("  detailed: " + detailed.format(romania))
check("Two strategies produce different output", compact.format(romania) != detailed.format(romania))

print("\n-- Registry + Flyweight: canonical ids and instance lookup --")
registry = ConceptRegistry()
check("Interned ids compare equal", registry.intern("wmoop.nature/Person") == registry.intern("wmoop.nature/Person"))
registry.register(ada)
registry.register(romania)
check("Registry resolves a registered entity", isinstance(registry.resolve("wmoop.nature/person/ada"), Person))
check("Registry holds 2 entities", registry.count == 2)

print(f"\n=== {'all checks passed' if _fail == 0 else str(_fail) + ' check(s) FAILED'} ===")
sys.exit(0 if _fail == 0 else 1)

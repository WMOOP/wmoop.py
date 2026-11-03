"""Runnable walkthrough — the Python twin of wmoop.net's Wmoop.Demo.

Same scenario, same output shape: cross-domain roles by composition, then the
Vehicle hierarchy polymorphically. The data classes (Person, Moped, Driver, Owner, …)
are GENERATED from the WML model in wmoop.doc (see generated/); the behaviour used
here (age_on, can_drive, describe) is hand-written, in the wmoop_ext mixins.
"""
import os
import sys

# The generated wmoop.* modules live in generated/; wmoop_ext and wmoop.patterns next to this file.
_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(_ROOT, "generated"), _ROOT]

from datetime import date  # noqa: E402

from wmoop.core import Quantity  # noqa: E402
from wmoop.nature import Person  # noqa: E402
from wmoop.transport import Driver, LicenceCategory, Moped, Motorcycle, Owner, Vehicle  # noqa: E402

print("=== WMOOP (.py) demo ===\n")

print("-- Part 1: a Person and the roles they play --")
# A Person is an intrinsic biological entity (wmoop.nature). Nothing here knows about vehicles.
today = date(2026, 10, 16)
ada = Person("wmoop.nature/person/ada-lovelace", "Ada", full_name="Ada Lovelace", leg_count=2,
             date_of_birth=date(1990, 1, 1))
print(f"{ada.name}: legs={ada.leg_count}, age on {today}={ada.age_on(today)}")

moped = Moped("wmoop.transport/moped/piaggio-ciao", "Piaggio Ciao", wheel_count=2,
              max_speed=Quantity(45, "km/h"), engine_displacement=Quantity(49, "cm3"))

# Grant two Transport facets to the SAME person, at the same time, by composition.
ada.add_role(Driver(licence_number="RO-AB-123456",
                    licence_categories=[LicenceCategory.AM, LicenceCategory.A1, LicenceCategory.B],
                    licence_expiry=date(2028, 6, 1)))
owner = ada.add_role(Owner(owned_since=date(2022, 3, 15)))
owner.owns.add(moped)  # a generated relation: the moped's owned_by follows

print(f"Is {ada.name} a driver? {ada.has_role(Driver)}")
print(f"Is {ada.name} an owner? {ada.has_role(Owner)}")
print(f"{ada.name} holds {len(ada.roles)} role(s):")
for role in ada.roles:
    print(f"   - {role.role_type} (on {role.subject.name})")

licence = ada.get_role(Driver)
print(f"Licence {licence.licence_number}: can ride a moped (AM) today? "
      f"{licence.can_drive(LicenceCategory.AM, today)}")
print(f"Can ride an unrestricted motorcycle (A) today? {licence.can_drive(LicenceCategory.A, today)}")
print(f"Owns '{', '.join(v.name for v in owner.owns)}' since {owner.owned_since}")
print(f"'{moped.name}' is owned by {', '.join(o.subject.name for o in moped.owned_by)}\n")

print("-- Part 2: the Vehicle hierarchy, polymorphically --")
fleet: "list[Vehicle]" = [
    moped,
    Motorcycle("wmoop.transport/motorcycle/bmw-r1250gs", "BMW R1250 GS", wheel_count=2,
               max_speed=Quantity(200, "km/h"), engine_displacement=Quantity(1254, "cm3")),
    Motorcycle("wmoop.transport/motorcycle/ural-gear-up", "Ural Gear-Up", wheel_count=3,  # a sidecar outfit
               max_speed=Quantity(110, "km/h"), engine_displacement=Quantity(749, "cm3")),
]
for vehicle in fleet:
    print(f"   {vehicle.describe()}")

print("\n=== demo complete ===")

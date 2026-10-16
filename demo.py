"""Runnable walkthrough — the Python twin of wmoop.net's Wmoop.Demo.

Same scenario, same output shape: cross-domain roles by composition, then the
Vehicle hierarchy polymorphically.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import date  # noqa: E402

from wmoop.core import Quantity  # noqa: E402
from wmoop.nature import Person  # noqa: E402
from wmoop.transport import DriverRole, Moped, Motorcycle, OwnerRole, Vehicle  # noqa: E402

print("=== WMOOP (.py) reference demo ===\n")

print("-- Part 1: a Person and the roles they play --")
ada = Person("wm:nature/person/ada-lovelace", "Ada", 1990)
print(f"{ada.name}: taxon={ada.taxon}, legs={ada.leg_count}, age in 2026={ada.age_at(2026)}")

moped = Moped("wm:transport/moped/piaggio-ciao", "Piaggio Ciao",
              Quantity(45, "km/h"), Quantity(49, "cc"))

ada.add_role(DriverRole("RO-AB-123456", ["AM", "A1", "B"], date(2018, 6, 1), date(2028, 6, 1)))
ada.add_role(OwnerRole(moped, date(2022, 3, 15)))

print(f"Is {ada.name} a driver? {ada.has_role(DriverRole)}")
print(f"Is {ada.name} an owner? {ada.has_role(OwnerRole)}")
print(f"{ada.name} holds {len(ada.roles)} role(s):")
for role in ada.roles:
    print(f"   - {role.role_type} (on {role.subject.name})")

licence = ada.get_role(DriverRole)
today = date(2026, 10, 16)
print(f"Licence {licence.licence_number}: can ride a moped (AM) today? {licence.can_drive('AM', today)}")
print(f"Can drive a truck (C) today? {licence.can_drive('C', today)}")

ownership = ada.get_role(OwnerRole)
print(f"Owns '{ownership.asset.name}' since {ownership.owned_since}\n")

print("-- Part 2: the Vehicle hierarchy, polymorphically --")
fleet: "list[Vehicle]" = [
    moped,
    Motorcycle("wm:transport/motorcycle/bmw-r1250", "BMW R1250 GS", Quantity(200, "km/h")),
    Motorcycle("wm:transport/motorcycle/ural-sidecar", "Ural Gear-Up", Quantity(110, "km/h"), has_sidecar=True),
]
for vehicle in fleet:
    print(f"   {vehicle.describe()}")

print("\n=== demo complete ===")

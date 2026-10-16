"""wmoop.transport — vehicle hierarchy + the cross-domain Driver/Owner roles.

Mirrors C# ``Wmoop.Transport``. The vehicle chain is a genuine, shallow is-a
hierarchy; the Driver/Owner facets of a :class:`~wmoop.nature.Person` are roles
attached by composition — never ``Driver(Person)``.
"""
from __future__ import annotations

from abc import abstractmethod
from datetime import date
from typing import Iterable

from .core import ConceptId, Entity, Quantity, Role


class Vehicle(Entity):
    """``wm:transport/Vehicle`` — root of the shallow is-a hierarchy."""

    def __init__(self, id, name, wheel_count: int, max_speed: Quantity) -> None:
        super().__init__(id, name)
        if wheel_count < 0:
            raise ValueError("wheel_count cannot be negative")
        self._wheel_count = wheel_count
        self._max_speed = max_speed

    @property
    def wheel_count(self) -> int:
        return self._wheel_count

    @property
    def max_speed(self) -> Quantity:
        return self._max_speed

    @property
    @abstractmethod
    def classification(self) -> str:
        ...

    def describe(self) -> str:
        return (f"{self.name} — a {self.classification} with {self.wheel_count} "
                f"wheels, top speed {self.max_speed}.")


class RoadVehicle(Vehicle):
    """``wm:transport/RoadVehicle`` — adds ``seat_count``; still abstract."""

    def __init__(self, id, name, wheel_count, max_speed, seat_count: int) -> None:
        super().__init__(id, name, wheel_count, max_speed)
        if seat_count < 1:
            raise ValueError("A road vehicle seats at least one.")
        self._seat_count = seat_count

    @property
    def seat_count(self) -> int:
        return self._seat_count


class Motorcycle(RoadVehicle):
    """``wm:transport/Motorcycle`` — wheel/seat counts derive from the sidecar choice."""

    def __init__(self, id, name, max_speed, has_sidecar: bool = False) -> None:
        super().__init__(id, name,
                         wheel_count=3 if has_sidecar else 2,
                         max_speed=max_speed,
                         seat_count=2 if has_sidecar else 1)
        self._has_sidecar = has_sidecar

    @property
    def has_sidecar(self) -> bool:
        return self._has_sidecar

    @property
    def classification(self) -> str:
        return "motorcycle"


class Moped(Motorcycle):
    """``wm:transport/Moped`` — a light motorcycle (leaf of the hierarchy)."""

    def __init__(self, id, name, max_speed, engine_displacement: Quantity) -> None:
        super().__init__(id, name, max_speed, has_sidecar=False)
        self._engine_displacement = engine_displacement

    @property
    def engine_displacement(self) -> Quantity:
        return self._engine_displacement

    @property
    def classification(self) -> str:
        return "moped"

    def describe(self) -> str:
        return super().describe() + f" Engine: {self._engine_displacement}."


class DriverRole(Role):
    """``wm:transport/role/Driver`` — the Transport facet of a Person (a role, by composition)."""

    TYPE_ID = ConceptId("wm:transport/role/Driver")

    def __init__(self, licence_number: str, categories: Iterable[str],
                 issue_date: date, expiry_date: date) -> None:
        super().__init__()
        if not licence_number or not licence_number.strip():
            raise ValueError("A driver role requires a licence number.")
        if expiry_date < issue_date:
            raise ValueError("Expiry date cannot precede issue date.")
        self._licence_number = licence_number
        self._categories = tuple(categories)
        self._issue_date = issue_date
        self._expiry_date = expiry_date

    @property
    def role_type(self) -> ConceptId:
        return DriverRole.TYPE_ID

    @property
    def licence_number(self) -> str:
        return self._licence_number

    @property
    def categories(self) -> "tuple[str, ...]":
        return self._categories

    @property
    def issue_date(self) -> date:
        return self._issue_date

    @property
    def expiry_date(self) -> date:
        return self._expiry_date

    def can_drive(self, category: str, on: date) -> bool:
        return (self._issue_date <= on <= self._expiry_date
                and any(c.lower() == category.lower() for c in self._categories))


class OwnerRole(Role):
    """``wm:transport/role/Owner`` — held alongside Driver, independently."""

    TYPE_ID = ConceptId("wm:transport/role/Owner")

    def __init__(self, asset: Vehicle, owned_since: date) -> None:
        super().__init__()
        if asset is None:
            raise ValueError("asset is required")
        self._asset = asset
        self._owned_since = owned_since

    @property
    def role_type(self) -> ConceptId:
        return OwnerRole.TYPE_ID

    @property
    def asset(self) -> Vehicle:
        return self._asset

    @property
    def owned_since(self) -> date:
        return self._owned_since

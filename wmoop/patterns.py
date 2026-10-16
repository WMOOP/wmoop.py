"""wmoop.patterns — hand-written behaviour over the model (mirrors C# ``Wmoop.Patterns``).

Visitor, Specification (with ``&``/``|``/``~`` operators), Builder, Strategy and a
Registry/Flyweight. Behaviour lives here, OUTSIDE the data model.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Callable, Generic, Optional, TypeVar

from .core import ConceptId, Entity, Role
from .nature import Person
from .transport import DriverRole, OwnerRole, Vehicle
from .geography import AdministrativeArea, City, Country, County


# --------------------------------------------------------------------------- Visitor
class PrettyPrintVisitor:
    """Renders an administrative tree as indented text — behaviour outside the model."""

    def __init__(self) -> None:
        self._lines: list[str] = []
        self._depth = 0

    @property
    def result(self) -> str:
        return ("\n".join(self._lines) + "\n") if self._lines else ""

    def _line(self, area: AdministrativeArea) -> None:
        indent = "  " * self._depth
        self._lines.append(f"{indent}- {area.name} ({area.area_kind}, pop {area.resident_population})")

    def _descend(self, area: AdministrativeArea) -> None:
        self._line(area)
        self._depth += 1
        for child in area.children:
            child.accept(self)
        self._depth -= 1

    def visit_country(self, country: Country) -> None:
        self._descend(country)

    def visit_county(self, county: County) -> None:
        self._descend(county)

    def visit_city(self, city: City) -> None:
        self._line(city)


class PopulationSumVisitor:
    """Totals population and counts cities by walking the Composite."""

    def __init__(self) -> None:
        self.total = 0
        self.city_count = 0

    def _recurse(self, area: AdministrativeArea) -> None:
        self.total += area.resident_population
        for child in area.children:
            child.accept(self)

    def visit_country(self, country: Country) -> None:
        self._recurse(country)

    def visit_county(self, county: County) -> None:
        self._recurse(county)

    def visit_city(self, city: City) -> None:
        self.total += city.resident_population
        self.city_count += 1


# ----------------------------------------------------------------------- Specification
T = TypeVar("T")


class Specification(ABC, Generic[T]):
    """Composable boolean rule; combine with ``&`` (and), ``|`` (or), ``~`` (not)."""

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        ...

    def __and__(self, other: "Specification[T]") -> "Specification[T]":
        return _And(self, other)

    def __or__(self, other: "Specification[T]") -> "Specification[T]":
        return _Or(self, other)

    def __invert__(self) -> "Specification[T]":
        return _Not(self)


class _And(Specification[T]):
    def __init__(self, a: Specification[T], b: Specification[T]) -> None:
        self._a, self._b = a, b

    def is_satisfied_by(self, candidate: T) -> bool:
        return self._a.is_satisfied_by(candidate) and self._b.is_satisfied_by(candidate)


class _Or(Specification[T]):
    def __init__(self, a: Specification[T], b: Specification[T]) -> None:
        self._a, self._b = a, b

    def is_satisfied_by(self, candidate: T) -> bool:
        return self._a.is_satisfied_by(candidate) or self._b.is_satisfied_by(candidate)


class _Not(Specification[T]):
    def __init__(self, a: Specification[T]) -> None:
        self._a = a

    def is_satisfied_by(self, candidate: T) -> bool:
        return not self._a.is_satisfied_by(candidate)


class ActiveDriverSpecification(Specification[Person]):
    """Satisfied when a Person holds a DriverRole valid for a category on a date."""

    def __init__(self, category: str, on: date) -> None:
        self._category = category
        self._on = on

    def is_satisfied_by(self, candidate: Person) -> bool:
        licence = candidate.get_role(DriverRole)
        return licence is not None and licence.can_drive(self._category, self._on)


# ----------------------------------------------------------------------------- Builder
class PersonBuilder:
    """Fluent builder assembling a Person together with the roles they play."""

    def __init__(self) -> None:
        self._id = None
        self._name = "Unnamed"
        self._birth_year = 1970
        self._role_factories: list[Callable[[], Role]] = []

    def with_id(self, id) -> "PersonBuilder":
        self._id = id
        return self

    def named(self, name: str) -> "PersonBuilder":
        self._name = name
        return self

    def born_in(self, year: int) -> "PersonBuilder":
        self._birth_year = year
        return self

    def with_driver_licence(self, number, categories, issue: date, expiry: date) -> "PersonBuilder":
        self._role_factories.append(lambda: DriverRole(number, categories, issue, expiry))
        return self

    def with_ownership(self, asset: Vehicle, since: date) -> "PersonBuilder":
        self._role_factories.append(lambda: OwnerRole(asset, since))
        return self

    def build(self) -> Person:
        if self._id is None:
            raise RuntimeError("A person needs a ConceptId; call with_id() first.")
        person = Person(self._id, self._name, self._birth_year)
        for make in self._role_factories:
            person.add_role(make())
        return person


# ---------------------------------------------------------------------------- Strategy
class AreaFormatStrategy(ABC):
    """Swappable algorithm for formatting an area label."""

    @abstractmethod
    def format(self, area: AdministrativeArea) -> str:
        ...


class CompactAreaFormat(AreaFormatStrategy):
    def format(self, area: AdministrativeArea) -> str:
        return f"{area.name} ({area.area_kind})"


class CensusAreaFormat(AreaFormatStrategy):
    def format(self, area: AdministrativeArea) -> str:
        return (f"{area.name} [{area.area_kind}] pop={area.total_population:,} "
                f"across {len(area.children)} sub-area(s)")


# -------------------------------------------------------------------- Registry+Flyweight
class ConceptRegistry:
    """Canonicalizes ConceptId values (Flyweight) and holds L2 individuals (Registry)."""

    def __init__(self) -> None:
        self._ids: dict[str, ConceptId] = {}
        self._entities: dict[str, Entity] = {}

    def intern(self, value: str) -> ConceptId:
        if value not in self._ids:
            self._ids[value] = ConceptId(value)
        return self._ids[value]

    def register(self, entity: Entity) -> Entity:
        self._entities[entity.id.value] = entity
        return entity

    def resolve(self, id) -> Optional[Entity]:
        key = id.value if isinstance(id, ConceptId) else str(id)
        return self._entities.get(key)

    @property
    def count(self) -> int:
        return len(self._entities)

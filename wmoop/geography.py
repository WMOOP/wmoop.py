"""wmoop.geography — administrative areas as a Composite (mirrors C# ``Wmoop.Geography``).

Containment (country ⊃ county ⊃ city) is ``part_of`` composition, NOT inheritance.
"""
from __future__ import annotations

from abc import abstractmethod
from typing import Protocol, runtime_checkable

from .core import Entity


@runtime_checkable
class AreaVisitor(Protocol):
    """Visitor hook (the behaviour home). Concrete visitors live in ``wmoop.patterns``."""

    def visit_country(self, country: "Country") -> None: ...
    def visit_county(self, county: "County") -> None: ...
    def visit_city(self, city: "City") -> None: ...


class AdministrativeArea(Entity):
    """Composite component. Areas *are* kinds of AdministrativeArea (inheritance),
    but their *containment* is a ``part_of`` relation (composition)."""

    def __init__(self, id, name, resident_population: int = 0) -> None:
        super().__init__(id, name)
        if resident_population < 0:
            raise ValueError("Population cannot be negative.")
        self._resident_population = resident_population
        self._children: list[AdministrativeArea] = []

    @property
    def resident_population(self) -> int:
        return self._resident_population

    @property
    def children(self) -> "tuple[AdministrativeArea, ...]":
        return tuple(self._children)

    @property
    @abstractmethod
    def area_kind(self) -> str:
        ...

    def add(self, child: "AdministrativeArea") -> "AdministrativeArea":
        if child is None:
            raise ValueError("child is required")
        self._children.append(child)
        return self

    @property
    def total_population(self) -> int:
        return self._resident_population + sum(c.total_population for c in self._children)

    @abstractmethod
    def accept(self, visitor: AreaVisitor) -> None:
        ...


class Country(AdministrativeArea):
    @property
    def area_kind(self) -> str:
        return "country"

    def accept(self, visitor: AreaVisitor) -> None:
        visitor.visit_country(self)


class County(AdministrativeArea):
    @property
    def area_kind(self) -> str:
        return "county"

    def accept(self, visitor: AreaVisitor) -> None:
        visitor.visit_county(self)


class City(AdministrativeArea):
    """A leaf: it has no sub-areas, so :meth:`add` is rejected."""

    @property
    def area_kind(self) -> str:
        return "city"

    def add(self, child: "AdministrativeArea") -> "AdministrativeArea":
        raise RuntimeError("A city is a leaf area and cannot contain sub-areas.")

    def accept(self, visitor: AreaVisitor) -> None:
        visitor.visit_city(self)

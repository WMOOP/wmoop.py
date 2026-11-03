"""Behaviour of the generated ``wmoop.geography`` classes: the composite and its visitor hook."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from wmoop.geography import City, Country, County


@runtime_checkable
class AreaVisitor(Protocol):
    """Visitor hook, where behaviour over the composite lives. Concrete visitors are in ``wmoop.patterns``."""

    def visit_country(self, country: Country) -> None: ...
    def visit_county(self, county: County) -> None: ...
    def visit_city(self, city: City) -> None: ...


class AdministrativeAreaExt:
    """Mixed into the generated ``wmoop.geography.AdministrativeArea``.

    The data, including the ``part_of`` / ``contains`` composite, is generated from
    ``wmoop.geography``; this only adds behaviour over it.
    """

    @property
    def area_kind(self) -> str:
        """A short kind name for display: ``country``, ``county``, ``city``."""
        return type(self).__name__.lower()

    @property
    def total_population(self) -> int:
        """This area's own residents plus those of every area it contains, recursively.

        An area whose resident population is not recorded counts as 0 here.
        """
        return (self.resident_population or 0) + sum(area.total_population for area in self.contains)

    def accept(self, visitor: AreaVisitor) -> None:
        """Double dispatch for :class:`AreaVisitor`; every kind of area overrides it."""
        raise NotImplementedError(f"{type(self).__name__} does not accept an AreaVisitor yet.")


class CountryExt:
    def accept(self, visitor: AreaVisitor) -> None:
        visitor.visit_country(self)


class CountyExt:
    def accept(self, visitor: AreaVisitor) -> None:
        visitor.visit_county(self)


class CityExt:
    def accept(self, visitor: AreaVisitor) -> None:
        visitor.visit_city(self)

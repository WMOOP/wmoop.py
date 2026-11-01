"""Generated from module wmoop.geography v0.2.0. DO NOT EDIT — regenerate with wmoop.tools."""
from __future__ import annotations
from ._runtime import ConceptId, Entity, Quantity, Role, HasRoles  # noqa: F401

class Place(Entity):
    """Place — wmoop.geography/Place. A location in space that can be referred to and contained within another."""
    WM_ID = "wmoop.geography/Place"
    WM_KIND = "abstract"
    def __init__(self, id, name):
        if type(self) is Place:
            raise TypeError("Place is abstract and cannot be instantiated directly.")
        super().__init__(id, name)

class AdministrativeArea(Place):
    """AdministrativeArea — wmoop.geography/AdministrativeArea. A government-defined area that may contain smaller administrative areas. Containment is a `part_of` relation (mereology), NOT inheritance: a city is not a *kind of* county."""
    WM_ID = "wmoop.geography/AdministrativeArea"
    WM_KIND = "abstract"
    def __init__(self, id, name, *, residentPopulation=None):
        if type(self) is AdministrativeArea:
            raise TypeError("AdministrativeArea is abstract and cannot be instantiated directly.")
        super().__init__(id, name)
        self._residentPopulation = residentPopulation
    @property
    def residentPopulation(self):
        return self._residentPopulation

class Country(AdministrativeArea):
    """Country — wmoop.geography/Country. A nation state or distinct territory."""
    WM_ID = "wmoop.geography/Country"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, residentPopulation=None):
        super().__init__(id, name, residentPopulation=residentPopulation)

class County(AdministrativeArea):
    """County — wmoop.geography/County. A first-level administrative subdivision of a country (exact meaning varies by country)."""
    WM_ID = "wmoop.geography/County"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, residentPopulation=None):
        super().__init__(id, name, residentPopulation=residentPopulation)

class City(AdministrativeArea):
    """City — wmoop.geography/City. A populated urban settlement; a leaf administrative area with no sub-areas."""
    WM_ID = "wmoop.geography/City"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, residentPopulation=None):
        super().__init__(id, name, residentPopulation=residentPopulation)

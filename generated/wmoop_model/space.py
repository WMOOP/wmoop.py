"""Generated from module wmoop.space v0.1.0. DO NOT EDIT — regenerate with wmoop.tools."""
from __future__ import annotations
from ._runtime import ConceptId, Entity, Quantity, Role, HasRoles  # noqa: F401

class CelestialBody(Entity):
    """CelestialBody — wmoop.space/CelestialBody. A naturally occurring physical body in outer space, such as a planet, star or moon."""
    WM_ID = "wmoop.space/CelestialBody"
    WM_KIND = "abstract"
    def __init__(self, id, name, *, mass=None, equatorialRadius=None):
        if type(self) is CelestialBody:
            raise TypeError("CelestialBody is abstract and cannot be instantiated directly.")
        super().__init__(id, name)
        self._mass = mass
        self._equatorialRadius = equatorialRadius
    @property
    def mass(self):
        return self._mass
    @property
    def equatorialRadius(self):
        return self._equatorialRadius

class Planet(CelestialBody):
    """Planet — wmoop.space/Planet. A celestial body that orbits the Sun, is massive enough for its self-gravity to pull it into a nearly round shape, and has cleared the neighbourhood around its orbit."""
    WM_ID = "wmoop.space/Planet"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, mass=None, equatorialRadius=None, orbitalPeriod=None, numberOfMoons=None):
        super().__init__(id, name, mass=mass, equatorialRadius=equatorialRadius)
        self._orbitalPeriod = orbitalPeriod
        self._numberOfMoons = numberOfMoons
    @property
    def orbitalPeriod(self):
        return self._orbitalPeriod
    @property
    def numberOfMoons(self):
        return self._numberOfMoons

class DwarfPlanet(CelestialBody):
    """DwarfPlanet — wmoop.space/DwarfPlanet. A celestial body that orbits the Sun and is nearly round, but has NOT cleared the neighbourhood around its orbit and is not a satellite."""
    WM_ID = "wmoop.space/DwarfPlanet"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, mass=None, equatorialRadius=None):
        super().__init__(id, name, mass=mass, equatorialRadius=equatorialRadius)

class Star(CelestialBody):
    """Star — wmoop.space/Star. A celestial body that shines by its own light through sustained nuclear fusion in its core."""
    WM_ID = "wmoop.space/Star"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, mass=None, equatorialRadius=None):
        super().__init__(id, name, mass=mass, equatorialRadius=equatorialRadius)

class NaturalSatellite(CelestialBody):
    """NaturalSatellite — wmoop.space/NaturalSatellite. A celestial body in orbit around a planet or other non-stellar body (a moon)."""
    WM_ID = "wmoop.space/NaturalSatellite"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, mass=None, equatorialRadius=None):
        super().__init__(id, name, mass=mass, equatorialRadius=equatorialRadius)

class PlanetarySystem(Entity):
    """PlanetarySystem — wmoop.space/PlanetarySystem. A collection of celestial bodies — a star (or stars) together with the planets, dwarf planets and smaller bodies gravitationally bound to it."""
    WM_ID = "wmoop.space/PlanetarySystem"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, numberOfPlanets=None):
        super().__init__(id, name)
        self._numberOfPlanets = numberOfPlanets
    @property
    def numberOfPlanets(self):
        return self._numberOfPlanets

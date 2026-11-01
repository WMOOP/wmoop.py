"""Generated from module wmoop.transport v0.3.0. DO NOT EDIT — regenerate with wmoop.tools."""
from __future__ import annotations
from enum import Enum
from ._runtime import ConceptId, Entity, Quantity, Role, HasRoles  # noqa: F401

class LicenceCategory(str, Enum):
    """LicenceCategory — wmoop.transport/LicenceCategory."""
    AM = "AM"
    A1 = "A1"
    A2 = "A2"
    A = "A"
    B = "B"

class Vehicle(Entity):
    """Vehicle — wmoop.transport/Vehicle. A man-made means of transport for moving people or goods."""
    WM_ID = "wmoop.transport/Vehicle"
    WM_KIND = "abstract"
    def __init__(self, id, name, *, wheelCount=None, maxSpeed=None):
        if type(self) is Vehicle:
            raise TypeError("Vehicle is abstract and cannot be instantiated directly.")
        super().__init__(id, name)
        self._wheelCount = wheelCount
        self._maxSpeed = maxSpeed
    @property
    def wheelCount(self):
        return self._wheelCount
    @property
    def maxSpeed(self):
        return self._maxSpeed

class RoadVehicle(Vehicle):
    """RoadVehicle — wmoop.transport/RoadVehicle. A vehicle designed to travel on public roads."""
    WM_ID = "wmoop.transport/RoadVehicle"
    WM_KIND = "abstract"
    def __init__(self, id, name, *, wheelCount=None, maxSpeed=None, roadLegal=True):
        if type(self) is RoadVehicle:
            raise TypeError("RoadVehicle is abstract and cannot be instantiated directly.")
        super().__init__(id, name, wheelCount=wheelCount, maxSpeed=maxSpeed)
        self._roadLegal = roadLegal
    @property
    def roadLegal(self):
        return self._roadLegal

class Motorcycle(RoadVehicle):
    """Motorcycle — wmoop.transport/Motorcycle. A two- or three-wheeled motor road vehicle."""
    WM_ID = "wmoop.transport/Motorcycle"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, wheelCount=None, maxSpeed=None, roadLegal=True, engineDisplacement=None):
        super().__init__(id, name, wheelCount=wheelCount, maxSpeed=maxSpeed, roadLegal=roadLegal)
        self._engineDisplacement = engineDisplacement
    @property
    def engineDisplacement(self):
        return self._engineDisplacement

class Moped(Motorcycle):
    """Moped — wmoop.transport/Moped. A low-powered motorcycle whose engine displacement and top speed are limited by law (EU category L1e-B)."""
    WM_ID = "wmoop.transport/Moped"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, wheelCount=None, maxSpeed=None, roadLegal=True, engineDisplacement=None):
        super().__init__(id, name, wheelCount=wheelCount, maxSpeed=maxSpeed, roadLegal=roadLegal, engineDisplacement=engineDisplacement)

class Driver(Role):
    """Driver role — wmoop.transport/Driver. The role of a licensed person who operates a road vehicle."""
    WM_ID = "wmoop.transport/Driver"
    WM_PLAYED_BY = "wmoop.nature/Person"
    def __init__(self, *, licenceNumber=None, licenceCategories=None, licenceExpiry=None):
        super().__init__()
        self._licenceNumber = licenceNumber
        self._licenceCategories = licenceCategories
        self._licenceExpiry = licenceExpiry
    @property
    def role_type(self):
        return ConceptId(self.WM_ID)
    @property
    def licenceNumber(self):
        return self._licenceNumber
    @property
    def licenceCategories(self):
        return self._licenceCategories
    @property
    def licenceExpiry(self):
        return self._licenceExpiry

class Owner(Role):
    """Owner role — wmoop.transport/Owner. The role of an entity that owns a vehicle. Held alongside Driver, independently."""
    WM_ID = "wmoop.transport/Owner"
    WM_PLAYED_BY = "wmoop.nature/Person"
    def __init__(self, *, ownedSince=None):
        super().__init__()
        self._ownedSince = ownedSince
    @property
    def role_type(self):
        return ConceptId(self.WM_ID)
    @property
    def ownedSince(self):
        return self._ownedSince

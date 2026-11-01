"""Generated from module wmoop.architecture v0.1.0. DO NOT EDIT — regenerate with wmoop.tools."""
from __future__ import annotations
from ._runtime import ConceptId, Entity, Quantity, Role, HasRoles  # noqa: F401

class Building(Entity):
    """Building — wmoop.architecture/Building. A roofed, permanent construction with walls, standing more or less independently, intended for human occupancy or use."""
    WM_ID = "wmoop.architecture/Building"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, floorCount=None):
        super().__init__(id, name)
        self._floorCount = floorCount
    @property
    def floorCount(self):
        return self._floorCount

class Room(Entity):
    """Room — wmoop.architecture/Room. An interior space within a building, enclosed by walls, floor and ceiling and normally entered through a door. A Room is a PART OF a Building (mereology), it is not a kind of Building."""
    WM_ID = "wmoop.architecture/Room"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, floorArea=None):
        super().__init__(id, name)
        self._floorArea = floorArea
    @property
    def floorArea(self):
        return self._floorArea

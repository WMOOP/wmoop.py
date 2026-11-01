"""Generated from module wmoop.org v0.1.0. DO NOT EDIT — regenerate with wmoop.tools."""
from __future__ import annotations
from ._runtime import ConceptId, Entity, Quantity, Role, HasRoles  # noqa: F401

class Organization(Entity):
    """Organization — wmoop.org/Organization. A structured, persistent group of people (and resources) acting together to pursue one or more shared goals, recognised as a single entity."""
    WM_ID = "wmoop.org/Organization"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, legalName=None, foundingDate=None):
        super().__init__(id, name)
        self._legalName = legalName
        self._foundingDate = foundingDate
    @property
    def legalName(self):
        return self._legalName
    @property
    def foundingDate(self):
        return self._foundingDate

class Employee(Role):
    """Employee role — wmoop.org/Employee. The role of a person engaged under a contract of employment by an organisation."""
    WM_ID = "wmoop.org/Employee"
    WM_PLAYED_BY = "wmoop.nature/Person"
    def __init__(self, *, employeeId=None, hiredOn=None):
        super().__init__()
        self._employeeId = employeeId
        self._hiredOn = hiredOn
    @property
    def role_type(self):
        return ConceptId(self.WM_ID)
    @property
    def employeeId(self):
        return self._employeeId
    @property
    def hiredOn(self):
        return self._hiredOn

"""Generated runtime kernel for the WMOOP Python binding. DO NOT EDIT."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ConceptId:
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("A ConceptId must be a non-empty identifier.")

    def __str__(self):
        return self.value


def _coerce_id(x):
    return x if isinstance(x, ConceptId) else ConceptId(x)


@dataclass(frozen=True)
class Quantity:
    value: float
    unit: str

    def __post_init__(self):
        if not self.unit or not self.unit.strip():
            raise ValueError("A Quantity must carry a unit.")

    def __str__(self):
        return f"{self.value:g} {self.unit}"


class Entity(ABC):
    def __init__(self, id, name):
        self._id = _coerce_id(id)
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def __str__(self):
        return f"{self._name} [{self._id}]"


class Role(ABC):
    def __init__(self):
        self._subject = None

    @property
    @abstractmethod
    def role_type(self):
        ...

    @property
    def subject(self):
        return self._subject

    def _attach(self, subject):
        if self._subject is not None:
            raise RuntimeError("Role is already attached to a subject.")
        self._subject = subject


class HasRoles:
    def _init_roles(self):
        self._roles = []

    @property
    def roles(self):
        return tuple(self._roles)

    def add_role(self, role):
        role._attach(self)
        self._roles.append(role)
        return role

    def has_role(self, role_cls):
        return self.get_role(role_cls) is not None

    def get_role(self, role_cls):
        for r in self._roles:
            if isinstance(r, role_cls):
                return r
        return None

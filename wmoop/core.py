"""wmoop.core — the L0 meta-model kernel (Python binding).

Mirrors the C# ``Wmoop.Core``: the foundational categories every domain builds on.
Idiomatic Python (frozen dataclasses for value objects, ABCs for abstractions,
a mixin for role composition); no third-party dependencies.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Type, TypeVar


@dataclass(frozen=True)
class ConceptId:
    """Stable, opaque global identifier (Invariant 4), e.g. ``wm:transport/Moped``.

    Value objects are frozen dataclasses, so equality and hashing are by value and
    identity cannot drift — the Python equivalent of C#'s ``readonly struct``.
    """

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("A ConceptId must be a non-empty, stable identifier.")

    def __str__(self) -> str:
        return self.value


def _coerce_id(id_: "ConceptId | str") -> ConceptId:
    """Accept a literal string wherever a ConceptId is expected (C# had an implicit cast)."""
    return id_ if isinstance(id_, ConceptId) else ConceptId(id_)


@dataclass(frozen=True)
class Quantity:
    """A magnitude paired with its unit (Invariant 4) — never a bare number."""

    value: float
    unit: str

    def __post_init__(self) -> None:
        if not self.unit or not self.unit.strip():
            raise ValueError("A Quantity must carry a non-empty unit symbol.")

    def __str__(self) -> str:
        return f"{self.value:g} {self.unit}"


class Entity(ABC):
    """Root of everything identifiable in the World Model (Invariant 4).

    Concrete domain types derive from it only where there is a genuine, stable
    *is-a-kind-of* relationship (Invariant 3). Cross-cutting facets are roles
    attached by composition, never subclasses.
    """

    def __init__(self, id: "ConceptId | str", name: str) -> None:
        if name is None:
            raise ValueError("name is required")
        self._id = _coerce_id(id)
        self._name = name

    @property
    def id(self) -> ConceptId:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return f"{self._name} [{self._id}]"


class Role(ABC):
    """A context-dependent facet an Entity can play, acquire or lose (Invariant 3).

    A human is intrinsically a ``Person`` for life, but a ``Driver`` only while
    licensed. Modelling ``Driver(Person)`` by inheritance is wrong; a role is a
    separate object attached by composition and queried through :class:`HasRoles`.
    """

    def __init__(self) -> None:
        self._subject: Optional[Entity] = None

    @property
    @abstractmethod
    def role_type(self) -> ConceptId:
        ...

    @property
    def subject(self) -> Optional[Entity]:
        return self._subject

    def _attach(self, subject: "Entity") -> None:
        if self._subject is not None:
            raise RuntimeError(
                f"Role '{self.role_type}' is already attached to "
                f"'{self._subject.name}' and cannot be reassigned."
            )
        if subject is None:
            raise ValueError("subject is required")
        self._subject = subject


TRole = TypeVar("TRole", bound=Role)


class HasRoles:
    """Mixin giving an Entity role-by-composition semantics (Invariant 3).

    "A Person HAS-A set of roles", not "a Person IS-A driver". The hosting class
    calls :meth:`_init_roles` from its own ``__init__``. Keeping this logic in one
    kernel mixin means every role-bearing entity gets correct, consistent semantics
    with no duplication.
    """

    def _init_roles(self) -> None:
        self._roles: list[Role] = []

    @property
    def roles(self) -> tuple[Role, ...]:
        return tuple(self._roles)

    def add_role(self, role: TRole) -> TRole:
        role._attach(self)  # type: ignore[arg-type]
        self._roles.append(role)
        return role

    def has_role(self, role_cls: Type[TRole]) -> bool:
        return self.get_role(role_cls) is not None

    def get_role(self, role_cls: Type[TRole]) -> Optional[TRole]:
        for r in self._roles:
            if isinstance(r, role_cls):
                return r
        return None

"""wmoop.nature — the biology branch (mirrors C# ``Wmoop.Nature``)."""
from __future__ import annotations

from abc import abstractmethod

from .core import Entity, HasRoles


class Animal(Entity):
    """``wm:nature/Animal`` — a genuine, stable *is-a-kind-of* abstraction (Invariant 3).

    Kept shallow and Liskov-clean: a subclass only ever *adds* intrinsic biological
    properties.
    """

    def __init__(self, id, name, leg_count: int) -> None:
        super().__init__(id, name)
        if leg_count < 0:
            raise ValueError("Leg count cannot be negative.")
        self._leg_count = leg_count

    @property
    def leg_count(self) -> int:
        return self._leg_count

    @property
    @abstractmethod
    def taxon(self) -> str:
        """Polymorphic biological taxon of the concrete kind."""
        ...


class Person(Animal, HasRoles):
    """``wm:nature/Person`` — a human individual; an L1 class that is-a ``Animal``.

    Carries only *intrinsic biological* state (legs via :class:`Animal`, birth year).
    Everything a person can additionally *do* or *be* in context — driver, owner,
    employee — is a role attached through :class:`~wmoop.core.HasRoles`, which this
    class satisfies by composing a role container. The deep biological ranks
    (Chordate, Mammal, Primate, Homo sapiens) are carried as classification facts
    elsewhere, not as inheritance levels.
    """

    def __init__(self, id, name, birth_year: int) -> None:
        super().__init__(id, name, leg_count=2)
        self._init_roles()
        self._birth_year = birth_year

    @property
    def birth_year(self) -> int:
        return self._birth_year

    @property
    def taxon(self) -> str:
        return "Homo sapiens"

    def age_at(self, year: int) -> int:
        return year - self._birth_year

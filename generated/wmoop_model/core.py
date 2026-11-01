"""Generated from module wmoop.core v1.1.0. DO NOT EDIT — regenerate with wmoop.tools."""
from __future__ import annotations
from enum import Enum
from ._runtime import ConceptId, Entity, Quantity, Role, HasRoles  # noqa: F401

class ProvenanceKind(str, Enum):
    """ProvenanceKind — wmoop.core/ProvenanceKind."""
    sourced = "sourced"
    definitional = "definitional"
    convention = "convention"

class Provenance(Entity):
    """Provenance — wmoop.core/Provenance. A single provenance record attached to a node, property or fact: where the claim comes from and how it is grounded. Reifies the built-in WML `provenance:` object so the kernel defines the very type the meta-level uses (Invariant 4 — nothing is unsourced)."""
    WM_ID = "wmoop.core/Provenance"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, source=None, kind=None, ref=None, url=None, note=None):
        super().__init__(id, name)
        self._source = source
        self._kind = kind
        self._ref = ref
        self._url = url
        self._note = note
    @property
    def source(self):
        return self._source
    @property
    def kind(self):
        return self._kind
    @property
    def ref(self):
        return self._ref
    @property
    def url(self):
        return self._url
    @property
    def note(self):
        return self._note

class QuantityKind(Entity):
    """QuantityKind — wmoop.core/QuantityKind. A kind of measurable quantity (Length, Mass, Speed, …) characterised by its SI Dimension: a 7-vector of integer exponents over the SI base dimensions (L, M, T, I, Θ, N, J) = (Length, Mass, Time, ElectricCurrent, Temperature, AmountOfSubstance, LuminousIntensity). A derived kind (Speed, Area, Volume) also records its dimension formula. A property measured in some kind is typed by that kind and carries a `unit:` (meta-model §6.4)."""
    WM_ID = "wmoop.core/QuantityKind"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, dimL=0, dimM=0, dimT=0, dimI=0, dimTheta=0, dimN=0, dimJ=0, canonicalUnit=None, derivation=None):
        super().__init__(id, name)
        self._dimL = dimL
        self._dimM = dimM
        self._dimT = dimT
        self._dimI = dimI
        self._dimTheta = dimTheta
        self._dimN = dimN
        self._dimJ = dimJ
        self._canonicalUnit = canonicalUnit
        self._derivation = derivation
    @property
    def dimL(self):
        return self._dimL
    @property
    def dimM(self):
        return self._dimM
    @property
    def dimT(self):
        return self._dimT
    @property
    def dimI(self):
        return self._dimI
    @property
    def dimTheta(self):
        return self._dimTheta
    @property
    def dimN(self):
        return self._dimN
    @property
    def dimJ(self):
        return self._dimJ
    @property
    def canonicalUnit(self):
        return self._canonicalUnit
    @property
    def derivation(self):
        return self._derivation

class Unit(Entity):
    """Unit — wmoop.core/Unit. A unit of measurement belonging to exactly one QuantityKind, with a linear conversion to that kind's canonical (SI) unit: canonical = factor · value + offset (the offset supports scales such as °C ↔ K). Units are first-class (meta-model §6.4, R5): a measured property names its Unit in `unit:`."""
    WM_ID = "wmoop.core/Unit"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, symbol=None, quantityKind=None, factor=1, offset=0):
        super().__init__(id, name)
        self._symbol = symbol
        self._quantityKind = quantityKind
        self._factor = factor
        self._offset = offset
    @property
    def symbol(self):
        return self._symbol
    @property
    def quantityKind(self):
        return self._quantityKind
    @property
    def factor(self):
        return self._factor
    @property
    def offset(self):
        return self._offset

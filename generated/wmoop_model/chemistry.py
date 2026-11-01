"""Generated from module wmoop.chemistry v0.1.0. DO NOT EDIT — regenerate with wmoop.tools."""
from __future__ import annotations
from enum import Enum
from ._runtime import ConceptId, Entity, Quantity, Role, HasRoles  # noqa: F401

class StateOfMatter(str, Enum):
    """StateOfMatter — wmoop.chemistry/StateOfMatter."""
    SOLID = "SOLID"
    LIQUID = "LIQUID"
    GAS = "GAS"

class ChemicalSubstance(Entity, HasRoles):
    """ChemicalSubstance — wmoop.chemistry/ChemicalSubstance. A form of matter with a definite chemical composition and characteristic properties."""
    WM_ID = "wmoop.chemistry/ChemicalSubstance"
    WM_KIND = "abstract"
    def __init__(self, id, name, *, standardState=None, meltingPoint=None):
        if type(self) is ChemicalSubstance:
            raise TypeError("ChemicalSubstance is abstract and cannot be instantiated directly.")
        super().__init__(id, name)
        self._init_roles()
        self._standardState = standardState
        self._meltingPoint = meltingPoint
    @property
    def standardState(self):
        return self._standardState
    @property
    def meltingPoint(self):
        return self._meltingPoint

class ChemicalElement(ChemicalSubstance):
    """ChemicalElement — wmoop.chemistry/ChemicalElement. A substance whose atoms all share the same number of protons and that cannot be broken down into simpler substances by chemical means."""
    WM_ID = "wmoop.chemistry/ChemicalElement"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, standardState=None, meltingPoint=None, atomicNumber=None, symbol=None, standardAtomicWeight=None):
        super().__init__(id, name, standardState=standardState, meltingPoint=meltingPoint)
        self._atomicNumber = atomicNumber
        self._symbol = symbol
        self._standardAtomicWeight = standardAtomicWeight
    @property
    def atomicNumber(self):
        return self._atomicNumber
    @property
    def symbol(self):
        return self._symbol
    @property
    def standardAtomicWeight(self):
        return self._standardAtomicWeight

class ChemicalCompound(ChemicalSubstance):
    """ChemicalCompound — wmoop.chemistry/ChemicalCompound. A substance made of two or more different chemical elements chemically bonded in a fixed proportion."""
    WM_ID = "wmoop.chemistry/ChemicalCompound"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, standardState=None, meltingPoint=None, chemicalFormula=None):
        super().__init__(id, name, standardState=standardState, meltingPoint=meltingPoint)
        self._chemicalFormula = chemicalFormula
    @property
    def chemicalFormula(self):
        return self._chemicalFormula

class Atom(Entity):
    """Atom — wmoop.chemistry/Atom. The smallest particle of a chemical element that retains that element's chemical identity."""
    WM_ID = "wmoop.chemistry/Atom"
    WM_KIND = "concrete"
    def __init__(self, id, name):
        super().__init__(id, name)

class Molecule(Entity):
    """Molecule — wmoop.chemistry/Molecule. An electrically neutral group of two or more atoms held together by chemical bonds, the smallest unit of a molecular substance."""
    WM_ID = "wmoop.chemistry/Molecule"
    WM_KIND = "concrete"
    def __init__(self, id, name):
        super().__init__(id, name)

class ChemicalReaction(Entity):
    """ChemicalReaction — wmoop.chemistry/ChemicalReaction. A process in which one or more chemical substances (reactants) are transformed into one or more different substances (products)."""
    WM_ID = "wmoop.chemistry/ChemicalReaction"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, isReversible=None):
        super().__init__(id, name)
        self._isReversible = isReversible
    @property
    def isReversible(self):
        return self._isReversible

class Catalyst(Role):
    """Catalyst role — wmoop.chemistry/Catalyst. The role of a substance that increases the rate of a chemical reaction without itself being consumed by it."""
    WM_ID = "wmoop.chemistry/Catalyst"
    WM_PLAYED_BY = "wmoop.chemistry/ChemicalSubstance"
    def __init__(self):
        super().__init__()
    @property
    def role_type(self):
        return ConceptId(self.WM_ID)

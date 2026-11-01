"""Generated from module wmoop.math v0.1.0. DO NOT EDIT — regenerate with wmoop.tools."""
from __future__ import annotations
from ._runtime import ConceptId, Entity, Quantity, Role, HasRoles  # noqa: F401

class MathematicalObject(Entity):
    """MathematicalObject — wmoop.math/MathematicalObject. An abstract object of mathematics: an entity existing outside space-time and without causal powers, individuated purely by its defining properties."""
    WM_ID = "wmoop.math/MathematicalObject"
    WM_KIND = "abstract"
    def __init__(self, id, name):
        if type(self) is MathematicalObject:
            raise TypeError("MathematicalObject is abstract and cannot be instantiated directly.")
        super().__init__(id, name)

class Collection(MathematicalObject):
    """Collection — wmoop.math/Collection. A 'many-as-one': a single abstract object that gathers zero or more member objects into a whole. The L0 Collection stereotype, realised here for the mathematical collections (whose members are themselves mathematical objects)."""
    WM_ID = "wmoop.math/Collection"
    WM_KIND = "abstract"
    def __init__(self, id, name, *, isEmpty=None):
        if type(self) is Collection:
            raise TypeError("Collection is abstract and cannot be instantiated directly.")
        super().__init__(id, name)
        self._isEmpty = isEmpty
    @property
    def isEmpty(self):
        return self._isEmpty

class Set(Collection):
    """Set — wmoop.math/Set. A set: a collection of distinct members, unordered and without repetition, determined entirely by which objects are its members (extensionality)."""
    WM_ID = "wmoop.math/Set"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, isEmpty=None, isFinite=None):
        super().__init__(id, name, isEmpty=isEmpty)
        self._isFinite = isFinite
    @property
    def isFinite(self):
        return self._isFinite

class Number(MathematicalObject):
    """Number — wmoop.math/Number. A mathematical object expressing magnitude, count, or position on the real number line. In this module 'Number' ranges over the real tower (ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ), which is totally ordered — hence IComparable."""
    WM_ID = "wmoop.math/Number"
    WM_KIND = "abstract"
    def __init__(self, id, name):
        if type(self) is Number:
            raise TypeError("Number is abstract and cannot be instantiated directly.")
        super().__init__(id, name)

class NaturalNumber(Number):
    """NaturalNumber — wmoop.math/NaturalNumber. A non-negative whole number 0, 1, 2, 3, … generated from zero by repeated succession (the counting numbers)."""
    WM_ID = "wmoop.math/NaturalNumber"
    WM_KIND = "concrete"
    def __init__(self, id, name):
        super().__init__(id, name)

class Integer(Number):
    """Integer — wmoop.math/Integer. A whole number — zero, a positive natural number, or its negative (…, −2, −1, 0, 1, 2, …). The naturals embed in the integers (ℕ ⊂ ℤ)."""
    WM_ID = "wmoop.math/Integer"
    WM_KIND = "concrete"
    def __init__(self, id, name):
        super().__init__(id, name)

class RationalNumber(Number):
    """RationalNumber — wmoop.math/RationalNumber. A number expressible as a ratio p/q of two integers with q ≠ 0, identified up to equality of ratios. The integers embed in the rationals (ℤ ⊂ ℚ)."""
    WM_ID = "wmoop.math/RationalNumber"
    WM_KIND = "concrete"
    def __init__(self, id, name):
        super().__init__(id, name)

class RealNumber(Number):
    """RealNumber — wmoop.math/RealNumber. A number on the continuous number line: a member of the unique complete totally ordered field, containing the rationals and their limits (ℚ ⊂ ℝ)."""
    WM_ID = "wmoop.math/RealNumber"
    WM_KIND = "concrete"
    def __init__(self, id, name):
        super().__init__(id, name)

class GeometricShape(MathematicalObject):
    """GeometricShape — wmoop.math/GeometricShape. An abstract geometric figure: that which is contained by one or more boundaries, studied up to its defining properties rather than any physical drawing of it."""
    WM_ID = "wmoop.math/GeometricShape"
    WM_KIND = "abstract"
    def __init__(self, id, name):
        if type(self) is GeometricShape:
            raise TypeError("GeometricShape is abstract and cannot be instantiated directly.")
        super().__init__(id, name)

class Polygon(GeometricShape):
    """Polygon — wmoop.math/Polygon. A plane figure bounded by a finite number of straight line segments (sides) joined end to end to form a single closed chain."""
    WM_ID = "wmoop.math/Polygon"
    WM_KIND = "abstract"
    def __init__(self, id, name, *, sideCount=None, isRegular=None):
        if type(self) is Polygon:
            raise TypeError("Polygon is abstract and cannot be instantiated directly.")
        super().__init__(id, name)
        self._sideCount = sideCount
        self._isRegular = isRegular
    @property
    def sideCount(self):
        return self._sideCount
    @property
    def isRegular(self):
        return self._isRegular

class Triangle(Polygon):
    """Triangle — wmoop.math/Triangle. A three-sided polygon (trilateral). Its three interior angles sum to two right angles (π rad)."""
    WM_ID = "wmoop.math/Triangle"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, sideCount=None, isRegular=None):
        super().__init__(id, name, sideCount=sideCount, isRegular=isRegular)

class Quadrilateral(Polygon):
    """Quadrilateral — wmoop.math/Quadrilateral. A four-sided polygon (quadrilateral). Its four interior angles sum to four right angles (2π rad)."""
    WM_ID = "wmoop.math/Quadrilateral"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, sideCount=None, isRegular=None):
        super().__init__(id, name, sideCount=sideCount, isRegular=isRegular)

class AlgebraicStructure(MathematicalObject):
    """AlgebraicStructure — wmoop.math/AlgebraicStructure. A set (the carrier) together with one or more operations on it that satisfy a fixed list of axioms. Concrete structures (groups, rings, fields, …) differ by their operations and the axioms those operations obey."""
    WM_ID = "wmoop.math/AlgebraicStructure"
    WM_KIND = "abstract"
    def __init__(self, id, name):
        if type(self) is AlgebraicStructure:
            raise TypeError("AlgebraicStructure is abstract and cannot be instantiated directly.")
        super().__init__(id, name)

class Group(AlgebraicStructure):
    """Group — wmoop.math/Group. An algebraic structure (G, ·): a set G with a single binary operation · that is closed, associative, has an identity element, and gives every element an inverse. Below, `·` denotes the group's binary operation and the four group axioms are stated as invariants (this is the 'axioms are invariants' case)."""
    WM_ID = "wmoop.math/Group"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, order=None, isAbelian=None):
        super().__init__(id, name)
        self._order = order
        self._isAbelian = isAbelian
    @property
    def order(self):
        return self._order
    @property
    def isAbelian(self):
        return self._isAbelian

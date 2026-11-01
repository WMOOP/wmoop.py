"""Generated from module wmoop.philosophy v0.1.0. DO NOT EDIT — regenerate with wmoop.tools."""
from __future__ import annotations
from enum import Enum
from ._runtime import ConceptId, Entity, Quantity, Role, HasRoles  # noqa: F401

class CategoricalForm(str, Enum):
    """CategoricalForm — wmoop.philosophy/CategoricalForm."""
    UNIVERSAL_AFFIRMATIVE = "UNIVERSAL_AFFIRMATIVE"
    UNIVERSAL_NEGATIVE = "UNIVERSAL_NEGATIVE"
    PARTICULAR_AFFIRMATIVE = "PARTICULAR_AFFIRMATIVE"
    PARTICULAR_NEGATIVE = "PARTICULAR_NEGATIVE"

class PhilosophicalConcept(Entity):
    """PhilosophicalConcept — wmoop.philosophy/PhilosophicalConcept. An abstract idea or universal that is an object of philosophical analysis (e.g. justice, causation, identity, being)."""
    WM_ID = "wmoop.philosophy/PhilosophicalConcept"
    WM_KIND = "abstract"
    def __init__(self, id, name):
        if type(self) is PhilosophicalConcept:
            raise TypeError("PhilosophicalConcept is abstract and cannot be instantiated directly.")
        super().__init__(id, name)

class Proposition(Entity):
    """Proposition — wmoop.philosophy/Proposition. A truth-apt content that is either true or false and can be affirmed, denied, or offered as a premise or a conclusion."""
    WM_ID = "wmoop.philosophy/Proposition"
    WM_KIND = "abstract"
    def __init__(self, id, name, *, content=None):
        if type(self) is Proposition:
            raise TypeError("Proposition is abstract and cannot be instantiated directly.")
        super().__init__(id, name)
        self._content = content
    @property
    def content(self):
        return self._content

class CategoricalProposition(Proposition):
    """CategoricalProposition — wmoop.philosophy/CategoricalProposition. A proposition that affirms or denies a predicate of a subject in one of the four standard forms, as used in categorical syllogisms."""
    WM_ID = "wmoop.philosophy/CategoricalProposition"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, content=None, form=None):
        super().__init__(id, name, content=content)
        self._form = form
    @property
    def form(self):
        return self._form

class Argument(Entity):
    """Argument — wmoop.philosophy/Argument. A structured set of propositions in which one or more premises are offered in support of a conclusion."""
    WM_ID = "wmoop.philosophy/Argument"
    WM_KIND = "abstract"
    def __init__(self, id, name, *, premiseCount=None):
        if type(self) is Argument:
            raise TypeError("Argument is abstract and cannot be instantiated directly.")
        super().__init__(id, name)
        self._premiseCount = premiseCount
    @property
    def premiseCount(self):
        return self._premiseCount

class DeductiveArgument(Argument):
    """DeductiveArgument — wmoop.philosophy/DeductiveArgument. An argument whose conclusion is claimed to follow of necessity from its premises, so that it is valid or invalid."""
    WM_ID = "wmoop.philosophy/DeductiveArgument"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, premiseCount=None, valid=None):
        super().__init__(id, name, premiseCount=premiseCount)
        self._valid = valid
    @property
    def valid(self):
        return self._valid

class InductiveArgument(Argument):
    """InductiveArgument — wmoop.philosophy/InductiveArgument. An argument whose premises are offered to make the conclusion probable rather than necessary, so that it is strong or weak rather than valid."""
    WM_ID = "wmoop.philosophy/InductiveArgument"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, premiseCount=None, strong=None):
        super().__init__(id, name, premiseCount=premiseCount)
        self._strong = strong
    @property
    def strong(self):
        return self._strong

class Syllogism(DeductiveArgument):
    """Syllogism — wmoop.philosophy/Syllogism. A categorical syllogism: a deductive argument with exactly two categorical premises and a categorical conclusion, linked through a shared middle term."""
    WM_ID = "wmoop.philosophy/Syllogism"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, premiseCount=None, valid=None, figure=None):
        super().__init__(id, name, premiseCount=premiseCount, valid=valid)
        self._figure = figure
    @property
    def figure(self):
        return self._figure

class PhilosophicalPosition(Entity):
    """PhilosophicalPosition — wmoop.philosophy/PhilosophicalPosition. A stance on a philosophical question, characterised by the propositions it affirms as true (for example a thesis such as realism or dualism)."""
    WM_ID = "wmoop.philosophy/PhilosophicalPosition"
    WM_KIND = "abstract"
    def __init__(self, id, name):
        if type(self) is PhilosophicalPosition:
            raise TypeError("PhilosophicalPosition is abstract and cannot be instantiated directly.")
        super().__init__(id, name)

class AristotelianCategory(Entity):
    """AristotelianCategory — wmoop.philosophy/AristotelianCategory. One of the ten highest kinds (categories) under which, in Aristotle's scheme, anything that can be said of a subject falls."""
    WM_ID = "wmoop.philosophy/AristotelianCategory"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, greekTerm=None):
        super().__init__(id, name)
        self._greekTerm = greekTerm
    @property
    def greekTerm(self):
        return self._greekTerm

class Branch(Entity):
    """Branch — wmoop.philosophy/Branch. A major field of philosophical inquiry, distinguished by the kind of question it asks."""
    WM_ID = "wmoop.philosophy/Branch"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, centralQuestion=None):
        super().__init__(id, name)
        self._centralQuestion = centralQuestion
    @property
    def centralQuestion(self):
        return self._centralQuestion

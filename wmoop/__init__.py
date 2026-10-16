"""WMOOP — World Map Object-Oriented Programming (Python reference binding).

A faithful Python projection of the same World Model implemented in C# in
``wmoop.net``. It demonstrates that the canonical, language-neutral model maps to
idiomatic code in any language with no duplication of the *concepts* — only an
idiomatic re-expression per language (here: dataclasses, ABCs, Protocols, dunder
operators).

Layers mirror the C# kernel:
    wmoop.core       — L0 meta-model (Entity, ConceptId, Quantity, Role, HasRoles)
    wmoop.nature     — Animal -> Person
    wmoop.transport  — Vehicle hierarchy + Driver/Owner roles
    wmoop.geography  — AdministrativeArea Composite (part_of)
    wmoop.patterns   — Visitor, Specification, Builder, Strategy, Registry
"""

__all__ = ["core", "nature", "transport", "geography", "patterns"]
__version__ = "0.1.0"

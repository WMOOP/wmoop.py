<p align="center">
  <img alt="wmoop.py" src="brand/wmoop.py.svg" width="340">
</p>

# wmoop.py

**The Python reference binding of [WMOOP](https://github.com/WMOOP) — *World Map
Object-Oriented Programming*.**

This is the **Python twin** of [`wmoop.net`](https://github.com/WMOOP/wmoop.net): the *same*
World Model — same domains, same cross-domain `Person`→`Driver` example, same design patterns —
re-expressed in idiomatic Python. It exists to prove the project's central claim: a single,
language-neutral model maps to any language **without duplicating the concepts**, only re-stating
them in each language's idioms.

> The canonical model and all design documents live in
> [`wmoop.doc`](https://github.com/WMOOP/wmoop.doc). In the target architecture these Python
> classes are **generated** from the WML model; this repo is the hand-written reference the
> generator's output will match (conformance-tested).

## Parity with the C# binding

| Concept | C# (`wmoop.net`) | Python (`wmoop.py`) |
|---------|------------------|---------------------|
| Value objects | `readonly struct` | `@dataclass(frozen=True)` |
| Abstraction | `abstract class` | `abc.ABC` + `@abstractmethod` |
| Role composition | `IHasRoles` + `RoleContainer` | `HasRoles` mixin |
| Visitor hook | interface `IAreaVisitor` | `typing.Protocol` |
| Specification combinators | `.And()/.Or()/.Not()` | `&` / `\|` / `~` dunder operators |
| Generics | `ISpecification<T>` | `Generic[T]` |
| Conformance tests | 13 checks, non-zero exit | the same 13 checks, non-zero exit |

Same semantics, idiomatic surface. That is exactly the "write once, replicate everywhere" story.

## Layout

```
wmoop.py/
├── wmoop/
│   ├── core.py        # L0 kernel: ConceptId, Quantity, Entity, Role, HasRoles
│   ├── nature.py      # Animal -> Person
│   ├── transport.py   # Vehicle -> RoadVehicle -> Motorcycle -> Moped + Driver/Owner roles
│   ├── geography.py   # AdministrativeArea Composite (part_of)
│   └── patterns.py    # Visitor, Specification, Builder, Strategy, Registry
├── demo.py            # cross-domain roles + polymorphism walkthrough
├── patterns_demo.py   # one section per design pattern, self-checking
└── tests.py           # the 13 conformance checks
```

## Run

Requires **Python 3.10+**. No third-party dependencies.

```bash
python demo.py
python patterns_demo.py
python tests.py        # exits non-zero on failure
```

(On Windows the launcher is usually `py` instead of `python`.)

## License

Code: **Apache-2.0**. Model data & docs (in `wmoop.doc`): **CC-BY-4.0**.

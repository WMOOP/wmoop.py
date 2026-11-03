# Contributing

This repository is the **Python reference binding** of the WMOOP World Model. WMOOP is a
multi-repository project, so the **canonical** contribution process, governance and ethics live in
the documentation repository, [`wmoop.doc`](https://github.com/WMOOP/wmoop.doc):

- [Contributing guide](https://github.com/WMOOP/wmoop.doc/blob/main/CONTRIBUTING.md)
- [AI contributor protocol](https://github.com/WMOOP/wmoop.doc/blob/main/AI_CONTRIBUTING.md)
- [Governance](https://github.com/WMOOP/wmoop.doc/blob/main/GOVERNANCE.md)
- [Ethics & quality](https://github.com/WMOOP/wmoop.doc/blob/main/ETHICS.md)
- [Design patterns & OOP practices](https://github.com/WMOOP/wmoop.doc/blob/main/PATTERNS.md)

> The code of conduct and the security policy are organisation-wide, in
> [`WMOOP/.github`](https://github.com/WMOOP/.github); GitHub shows them in this repository too.

## Working in this repository

- **Run:** see the [README](README.md) (`python demo.py`, `python conformance.py`).
- **Checks:** the conformance vectors are shared by every binding and live in
  [`wmoop.doc/conformance`](https://github.com/WMOOP/wmoop.doc/tree/main/conformance). A new check
  is a vector there, not a test here. `conformance.py` only runs them.
- **Where changes belong:** the data classes are generated from the canonical WML model in
  [`wmoop.doc/model`](https://github.com/WMOOP/wmoop.doc/tree/main/model) by
  [`wmoop.tools`](https://github.com/WMOOP/wmoop.tools). `generated/` is written only by the
  generator, from the pinned submodules: never edit it; regenerate it as the README describes. To
  change data, change the **model** in `wmoop.doc`. Behaviour belongs here: in a `<Name>Ext` mixin
  in `wmoop_ext/<domain>.py`, or in `wmoop/patterns.py` (visitors, strategies, specifications).
- **Licensing:** by contributing you agree your contributions are released under this repository's
  [LICENSE](LICENSE) (Apache-2.0).

"""Hand-written behaviour for the generated ``wmoop`` classes (the generation gap, Python style).

Every class generated in ``generated/wmoop/<domain>.py`` puts the mixin ``<Name>Ext`` from
``wmoop_ext.<domain>`` first among its bases, when this package defines one. A mixin adds
behaviour only: the data, the roles and the relations stay generated. Its methods override the
generated chain and are inherited down it, so ``VehicleExt.describe`` serves every vehicle and
``MotorcycleExt`` refines it through ``super()``.

A mixin module is imported while its generated module is still loading. Import generated classes
only for annotations (under ``TYPE_CHECKING``), never at module level.
"""

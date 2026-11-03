"""Behaviour of the generated ``wmoop.transport`` classes: describing vehicles, what a licence allows."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wmoop.transport import LicenceCategory


class VehicleExt:
    """Mixed into the generated ``wmoop.transport.Vehicle``, so every vehicle inherits it."""

    @property
    def classification(self) -> str:
        """A short kind name for display; each kind of vehicle refines it."""
        return "vehicle"

    def describe(self) -> str:
        speed = self.max_speed if self.max_speed is not None else "unknown"
        return f"{self.name} — a {self.classification} with {self.wheel_count} wheels, top speed {speed}."


class MotorcycleExt:
    """Mixed into the generated ``wmoop.transport.Motorcycle``, and inherited by ``Moped``."""

    @property
    def classification(self) -> str:
        return "motorcycle"

    def describe(self) -> str:
        return super().describe() + f" Engine: {self.engine_displacement}."


class MopedExt:
    """Mixed into the generated ``wmoop.transport.Moped``."""

    @property
    def classification(self) -> str:
        return "moped"


class DriverExt:
    """Mixed into the generated ``wmoop.transport.Driver`` role: what the licence allows."""

    def can_drive(self, category: LicenceCategory | str, on: datetime.date) -> bool:
        """True when the licence covers ``category`` and has not expired on ``on``.

        The model records no issue date, and a licence whose expiry is not recorded counts as valid.
        """
        expiry = self.licence_expiry
        return category in self.licence_categories and (expiry is None or on <= expiry)

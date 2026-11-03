"""Behaviour of the generated ``wmoop.nature`` classes."""

from __future__ import annotations

import datetime


class PersonExt:
    """Mixed into the generated ``wmoop.nature.Person``."""

    def age_on(self, on: datetime.date) -> int | None:
        """Age in whole years on ``on``, or None when the date of birth is not recorded."""
        born = self.date_of_birth
        if born is None:
            return None
        return on.year - born.year - ((on.month, on.day) < (born.month, born.day))

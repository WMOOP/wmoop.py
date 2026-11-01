"""Generated from module wmoop.music v0.1.0. DO NOT EDIT — regenerate with wmoop.tools."""
from __future__ import annotations
from ._runtime import ConceptId, Entity, Quantity, Role, HasRoles  # noqa: F401

class PitchClass(Entity):
    """PitchClass — wmoop.music/PitchClass. One of the twelve pitch classes of the chromatic scale (C, C#, D, …), each the set of all pitches an whole number of octaves apart; an abstract entity independent of octave or instrument."""
    WM_ID = "wmoop.music/PitchClass"
    WM_KIND = "concrete"
    def __init__(self, id, name):
        super().__init__(id, name)

class Interval(Entity):
    """Interval — wmoop.music/Interval. The pitch distance between two notes, measured in semitones."""
    WM_ID = "wmoop.music/Interval"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, semitones=None):
        super().__init__(id, name)
        self._semitones = semitones
    @property
    def semitones(self):
        return self._semitones

class Scale(Entity):
    """Scale — wmoop.music/Scale. An ordered collection of pitch classes spanning an octave, from which the pitch material of a passage is drawn (e.g. the major scale). A Collection of pitch classes (membership, not mereological parthood)."""
    WM_ID = "wmoop.music/Scale"
    WM_KIND = "concrete"
    def __init__(self, id, name):
        super().__init__(id, name)

class Chord(Entity):
    """Chord — wmoop.music/Chord. A set of three or more pitch classes conceived as sounding together. A Collection of pitch classes (an abstract harmonic object)."""
    WM_ID = "wmoop.music/Chord"
    WM_KIND = "concrete"
    def __init__(self, id, name):
        super().__init__(id, name)

class MusicalWork(Entity):
    """MusicalWork — wmoop.music/MusicalWork. An abstract musical composition — the work itself, as distinct from any particular performance or recording of it (a C# in it is the same work's note in every performance)."""
    WM_ID = "wmoop.music/MusicalWork"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, title=None):
        super().__init__(id, name)
        self._title = title
    @property
    def title(self):
        return self._title

class MusicalInstrument(Entity):
    """MusicalInstrument — wmoop.music/MusicalInstrument. A device constructed or adapted to produce musical sound."""
    WM_ID = "wmoop.music/MusicalInstrument"
    WM_KIND = "abstract"
    def __init__(self, id, name):
        if type(self) is MusicalInstrument:
            raise TypeError("MusicalInstrument is abstract and cannot be instantiated directly.")
        super().__init__(id, name)

class Idiophone(MusicalInstrument):
    """Idiophone — wmoop.music/Idiophone. An instrument that produces sound by the vibration of its own rigid body, without strings or a membrane (e.g. a xylophone, a bell)."""
    WM_ID = "wmoop.music/Idiophone"
    WM_KIND = "concrete"
    def __init__(self, id, name):
        super().__init__(id, name)

class Membranophone(MusicalInstrument):
    """Membranophone — wmoop.music/Membranophone. An instrument that produces sound by the vibration of a stretched membrane (e.g. a drum)."""
    WM_ID = "wmoop.music/Membranophone"
    WM_KIND = "concrete"
    def __init__(self, id, name):
        super().__init__(id, name)

class Chordophone(MusicalInstrument):
    """Chordophone — wmoop.music/Chordophone. An instrument that produces sound by the vibration of one or more stretched strings (e.g. a violin, a piano)."""
    WM_ID = "wmoop.music/Chordophone"
    WM_KIND = "concrete"
    def __init__(self, id, name):
        super().__init__(id, name)

class Aerophone(MusicalInstrument):
    """Aerophone — wmoop.music/Aerophone. An instrument that produces sound by a vibrating column or body of air (e.g. a flute, a trumpet)."""
    WM_ID = "wmoop.music/Aerophone"
    WM_KIND = "concrete"
    def __init__(self, id, name):
        super().__init__(id, name)

class Electrophone(MusicalInstrument):
    """Electrophone — wmoop.music/Electrophone. An instrument in which sound is generated or primarily produced by electrical or electronic means (e.g. a synthesizer)."""
    WM_ID = "wmoop.music/Electrophone"
    WM_KIND = "concrete"
    def __init__(self, id, name):
        super().__init__(id, name)

class MusicalPerformance(Entity):
    """MusicalPerformance — wmoop.music/MusicalPerformance. A particular event of performing music: a rendering, bounded in time, of a musical work (or an improvisation), made up of note occurrences."""
    WM_ID = "wmoop.music/MusicalPerformance"
    WM_KIND = "concrete"
    def __init__(self, id, name):
        super().__init__(id, name)

class NoteOccurrence(Entity):
    """NoteOccurrence — wmoop.music/NoteOccurrence. A single sounded note within a performance: the event of a pitch class being sounded for a span of time. The concrete, in-time counterpart of the abstract pitch class."""
    WM_ID = "wmoop.music/NoteOccurrence"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, duration=None):
        super().__init__(id, name)
        self._duration = duration
    @property
    def duration(self):
        return self._duration

class Performer(Role):
    """Performer role — wmoop.music/Performer. The role of a person who performs music."""
    WM_ID = "wmoop.music/Performer"
    WM_PLAYED_BY = "wmoop.nature/Person"
    def __init__(self):
        super().__init__()
    @property
    def role_type(self):
        return ConceptId(self.WM_ID)

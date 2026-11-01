"""Generated from module wmoop.education v0.1.0. DO NOT EDIT — regenerate with wmoop.tools."""
from __future__ import annotations
from enum import Enum
from ._runtime import ConceptId, Entity, Quantity, Role, HasRoles  # noqa: F401
from .architecture import Building
from .architecture import Room
from .org import Organization

class ISCEDLevel(str, Enum):
    """ISCEDLevel — wmoop.education/ISCEDLevel."""
    EARLY_CHILDHOOD = "EARLY_CHILDHOOD"
    PRIMARY = "PRIMARY"
    LOWER_SECONDARY = "LOWER_SECONDARY"
    UPPER_SECONDARY = "UPPER_SECONDARY"
    POST_SECONDARY_NON_TERTIARY = "POST_SECONDARY_NON_TERTIARY"
    SHORT_CYCLE_TERTIARY = "SHORT_CYCLE_TERTIARY"
    BACHELOR_OR_EQUIVALENT = "BACHELOR_OR_EQUIVALENT"
    MASTER_OR_EQUIVALENT = "MASTER_OR_EQUIVALENT"
    DOCTORAL_OR_EQUIVALENT = "DOCTORAL_OR_EQUIVALENT"

class GradingScale(str, Enum):
    """GradingScale — wmoop.education/GradingScale."""
    ROMANIAN_1_10 = "ROMANIAN_1_10"
    PERCENTAGE_0_100 = "PERCENTAGE_0_100"
    GPA_0_4 = "GPA_0_4"

class EducationalInstitution(Organization):
    """EducationalInstitution — wmoop.education/EducationalInstitution. An organisation whose primary purpose is to provide education through one or more educational programmes."""
    WM_ID = "wmoop.education/EducationalInstitution"
    WM_KIND = "abstract"
    def __init__(self, id, name, *, legalName=None, foundingDate=None, iscedLevels=None):
        if type(self) is EducationalInstitution:
            raise TypeError("EducationalInstitution is abstract and cannot be instantiated directly.")
        super().__init__(id, name, legalName=legalName, foundingDate=foundingDate)
        self._iscedLevels = iscedLevels
    @property
    def iscedLevels(self):
        return self._iscedLevels

class School(EducationalInstitution):
    """School — wmoop.education/School. An institution providing primary and/or secondary education (typically ISCED levels 1-3)."""
    WM_ID = "wmoop.education/School"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, legalName=None, foundingDate=None, iscedLevels=None):
        super().__init__(id, name, legalName=legalName, foundingDate=foundingDate, iscedLevels=iscedLevels)

class SchoolBuilding(Building):
    """SchoolBuilding — wmoop.education/SchoolBuilding. A building designed for or used by a school to deliver education."""
    WM_ID = "wmoop.education/SchoolBuilding"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, floorCount=None):
        super().__init__(id, name, floorCount=floorCount)

class Classroom(Room):
    """Classroom — wmoop.education/Classroom. A room in which a class of students is taught."""
    WM_ID = "wmoop.education/Classroom"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, floorArea=None, seatingCapacity=None):
        super().__init__(id, name, floorArea=floorArea)
        self._seatingCapacity = seatingCapacity
    @property
    def seatingCapacity(self):
        return self._seatingCapacity

class Laboratory(Room):
    """Laboratory — wmoop.education/Laboratory. A room equipped for practical scientific, technical or computing instruction."""
    WM_ID = "wmoop.education/Laboratory"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, floorArea=None, discipline=None):
        super().__init__(id, name, floorArea=floorArea)
        self._discipline = discipline
    @property
    def discipline(self):
        return self._discipline

class CurriculumSubject(Entity):
    """CurriculumSubject — wmoop.education/CurriculumSubject. A branch of knowledge studied and taught as part of a curriculum (e.g. Mathematics, Biology, Music). An abstract entity; the specific subjects are reference individuals at L2."""
    WM_ID = "wmoop.education/CurriculumSubject"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, iscedfField=None):
        super().__init__(id, name)
        self._iscedfField = iscedfField
    @property
    def iscedfField(self):
        return self._iscedfField

class Mark(Entity):
    """Mark — wmoop.education/Mark. A grade awarded to a student for a curriculum subject: a numeric value on a named grading scale, at a point in time. Reified so the (student, subject, value, date) fact is a first-class object [meta-model §10 Q5]."""
    WM_ID = "wmoop.education/Mark"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, value=None, scale=None, awardedOn=None):
        super().__init__(id, name)
        self._value = value
        self._scale = scale
        self._awardedOn = awardedOn
    @property
    def value(self):
        return self._value
    @property
    def scale(self):
        return self._scale
    @property
    def awardedOn(self):
        return self._awardedOn

class StudentClass(Entity):
    """StudentClass — wmoop.education/StudentClass. A cohort of students taught together as a unit (a 'class' or 'form'). A Collection: a many-as-one with its own identity, label and tutor."""
    WM_ID = "wmoop.education/StudentClass"
    WM_KIND = "concrete"
    def __init__(self, id, name, *, label=None, studyYear=None):
        super().__init__(id, name)
        self._label = label
        self._studyYear = studyYear
    @property
    def label(self):
        return self._label
    @property
    def studyYear(self):
        return self._studyYear

class Student(Role):
    """Student role — wmoop.education/Student. The role of a person enrolled at an educational institution to follow a programme of study."""
    WM_ID = "wmoop.education/Student"
    WM_PLAYED_BY = "wmoop.nature/Person"
    def __init__(self, *, enrolmentId=None, studyYear=None):
        super().__init__()
        self._enrolmentId = enrolmentId
        self._studyYear = studyYear
    @property
    def role_type(self):
        return ConceptId(self.WM_ID)
    @property
    def enrolmentId(self):
        return self._enrolmentId
    @property
    def studyYear(self):
        return self._studyYear

class Teacher(Role):
    """Teacher role — wmoop.education/Teacher. The role of a person who instructs students in one or more curriculum subjects."""
    WM_ID = "wmoop.education/Teacher"
    WM_PLAYED_BY = "wmoop.nature/Person"
    def __init__(self, *, staffId=None):
        super().__init__()
        self._staffId = staffId
    @property
    def role_type(self):
        return ConceptId(self.WM_ID)
    @property
    def staffId(self):
        return self._staffId

class FormTutor(Role):
    """FormTutor role — wmoop.education/FormTutor. The role of a teacher additionally responsible for the pastoral oversight and administration of one specific class/form. Known in Romanian as 'diriginte' (English: form tutor / homeroom teacher)."""
    WM_ID = "wmoop.education/FormTutor"
    WM_PLAYED_BY = "wmoop.nature/Person"
    def __init__(self):
        super().__init__()
    @property
    def role_type(self):
        return ConceptId(self.WM_ID)

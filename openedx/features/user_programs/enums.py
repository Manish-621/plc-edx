from enum import Enum

class ProgramPaceChoice(Enum):
    Self = "SELF"
    Instructor = "INSTRUCTOR"

class EntityGroupChoice(Enum):
    Program = "PROGRAM"
    Project = "PROJECT"
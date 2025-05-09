from enum import Enum
from typing import List

from models.Exercise import ExerciseType
from pydantic import BaseModel

from .option import OptionCreate, OptionOut


class ExerciseBase(BaseModel):
    title: str
    ex_type: ExerciseType
    exercise_text: str
    created_by: str
    lesson_id: int


class ExerciseCreate(ExerciseBase):
    options: List[OptionCreate]


class ExerciseOut(ExerciseBase):
    id: int
    options: List[OptionOut]

    class Config:
        orm_mode = True


class ExerciseTypeListOut(BaseModel):
    types: List[str]

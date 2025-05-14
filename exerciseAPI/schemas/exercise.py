from typing import List

from models.Exercise import ExerciseType
from pydantic import BaseModel

from .option import OptionCreate, OptionSafeOut


class ExerciseBase(BaseModel):
    title: str
    ex_type: ExerciseType
    exercise_text: str
    created_by: str
    lesson_id: int


class ExerciseCreate(ExerciseBase):
    options: List[OptionCreate]


class ExerciseListOut(BaseModel):
    id: int
    title: str
    ex_type: ExerciseType
    exercise_text: str
    lesson_name: int
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": ".....",
                    "ex_type": "MULTIPLE_CHOICE",
                    "exercise_text": ".....",
                    "lesson_name": ".....",
                }
            ],
        },
    }


class ExerciseDetailOut(BaseModel):
    id: int
    title: str
    ex_type: ExerciseType
    exercise_text: str
    lesson_name: str
    options: List[OptionSafeOut]

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 12,
                    "title": "...",
                    "ex_type": "...",
                    "exercise_text": "...",
                    "lesson_name": "...",
                    "options": [
                        {"id": 1, "text": "..."},
                        {"id": 2, "text": "..."},
                        {"id": 3, "text": "..."},
                    ],
                }
            ],
        },
    }

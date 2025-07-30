from typing import List, Optional

from pydantic import BaseModel

from exerciseAPI.models.Exercise import ExerciseType
from exerciseAPI.schemas.lesson import LessonExerciseOut

from .option import OptionCreate, OptionExerciseOut, OptionUpdate


class ExerciseBase(BaseModel):
    title: str
    ex_type: ExerciseType
    exercise_text: str
    created_by: str
    lesson_id: int


class ExerciseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[ExerciseType] = None
    difficulty_level: Optional[str] = None
    topic_id: Optional[int] = None
    options: Optional[List[OptionUpdate]] = None


class ExerciseCreate(ExerciseBase):
    options: List[OptionCreate]


class ExerciseOut(BaseModel):
    id: int
    title: str
    ex_type: ExerciseType
    exercise_text: str

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
    created_by: str
    lesson: LessonExerciseOut

    options: List[OptionExerciseOut]

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 12,
                    "title": "...",
                    "ex_type": "...",
                    "exercise_text": "...",
                    "lesson": {
                        "id": 1,
                        "title": "Solving linear equations",
                        "topic": {
                            "id": 1,
                            "title": "linear equations",
                            "course": {
                                "id": 1,
                                "title": "Precalculus",
                                "description": "Curso de precálculo",
                                "image_url": "http://example.com/image.jpg",
                            },
                        },
                    },
                    "options": [
                        {"id": 1, "text": "..."},
                        {"id": 2, "text": "..."},
                        {"id": 3, "text": "..."},
                    ],
                }
            ],
        },
    }

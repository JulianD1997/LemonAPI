from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, computed_field

from exerciseAPI.models.Exercise import ExerciseType
from exerciseAPI.schemas.topic import TopicOut

from .option import OptionCreate, OptionSafeOut


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


class ExerciseCreate(ExerciseBase):
    options: List[OptionCreate]


class ExerciseListOut(BaseModel):
    id: int
    title: str
    ex_type: ExerciseType
    exercise_text: str

    @computed_field
    @property
    def lesson_name(self) -> str:
        return self.lesson.name

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

    @computed_field
    @property
    def lesson_name(self) -> str:
        return self.lesson.name

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


class ExerciseOut(BaseModel):
    id: int
    title: str
    description: str
    type: ExerciseType
    difficulty_level: str
    updated_at: datetime
    created_at: datetime
    topic: TopicOut

    class Config:
        from_attributes = True

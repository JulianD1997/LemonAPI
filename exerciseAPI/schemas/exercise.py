import json
from typing import List, Optional

from pydantic import BaseModel, computed_field

from exerciseAPI.models.Exercise import ExerciseType, MathType
from exerciseAPI.schemas.lesson import LessonExerciseOut

from .option import OptionCreate, OptionExerciseOut, OptionUpdate


class ExerciseBase(BaseModel):
    title: str
    ex_type: ExerciseType
    exercise_text: Optional[str] = None
    initial_expression: Optional[str] = None
    expected_solution: Optional[str] = None
    math_type: Optional[MathType] = None
    created_by: str
    lesson_id: int


class ExerciseUpdate(BaseModel):
    title: Optional[str] = None
    ex_type: Optional[ExerciseType] = None
    exercise_text: Optional[str] = None
    initial_expression: Optional[str] = None
    expected_solution: Optional[str] = None
    math_type: Optional[MathType] = None
    lesson_id: Optional[int] = None
    options: Optional[List[OptionUpdate]] = None


class ExerciseCreate(ExerciseBase):
    options: List[OptionCreate] = []
    interactive_code: Optional[str] = None


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
    exercise_text: Optional[str]
    created_by: str
    lesson: LessonExerciseOut
    options: List[OptionExerciseOut]

    @computed_field(return_type=Optional[str])
    @property
    def interactive_code(self) -> Optional[str]:
        """
        Genera el campo 'interactive_code' dinámicamente si el tipo de
        ejercicio es 'interactive_function'.
        """
        if self.ex_type == ExerciseType.interactive_function:
            try:
                elements = [json.loads(opt.text) for opt in self.options]
                view_box = {"x": [-10, 10], "y": [-10, 10]}
                return json.dumps({"elements": elements, "viewBox": view_box})
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def model_dump(self, *args, **kwargs):
        """
        Sobrescribe la serialización para excluir campos dinámicamente.
        FastAPI usará este método para generar la respuesta JSON.
        """
        if self.ex_type == ExerciseType.interactive_function:
            # Añade 'options' al set de exclusión si no está ya presente
            kwargs["exclude"] = kwargs.get("exclude", set()) | {"options"}

        return super().model_dump(*args, **kwargs)

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

from typing import Optional

from pydantic import BaseModel


class OptionBase(BaseModel):
    text: str
    is_correct: bool


class OptionCreate(OptionBase):
    pass


class OptionUpdate(BaseModel):
    id: Optional[int] = None
    text: Optional[str] = None
    is_correct: Optional[bool] = None


class OptionOut(OptionBase):
    id: int

    class Config:
        from_attributes = True


class OptionSafeOut(BaseModel):
    id: int
    text: str

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "text": ".....",
                }
            ],
        },
    }


class OptionExerciseOut(BaseModel):
    id: int
    text: str
    is_correct: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": 1,
                    "text": ".....",
                    "is_correct": True,
                }
            ],
        }

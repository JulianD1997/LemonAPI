from pydantic import BaseModel


class OptionBase(BaseModel):
    text: str
    is_correct: bool


class OptionCreate(OptionBase):
    pass


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

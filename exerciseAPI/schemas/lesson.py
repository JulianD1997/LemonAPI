from pydantic import BaseModel, computed_field


class LessonBase(BaseModel):
    name: str
    topic_id: int


class LessonCreate(LessonBase):
    pass


class LessonUpdate(LessonBase):
    pass


class LessonOut(BaseModel):
    id: int
    name: str

    @computed_field
    @property
    def topic_name(self) -> str:
        return self.topic.name

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "Solving linear equations",
                    "topic_name": "Linear equations",
                }
            ],
        },
    }

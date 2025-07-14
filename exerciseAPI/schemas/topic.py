from pydantic import BaseModel, computed_field


class TopicBase(BaseModel):
    name: str
    course_id: int


class TopicCreate(TopicBase):
    pass


class TopicUpdate(TopicBase):
    pass


class TopicOut(BaseModel):
    id: int
    name: str

    @computed_field
    @property
    def course_name(self) -> str:
        return self.course.name

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "course_name": "Precalculus",
                    "name": "linear equations",
                }
            ],
        },
    }

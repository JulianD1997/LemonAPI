from pydantic import BaseModel


class TopicBase(BaseModel):
    name: str
    course_id: int


class TopicCreate(TopicBase):
    pass


class TopicUpdate(TopicBase):
    pass


class TopicOut(BaseModel):
    id: int
    course_name: str
    name: str
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "course_name": "precalculus",
                    "name": "linear equations",
                }
            ],
        },
    }

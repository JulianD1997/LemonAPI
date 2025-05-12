from pydantic import BaseModel


class LessonBase(BaseModel):
    name: str
    topic_id: int


class LessonCreate(LessonBase):
    pass


class LessonUpdate(LessonBase):
    pass


class LessonOut(LessonBase):
    id: int

    class Config:
        from_attributes = True

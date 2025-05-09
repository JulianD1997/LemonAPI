from pydantic import BaseModel


class TopicBase(BaseModel):
    name: str
    course_id: int


class TopicCreate(TopicBase):
    pass


class TopicUpdate(TopicBase):
    pass


class TopicOut(TopicBase):
    id: int

    class Config:
        orm_mode = True

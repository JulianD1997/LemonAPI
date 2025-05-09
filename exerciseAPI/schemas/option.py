from pydantic import BaseModel


class OptionBase(BaseModel):
    text: str
    is_correct: bool


class OptionCreate(OptionBase):
    pass


class OptionOut(OptionBase):
    id: int

    class Config:
        orm_mode = True

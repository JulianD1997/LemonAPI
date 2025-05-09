from enum import Enum

from database.config import Base
from sqlalchemy import Boolean, Column
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class ExerciseType(str, Enum):
    multiple_choice = "multiple_choice"
    true_false = "true_false"
    unique_answer = "unique_answer"


class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True, index=True)
    ex_type = Column(SQLAlchemyEnum(ExerciseType), nullable=False)
    title = Column(String, nullable=False, index=True)
    exercise_text = Column(Text)
    created_by = Column(String, nullable=False)
    lesson_id = Column(
        Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False
    )
    lesson = relationship("Lesson", back_populates="exercises")
    options = relationship(
        "Option", back_populates="exercise", cascade="all, delete-orphan"
    )


class Option(Base):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)
    exercise_id = Column(
        Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False
    )
    exercise = relationship("Exercise", back_populates="options")

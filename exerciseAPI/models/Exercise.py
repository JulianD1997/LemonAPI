from enum import Enum

from sqlalchemy import Boolean, Column
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from exerciseAPI.core.database import Base


class ExerciseType(str, Enum):
    multiple_choice = "multiple_choice"
    true_false = "true_false"
    unique_answer = "unique_answer"
    interactive_function = "interactive_function"


class MathType(str, Enum):
    SOLVE = "SOLVE"
    REDUCE = "REDUCE"
    DERIVE = "DERIVE"


class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ex_type = Column(SQLAlchemyEnum(ExerciseType), nullable=False)
    title = Column(String, nullable=False, index=True)
    exercise_text = Column(Text)
    initial_expression = Column(String, nullable=True)
    expected_solution = Column(String, nullable=True)
    math_type = Column(SQLAlchemyEnum(MathType), nullable=True)
    created_by = Column(String, nullable=False)
    lesson_id = Column(
        Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False
    )
    lesson = relationship("Lesson", back_populates="exercises", lazy="selectin")
    options = relationship(
        "Option",
        back_populates="exercise",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    module = relationship(
        "Module",
        secondary="module_exercise",
        back_populates="exercises",
        lazy="selectin",
    )

    def __repr__(self):
        return f"<Exercise(id={self.id}, title='{self.title}', type='{self.ex_type}')>"


class Option(Base):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)
    exercise_id = Column(
        Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False
    )
    exercise = relationship("Exercise", back_populates="options", lazy="selectin")

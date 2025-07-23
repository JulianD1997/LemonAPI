from nanoid import generate
from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from exerciseAPI.core.database import Base

module_exercise = Table(
    "module_exercise",
    Base.metadata,
    Column(
        "module_id",
        String(10),
        ForeignKey("modules.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "exercise_id",
        Integer,
        ForeignKey("exercises.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


def generate_nanoid():
    return generate(size=10)


class Module(Base):
    __tablename__ = "modules"
    id = Column(String(10), primary_key=True, default=generate_nanoid, unique=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    course_id = Column(
        Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )

    course = relationship("Course", back_populates="modules", lazy="selectin")
    exercises = relationship(
        "Exercise",
        secondary="module_exercise",
        back_populates="module",
        lazy="selectin",
    )

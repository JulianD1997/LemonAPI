from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from exerciseAPI.settings.database.config import Base


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    topic_id = Column(
        Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    topic = relationship("Topic", back_populates="lessons")
    exercises = relationship(
        "Exercise", back_populates="lesson", cascade="all, delete-orphan"
    )

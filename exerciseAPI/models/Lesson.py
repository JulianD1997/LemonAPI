from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from exerciseAPI.core.database import Base


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    topic_id = Column(
        Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    topic = relationship("Topic", back_populates="lessons", lazy="select")
    exercises = relationship(
        "Exercise",
        back_populates="lesson",
        cascade="all, delete-orphan",
        lazy="select",
    )

    def __repr__(self):
        return f"<Lesson(id={self.id}, title='{self.title}')>"

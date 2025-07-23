from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from exerciseAPI.core.database import Base


class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    course_id = Column(
        Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    course = relationship("Course", back_populates="topics", lazy="select")
    lessons = relationship(
        "Lesson", back_populates="topic", cascade="all, delete-orphan", lazy="select"
    )

    def __repr__(self):
        return f"<Topic(id={self.id}, title='{self.title}')>"

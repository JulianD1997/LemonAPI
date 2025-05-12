from settings.database.config import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    course_id = Column(
        Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    course = relationship("Course", back_populates="topics")
    lessons = relationship(
        "Lesson", back_populates="topic", cascade="all, delete-orphan"
    )

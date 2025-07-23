from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from exerciseAPI.core.database import Base


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    topics = relationship(
        "Topic", back_populates="course", cascade="all, delete-orphan", lazy="select"
    )
    modules = relationship(
        "Module", back_populates="course", cascade="all, delete-orphan", lazy="select"
    )

    def __repr__(self) -> str:

        return f"<Course(id={self.id}, title='{self.title}')>"

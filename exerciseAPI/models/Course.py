from settings.database.config import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    topics = relationship(
        "Topic", back_populates="course", cascade="all, delete-orphan"
    )

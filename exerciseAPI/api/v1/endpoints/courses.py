from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from exerciseAPI.models import Course
from exerciseAPI.schemas.course import CourseCreate
from exerciseAPI.schemas.response import ResponseBase
from exerciseAPI.settings.database.config import get_db

router = APIRouter()


@router.post(
    "/", response_model=ResponseBase[None], status_code=status.HTTP_201_CREATED
)
async def create_course(course_create: CourseCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo curso.
    """
    new_course = Course(name=course_create.name)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return ResponseBase(
        status_code=status.HTTP_201_CREATED,
        message="Curso creado con éxito",
        success=True,
    )

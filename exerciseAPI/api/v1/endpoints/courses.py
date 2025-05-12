from fastapi import APIRouter, Depends, status
from models import Course
from schemas.course import CourseCreate, CourseOut, CourseUpdate
from schemas.response import ResponseBase, common_response
from settings.database.config import get_db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/",
    response_model=ResponseBase,
    status_code=status.HTTP_201_CREATED,
    responses={201: common_response[201], 500: common_response[500]},
)
async def create_course(course_create: CourseCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo curso.
    """
    try:
        new_course = Course(course_create.model_dump())
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        return ResponseBase(
            status_code=status.HTTP_201_CREATED,
            message="Curso creado con éxito",
            success=True,
        )
    except SQLAlchemyError:
        db.rollback()
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error al crear el curso",
            success=False,
        )


@router.get(
    "/",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    responses={200: common_response[200], 500: common_response[500]},
)
async def get_courses(db: Session = Depends(get_db)):
    """
    Obtiene todos los cursos.
    """
    try:
        orm_courses = db.query(Course).all()
        courses = [
            CourseOut.model_validate(course, from_attributes=True)
            for course in orm_courses
        ]
        return ResponseBase(
            status_code=status.HTTP_200_OK,
            message="Cursos obtenidos con éxito",
            success=True,
            results=courses,
        )
    except SQLAlchemyError:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error al obtener los cursos",
            success=False,
        )


@router.get(
    "/{course_id}",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    responses={
        200: common_response[200],
        404: common_response[400],
        500: common_response[500],
    },
)
async def get_course(course_id: int, db: Session = Depends(get_db)):
    """
    Obtiene todos los cursos.
    """
    try:
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            return ResponseBase(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Curso no encontrado",
                success=False,
            )
        course = CourseOut.model_validate(course, from_attributes=True)
        return ResponseBase(
            status_code=status.HTTP_200_OK,
            message="Curso obtenido con éxito",
            success=True,
            results=[course],
        )
    except SQLAlchemyError:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error al obtener el curso",
            success=False,
        )


@router.put(
    "/{course_id}",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    responses={
        200: common_response[200],
        404: common_response[400],
        500: common_response[500],
    },
)
async def update_course(
    course_id: int, course_update: CourseUpdate, db: Session = Depends(get_db)
):
    """
    Obtiene todos los cursos.
    """
    try:
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            return ResponseBase(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Curso no encontrado",
                success=False,
            )

        course.name = course_update.name
        db.commit()
        db.refresh(course)
        return ResponseBase(
            status_code=status.HTTP_200_OK,
            message="Curso actualizado con éxito",
            success=True,
        )
    except SQLAlchemyError:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error al actualizar el curso",
            success=False,
        )


@router.delete(
    "/{course_id}",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    responses={
        200: common_response[200],
        404: common_response[400],
        500: common_response[500],
    },
)
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    """
    Obtiene todos los cursos.
    """
    try:
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            return ResponseBase(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Curso no encontrado",
                success=False,
            )
        db.delete(course)
        db.commit()
        db.refresh(course)
        return ResponseBase(
            status_code=status.HTTP_200_OK,
            message="Curso actualizado con éxito",
            success=True,
        )
    except SQLAlchemyError:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error al actualizar el curso",
            success=False,
        )

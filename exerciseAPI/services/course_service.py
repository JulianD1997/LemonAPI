from exerciseAPI.models import Course
from exerciseAPI.schemas.course import CourseCreate, CourseUpdate

from .base_service import BaseService


class CourseService(BaseService[Course, CourseCreate, CourseUpdate]):
    pass


course_service = CourseService(Course)

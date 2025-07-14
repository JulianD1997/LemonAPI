"""seed initial data for courses, topics, and lessons

Revision ID: 53100ba9aaa2
Revises: 5748487180d8
Create Date: 2025-07-14 12:06:43.781029

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "53100ba9aaa2"
down_revision: Union[str, None] = "5748487180d8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Inserta los datos iniciales para las tablas courses, topics y lessons.
    """
    # Define una representación temporal de las tablas para poder insertar datos.
    # Esto evita tener que importar los modelos, lo que es una buena práctica en migraciones.
    courses_table = sa.table(
        "courses", sa.column("id", sa.Integer), sa.column("name", sa.String)
    )
    op.bulk_insert(
        courses_table,
        [
            {"id": 1, "name": "precalculus"},
            {"id": 2, "name": "diferential calculus"},
            {"id": 3, "name": "linear algebra"},
            {"id": 4, "name": "vector calculus"},
        ],
    )

    topics_table = sa.table(
        "topics",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
        sa.column("course_id", sa.Integer),
    )
    op.bulk_insert(
        topics_table,
        [
            {"id": 1, "name": "linear equations", "course_id": 1},
            {"id": 2, "name": "inequatilies", "course_id": 1},
            {"id": 3, "name": "derivates", "course_id": 2},
            {"id": 4, "name": "operations with vectors", "course_id": 3},
            {"id": 5, "name": "equation of the line", "course_id": 1},
        ],
    )

    lessons_table = sa.table(
        "lessons",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
        sa.column("topic_id", sa.Integer),
    )
    op.bulk_insert(
        lessons_table,
        [
            {"id": 1, "name": "solving linear equations", "topic_id": 1},
            {"id": 2, "name": "solving linear inequalities", "topic_id": 2},
            {"id": 3, "name": "deriving exponential functions", "topic_id": 3},
            {"id": 4, "name": "reducing operations between vectors", "topic_id": 4},
            {"id": 5, "name": "finding the equation given two points", "topic_id": 5},
        ],
    )
    # No se insertan datos en exercises y options ya que estaban vacíos en el backup.


def downgrade() -> None:
    """
    Elimina los datos insertados. El orden es inverso al de inserción para
    respetar las claves foráneas (foreign keys).
    """
    op.execute("DELETE FROM lessons;")
    op.execute("DELETE FROM topics;")
    op.execute("DELETE FROM courses;")

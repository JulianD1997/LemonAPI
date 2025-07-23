"""update atributes models

Revision ID: 9ec44b047d06
Revises: 0261573e1d6d
Create Date: 2025-07-21 14:05:41.351005

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9ec44b047d06"
down_revision: Union[str, None] = "0261573e1d6d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### Comandos ajustados manualmente para renombrar columnas ###

    # --- Tabla: courses ---
    op.alter_column("courses", "name", new_column_name="title")
    op.add_column("courses", sa.Column("description", sa.String(), nullable=True))
    op.add_column("courses", sa.Column("image_url", sa.String(), nullable=True))
    op.drop_index("ix_courses_name", table_name="courses")
    op.create_index(op.f("ix_courses_title"), "courses", ["title"], unique=False)

    # --- Tabla: lessons ---
    op.alter_column("lessons", "name", new_column_name="title")
    op.add_column("lessons", sa.Column("description", sa.String(), nullable=True))
    op.drop_index("ix_lessons_name", table_name="lessons")
    op.create_index(op.f("ix_lessons_title"), "lessons", ["title"], unique=False)

    # --- Tabla: topics ---
    op.alter_column("topics", "name", new_column_name="title")
    op.add_column("topics", sa.Column("description", sa.String(), nullable=True))
    op.drop_index("ix_topics_name", table_name="topics")
    op.create_index(op.f("ix_topics_title"), "topics", ["title"], unique=False)
    # ### Fin de los comandos ajustados ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### Comandos ajustados manualmente para revertir el renombrado ###

    # --- Tabla: topics ---
    op.alter_column("topics", "title", new_column_name="name")
    op.drop_column("topics", "description")
    op.drop_index(op.f("ix_topics_title"), table_name="topics")
    op.create_index("ix_topics_name", "topics", ["name"], unique=False)

    # --- Tabla: lessons ---
    op.alter_column("lessons", "title", new_column_name="name")
    op.drop_column("lessons", "description")
    op.drop_index(op.f("ix_lessons_title"), table_name="lessons")
    op.create_index("ix_lessons_name", "lessons", ["name"], unique=False)

    # --- Tabla: courses ---
    op.alter_column("courses", "title", new_column_name="name")
    op.drop_column("courses", "description")
    op.drop_column("courses", "image_url")
    op.drop_index(op.f("ix_courses_title"), table_name="courses")
    op.create_index("ix_courses_name", "courses", ["name"], unique=False)
    # ### Fin de los comandos ajustados ###

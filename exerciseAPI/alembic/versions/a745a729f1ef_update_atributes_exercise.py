"""update atributes exercise

Revision ID: a745a729f1ef
Revises: 9ec44b047d06
Create Date: 2025-07-30 14:26:34.969755

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a745a729f1ef"
down_revision: Union[str, None] = "9ec44b047d06"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


math_type_enum = sa.Enum("SOLVE", "REDUCE", "DERIVE", name="mathtype")


def upgrade() -> None:
    """Upgrade schema."""
    math_type_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "exercises", sa.Column("initial_expression", sa.String(), nullable=True)
    )
    op.add_column(
        "exercises", sa.Column("expected_solution", sa.String(), nullable=True)
    )

    op.add_column("exercises", sa.Column("math_type", math_type_enum, nullable=True))


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("exercises", "math_type")
    op.drop_column("exercises", "expected_solution")
    op.drop_column("exercises", "initial_expression")

    math_type_enum.drop(op.get_bind(), checkfirst=True)

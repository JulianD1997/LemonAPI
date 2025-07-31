"""add_interactive_function_to_exercisetype

Revision ID: 642e9e120a75
Revises: a745a729f1ef
Create Date: 2025-07-30 14:39:14.845386

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "642e9e120a75"
down_revision: Union[str, None] = "a745a729f1ef"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE exercisetype ADD VALUE 'interactive_function'")


def downgrade() -> None:
    """Downgrade schema."""
    pass

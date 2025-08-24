"""Add transactions model

Revision ID: 7647a207d9d1
Revises: 14b8a8cb8cee
Create Date: 2025-08-24 23:17:26.155350

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7647a207d9d1'
down_revision: Union[str, Sequence[str], None] = '14b8a8cb8cee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

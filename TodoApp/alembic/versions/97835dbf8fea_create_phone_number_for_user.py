"""create phone number for user

Revision ID: 97835dbf8fea
Revises: 
Create Date: 2026-04-12 22:01:46.559734

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97835dbf8fea'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('user', sa.Column('phone_number', sa.String, nullable=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('user', 'phone_number')
    pass

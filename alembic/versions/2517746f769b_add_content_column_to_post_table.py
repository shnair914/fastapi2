"""add content column to post table

Revision ID: 2517746f769b
Revises: 6856a24de1b6
Create Date: 2025-08-06 12:22:20.333091

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2517746f769b'
down_revision: Union[str, Sequence[str], None] = '6856a24de1b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass

"""fix table aticle

Revision ID: dc97bb01aaf5
Revises: a13c3a72dfd4
Create Date: 2025-01-08 15:24:22.922130

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'dc97bb01aaf5'
down_revision: Union[str, None] = 'a13c3a72dfd4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('articles', 'image',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('articles', 'image',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###

"""fix: team_id and assignee_id in tasks have been edited to nullable=True

Revision ID: 3c0a9e728c88
Revises: 8d0b1d3099d2
Create Date: 2025-05-23 09:31:26.375051

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '3c0a9e728c88'
down_revision: Union[str, None] = '8d0b1d3099d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tasks', 'team_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('tasks', 'assignee_id',
               existing_type=sa.UUID(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tasks', 'assignee_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('tasks', 'team_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###

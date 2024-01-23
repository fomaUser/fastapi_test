"""Initial migration

Revision ID: 0a61187b37e0
Revises: 197389f7d452
Create Date: 2024-01-23 16:09:25.044149

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a61187b37e0'
down_revision: Union[str, None] = '197389f7d452'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    op.add_column('posts', sa.Column('rating', sa.Integer(), nullable=True))
    op.add_column('posts', sa.Column('rating_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'rating_id')
    op.drop_column('posts', 'rating')
    op.create_table('votes',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('rating', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='votes_post_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='votes_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='votes_pkey')
    )
    # ### end Alembic commands ###
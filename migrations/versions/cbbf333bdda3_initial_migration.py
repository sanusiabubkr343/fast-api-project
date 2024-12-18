"""Initial migration

Revision ID: cbbf333bdda3
Revises: 
Create Date: 2024-12-18 21:56:13.013039

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cbbf333bdda3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vote')
    op.drop_table('comment')
    op.drop_table('post')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=50), nullable=False),
    sa.Column('hashed_password', sa.VARCHAR(length=128), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=100), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('author_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('author_id', sa.INTEGER(), nullable=False),
    sa.Column('post_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vote',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('post_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
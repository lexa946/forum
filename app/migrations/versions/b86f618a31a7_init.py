"""Init

Revision ID: b86f618a31a7
Revises: 
Create Date: 2024-10-03 15:38:26.671682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b86f618a31a7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nick', sa.String(length=15), nullable=True),
    sa.Column('text', sa.String(length=1500), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('thread_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)
    op.create_index(op.f('ix_comments_thread_id'), 'comments', ['thread_id'], unique=False)
    op.create_table('threads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=150), nullable=False),
    sa.Column('text', sa.String(length=1500), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('nick', sa.String(length=15), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_threads_id'), 'threads', ['id'], unique=False)
    op.create_table('comments_media',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=150), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_media_comment_id'), 'comments_media', ['comment_id'], unique=False)
    op.create_index(op.f('ix_comments_media_id'), 'comments_media', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comments_media_id'), table_name='comments_media')
    op.drop_index(op.f('ix_comments_media_comment_id'), table_name='comments_media')
    op.drop_table('comments_media')
    op.drop_index(op.f('ix_threads_id'), table_name='threads')
    op.drop_table('threads')
    op.drop_index(op.f('ix_comments_thread_id'), table_name='comments')
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_table('comments')
    # ### end Alembic commands ###

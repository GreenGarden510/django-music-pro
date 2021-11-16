"""empty message

Revision ID: c20fe272efb2
Revises: cbfeefcd27f9
Create Date: 2021-07-15 17:11:57.248443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c20fe272efb2'
down_revision = 'cbfeefcd27f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('caption', sa.String(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('featured_image_url', sa.String(), nullable=True),
    sa.Column('featured_video_url', sa.String(), nullable=True),
    sa.Column('featured_audio_url', sa.String(), nullable=True),
    sa.Column('images', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('videos', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('post_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    # ### end Alembic commands ###

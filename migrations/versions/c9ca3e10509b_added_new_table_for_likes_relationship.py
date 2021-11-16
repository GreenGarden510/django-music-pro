"""=Added new table for likes relationship

Revision ID: c9ca3e10509b
Revises: aa891caec256
Create Date: 2021-06-01 18:16:16.133218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9ca3e10509b'
down_revision = 'aa891caec256'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('media_user_likes',
    sa.Column('media_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['media_id'], ['media.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('media_user_likes')
    # ### end Alembic commands ###
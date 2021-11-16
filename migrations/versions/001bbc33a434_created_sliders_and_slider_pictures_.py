"""Created sliders and slider pictures tables

Revision ID: 001bbc33a434
Revises: 52c28508acf0
Create Date: 2021-04-12 23:26:52.354851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001bbc33a434'
down_revision = '52c28508acf0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sliders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slider_id', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slider_id')
    )
    op.create_table('slider_pictures',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slider_id', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('alt', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['slider_id'], ['sliders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('slider_pictures')
    op.drop_table('sliders')
    # ### end Alembic commands ###

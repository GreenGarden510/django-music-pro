"""empty message

Revision ID: 1fec908d141f
Revises: 19c2e63baa4c
Create Date: 2021-04-20 16:18:49.752474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fec908d141f'
down_revision = '19c2e63baa4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'slider_items', 'sliders', ['slider_id'], ['slider_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'slider_items', type_='foreignkey')
    # ### end Alembic commands ###

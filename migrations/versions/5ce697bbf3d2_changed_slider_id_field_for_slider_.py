"""=Changed slider_id field for slider_items to string instead of int

Revision ID: 5ce697bbf3d2
Revises: 3e07b8561bde
Create Date: 2021-04-20 14:26:42.123374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ce697bbf3d2'
down_revision = '3e07b8561bde'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('slider_items_slider_id_fkey', 'slider_items', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('slider_items_slider_id_fkey', 'slider_items', 'sliders', ['slider_id'], ['id'])
    # ### end Alembic commands ###

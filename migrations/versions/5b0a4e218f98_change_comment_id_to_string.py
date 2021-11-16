"""change comment_id to string

Revision ID: 5b0a4e218f98
Revises: f2e03ba79fb2
Create Date: 2021-01-18 07:24:37.201668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b0a4e218f98'
down_revision = 'f2e03ba79fb2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comments', 'comment_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=50),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comments', 'comment_id',
               existing_type=sa.String(length=50),
               type_=sa.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
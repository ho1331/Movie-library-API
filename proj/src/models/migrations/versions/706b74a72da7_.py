"""empty message

Revision ID: 706b74a72da7
Revises: 70cf715fdf15
Create Date: 2021-07-16 12:17:36.295028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '706b74a72da7'
down_revision = '70cf715fdf15'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('films', sa.Column('is_admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('films', 'is_admin')
    # ### end Alembic commands ###
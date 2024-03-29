"""Add column date_joined to User model

Revision ID: 25458c30563c
Revises: 99f185d58885
Create Date: 2022-08-31 15:25:32.461172

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25458c30563c'
down_revision = '99f185d58885'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('date_joined', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'date_joined')
    # ### end Alembic commands ###

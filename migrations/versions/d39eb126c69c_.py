"""empty message

Revision ID: d39eb126c69c
Revises: 300bb23ead54
Create Date: 2024-09-13 22:15:47.166207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd39eb126c69c'
down_revision = '300bb23ead54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite__planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite__planet', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
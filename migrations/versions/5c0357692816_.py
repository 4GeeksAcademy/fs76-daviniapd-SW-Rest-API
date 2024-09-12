"""empty message

Revision ID: 5c0357692816
Revises: b6d1c522af7f
Create Date: 2024-09-11 19:09:20.706520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c0357692816'
down_revision = 'b6d1c522af7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('firstname', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('lastname', sa.String(length=120), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('lastname')
        batch_op.drop_column('firstname')

    # ### end Alembic commands ###
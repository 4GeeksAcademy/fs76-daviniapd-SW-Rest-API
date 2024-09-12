"""empty message

Revision ID: 61e12a2e6cae
Revises: 131b9d01fc2c
Create Date: 2024-09-12 12:34:17.854149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61e12a2e6cae'
down_revision = '131b9d01fc2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('users_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'users', ['users_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('users_id')

    # ### end Alembic commands ###
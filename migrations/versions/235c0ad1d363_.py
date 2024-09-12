"""empty message

Revision ID: 235c0ad1d363
Revises: 2148d33427c3
Create Date: 2024-09-12 11:38:06.091678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '235c0ad1d363'
down_revision = '2148d33427c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.drop_constraint('planet_judge_key', type_='unique')
        batch_op.drop_column('judge')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('judge', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
        batch_op.create_unique_constraint('planet_judge_key', ['judge'])

    # ### end Alembic commands ###
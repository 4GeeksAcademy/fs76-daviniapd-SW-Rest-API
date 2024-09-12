"""empty message

Revision ID: 8190c08ac531
Revises: 235c0ad1d363
Create Date: 2024-09-12 11:43:58.077218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8190c08ac531'
down_revision = '235c0ad1d363'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('specie', sa.String(length=120), nullable=True),
    sa.Column('role', sa.String(length=120), nullable=True),
    sa.Column('life_status', sa.String(length=120), nullable=True),
    sa.Column('gender', sa.String(length=120), nullable=True),
    sa.Column('homeworld_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['homeworld_id'], ['planet.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('gender'),
    sa.UniqueConstraint('life_status'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('role'),
    sa.UniqueConstraint('specie')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('character')
    # ### end Alembic commands ###
"""empty message

Revision ID: c0f55893999b
Revises: 61e12a2e6cae
Create Date: 2024-09-13 19:19:44.042826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0f55893999b'
down_revision = '61e12a2e6cae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite__planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=True),
    sa.Column('planets_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['planets_id'], ['planets.id'], ),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('favorites')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorites',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('planets_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('characters_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('vehicles_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('users_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['characters_id'], ['characters.id'], name='favorites_characters_id_fkey'),
    sa.ForeignKeyConstraint(['planets_id'], ['planets.id'], name='favorites_planets_id_fkey'),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], name='favorites_users_id_fkey'),
    sa.ForeignKeyConstraint(['vehicles_id'], ['vehicles.id'], name='favorites_vehicles_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='favorites_pkey')
    )
    op.drop_table('favorite__planet')
    # ### end Alembic commands ###
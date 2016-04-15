"""Add parties references to the 'users' and 'fraternities'

Revision ID: 6451c45cc96d
Revises: e2200226cabc
Create Date: 2016-04-15 19:15:32.280974

"""

# revision identifiers, used by Alembic.
revision = '6451c45cc96d'
down_revision = 'e2200226cabc'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('parties', sa.Column('creator_id', sa.Integer(), nullable=False))
    op.add_column('parties', sa.Column('fraternity_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'parties', 'users', ['creator_id'], ['id'])
    op.create_foreign_key(None, 'parties', 'fraternities', ['fraternity_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'parties', type_='foreignkey')
    op.drop_constraint(None, 'parties', type_='foreignkey')
    op.drop_column('parties', 'fraternity_id')
    op.drop_column('parties', 'creator_id')
    ### end Alembic commands ###

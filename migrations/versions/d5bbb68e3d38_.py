"""Adds 'can_have_parties' boolean to fraternities

Revision ID: d5bbb68e3d38
Revises: efe2394273fe
Create Date: 2016-04-24 12:09:08.506736

"""

# revision identifiers, used by Alembic.
revision = 'd5bbb68e3d38'
down_revision = 'efe2394273fe'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fraternities', sa.Column('can_have_parties', sa.Boolean()))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('fraternities', 'can_have_parties')
    ### end Alembic commands ###
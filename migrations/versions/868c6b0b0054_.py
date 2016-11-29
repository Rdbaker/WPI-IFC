"""Adds parties.ended column

Revision ID: 868c6b0b0054
Revises: cc3b6c92f663
Create Date: 2016-11-28 20:15:30.248431

"""

# revision identifiers, used by Alembic.
revision = '868c6b0b0054'
down_revision = 'cc3b6c92f663'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('parties', sa.Column('ended', sa.Boolean(), nullable=True))

    op.execute('UPDATE parties SET ended=false;')

    op.alter_column('parties', 'ended',
                    existing_type=sa.BOOLEAN(),
                    nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('parties', 'ended')
    # ### end Alembic commands ###

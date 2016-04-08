"""Created a Fraternity Table

Revision ID: cf49f49a2c66
Revises: 7cc0f8aca352
Create Date: 2016-04-08 12:27:31.622357

"""

# revision identifiers, used by Alembic.
revision = 'cf49f49a2c66'
down_revision = '7cc0f8aca352'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fraternities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.add_column(u'users', sa.Column('fraternity_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'users', 'fraternities', ['fraternity_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column(u'users', 'fraternity_id')
    op.drop_table('fraternities')
    ### end Alembic commands ###
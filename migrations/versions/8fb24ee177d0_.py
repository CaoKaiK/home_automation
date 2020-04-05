"""empty message

Revision ID: 8fb24ee177d0
Revises: c83eebbc93fd
Create Date: 2020-04-03 18:52:31.529173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fb24ee177d0'
down_revision = 'c83eebbc93fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_thing_name', table_name='thing')
    op.create_index(op.f('ix_thing_name'), 'thing', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_thing_name'), table_name='thing')
    op.create_index('ix_thing_name', 'thing', ['name'], unique=1)
    # ### end Alembic commands ###
"""empty message

Revision ID: c83eebbc93fd
Revises: d791b1e6de01
Create Date: 2020-04-02 16:39:28.586097

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c83eebbc93fd'
down_revision = 'd791b1e6de01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('thing', sa.Column('last_switched', sa.DateTime(), nullable=True))
    op.add_column('thing', sa.Column('status', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('thing', 'status')
    op.drop_column('thing', 'last_switched')
    # ### end Alembic commands ###
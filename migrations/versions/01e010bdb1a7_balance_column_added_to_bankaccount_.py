"""balance column added to bankaccount table

Revision ID: 01e010bdb1a7
Revises: 3a3394cbde71
Create Date: 2023-08-18 21:12:33.400541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01e010bdb1a7'
down_revision = '3a3394cbde71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bankaccount', schema=None) as batch_op:
        batch_op.add_column(sa.Column('balance', sa.Float(), server_default=sa.text('(0.0)'), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bankaccount', schema=None) as batch_op:
        batch_op.drop_column('balance')

    # ### end Alembic commands ###

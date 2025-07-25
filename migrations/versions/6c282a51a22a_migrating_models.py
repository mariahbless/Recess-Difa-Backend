"""Migrating models

Revision ID: 6c282a51a22a
Revises: 69a586fd0da3
Create Date: 2025-07-15 10:03:36.206678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c282a51a22a'
down_revision = '69a586fd0da3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('organisations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('message', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('password', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('organisations', schema=None) as batch_op:
        batch_op.drop_column('password')
        batch_op.drop_column('message')

    # ### end Alembic commands ###

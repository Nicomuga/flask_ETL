"""Mensaje de migración

Revision ID: acfd6171dc52
Revises: ea79df2773fd
Create Date: 2024-06-21 14:47:47.932164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acfd6171dc52'
down_revision = 'ea79df2773fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('revision_qa', schema=None) as batch_op:
        batch_op.add_column(sa.Column('file', sa.String(), nullable=False))
        batch_op.drop_column('origen')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('revision_qa', schema=None) as batch_op:
        batch_op.add_column(sa.Column('origen', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.drop_column('file')

    # ### end Alembic commands ###

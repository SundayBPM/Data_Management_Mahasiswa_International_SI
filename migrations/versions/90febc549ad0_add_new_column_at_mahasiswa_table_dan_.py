"""add new column at Mahasiswa Table dan ExchangeOutbound table

Revision ID: 90febc549ad0
Revises: c15a9c01d3d1
Create Date: 2024-11-20 10:06:59.124683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90febc549ad0'
down_revision = 'c15a9c01d3d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exchange_outbound', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sem_at_telu', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('sem_at_exch', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('gpa', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('update_gpa', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('folder', sa.String(), nullable=True))
        batch_op.drop_column('semester_at_telu')

    with op.batch_alter_table('mahasiswa', schema=None) as batch_op:
        batch_op.add_column(sa.Column('gpa', sa.String(), nullable=False))
        batch_op.drop_column('student_folder')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mahasiswa', schema=None) as batch_op:
        batch_op.add_column(sa.Column('student_folder', sa.VARCHAR(), nullable=False))
        batch_op.drop_column('gpa')

    with op.batch_alter_table('exchange_outbound', schema=None) as batch_op:
        batch_op.add_column(sa.Column('semester_at_telu', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('folder')
        batch_op.drop_column('update_gpa')
        batch_op.drop_column('gpa')
        batch_op.drop_column('sem_at_exch')
        batch_op.drop_column('sem_at_telu')

    # ### end Alembic commands ###

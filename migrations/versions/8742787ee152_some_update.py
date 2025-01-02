"""some update

Revision ID: 8742787ee152
Revises: d55265c42672
Create Date: 2025-01-02 11:34:38.012601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8742787ee152'
down_revision = 'd55265c42672'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exchange_outbound', schema=None) as batch_op:
        batch_op.drop_column('folder')
        batch_op.drop_column('student_folder')

    with op.batch_alter_table('mahasiswa', schema=None) as batch_op:
        batch_op.alter_column('tanggal_keluar',
               existing_type=sa.DATE(),
               nullable=True)
        batch_op.drop_column('esyp')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mahasiswa', schema=None) as batch_op:
        batch_op.add_column(sa.Column('esyp', sa.VARCHAR(), nullable=False))
        batch_op.alter_column('tanggal_keluar',
               existing_type=sa.DATE(),
               nullable=False)

    with op.batch_alter_table('exchange_outbound', schema=None) as batch_op:
        batch_op.add_column(sa.Column('student_folder', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('folder', sa.VARCHAR(), nullable=True))

    # ### end Alembic commands ###

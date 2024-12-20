"""add new column at ExchangeOutbound table

Revision ID: eb59946dd026
Revises: 90febc549ad0
Create Date: 2024-11-20 10:24:50.431328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb59946dd026'
down_revision = '90febc549ad0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exchange_outbound', schema=None) as batch_op:
        batch_op.add_column(sa.Column('transcript_telu', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('transcript_exch', sa.String(), nullable=True))
        batch_op.alter_column('update_gpa',
               existing_type=sa.VARCHAR(),
               type_=sa.Date(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exchange_outbound', schema=None) as batch_op:
        batch_op.alter_column('update_gpa',
               existing_type=sa.Date(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
        batch_op.drop_column('transcript_exch')
        batch_op.drop_column('transcript_telu')

    # ### end Alembic commands ###

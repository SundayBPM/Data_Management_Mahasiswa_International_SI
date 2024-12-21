"""menambah kolom id

Revision ID: fba6b9c997eb
Revises: 434c96562974
Create Date: 2024-12-21 23:53:59.183637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fba6b9c997eb'
down_revision = '434c96562974'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('exchange_outbound') as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), autoincrement=True, nullable=True))

    # Assign default values to existing rows
    op.execute(
        """
        UPDATE exchange_outbound
        SET id = rowid
        WHERE id IS NULL
        """
    )

    # Make the column non-nullable
    with op.batch_alter_table('exchange_outbound') as batch_op:
        batch_op.alter_column('id', nullable=False)

def downgrade():
    with op.batch_alter_table('exchange_outbound') as batch_op:
        batch_op.drop_column('id')


    # ### end Alembic commands ###

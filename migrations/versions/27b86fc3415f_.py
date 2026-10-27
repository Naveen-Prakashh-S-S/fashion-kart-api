"""empty message

Revision ID: 27b86fc3415f
Revises: 9811acc5732d
Create Date: 2026-10-27 23:22:01.475438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27b86fc3415f'
down_revision = '9811acc5732d'
branch_labels = None
depends_on = None



def upgrade():
    with op.batch_alter_table('order_items', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('size_id', sa.Integer(), nullable=True)
        )
        batch_op.create_foreign_key(
            "fk_order_items_size_id_sizes",
            'sizes',
            ['size_id'],
            ['id']
        )


def downgrade():
    with op.batch_alter_table('order_items', schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_order_items_size_id_sizes",
            type_='foreignkey'
        )
        batch_op.drop_column('size_id')


"""add-foreign-key-to-post-table

Revision ID: 08ccaeada2da
Revises: 483552c6f922
Create Date: 2021-11-04 22:50:10.028634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08ccaeada2da'
down_revision = '483552c6f922'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'posts_users_fk',
        source_table='posts',
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')

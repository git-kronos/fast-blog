"""add-rest-columns-to-post-table

Revision ID: bb69fe68e974
Revises: 08ccaeada2da
Create Date: 2021-11-04 22:57:55.154602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb69fe68e974'
down_revision = '08ccaeada2da'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column(
            'is_published',
            sa.Boolean(),
            nullable=False,
            server_default='TRUE'
        )
    )
    op.add_column(
        'posts',
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        )
    )


def downgrade():
    op.drop_column('posts', 'is_published')
    op.drop_column('posts', 'created_at')


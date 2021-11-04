"""user-table-create

Revision ID: 483552c6f922
Revises: a054ba88e2fa
Create Date: 2021-11-04 22:38:26.098306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '483552c6f922'
down_revision = 'a054ba88e2fa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )


def downgrade():
    op.drop_table('users')

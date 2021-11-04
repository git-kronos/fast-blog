"""add content coloumn in post table

Revision ID: a054ba88e2fa
Revises: 6c1ff09f1091
Create Date: 2021-11-04 22:30:29.341867

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a054ba88e2fa'
down_revision = '6c1ff09f1091'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')

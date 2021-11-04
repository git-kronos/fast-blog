"""Create a post table

Revision ID: 6c1ff09f1091
Revises: 
Create Date: 2021-11-04 22:21:38.718057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c1ff09f1091'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False)
    )


def downgrade():
    op.drop_table('posts')

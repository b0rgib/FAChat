"""username unique

Revision ID: 6d59d9d0032f
Revises: 86dd2096c712
Create Date: 2023-02-17 14:24:22.187681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d59d9d0032f'
down_revision = '86dd2096c712'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'User', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'User', type_='unique')
    # ### end Alembic commands ###

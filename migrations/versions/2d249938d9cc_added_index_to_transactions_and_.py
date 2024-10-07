"""added index to transactions and ondelete cascade to user

Revision ID: 2d249938d9cc
Revises: 913ca1d145e5
Create Date: 2024-10-07 10:26:11.380975

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2d249938d9cc"
down_revision: Union[str, None] = "913ca1d145e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index("idx_date", "transactions", ["date"], unique=False)
    op.create_index("idx_exttrid", "transactions", ["exttrid"], unique=False)
    op.create_index("idx_user_id", "transactions", ["user_id"], unique=False)
    op.create_unique_constraint("uq_exttrid", "transactions", ["exttrid"])
    op.create_unique_constraint(None, "transactions", ["exttrid"])
    op.drop_constraint("transactions_user_id_fkey", "transactions", type_="foreignkey")
    op.create_foreign_key(
        None, "transactions", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "transactions", type_="foreignkey")
    op.create_foreign_key(
        "transactions_user_id_fkey", "transactions", "users", ["user_id"], ["id"]
    )
    op.drop_constraint(None, "transactions", type_="unique")
    op.drop_constraint("uq_exttrid", "transactions", type_="unique")
    op.drop_index("idx_user_id", table_name="transactions")
    op.drop_index("idx_exttrid", table_name="transactions")
    op.drop_index("idx_date", table_name="transactions")
    # ### end Alembic commands ###

"""add_unique_constraint_to_reviews_table

Revision ID: f09bf08f1fc4
Revises: 7651152492e3
Create Date: 2024-10-05 15:16:44.209596

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "f09bf08f1fc4"
down_revision: Union[str, None] = "7651152492e3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "reviews", "reviewed_user_id", existing_type=mysql.INTEGER(), nullable=False
    )
    op.create_unique_constraint(
        "unique_reviewer_reviewed_user_product",
        "reviews",
        ["reviewer_id", "reviewed_user_id", "product_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "unique_reviewer_reviewed_user_product", "reviews", type_="unique"
    )
    op.alter_column(
        "reviews", "reviewed_user_id", existing_type=mysql.INTEGER(), nullable=True
    )

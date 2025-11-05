"""~users, email->unique

Revision ID: 2bf5e313914e
Revises: a031ce5c26ba
Create Date: 2025-10-16 16:46:10.405630

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "2bf5e313914e"
down_revision: Union[str, Sequence[str], None] = "a031ce5c26ba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])



def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")

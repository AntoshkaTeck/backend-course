"""cascade delete room

Revision ID: 36f9a9cffcee
Revises: a48b6fa85b8e
Create Date: 2025-11-17 00:26:40.888616

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "36f9a9cffcee"
down_revision: Union[str, Sequence[str], None] = "a48b6fa85b8e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(op.f("rooms_hotel_id_fkey"), "rooms", type_="foreignkey")
    op.create_foreign_key(None, "rooms", "hotels", ["hotel_id"], ["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint(None, "rooms", type_="foreignkey")  # pyright: ignore
    op.create_foreign_key(op.f("rooms_hotel_id_fkey"), "rooms", "hotels", ["hotel_id"], ["id"])
